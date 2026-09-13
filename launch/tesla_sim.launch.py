"""Webots Tesla with camera + depth camera, controllable over ROS 2.

Launch arguments:
  world        world file in tesla_sim/worlds (default: tesla_city.wbt)
  pointcloud   publish a PointCloud2 on /vehicle/points (default: true).
               The driver also publishes an uncoloured cloud on
               /vehicle/range_finder/point_cloud regardless of this argument.
  colored      colour the cloud from the RGB camera (default: true)
  autonomous   also run the upstream lane follower, which drives the car by
               publishing /cmd_ackermann (default: false)
  rviz         open RViz2 with the camera and cloud displayed (default: false)
"""

import os

import launch
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from webots_ros2_driver.webots_controller import WebotsController
from webots_ros2_driver.webots_launcher import WebotsLauncher


def generate_launch_description():
    package_dir = get_package_share_directory('tesla_sim')
    world = LaunchConfiguration('world')
    pointcloud = LaunchConfiguration('pointcloud')
    colored = LaunchConfiguration('colored')

    webots = WebotsLauncher(
        world=PathJoinSubstitution([package_dir, 'worlds', world]),
        ros2_supervisor=True,
    )

    tesla_driver = WebotsController(
        robot_name='vehicle',
        parameters=[{'robot_description': os.path.join(package_dir, 'resource', 'tesla.urdf')}],
        respawn=True,
        # Default respawn_delay is 0.0 -- instant retry. Observed in practice:
        # if the driver can't create a DDS node (e.g. domain participant slots
        # exhausted), it aborts via an uncaught C++ exception rather than a
        # clean shutdown, respawns immediately, fails the same way again, and
        # can potentially leak another half-initialized participant slot each
        # time -- an instant-retry loop turns one transient DDS hiccup into a
        # crash storm that burns through the entire remaining participant pool
        # in seconds, guaranteeing it can never recover on its own. A short
        # cooldown gives transient conditions (like that) a chance to clear
        # between attempts instead of compounding them.
        respawn_delay=2.0,
    )

    # webots_ros2_driver already publishes a plain XYZ cloud on
    # /vehicle/range_finder/point_cloud. depth_image_proc is here to add colour
    # from the RGB camera. Camera and depth now have different FOVs/resolutions
    # (matching real D435 specs, see tesla.urdf), so unlike the old
    # single-camera setup, the depth image is NOT already registered to the
    # colour image -- register_node has to reproject it first, the same thing
    # the real RealSense SDK's align_depth does.
    register_depth = Node(
        package='depth_image_proc',
        executable='register_node',
        name='register_depth',
        remappings=[
            ('rgb/camera_info', '/vehicle/camera/camera_info'),
            ('depth/camera_info', '/vehicle/range_finder/camera_info'),
            ('depth/image_rect', '/vehicle/range_finder/image'),
            ('depth_registered/image_rect', '/vehicle/range_finder/image_registered'),
            ('depth_registered/camera_info', '/vehicle/range_finder/camera_info_registered'),
        ],
        condition=IfCondition(
            launch.substitutions.PythonExpression(["'", pointcloud, "' == 'true' and '", colored, "' == 'true'"])),
    )
    cloud_remappings = [
        ('depth_registered/image_rect', '/vehicle/range_finder/image_registered'),
        ('rgb/image_rect_color', '/vehicle/camera/image_color'),
        ('rgb/camera_info', '/vehicle/camera/camera_info'),
        ('points', '/vehicle/points'),
    ]
    colored_cloud = Node(
        package='depth_image_proc',
        executable='point_cloud_xyzrgb_node',
        name='point_cloud_xyzrgb',
        remappings=cloud_remappings,
        condition=IfCondition(
            launch.substitutions.PythonExpression(["'", pointcloud, "' == 'true' and '", colored, "' == 'true'"])),
    )
    plain_cloud = Node(
        package='depth_image_proc',
        executable='point_cloud_xyz_node',
        name='point_cloud_xyz',
        remappings=[
            ('image_rect', '/vehicle/range_finder/image'),
            ('camera_info', '/vehicle/range_finder/camera_info'),
            ('points', '/vehicle/points'),
        ],
        condition=IfCondition(
            launch.substitutions.PythonExpression(["'", pointcloud, "' == 'true' and '", colored, "' != 'true'"])),
    )

    lane_follower = Node(
        package='webots_ros2_tesla',
        executable='lane_follower',
        condition=IfCondition(LaunchConfiguration('autonomous')),
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(package_dir, 'config', 'tesla_sim.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz')),
    )

    # The range finder's device data (tesla.urdf names it "range_finder_optical")
    # comes out in camera-optical convention: X right, Y down, Z forward/depth.
    # With no TF at all, RViz would use those axes as world axes directly --
    # "forward" ends up along Z, which renders as vertical against a
    # Z-up grid. This is the standard fix every ROS camera/depth driver uses:
    # publish the body-frame ("range_finder", X forward/Y left/Z up, matching
    # the vehicle) as the parent of the optical frame, related by the fixed
    # optical-frame rotation. RViz's Fixed Frame stays "range_finder".
    range_finder_optical_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--roll', '-1.5707963267948966', '--pitch', '0', '--yaw', '-1.5707963267948966',
            '--frame-id', 'range_finder', '--child-frame-id', 'range_finder_optical',
        ],
    )

    # Same split for the camera, needed now that camera and depth have
    # different FOVs (see tesla.urdf) and depth_image_proc has to actually
    # register them rather than assume identical framing.
    camera_optical_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--roll', '-1.5707963267948966', '--pitch', '0', '--yaw', '-1.5707963267948966',
            '--frame-id', 'camera', '--child-frame-id', 'camera_optical',
        ],
    )

    # Real D435 hardware offsets the depth module from the RGB module by
    # ~25mm; the world file places both devices at the identical translation
    # (an approximation -- 25mm is negligible against the meters-scale
    # distances this vehicle cares about). This TF is what lets
    # depth_image_proc project depth points into the camera's image to sample
    # colour; with it being an identity transform, the two body frames are
    # exactly coincident, matching the world file.
    camera_to_range_finder_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--roll', '0', '--pitch', '0', '--yaw', '0',
            '--frame-id', 'camera', '--child-frame-id', 'range_finder',
        ],
    )

    # The IMU is physically inside the same D435i module -- same co-located
    # approximation as camera_to_range_finder_tf above. Accelerometer/Gyro
    # devices (unlike Camera/RangeFinder) report along their own local axes
    # directly with no optical-frame convention involved, so this needs no
    # rotation, just a place in the TF tree.
    camera_to_imu_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--roll', '0', '--pitch', '0', '--yaw', '0',
            '--frame-id', 'camera', '--child-frame-id', 'imu',
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument('world', default_value='tesla_city.wbt'),
        DeclareLaunchArgument('pointcloud', default_value='true'),
        DeclareLaunchArgument('colored', default_value='true'),
        DeclareLaunchArgument('autonomous', default_value='false'),
        DeclareLaunchArgument('rviz', default_value='false'),
        webots,
        webots._supervisor,
        tesla_driver,
        register_depth,
        colored_cloud,
        plain_cloud,
        lane_follower,
        range_finder_optical_tf,
        camera_optical_tf,
        camera_to_range_finder_tf,
        camera_to_imu_tf,
        rviz,
        # Shut the whole launch down when Webots exits.
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        ),
    ])

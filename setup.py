from glob import glob

from setuptools import setup

package_name = 'tesla_sim'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/worlds', glob('worlds/*.wbt')),
        ('share/' + package_name + '/resource', glob('resource/*.urdf')),
        ('share/' + package_name + '/config', glob('config/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='neel',
    maintainer_email='neelnaik2005@gmail.com',
    description='Webots Tesla simulation with an RGB + depth camera, driven over ROS 2 topics.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'ackermann_teleop_keyboard = tesla_sim.ackermann_teleop_keyboard:main',
        ],
    },
)

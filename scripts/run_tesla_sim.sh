#!/usr/bin/env bash
# tesla_sim launcher.
#
# Works on both setups the team uses, without editing anything:
#
#   * a distrobox container (ROS 2 Humble) with Webots as the host snap,
#     reached through /run/host
#   * a plain Ubuntu 24.04 machine (ROS 2 Jazzy) with Webots built from
#     source in $HOME/webots, no container involved
#
# Everything below is detected rather than hardcoded, so the same script
# serves both. Override any of WEBOTS_HOME, TESLA_SIM_WS, ROS_DISTRO,
# QT_QPA_PLATFORM or QT_PLUGIN_PATH in the environment to force a choice.
#
# Usage:
#   run_tesla_sim.sh
#   run_tesla_sim.sh autonomous:=true rviz:=true
#
# `set -u` is deliberately NOT used: the ROS setup scripts reference unbound
# variables (AMENT_TRACE_SETUP_FILES and friends) and would abort under it.
set -eo pipefail

die() { echo "run_tesla_sim.sh: $*" >&2; exit 1; }

# --- Webots ----------------------------------------------------------------
# Source builds keep the launcher at $WEBOTS_HOME/webots; so does the snap
# tree. Probe the usual locations, most specific first.
if [ -z "${WEBOTS_HOME:-}" ]; then
  for candidate in \
      "$HOME/webots" \
      /usr/local/webots \
      /run/host/snap/webots/current/usr/share/webots \
      /snap/webots/current/usr/share/webots; do
    if [ -x "$candidate/webots" ]; then
      WEBOTS_HOME="$candidate"
      break
    fi
  done
fi
[ -n "${WEBOTS_HOME:-}" ] || die "could not find Webots. Set WEBOTS_HOME to the directory containing the 'webots' launcher."
[ -x "$WEBOTS_HOME/webots" ] || die "WEBOTS_HOME=$WEBOTS_HOME has no executable 'webots' launcher in it."
export WEBOTS_HOME

# webots_ros2_driver links against libController, and the Python controller
# API lives beside it. A source build does not install either system-wide.
export LD_LIBRARY_PATH="$WEBOTS_HOME/lib/controller${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PYTHONPATH="$WEBOTS_HOME/lib/controller/python${PYTHONPATH:+:$PYTHONPATH}"

# --- Qt --------------------------------------------------------------------
# Wayland is the default session on 24.04, but the container has no wayland
# client libs and Webots is happiest on xcb either way (needs libxcb-cursor0).
export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-xcb}"

# An official build ships its own Qt under lib/webots/qt. A source build that
# was linked against the distro's Qt6 instead has no such directory and needs
# to be pointed at the system plugins, or it aborts with "no Qt platform
# plugin could be initialized". Derive the multiarch dir so this holds on both
# x86_64 and arm64 (Jetson).
if [ ! -d "$WEBOTS_HOME/lib/webots/qt" ] && [ -z "${QT_PLUGIN_PATH:-}" ]; then
  multiarch="$(dpkg-architecture -qDEB_HOST_MULTIARCH 2>/dev/null || echo "$(uname -m)-linux-gnu")"
  if [ -d "/usr/lib/$multiarch/qt6/plugins" ]; then
    export QT_PLUGIN_PATH="/usr/lib/$multiarch/qt6/plugins"
  fi
fi

# --- ROS -------------------------------------------------------------------
# Prefer an already-sourced environment; otherwise take the newest distro
# present. Jazzy is what Ubuntu 24.04 ships, Humble is what the container has.
if [ -z "${ROS_DISTRO:-}" ]; then
  for distro in /opt/ros/jazzy /opt/ros/humble /opt/ros/*; do
    if [ -f "$distro/setup.bash" ]; then
      # shellcheck disable=SC1091
      source "$distro/setup.bash"
      break
    fi
  done
fi
[ -n "${ROS_DISTRO:-}" ] || die "no ROS 2 environment found under /opt/ros. Source one first."

# --- workspace overlay -----------------------------------------------------
# tesla_sim depends on vehicle_bridge (tesla_driver imports relay_steering
# from it), so both packages must be built into the same workspace.
WS="${TESLA_SIM_WS:-$HOME/ros2_ws}"
if [ -f "$WS/install/setup.bash" ]; then
  # shellcheck disable=SC1091
  source "$WS/install/setup.bash"
else
  echo "run_tesla_sim.sh: warning: no overlay at $WS/install/setup.bash;" >&2
  echo "  relying on tesla_sim and vehicle_bridge being on the ROS path already." >&2
  echo "  Set TESLA_SIM_WS if your workspace lives elsewhere." >&2
fi

# ROS_DOMAIN_ID and CYCLONEDDS_URI are deliberately left alone -- see the
# README. Every terminal you use with tesla_sim must agree on the domain.
exec ros2 launch tesla_sim tesla_sim.launch.py "$@"

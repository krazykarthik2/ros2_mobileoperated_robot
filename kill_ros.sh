#!/bin/bash
echo "Nuking all ROS 2 and related processes..."

# 1. Kill ROS 2 Nodes and Launch files
pkill -9 -f ros2
pkill -9 -f move_group
pkill -9 -f robot_state_publisher
pkill -9 -f joint_state_publisher
pkill -9 -f rviz2

# 2. Kill Python scripts (Your bridge and web server)
pkill -9 -f simple_move.py
pkill -9 -f http.server

# 3. Clear Ports
sudo fuser -k 9090/tcp 8080/tcp 9009/tcp > /dev/null 2>&1

# 4. Clean ROS 2 Daemon (The most important step for 'ghost' nodes)
ros2 daemon stop
ros2 daemon start

echo "Environment Cleaned. Ready for a fresh ./run.sh"

#!/bin/bash
# Clean up everything first
sudo fuser -k 9090/tcp 80/tcp
pkill -f static_transform_publisher
pkill -f simple_move

source /opt/ros/jazzy/setup.bash

# 1. Start Bridge
ros2 launch rosbridge_server rosbridge_websocket_launch.xml address:=0.0.0.0 &
sleep 2

# 2. Start Model (Ensure your launch_robot.py has NO static_transform_publisher)
ros2 launch launch_robot.py &
sleep 1

# 3. Start the Mover (The "Engine")
python3 simple_move.py &
sleep 1

# 4. Start Server
python3 -m http.server 80 &

# 5. Start RViz
rviz2

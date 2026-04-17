#!/bin/bash
./kill_ros.sh
# 1. CLEANUP
# Kills existing processes and clears the ports
echo "Cleaning up old processes..."
sudo fuser -k 9090/tcp 8080/tcp > /dev/null 2>&1
pkill -f simple_move
pkill -f move_group
pkill -f robot_state_publisher

# 2. ENVIRONMENT SETUP
source /opt/ros/jazzy/setup.bash
WORKSPACE_DIR=$(pwd)

# Source your local built package
if [ -f "$WORKSPACE_DIR/install/setup.bash" ]; then
    source "$WORKSPACE_DIR/install/setup.bash"
else
    echo "ERROR: install/setup.bash not found. Run 'colcon build' first."
    exit 1
fi

# Set graphics platform for RViz2 stability
export QT_QPA_PLATFORM=xcb

# 3. START ROSBRIDGE (Web Support) on Port 9090
echo "Starting Rosbridge on port 9090..."
ros2 launch rosbridge_server rosbridge_websocket_launch.xml address:=0.0.0.0 port:=9090 &
sleep 2

# 4. START ROBOT STATE & TRANSFORMS (launch_robot.py)
echo "Launching Robot Model, Joint States, and TFs..."
ros2 launch "$WORKSPACE_DIR/launch_robot.py" & 
sleep 2

# 5. START MOVEIT (The Brain)
echo "Launching MoveIt 2..."
# We use the absolute path to the install file to ensure our OMPL fix is active
ros2 launch "$WORKSPACE_DIR/install/gearxmoveitconfig/share/gearxmoveitconfig/launch/move_group.launch.py" &
sleep 10  # MoveIt needs time to load the OMPL planner plugins

# 6. START THE COMMAND BRIDGE (MoveIt -> ESP32)
echo "Starting Command Bridge..."
python3 "$WORKSPACE_DIR/simple_move.py" &

# 7. START WEB SERVER (Port 8080)
echo "Starting Control Panel on http://localhost:8080"
python3 -m http.server 8080 &

# 8. START RVIZ2
echo "Opening RViz2..."
ros2 launch gearxmoveitconfig moveit_rviz.launch.py

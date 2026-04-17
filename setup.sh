sudo apt update
sudo apt install avahi-daemon

sudo hostnamectl set-hostname robot

sudo apt install ros-$ROS_DISTRO-rosbridge-suite
sudo apt install ros-$ROS_DISTRO-dummy-robot-cmds

sudo apt install ros-jazzy-joint-state-publisher ros-jazzy-joint-state-publisher-gui

sudo apt install ros-jazzy-moveit-setup-assistant ros-jazzy-moveit
sudo apt install ros-jazzy-joint-state-publisher
echo "export ROS_DOMAIN_ID=0" >> ~/.bashrc
# 1. Add QT_QPA_PLATFORM to .bashrc if not already present
if ! grep -q "export QT_QPA_PLATFORM=xcb" ~/.bashrc; then
    echo 'export QT_QPA_PLATFORM=xcb' >> ~/.bashrc
    echo "Added QT_QPA_PLATFORM=xcb to ~/.bashrc"
fi

# 2. Add an alias for convenience
if ! grep -q "alias moveit_setup" ~/.bashrc; then
    echo "alias moveit_setup='QT_QPA_PLATFORM=xcb ros2 run moveit_setup_assistant moveit_setup_assistant'" >> ~/.bashrc
    echo "Added moveit_setup alias to ~/.bashrc"
fi

# 3. Source the bashrc for the current session
# Note: sourcing from within a script only affects the script's subshell.
# You will still need to run 'source ~/.bashrc' once manually after this script finishes.
export QT_QPA_PLATFORM=xcb

source ~/.bashrc

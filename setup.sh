sudo apt update
sudo apt install avahi-daemon

sudo hostnamectl set-hostname robot

sudo apt install ros-$ROS_DISTRO-rosbridge-suite
sudo apt install ros-$ROS_DISTRO-dummy-robot-cmds

echo "export ROS_DOMAIN_ID=0" >> ~/.bashrc
source ~/.bashrc

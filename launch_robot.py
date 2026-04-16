from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Use an absolute path or ensure the script runs where robot.urdf is
    urdf_path = 'robot.urdf' 
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}]
        )
    ])

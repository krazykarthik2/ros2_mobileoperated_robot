import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    workspace_path = "/home/karthikkrazy/robotcontrolled"
    
    with open(os.path.join(workspace_path, "robot.urdf"), 'r') as f:
        robot_description = {"robot_description": f.read()}

    with open(os.path.join(workspace_path, "gearxmoveitconfig/config/gearx_robot.srdf"), 'r') as f:
        robot_description_semantic = {"robot_description_semantic": f.read()}

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", os.path.join(workspace_path, "gearxmoveitconfig/config/moveit.rviz")],
        parameters=[
            robot_description,
            robot_description_semantic,
        ],
    )

    return LaunchDescription([rviz_node])

import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Define the absolute path to your URDF
    # Hardcoding this ensures ROS doesn't look for an old cached version
    urdf_path = '/home/karthikkrazy/robotcontrolled/robot.urdf'
    
    if not os.path.exists(urdf_path):
        print(f"ERROR: URDF file not found at {urdf_path}")

    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # A. Robot State Publisher (Handles the URDF and fixed joints)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_desc,
                'use_sim_time': False
            }]
        ),

        # B. Joint State Publisher (Fixes the "No transform" error for the wheels)
        # It provides the 0-position for the continuous wheel joints
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_sim_time': False}]
        ),

        # C. Static Transform Publisher (Connects the robot to the world)
        # This maps the 'odom' frame to your 'base_footprint'
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_odom_to_footprint',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_footprint']
        )
    ])

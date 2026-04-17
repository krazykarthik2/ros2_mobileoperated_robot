import os
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    path = "/home/karthikkrazy/robotcontrolled"
    
    # 1. Load URDF & SRDF
    with open(os.path.join(path, "robot.urdf"), 'r') as f:
        robot_description = {"robot_description": f.read()}
    with open(os.path.join(path, "gearxmoveitconfig/config/gearx_robot.srdf"), 'r') as f:
        robot_description_semantic = {"robot_description_semantic": f.read()}

    # 2. Load Kinematics
    with open(os.path.join(path, "gearxmoveitconfig/config/kinematics.yaml"), 'r') as f:
        kinematics = {"robot_description_kinematics": yaml.safe_load(f)}

    # 3. FIX: Define the Planning Pipeline (This stops the "Aborted" crash)
    planning_pipeline_config = {
        "move_group": {
            "planning_plugin": "ompl_interface/OMPLPlanner",
            "request_adapters": """default_planner_request_adapters/AddTimeOptimalParameterization default_planner_request_adapters/FixWorkspaceBounds default_planner_request_adapters/FixStartStateBounds default_planner_request_adapters/FixStartStateCollision default_planner_request_adapters/FixStartStatePathConstraints""",
            "start_state_max_bounds_error": 0.1,
        }
    }

    return LaunchDescription([
        Node(
            package="moveit_ros_move_group",
            executable="move_group",
            output="screen",
            parameters=[
                robot_description,
                robot_description_semantic,
                kinematics,
                planning_pipeline_config,  # Manually injecting the missing planner info
                {"use_sim_time": False},
                {"publish_robot_description_semantic": True},
            ],
        )
    ])

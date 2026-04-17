import os
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    path = "/home/karthikkrazy/robotcontrolled"
    config_path = os.path.join(path, "gearxmoveitconfig/config")
    
    # 1. Load URDF & SRDF
    with open(os.path.join(path, "robot.urdf"), 'r') as f:
        robot_description = {"robot_description": f.read()}
    with open(os.path.join(config_path, "gearx_robot.srdf"), 'r') as f:
        robot_description_semantic = {"robot_description_semantic": f.read()}

    # 2. Load YAML Configs
    def load_yaml(file_name):
        file_path = os.path.join(config_path, file_name)
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)

    kinematics = {"robot_description_kinematics": load_yaml("kinematics.yaml")}
    joint_limits = {"robot_description_planning": load_yaml("joint_limits.yaml")}

    # 3. Planning Pipeline (OMPL)
    ompl_config = {
        "planning_plugin": "ompl_interface/OMPLPlanner",
        "planning_pipelines": ["ompl"],
        "default_planning_pipeline": "ompl",
        "request_adapters": "default_planner_request_adapters/AddTimeOptimalParameterization default_planner_request_adapters/FixWorkspaceBounds default_planner_request_adapters/FixStartStateBounds default_planner_request_adapters/FixStartStateCollision default_planner_request_adapters/FixStartStatePathConstraints",
        "start_state_max_bounds_error": 0.1,
    }

    # 4. Trajectory Execution (Required for Action Server)
    trajectory_execution = {
        "moveit_manage_controllers": True,
        "trajectory_execution.allowed_execution_duration_scaling": 1.2,
        "trajectory_execution.allowed_goal_duration_margin": 0.5,
        "trajectory_execution.execution_duration_monitoring": False,
    }

    return LaunchDescription([
        Node(
            package="moveit_ros_move_group",
            executable="move_group",
            name="move_group",
            output="screen",
            parameters=[
                robot_description,
                robot_description_semantic,
                kinematics,
                joint_limits,
                ompl_config,
                trajectory_execution,
                {"use_sim_time": False},
                {"publish_robot_description_semantic": True},
            ],
        )
    ])

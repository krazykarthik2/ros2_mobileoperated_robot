import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from moveit_msgs.action import MoveGroup
from geometry_msgs.msg import Pose, PoseStamped, TransformStamped, Twist
from trajectory_msgs.msg import JointTrajectory
from tf2_ros import TransformBroadcaster
import math

class GearXBridge(Node):
    def __init__(self):
        super().__init__('gearx_bridge')
        self.br = TransformBroadcaster(self)
        
        # Action Client - ensure name is exactly '/move_group'
        self._action_client = ActionClient(self, MoveGroup, '/move_group')

        self.target_sub = self.create_subscription(PoseStamped, '/target_pose', self.web_target_callback, 10)
        self.traj_sub = self.create_subscription(JointTrajectory, '/base_controller/joint_trajectory', self.traj_callback, 10)
        self.pose_pub = self.create_publisher(Pose, '/robot_pose', 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.x, self.y, self.th = 0.0, 0.0, 0.0
        self.create_timer(0.1, self.update_loop)
        self.get_logger().info("GearX Bridge initialized.")

    def web_target_callback(self, msg):
        self.get_logger().info(f"Targeting: X={msg.pose.position.x}, Y={msg.pose.position.y}")
        
        # Teleport for UI feedback test
        self.x = msg.pose.position.x
        self.y = msg.pose.position.y
        
        self.send_moveit_goal(msg.pose)

    def send_moveit_goal(self, pose):
        if not self._action_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error("Action Server Timeout! MoveIt node is likely crashing or uninitialized.")
            return

        goal_msg = MoveGroup.Goal()
        goal_msg.request.group_name = "base_group"
        goal_msg.request.num_planning_attempts = 10
        goal_msg.request.allowed_planning_time = 5.0
        
        # Send goal
        self._action_client.send_goal_async(goal_msg)

    def traj_callback(self, msg):
        if not msg.points: return
        point = msg.points[0]
        self.x, self.y, self.th = point.positions[0], point.positions[1], point.positions[2]

    def update_loop(self):
        p = Pose()
        p.position.x, p.position.y = self.x, self.y
        self.pose_pub.publish(p)

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id, t.child_frame_id = 'odom', 'base_footprint'
        t.transform.translation.x, t.transform.translation.y = self.x, self.y
        t.transform.rotation.z, t.transform.rotation.w = math.sin(self.th / 2.0), math.cos(self.th / 2.0)
        self.br.sendTransform(t)

def main():
    rclpy.init()
    rclpy.spin(GearXBridge())
    rclpy.shutdown()

if __name__ == '__main__':
    main()

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from geometry_msgs.msg import Twist
import math

class MoveItToCmdVel(Node):
    def __init__(self):
        super().__init__('moveit_bridge')
        # Change this to match your MoveIt controller topic
        self.subscription = self.create_subscription(
            JointTrajectory,
            '/base_controller/joint_trajectory', 
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def listener_callback(self, msg):
        if len(msg.points) > 0:
            target_point = msg.points[0]
            twist = Twist()
            
            # Map MoveIt planar velocities to Twist
            # Assuming Joint 0 = X, Joint 1 = Y, Joint 2 = Theta
            twist.linear.x = target_point.velocities[0]
            twist.angular.z = target_point.velocities[2]
            
            self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = MoveItToCmdVel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

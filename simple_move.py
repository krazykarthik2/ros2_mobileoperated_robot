import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from tf2_ros import TransformBroadcaster
import math

class SimpleMover(Node):
    def __init__(self):
        super().__init__('simple_mover')
        
        # This sends the "position" to RViz
        self.br = TransformBroadcaster(self)
        
        # This listens to your HTML buttons
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10)
            
        # Initial Position
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0 # Theta (Rotation)
        
        # Current Velocities
        self.linear_v = 0.0
        self.angular_v = 0.0
        
        # Run the math loop at 20Hz (every 0.05 seconds)
        self.timer = self.create_timer(0.05, self.update_position)
        self.get_logger().info("Simple Mover Node Started. Waiting for /cmd_vel...")

    def cmd_callback(self, msg):
        self.linear_v = msg.linear.x
        self.angular_v = msg.angular.z

    def update_position(self):
        dt = 0.05
        
        # 1. Calculate new coordinates based on velocity
        # New X = current X + (speed * cos(angle) * time)
        self.x += self.linear_v * math.cos(self.th) * dt
        self.y += self.linear_v * math.sin(self.th) * dt
        self.th += self.angular_v * dt

        # 2. Create the Transform Message for RViz
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = 'base_link'

        # Translation (Movement)
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0

        # Rotation (Quaternion math for 2D)
        t.transform.rotation.z = math.sin(self.th / 2.0)
        t.transform.rotation.w = math.cos(self.th / 2.0)

        # 3. Shout it out to RViz
        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = SimpleMover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()

if __name__ == '__main__':
    main()

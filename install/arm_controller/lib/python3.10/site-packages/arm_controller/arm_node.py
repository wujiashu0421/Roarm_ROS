#! /usr/bin/python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point, Pose
from sensor_msgs.msg import JointState

class ArmInfoNode(Node):

    def __init__(self):
        super.__init__("Arm_Info")
        # 10 is the queue size, which is a publish buffer
        self.pose_pub = self.create_publisher(JointState, "joint_states", 10)
        self.get_logger().info("Arm info node started")
    
    def send_pose(self):
        
        msg = Pose()



def main(args=None):
    rclpy.init(args=args)

    rclpy.shutdown()

if __name__ == "__main__":
    main()
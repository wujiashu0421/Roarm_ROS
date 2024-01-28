#! /usr/bin/python3

import rclpy
from rclpy.node import Node

class CommNode(Node):
    
    def __init__(self):
        # Instantiase the node using the node definition in rclpy. Set name in parentheses
        super().__init__("Controller")
        self.create_timer(1.0, self.timer_callback)
    
    def timer_callback(self):
        self.get_logger().info("Hello")


def main(args=None):
    ## Initiate ROS 2 communication , equivlent to ROS::start in ros1 i think
    rclpy.init(args=args)

    node = CommNode()
    rclpy.spin(node)

    ## Stop ROS communication service entirely
    rclpy.shutdown()

if __name__ == '__main__':
    main()


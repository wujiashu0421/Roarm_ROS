#! /usr/bin/python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger, Empty

class FeedbackService(Node):
    
    def __init__(self):
        # Instantiase the node using the node definition in rclpy. Set name in parentheses
        super().__init__("feedback_service")
        self.srv = self.create_service(Trigger, 'robot_feedback', self.srv_callback)
    
    def srv_callback(self, _, response):

        print("Hello")
        self.get_logger().info('Hello')
        response.success = True
        response.message = "1, 2, 3, 4"

        return response

def main(args=None):
    ## Initiate ROS 2 communication , equivlent to ROS::start in ros1 i think
    rclpy.init(args=args)

    feedback_service = FeedbackService()

    rclpy.spin(feedback_service)

    ## Stop ROS communication service entirely
    rclpy.shutdown()

if __name__ == '__main__':
    main()
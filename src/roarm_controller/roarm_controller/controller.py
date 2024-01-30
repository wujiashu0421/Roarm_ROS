import rclpy
from rclpy.node import Node
import array

from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from std_srvs.srv import Trigger

import time
import json
import serial

# Serial Object. Change USB port number and baud rate respectively for connection to other machines
ser = serial.Serial("/dev/ttyUSB0",115200)

# Subscriber which listens to any published joint state information which then commands the arm to move.
class ControlSubscriber(Node):

    def __init__(self):
        super().__init__('serial_ctrl')
        self.position = []
        self.subscription = self.create_subscription(
            JointState,
            '/matlab_control',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.srv = self.create_service(Trigger, 'robot_feedback', self.srv_callback)

    # Get arm position
    def posGet(self, radInput, direcInput, multiInput):
        if radInput == 0:
            return 2047
        else:
            getPos = int(2047 + (direcInput * radInput / 3.1415926 * 2048 * multiInput) + 0.5)
            return getPos

    def listener_callback(self, msg):
        a = msg.position
        data = json.dumps({'T':102,'base':a[0],'shoulder':a[1],'elbow':a[2],'hand':a[3]+3.1415926,'spd':a[4],'acc':a[5]}) + "\n"
        ser.write(data.encode())
        print(data)

    def srv_callback(self, _, response):

        self.get_logger().info('Service Callback Initiated')
        ser.flush()
        # Request feedback data
        data = json.dumps({'T':105}) + "\n"
        ser.write(data.encode())
        # Wait for the output from arm to arrive
        while(ser.in_waiting == 0):
            continue
        # Default read until newline
        msg = ser.read_all().decode("utf-8") 
        response.success = True
        response.message = msg

        return response


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = ControlSubscriber()
    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

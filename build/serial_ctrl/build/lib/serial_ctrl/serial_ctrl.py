import rclpy
from rclpy.node import Node
import array

from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

import json
import serial

# Serial Object. Change USB port number and baud rate respectively for connection to other machines
ser = serial.Serial("/dev/ttyUSB0",115200)

# Create ROS Service which replies the client with the feedback information every time it's called



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
    

    # Get arm position
    def posGet(self, radInput, direcInput, multiInput):
        if radInput == 0:
            return 2047
        else:
            getPos = int(2047 + (direcInput * radInput / 3.1415926 * 2048 * multiInput) + 0.5)
            return getPos

    def listener_callback(self, msg):
        a = msg.position
        data = json.dumps({'T':102,'base':a[0],'shoulder':a[1],'elbow':a[2],'hand':a[3]+3.1415926,'spd':0,'acc':0}) + "\n"
        ser.write(data.encode())
        print(data)


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

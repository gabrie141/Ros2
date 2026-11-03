#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

class MecanumKinematics(Node):
    def __init__(self):
        super().__init__('mecanum_kinematics')
        # Parámetros del robot
        self.L = 0.057   # mitad de la distancia entre ejes (wheel_base/2)
        self.W = 0.106   # mitad de la distancia entre ruedas (wheel_separation/2)
        self.R = 0.029   # radio de la rueda

        self.sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_cb, 10)

        self.pub_fl = self.create_publisher(Float64, '/fl_wheel_cmd', 10)
        self.pub_fr = self.create_publisher(Float64, '/fr_wheel_cmd', 10)
        self.pub_rl = self.create_publisher(Float64, '/rl_wheel_cmd', 10)
        self.pub_rr = self.create_publisher(Float64, '/rr_wheel_cmd', 10)

    def cmd_vel_cb(self, msg):
        vx = msg.linear.x
        vy = msg.linear.y
        omega = msg.angular.z

        # Cinemática inversa Mecanum
        v_fl = (vx - vy - (self.L + self.W) * omega) / self.R
        v_fr = (vx + vy + (self.L + self.W) * omega) / self.R
        v_rl = (vx + vy - (self.L + self.W) * omega) / self.R
        v_rr = (vx - vy + (self.L + self.W) * omega) / self.R

        self.pub_fl.publish(Float64(data=v_fl))
        self.pub_fr.publish(Float64(data=v_fr))
        self.pub_rl.publish(Float64(data=v_rl))
        self.pub_rr.publish(Float64(data=v_rr))

def main(args=None):
    rclpy.init(args=args)
    node = MecanumKinematics()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

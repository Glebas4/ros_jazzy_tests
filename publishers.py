import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class MinimalPublisher(Node):
    def __init__(self, name, topic, val):
        super().__init__(name)
        self.publisher_ = self.create_publisher(Int32, topic, 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.val = val

    def timer_callback(self):
        msg = Int32()
        msg.data = self.val
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
       

def main(args=None):
    rclpy.init(args=args)

    pub_1 = MinimalPublisher("smoke", "/sensor/smoke_sensor", 921)
    pub_2 = MinimalPublisher("light", "/sensor/light_sensor", 1232)
    pub_3 = MinimalPublisher("heat", "/sensor/heat_sensor", -234)

    rclpy.spin(pub_1)
    rclpy.spin(pub_2)
    rclpy.spin(pub_3)

    pub_1.destroy_node()
    pub_2.destroy_node()
    pub_3.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()

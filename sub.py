import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class subscriber(Node):
    def __init__(self, topic_name):
        super().__init__(topic_name)
        self.topic_name = topic_name
        self.subscription = self.create_subscription(Int32, self.topic_name, self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        val = msg.data
        if -1000 <= val and val <= 1000:
            print(self.topic_name[8:], val, "\n")
        else:
            print(self.topic_name[8:], "ERROR\n")


def main(args=None):
    rclpy.init(args=None)
    node = rclpy.create_node('node')

    topic_list = node.get_topic_names_and_types()
    sensor_topics = [topic for topic, types in topic_list if topic.startswith('/sensor/')]
    #for n in range(len(sensor_topics)):
     #   sensor_topics[n] = sensor_topics[n][8:]

    for topic in sensor_topics:
        obj = subscriber(topic[0])

    rclpy.shutdown()


if __name__ == '__main__':
    main()

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class subscriber(Node):
    def __init__(self, node_name):
        super().__init__(node_name)

    def subscribe(self, topic_name):
        self.flag = False
        self.topic_name = topic_name
        self.subscription = self.create_subscription(Int32, self.topic_name, self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        val = msg.data
        if -1000 <= val and val <= 1000:
            val = val
        else:
            val = "ERROR"

        print(self.topic_name[8:], val)
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=None)
    node = Node()
    
    topic_list = node.get_topic_names_and_types()
    sensor_topics = [topic for topic, types in topic_list if topic.startswith('/sensor/')]
    node.topics = len(sensor_topics)

    for topic in sensor_topics:
        print(topic)
        sub = subscriber("subscribeeer")
        sub.subscribe(topic)


if __name__ == '__main__':
    main()

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class subscriber(Node):
    def __init__(self, node_name):
        super().__init__(node_name)

    def subscribe(self, topic_name):
        msg = rclpy.wait_for_message(topic_name, Int32, timeout_sec=0.2)
        val = msg.data
        if -1000 <= val and val <= 1000:
            val = val
        else:
            val = "ERROR"

        print(self.topic_name[8:], val)


def main(args=None):
    rclpy.init(args=None)
    sub = subscriber("subs")
    
    topic_list = sub.get_topic_names_and_types()
    sensor_topics = [topic for topic, types in topic_list if topic.startswith('/sensor/')]
    sub.topics = len(sensor_topics)

    for topic in sensor_topics:
        print(topic)
        sub.subscribe(topic)


if __name__ == '__main__':
    main()

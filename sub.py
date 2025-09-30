import rclpy
from rclpy.node import Node
from rclpy.wait_for_message import wait_for_message
from std_msgs.msg import Int32

answer = {}


class subscriber(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.count = 0
        self.topics = 0

    def subscribe(self, topic_name):
        msg = wait_for_message(
            Int32,
            self,
            topic_name,
            qos_profile=rclpy.qos.qos_profile_sensor_data, # Or rclpy.qos.qos_profile_system_default, etc.
            time_to_wait=0.2
        )

        val = msg.data
        if -1000 <= val and val <= 1000:
            val = val
        else:
            val = "ERROR"
        answer[self.topic_name] = val

        if self.topics == self.count:
            for key, val in answer.items():
                print(key, val)
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=None)
    #sub = subscriber("/sensor/smoke_sensor")
    sub = subscriber("subs")
    
    
    topic_list = sub.get_topic_names_and_types()
    sensor_topics = [topic for topic, types in topic_list if topic.startswith('/sensor/')]
    sub.topics = len(sensor_topics)
    #for n in range(len(sensor_topics)):
        #sensor_topics[n] = sensor_topics[n][8:]

    #print(sensor_topics)
    for topic in sensor_topics:
        print(topic)
        sub.subscribe(topic)
    

    rclpy.spin(sub)


if __name__ == '__main__':
    main()

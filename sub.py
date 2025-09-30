import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

answer = {}

class subscriber(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.count = 0
        self.topics = 0

    def subscribe(self, topic_name):
        self.topic_name = topic_name
        self.subscription = self.create_subscription(Int32, self.topic_name, self.listener_callback, 10)
        self.subscription  # prevent unused variable warning


    def listener_callback(self, msg):
        self.count += 1
        val = msg.data
        if -1000 <= val and val <= 1000:
            val = val
        else:
            val = "ERROR"
        answer[self.topic_name] = val
        
        self.destroy_subscription(self.subscription)

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

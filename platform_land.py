import rospy  # type: ignore
from clover import srv 
from std_srvs.srv import Trigger
from aruco_pose.msg import MarkerArray
from sensor_msgs.msg import Range
from mavros_msgs.srv import CommandBool
import math


rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
land = rospy.ServiceProxy('land', Trigger)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
z = 1.5


def marker_callback(msg):
    global marker
    if 157 in msg.markers:
        marker = True
    else:
        marker = False


def range_callback(msg):
    global dist
    dist = msg.range


def takeoff():
    navigate(x=0, y=0, z=1.5, speed=0.5, frame_id='body', auto_arm=True)
    rospy.sleep(5)


def main(args=None):
    print("Start")
    takeoff()
    set_position(x=3, y=2.5, z=z, frame_id='aruco_map')
    
    while True:
        if marker:
            z -= 0.05
            set_position(x=0, y=0, z=z, frame_id='aruco_157')
            if dist <= 0.3:
                arming(False)
                break
            rospy.sleep(0.1)
        else:
            z = 1.5
            set_position(x=3, y=2.5, z=z, frame_id='aruco_map')
    print("Done")


if __name__ == '__main__':
    rospy.Subscriber('aruco_detect/markers', MarkerArray, marker_callback)
    rospy.Subscriber('rangefinder/range', Range, range_callback)
    main()

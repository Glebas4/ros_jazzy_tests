import rospy  # type: ignore
from clover import srv 
from std_srvs.srv import Trigger
from aruco_pose.msg import MarkerArray
from sensor_msgs.msg import Range
from mavros_msgs.srv import CommandBool 
import math


get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
land = rospy.ServiceProxy('land', Trigger)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

z = 1.5
kx = 1
ky = 0.5
num = 0
coords = [[1, 0.5], [1, 2], [3, 2], [3, 0.5]]


def marker_callback(msg):
    global flag
    markers = msg.markers
    for mark in markers: 
        if mark.id == 157:
            flag = True
            return
    flag = False


def range_callback(msg):
    global dist
    dist = msg.range


def start():
    navigate(x=0, y=0, z=1.7, speed=1, frame_id='body', auto_arm=True)
    rospy.sleep(3)
    navigate(x=2, y=1.5, z=1.7, speed=1, frame_id='aruco_map')
    

def main(args=None):
    global z, num
    print("Start")
    start()
    while dist > 0.25:
        if not flag:
            cx = coords[num][0]
            cy = coords[num][1]
            num+=1
            if num = 3:
                num = 0
            navigate(x=cx, y=cy, z=1.7, speed=1, frame_id='aruco_map')
            rospy.sleep(5)
        else:
            z -= 0.05
            set_position(x=0, y=0, z=z, frame_id='aruco_157')
            rospy.sleep(0.1)
    arming(False)
    print("Done")


if __name__ == '__main__':
    rospy.init_node('flight')
    rospy.Subscriber('aruco_detect/markers', MarkerArray, marker_callback)
    rospy.Subscriber('rangefinder/range', Range, range_callback)
    main()

import rospy
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


def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not flag:
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)


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
    navigate_wait(x=0, y=0, z=1.8, speed=1, frame_id='body', auto_arm=True)
    rospy.sleep(3)
    navigate_wait(x=2, y=1.5, z=1.8)
    

def main():
    global z, num
    print("Start")
    start()
    while dist > 0.3:
        if not flag:
            z = 1.8
            cx = coords[num][0]
            cy = coords[num][1]
            num+=1
            if num == 3:
                num = 0
            navigate_wait(x=cx, y=cy, z=1.8)
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

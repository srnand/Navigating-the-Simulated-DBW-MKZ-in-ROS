#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class ObstacleStopper():
    def __init__(self,min_dist):
        self.min_dist=min_dist
        rospy.Subscriber('/catvehicle/cmd_vel',Twist,self.callBack)
        self.pub = rospy.Publisher('/catvehicle/cmd_vel_safe',Twist,queue_size=0)
    
    def callBack(self,data):
        try:
            closest_distance = rospy.wait_for_message('/distanceEstimator/dist', Float32, timeout=1).data
        except:
            closest_distance = None
        safe_twist=data
        if closest_distance:
            if closest_distance<self.min_dist:
                safe_twist.linear.x=0
        else:
            safe_twist.linear.x=0
        self.pub.publish(safe_twist)

rospy.init_node('obstacle_stopper')
obj = ObstacleStopper(5.0)
rospy.spin()

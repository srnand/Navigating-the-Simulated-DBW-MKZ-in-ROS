#! /usr/bin/env python
import rospy
import actionlib
print "test2..."
from gps_subscriber import GPSSubscriber,WayPoint
print "test1..."
from actionlib.msg import TestFeedback, TestAction
from geometry_msgs.msg import Twist

class GPSActionServer():
    def __init__(self):
        self._as = actionlib.SimpleActionServer("/move_to_waypoint_server",TestAction,self.goal_callback,False)
        self._feedback = TestFeedback()
        self.GPSSubs = GPSSubscriber()
        self.WayPoint = WayPoint()
        self.error=3
        waypoint1 = WayPoint(59.900090,10.899960,0.000000)
        self._waypoint_dict = {1:waypoint1}
        self._as.start()
        self.pub=rospy.Publisher('/catvehicle/cmd_vel_safe',Twist,100)
        self.twist=Twist()
        self.twist.linear.x=0.5
        rospy.loginfo('Action Server Initialized...')
        
    def goal_callback(self,goal):
        
        rospy.loginfo('Action Server Called...')
        rate = rospy.Rate(10)
        waypoint_gps_pos = self._waypoint_dict.get(goal.goal)
        distance = self.GPSSubs.distance_from_waypoint(waypoint_gps_pos)
        
        print distance
        rospy.loginfo(distance)
        ROS_INFO("hello")
        
        while int(distance)>=int(self.error):
            self._feedback.feedback = int(distance)
            self._as.publish_feedback(self._feedback)
            rate.sleep()
            self.pub.publish(self.twist)
            distance=self.GPSSubs.distance_from_waypoint(self.goal)
        return

print "OO test"
rospy.init_node('move_to_waypoint')
print('Server Starting...')
GPSActionServer()
rospy.spin()

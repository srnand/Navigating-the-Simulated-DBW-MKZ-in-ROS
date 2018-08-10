#! /usr/bin/env python
import rospy
import actionlib
from actionlib.msg import TestAction, TestGoal, TestResult, TestFeedback

def feedback_callback(feedback):
    return

rospy.init_node('move_to_waypoint_c')
client = actionlib.SimpleActionClient('move_to_waypoint_server',TestAction)
client.wait_for_server()
rospy.loginfo('Action Server Found...')
goal = TestGoal()
goal.goal=1

client.send_goal(goal,feedback_cb=feedback_callback)
rate = rospy.Rate(10)

while client.get_state() < 2:
    print client.get_state()
    rate.sleep()

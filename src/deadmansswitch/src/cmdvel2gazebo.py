#! /usr/bin/env python
import rospy
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Twist, Pose
import sys, getopt, math

class DMS():
    def __init__(self):
        rospy.init_node('cmdvel2gazebo')
        self.timeout = rospy.Duration.from_sec(0.2)
        self.pubFL=rospy.Publisher('/catvehicle/front_left_steering_position_controller/command',Float64,queue_size=1)
        self.pubFR=rospy.Publisher('/catvehicle/front_right_steering_position_controller/command',Float64,queue_size=1)
        self.pubJ1=rospy.Publisher('/catvehicle/joint1_velocity_controller/command',Float64,queue_size=1)
        self.pubJ2=rospy.Publisher('/catvehicle/joint2_velocity_controller/command',Float64,queue_size=1)
        
        rospy.Subscriber('/catvehicle/cmd_vel_safe',Twist,self.callBack)
        self.L=2.62
        self.T=1.301
        self.x=self.z=0
        
        self.maxsteerL = 0.6
        self.maxrL = self.L/(math.tan(self.maxsteerL))
        
        self.maxsteer = math.atan2(self.L,self.maxrL+(self.T/2.0))
        
        print ("Maximum Steering : ",self.maxsteer)
        
    def callBack(self,data):
        self.x = 2.8101*data.linear.x
        self.z = max(-self.maxsteer,min(self.maxsteer,data.angular.z))
        
    def publish(self):
        newTime = rospy.Time.now()
        if not self.oldTime:
            diff=rospy.Time.now()-rospy.Time.now()
        else:
            diff = newTime - self.oldTime
        self.oldTime=newTime
        if diff>self.timeout:
            self.x=0
            msgRear = Float64()
            msgRear.data = self.x
            self.pubJ1.publish(msgRear)
            self.pubJ2.publish(msgRear)
        else:
            msgRearR = Float64()
            msgRearL = Float64()
            msgSteerL = Float64()
            msgSteerR = Float64()
            
            if self.z==0:
                msgRearR.data=msgRearL.data=self.x
                msgSteerL.data = msgSteerR.data = self.z
            else:
                r = self.L/math.fabs(math.tan(self.z))
                rL = r-(math.copysign(1,self.z)*(self.T/2.0))
                rR = r+(math.copysign(1,self.z)*(self.T/2.0))
                
                msgRearR.data = self.x*rR/r
                msgRearL.data = self.x*rL/r
                
                msgSteerL.data = math.atan2(self.L,rL)*math.copysign(1,self.z)
                msgSteerR.data = math.atan2(self.L,rR)*math.copysign(1,self.z)
                
            self.pubFL.publish(msgSteerL)
            self.pubFR.publish(msgSteerR)
            self.pubJ1.publish(msgRearL)
            self.pubJ1.publish(msgRearR)
            
dms = DMS()
rate=rospy.Rate(1)
dms.oldTime = None
while not rospy.is_shutdown():
    dms.publish()
    rate.sleep()
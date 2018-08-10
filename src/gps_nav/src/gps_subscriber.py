#! /usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
from geopy.distance import vincenty

class WayPoint():
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

class GPSSubscriber():
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        rospy.Subscriber('/fix',NavSatFix,self.callBack)
    
    def get_current_gps(self):
        return WayPoint(self.latitude, self.longitude, self.altitude)
    
    def callBack(self,data):
        self.latitude=round(data.latitude,5)
        self.longitude=round(data.longitude,5)
    
    def distance_from_waypoint(goal):
        origin=(self.latitude,self.longitude)
        goal=(goal.latitude,goal.longitude)
        return vincenty(origin,goal).meters

rospy.init_node('gps_subscriber')
rospy.loginfo('Subscriber Starts...')
GPSSubs = GPSSubscriber()
print "OO test3"
rospy.spin()
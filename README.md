# Navigating-the-Simulated-DBW-MKZ-in-ROS
Navigating a real car prototype in ROS with GPS based localization and laser based obstacle avoidance.

* Performed Autonomous navigation using GPS data and performed Obstacle avoidance using Laser Data.
  * Implemented a SimpleActionServer which constantly calculate the distance to the goal, and return the distance in meters, in integer format, as feedback using **Vincenty's Formula**.
  * Implemented a SimpleActionClient that calls the server and moves the car to the given goal.
* Implemented the Ackerman Steering Geometry for the navigation of the car and featured with DeadMansSwitch functionality.

## Car Following a Circular Route With Ackerman Steering Geometry.

<img src="images/Screen Shot 2018-08-10 at 2.12.47 AM.png" width=650 height=400 >
<br/>

<img src="images/Screen Shot 2018-08-10 at 2.12.53 AM.png" width=650 height=400 >
<br/>

<img src="images/Screen Shot 2018-08-10 at 2.12.58 AM.png" width=650 height=400 >
<br/>

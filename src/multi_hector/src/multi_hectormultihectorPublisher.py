#!/usr/bin/env python
"""
Args: in the command line run
python multibotPublisher.py nBots
Returns:
This python scripts loops indefinitely and reads from the csv file "
pubRate" times
per second and publishes the velocity commands to ROS /mobile_base/
commands/velocity for each bot.
The input file must use the csv format with each row representing the
velocities
for one bot. Each row should follow the format
[velX,velY,velZ,angVelX,angVelY,angVelZ]
"""
import time
import sys
import csv
# ROS Interface
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
fwdVel = 0.0
angVel = 0.0
pubRate = 30

def talker():
    pub = [None]*nBots
    for i in range(nBots):
        topicName = 'robot'+str(i+1)+'/cmd_vel'
        pub[i] = rospy.Publisher(topicName,Twist,queue_size=10)
    rospy.init_node('act', anonymous=True)
    rate = rospy.Rate(pubRate) #hz
    while not rospy.is_shutdown():
        with open('dataExchangeMathROS.csv', 'r') as f:
            try:
                reader = csv.reader(f)
                velList = list(reader) # list of the form [velX,velY, velZ,angVelX,angVelY,angVelZ]
                print "New cmnd", velList
                print "nBots:", nBots
                for i in range(0,nBots):
                    linX = float(velList[i][0])
                    linY = float(velList[i][1])
                    
                    linZ = float(velList[i][2])
                    angX = float(velList[i][3])
                    angY = float(velList[i][4])
                    angZ = float(velList[i][5])
                    linear = [linX,linY,linZ]
                    angular = [angX,angY,angZ]
                    pub[i].publish(Twist(Vector3(linear[0],linear[1],
                    linear[2]),Vector3(angular[0],angular[1],
                    angular[2])))
            except:
                pass
        rate.sleep()
        #time.sleep(0.1)

if __name__ == '__main__':
    try:
        nBots = int(sys.argv[1])
    except ValueError:
        print "The 'nBots' parameteter is required. \n Try '***.py nBots'"
        sys.exit()
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
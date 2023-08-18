#!/usr/bin/env python

import math
import rospy

from offboard_control.px4_modes import PX4_MODE_OFFBOARD
from offboard_control.px4_builder import SetPositionWithYawCmdBuilder,SetVelocityCmdBuilder,SetRawCmdBuilder
from offboard_control.px4_vehicle import PX4Vehicle

def offboard_hover():
    # Create a copter instance and arm the copter.
    rospy.loginfo("Connecting to the vehicle.")
    copter = PX4Vehicle(auto_connect = True)
    copter.arm()
    copter.wait_for_status(copter.is_armed, True, 2)

    # Request the copter to hover using local position commands.
    rospy.loginfo("Sending the set position commands.")
    cmd_p = SetPositionWithYawCmdBuilder.build(x= 5,z = 5)    #绝对位置
    cmd_v = SetVelocityCmdBuilder.build(vx=10,vz=10)
    cmd = SetRawCmdBuilder.build(x=5,z=5,vx=2.5,vz=2.5)
    #copter.set_pose2d(cmd_p)
    #copter.set_velocity(cmd_v)
    copter.set_posvelacc(cmd)

    copter.sleep(2)

    rospy.loginfo("Changing to offboard mode.")
    copter.set_mode(PX4_MODE_OFFBOARD)
    copter.sleep(10.)

    rospy.loginfo("Landing the copter.")
    copter.land(block=True)
    if copter.is_armed():
        copter.disarm()
    copter.disconnect()
#end def

if __name__ == "__main__":
    rospy.init_node("offboard_hover")
    offboard_hover()
    rospy.spin()
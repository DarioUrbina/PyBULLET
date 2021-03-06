import pybullet as p
import time
import math as m
import numpy as np

p.connect(p.GUI)
plane = p.loadURDF("plane.urdf")

cubeStartPos = [-2.65,0,1.5]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
#pendulum = p.loadURDF("r2d2_Dario.urdf",cubeStartPos, cubeStartOrientation, useFixedBase=1)
pendulum = p.loadURDF("Pendulum_for_cart_actuation.urdf",cubeStartPos, cubeStartOrientation, useFixedBase=1, flags=p.URDF_USE_SELF_COLLISION)
p.setGravity(0,0,-10)

motorForce=700

proportional_gain = -1500
integral_gain = -1000
derivative_gain = 3000

"""to keep cart centered: """

proportional_gain_2 = 800
integral_gain_2 = 0
derivative_gain_2 = 0

previous_pendulum_angle = 0
previous_cart_position = 0

for i in range(p.getNumJoints(pendulum)):
    """If more links or joints are added, the joint indexes change"""
    info=p.getJointInfo(pendulum, i)
    print(p.getJointInfo(pendulum, i))
    #print(info[0])
    #print(p.getJointState(pendulum,info[0]))
    #print(info([ info[i] for i in [0,1] ]))

for joint in range(p.getNumJoints(pendulum)):
    p.setJointMotorControl2(pendulum, joint, p.VELOCITY_CONTROL, targetVelocity=10, force=0)
    p.getJointInfo(pendulum, joint)

p.changeDynamics(pendulum, linkIndex=1 , mass=100, restitution=.1)


for i in range (20000):
    p.stepSimulation()
    #info=p.getJointInfo(pendulum, 4)
    pendulum_angle=p.getJointState(pendulum,4)
    cart_position=p.getJointState(pendulum,3)
    #print(pendulum_angle[0])
    print("Cart_position:")
    print(cart_position[0])
    angle_delta_error = 0-pendulum_angle[0]
    #cart_position_delta_error = 0-cart_position[0]
    print("Angle_Delta_Error:")
    print(angle_delta_error)

    #PROPPORTIONAL
    p_correction = proportional_gain * pendulum_angle[0]

    #INTEGRAL
    i_correction = integral_gain * (previous_pendulum_angle + pendulum_angle[0])
    previous_pendulum_angle = pendulum_angle[0]

    #DERIVATIVE
    d_correction = derivative_gain * angle_delta_error

    """to keep cart centered"""
    #PROPPORTIONAL for cart position
    p_correction_2 = proportional_gain_2 * cart_position[0]

    #INTEGRAL for cart position
    i_correction_2 = integral_gain_2 * (previous_cart_position + cart_position[0])
    previous_cart_position = cart_position[0]

    #DERIVATIVE for cart position
    d_correction_2 = derivative_gain_2 * (-cart_position[0])
    """end of to keep cart centered"""
    
    #Input Signal
    u = p_correction + i_correction + d_correction
    u = u + p_correction_2 + i_correction_2 + d_correction_2
    
    p.setJointMotorControl2(pendulum, 3, p.VELOCITY_CONTROL, targetVelocity=10, force=u)

    
        
    time.sleep(1./240.)
p.disconnect()




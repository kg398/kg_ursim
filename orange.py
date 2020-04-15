import numpy as np
import time
import math
from math import pi

import waypoints as wp


def orange(robot):
    start_orange(robot)
    pick_orange(robot)
    cut_orange(robot)
    juice_orange(robot)
    weigh_juice(robot)
    ph_test(robot)
    refrac_test(robot)
    end_orange(robot)
    return

def start_orange(robot):
    '''
    any initialisation here
    '''

    return

def pick_orange(robot):
    '''
    pick orange with suction from a known location
    '''
    robot.movel(wp.orange_home)
    robot.set_digital_out(0,1)
    robot.translatel([-0.325, -0.42, 0.3])
    robot.translatel_rel([0, 0, -0.2])
    robot.set_digital_out(0,0)
    #robot.force_move([0,0,-0.1],force=40)
    time.sleep(1)
    robot.translatel_rel([0,0,0.1])
    robot.movel(wp.orange_home)
    return

def cut_orange(robot):
    '''
    cut orange with fixed knife
    '''
    robot.movej(wp.knife_home)
    robot.translatel_rel([0, 0.1, -0.15])
    sign = 1
    for i in range(0,22):
        robot.translatel_rel([sign*0.04, 0, -0.005])
        time.sleep(0.1) # To lose our momentum
        sign = -sign
    robot.translatel_rel([0, 0.05, 0, 0, 0, 0])
    robot.translatel_rel([0,0,0.1])
    robot.home()
    return

def juice_orange(robot):
    '''
    juice both halves of the orange with electric juicer
    '''
    juice_half(robot)

    robot.movel([-0.12,-0.46,  0.0,0.0,1.5*pi,0.0]) #Rotate end-effector

    robot.movej([-64.0*pi/180,-144.51*pi/180,-117.23*pi/180,-58.63*pi/180,32.80*pi/180,56.40*pi/180])
    robot.set_digital_out(0,0)
    robot.translatel_rel([-0.045,0,0])
    time.sleep(0.5)
    robot.translatel_rel([0.005,0,0])
    robot.translatel_rel([0,0,0.2])

    robot.movel(wp.orange_home)

    juice_half(robot)
    return

def juice_half(robot):
    robot.movel(wp.orange_home)
    robot.translatel([0.275, -0.245, 0.3]) #Over Juicer
    robot.translatel_rel([0, 0, -0.05]) #Onto Juicer
    robot.force_move([0, 0, -0.2], force=40)
    robot.force_move([0, 0, -0.1], force=40)
    time.sleep(2)
    robot.force_move([0, 0, -0.1], force=50)
    time.sleep(2)
    centre_pos = robot.getl()
    for i in range(0, 8):
        robot.translatel_rel([0, 0, 0.05])
        robot.translatel([centre_pos[0]+0.003*np.sin(i*2*pi/8), centre_pos[1]+0.003*np.cos(i*2*pi/8), centre_pos[2]])
        robot.force_move([0, 0, -0.1], force=40)
        time.sleep(2)
        robot.force_move([0, 0, -0.1], force=50)
        time.sleep(2)
    robot.translatel_rel([0, 0, 0.5])
    robot.translatel([0.4, -0.245, 0.3])
    robot.set_digital_out(0, 1)
    time.sleep(0.5)
    robot.movel(wp.orange_home)
    return

def weigh_juice(robot):
    '''
    pick juicer jug with suction, place on scales then pick again
    '''
    return

def ph_test(robot):
    '''
    read ph probe, ignore for now
    '''

    return

def refrac_test(robot):
    '''
    read refractometer, ignore for now
    '''

    return

def end_orange(robot):
    '''
    any additional cleanup, rinse juicer/refractometer etc...
    '''

    return
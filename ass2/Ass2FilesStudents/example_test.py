'''
COMP9418 Assignment 2
This file is similar to the file that will be used to test your assignment
It should be used to make sure you code will work during testing
'''
# Make division default to floating-point, saving confusion
from __future__ import division
from __future__ import print_function

# Allowed libraries 
import numpy as np
import pandas as pd
import scipy as sp
import scipy.special
import heapq as pq
import matplotlib as mp
import matplotlib.pyplot as plt
import math
from itertools import product, combinations
from collections import OrderedDict as odict
import collections
from graphviz import Digraph, Graph
from tabulate import tabulate
import copy
import sys
import os
import datetime
import sklearn
import re
import ast


# import the function written by the student
from example_solution import get_action

# simulator code
class Person:    
    def __init__(self, name, office=None):
        self.name = name
        
    def timestep(self, building_simulator):
        pass

class ReliableSensor:
    def __init__(self, name, room):
        self.room = room
        self.name = name
    def get_output(self, room_occupancy):
        pass

class UnreliableSensor:
    def __init__(self, name, room):
        self.room = room
        self.name = name
    def get_output(self, room_occupancy):
        pass

class DoorSensor:
    def __init__(self, name, rooms):
        self.rooms = rooms #pair of rooms
        self.name = name
    def get_output(self, building_simulator):
        pass

class Robot:
    def __init__(self, name, start_room):
        self.name = name
        self.current_location = start_room
    def timestep(self, building_simulator):
        pass
    

# part of the code from the building simulator.
class SmartBuildingSimulatorExample:
    def __init__(self):
        self.data = pd.read_csv('data.csv')

        self.num_lights = 35
        self.num_people = 20 
        self.start_time = datetime.time(hour=8,minute=0)
        self.end_time = datetime.time(18,0)
        self.time_step = datetime.timedelta(seconds=15) # 15 second
        
        self.current_time = self.start_time

        self.current_electricity_price = 1.0
        self.productivity_cost = 4 
        # cumulative cost so far today
        self.cost = 0

        self.people = [Person(i) for i in range(1,self.num_people+1)]

        self.room_occupancy = dict([(room, 0) for room in ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'r22', 'r23', 'r24', 'r25', 'r26', 'r27', 'r28', 'r29', 'r30', 'r31', 'r32', 'r33', 'r34', 'r35', 'c1', 'c2', 'c3', 'c4', 'o1', 'outside']])
        self.room_occupancy['outside'] = self.num_people
        
        # current state of lights
        lights = {}
        for i in range(1,self.num_lights+1):
            lights["lights"+str(i)] = "off"

        self.lights = lights
            
        # set up of all sensors
        self.reliable_motion_sensors = [ReliableSensor('reliable_sensor1','r16'),
                                   ReliableSensor('reliable_sensor2','r5'),
                                   ReliableSensor('reliable_sensor3','r25'),
                                   ReliableSensor('reliable_sensor4','r31'),
                                  ]
        self.unreliable_motion_sensors = [UnreliableSensor('unreliable_sensor1','o1'),
                                     UnreliableSensor('unreliable_sensor2','c3'),
                                     UnreliableSensor('unreliable_sensor3','r1'),
                                     UnreliableSensor('unreliable_sensor4','r24'),
                                    ]

        self.door_sensors = [DoorSensor('door_sensor1',('r8','r9')),
                        DoorSensor('door_sensor2',('c1','c2')),
                        DoorSensor('door_sensor3',('r26','r27')),
                        DoorSensor('door_sensor4',('c4','r35'))
                       ]

        # the robot starts in room 1, and randomly wanders
        self.robot_sensors = [Robot('robot1','r1'), Robot('robot2', 'r19')]

        self.curr_step = 0
        
    def timestep(self, actions_dict=None):
        '''
        actions_dict is a dictionary that maps from action strings to either 'on' or 'off'
        '''
        # do actions
        if actions_dict is not None:
            for key in actions_dict:
                self.lights[key] # test that that action exists
                self.lights[key] = actions_dict[key]
                
        # get data for current timestep (only for example)
        current_data = self.data.iloc[self.curr_step]
        # move people 
        for room in self.room_occupancy:
            self.room_occupancy[room] = current_data.loc[room]

        # increment time
        self.current_time = (datetime.datetime.combine(datetime.date.today(), self.current_time) + self.time_step).time()

        # calculate cost
        self.cost += self.cost_of_prev_timestep(self.current_electricity_price)
        
        # update electricity price
        #self.current_electricity_price *= np.random.choice([0.98,1/0.98,1.0]) # simple martingale
        self.current_electricity_price *= 1
        
        # work out sensor data
        sensor_data = {}
        for sensor in self.reliable_motion_sensors + self.unreliable_motion_sensors:
            sensor_data[sensor.name] = current_data[sensor.name]
        for robot in self.robot_sensors:
            sensor_data[robot.name] = current_data[robot.name]
        for sensor in self.door_sensors:
            sensor_data[sensor.name] = current_data[sensor.name]

        # To make sure your code can handle this case,
        # set one random sensor to None
        broken_sensor = np.random.choice(list(sensor_data.keys())) 
        sensor_data[broken_sensor] = None

        sensor_data['time'] = self.current_time
        sensor_data['electricity_price'] = self.current_electricity_price

        self.curr_step += 1
        
        return sensor_data

    def cost_of_prev_timestep(self, electricity_price):
        '''
        calculates the cost incurred in the previous 2 minutes
        '''
        cost = 0
        for light, state in self.lights.items():
            room_num = 'r' + (light[6:]) # extract number from string
            if state == 'on':
                cost += self.current_electricity_price
            elif state == 'off':
                cost += self.productivity_cost*self.room_occupancy[room_num]
            else:
                raise Exception("Invalid light state")
        return cost



simulator = SmartBuildingSimulatorExample()

sensor_data = simulator.timestep()
for i in range(len(simulator.data)-1):
    actions_dict = get_action(sensor_data)
    sensor_data = simulator.timestep(actions_dict)

print(f"Total cost for the day: {simulator.cost} cents")

import numpy as np
import pandas as pd

data = pd.read_csv('data.csv')

#reliability of two robots
c_r1 = 0
c_r2 = 0
for i in range(len(data)):
    ob1 = data['robot1'].iloc[i].split('\'')[1]
    ob2 = data['robot2'].iloc[i].split('\'')[1]
    ob_num1 = data['robot1'].iloc[i].split(',')[1].split(')')[0]
    ob_num2 = data['robot2'].iloc[i].split(',')[1].split(')')[0]
    re_num1 = data[ob1].iloc[i]
    re_num2 = data[ob2].iloc[i]
    if int(ob_num1) == int(re_num1):
        c_r1 += 1
    if int(ob_num2) == int(re_num2):
        c_r2 +=1
print(c_r1/len(data))
print(c_r2/len(data))


#function that is used to compute the TP and FN rate of reliable and unreliable sensors
def compute_relia_sensor(sensor,room):
    acc_t = 0
    acc_f = 0
    all_motion_sen = 0
    all_no_motion_sen = 0
    for i in range(len(data)):
        ob = data[sensor].iloc[i]
        ob_room = data[room].iloc[i]
        if ob == 'motion':
            all_motion_sen += 1
            if int(ob_room) > 0:
                acc_t += 1
        else:
            all_no_motion_sen += 1
            if int(ob_room) > 0:
                acc_f += 1
    print('TP for',sensor,':',acc_t/all_motion_sen)
    print('FN for',sensor,':',acc_f/all_no_motion_sen)
        
#reliability of un_r_1
compute_relia_sensor('unreliable_sensor1','o1')
print()

#reliability of un_r_2
compute_relia_sensor('unreliable_sensor2','c3')
print()

#reliability of un_r_3
compute_relia_sensor('unreliable_sensor3','r1')
print()

#reliability of un_r_4
compute_relia_sensor('unreliable_sensor4','r24')
print()

#reliability of r_sensor1
compute_relia_sensor('reliable_sensor1','r16')
print()

#reliability of r_sensor2
compute_relia_sensor('reliable_sensor2','r5')
print()

#reliability of r_sensor3
compute_relia_sensor('reliable_sensor3','r25')
print()

#reliability of r_sensor4
compute_relia_sensor('reliable_sensor4','r31')
print()

#function that is used to compute the TP and FN rate of door sensors of both side.
def compute_relia_door_sensor(sensor,room1,room2):
    acc_t_r1 = 0
    acc_f_r1 = 0
    acc_t_r2 = 0
    acc_f_r2 = 0
    all_motion_sen = 0
    all_no_motion_sen = 0
    for i in range(len(data)):
        ob = data[sensor].iloc[i]
        ob_room1 = data[room1].iloc[i]
        ob_room2 = data[room2].iloc[i]
        if int(ob) > 0:
            all_motion_sen += 1
            if int(ob_room1) > 0:
                acc_t_r1 += 1
            if int(ob_room2) > 0:
                acc_t_r2 += 1
        else:
            all_no_motion_sen += 1
            if int(ob_room1) > 0:
                acc_f_r1 += 1
            if int(ob_room2) > 0:
                acc_f_r2 += 1
    print('TP for',sensor,'of',room1,':',acc_t_r1/all_motion_sen)
    print('FN for',sensor,'of',room1,':',acc_f_r1/all_no_motion_sen)
    print('TP for',sensor,'of',room2,':',acc_t_r2/all_motion_sen)
    print('FN for',sensor,'of',room2,':',acc_f_r2/all_no_motion_sen)

#door sensor 1
compute_relia_door_sensor('door_sensor1','r8','r9')
print()

#door sensor 2
compute_relia_door_sensor('door_sensor2','c1','c2')
print()

#door sensor 3
compute_relia_door_sensor('door_sensor3','r26','r27')
print()

#door sensor 4
compute_relia_door_sensor('door_sensor4','r35','c4')

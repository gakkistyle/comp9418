
import pandas as pd
import numpy as np


'''
This script is used to generate the 5 time period transaction matrix and store the values into a csv file.
'''

#possible room each room goes to next time step
outcomeSpace = {'r1':['r2','r3','r4','r7'],
                'r2':['r1','r4','r3'],
                'r3':['r1','r7','c1'],
                'r4':['r2','r8','r9','r13'],
                'r5':['r6','r9','c3','r13','r11','o1'],
                'r6':['r5','c3'],
                'r7':['r3','c1','r1','r26'],
                'r8':['r4','r5','r9'],
                'r9':['r5','r8','r13'],
                'r10':['c3','r11','r16'],
                'r11':['c3','r5','o1'],
                'r12':['r22','r25','outside'],
                'r13':['r24','r9','r4','r5','r23','r8'],
                'r14':['r24','r13'],
                'r15':['c3','r10','r11'],
                'r16':['c3','r10','o1','r18','r5'],
                'r17':['c3','r11','r21','r18','r16','r5'],
                'r18':['c3','r11','r10','r16','o1'],
                'r19':['c3','r10','o1','r17'],
                'r20':['c3','o1','r11','r6'],
                'r21':['c3','r15','r16','r19','o1'],
                'r22':['c1','c2','r25','r12','outside'],
                'r23':['r24','r13'],
                'r24':['r14','r13','r23'],
                'r25':['r12','c1','c2','r26','r27','r22','r7','c4','r3'],
                'r26':['r27','r25','c1','r32','r22','r7'],
                'r27':['r32','r26','r25','r33','r31'],
                'r28':['c4'],
                'r29':['c4','r30'],
                'r30':['r29'],
                'r31':['r32','r27'],
                'r32':['r31','r33','r27'],
                'r33':['r32','r27'],
                'r34':['c2','c4','c1'],
                'r35':['c4','o1','c2'],
                'c1':['r7','c2','r25','c4','o1','r3','r22'],
                'c2':['c4','c1','r34','o1','c3','r35','r29','r7','r25'],
                'c3':['r15','r10','r11','r16','r17','r18','r19','r5','o1','r9','r20','r21'],
                'c4':['r35','c2','o1','r29','c3','r28','r34','r19','r30'],
                'o1':['c4','c3','r16','r10','r15','c2','r19','c2','r35','r11','r5','r20'],
                'outside':['r12','r22','r25']
}

# function that counts the possiblity of tranfering out from the tar.
def count_tran(data,tar):
    d1 = list(data[tar])
    d2 = d1[1:]
    d2.append(0)
    d1 = np.array(d1)
    if d1.sum() == 0:
        return 0
    d2 = np.array(d2)
    d = d1-d2
    sum = 0
    for once in d:
        if once > 0:
            sum += once

    return sum/d1.sum()

#index is the dictionary, key is the space and value is the corresponding index number.
index = {}
start = 0
for key in outcomeSpace.keys():
    index[key] = start
    start+=1


data = pd.read_csv('data.csv')

#output is the 5 time period transaction matrix, will be stored in tran_matrix.csv file.
output = {}

#first time period (8:00 - 8:05)
for key in outcomeSpace.keys():
    #the transaction rate of the specific space. Inialize it to be all 0.
    tran = [0]*41

    #count the possiblity of moving to other rooms
    for i in range(len(data[:19])-1):
        t1_d = data.iloc[i]
        t2_d = data.iloc[i+1]

        if int(t2_d[key]) < int(t1_d[key]):
            diff = int(t1_d[key]) - int(t2_d[key])
            for mov in outcomeSpace[key]:
                t1_dm = t1_d[mov]
                t2_dm = t2_d[mov]
                diff_m = int(t2_dm)-int(t1_dm)
                if diff_m >= diff:
                    tran[index[mov]] += diff
                    break
                else:
                    if diff_m >0:
                        tran[index[mov]] += diff_m
                        diff -= diff_m
    
    d1 = list(data[:19][key])
    d1 = np.array(d1)
    if d1.sum() != 0:
        tran[:] = [x/d1.sum() for x in tran]
    tran[index[key]] = 1 - count_tran(data[:19], key)
    output[key+'_s1'] = tran

#second time period (8:05 - 17:30)
for key in outcomeSpace.keys():
    tran = [0]*41
    #count the possiblity of moving to other rooms
    for i in range(len(data[19:2279])-1):
        t1_d = data.iloc[19+i]
        t2_d = data.iloc[19+i+1]

        if int(t2_d[key]) < int(t1_d[key]):
            diff = int(t1_d[key]) - int(t2_d[key])
            for mov in outcomeSpace[key]:
                t1_dm = t1_d[mov]
                t2_dm = t2_d[mov]
                diff_m = int(t2_dm)-int(t1_dm)
                if diff_m >= diff:
                    tran[index[mov]] += diff
                    break
                else:
                    if diff_m >0:
                        tran[index[mov]] += diff_m
                        diff -= diff_m
    d1 = list(data[19:2279][key])
    d1 = np.array(d1)
    if d1.sum() != 0:
        tran[:] = [x/d1.sum() for x in tran]
    tran[index[key]] = 1 - count_tran(data[19:2279], key)
    output[key+'_s2'] = tran

#third time period (17:30 - 18:00)
for key in outcomeSpace.keys():
    tran = [0]*41

    #count the possiblity of moving to other rooms
    for i in range(len(data[2279:])-1):
        t1_d = data.iloc[2279+i]
        t2_d = data.iloc[2279+i+1]

        if int(t2_d[key]) < int(t1_d[key]):
            diff = int(t1_d[key]) - int(t2_d[key])
            for mov in outcomeSpace[key]:
                t1_dm = t1_d[mov]
                t2_dm = t2_d[mov]
                diff_m = int(t2_dm)-int(t1_dm)
                if diff_m >= diff:
                    tran[index[mov]] += diff
                    break
                else:
                    if diff_m >0:
                        tran[index[mov]] += diff_m
                        diff -= diff_m
    d1 = list(data[2279:][key])
    d1 = np.array(d1)
    if d1.sum() != 0:
        tran[:] = [x/d1.sum() for x in tran]
    if count_tran(data[2279:], key) == 0:
        tran[index[key]] = 0
    else:
        tran[index[key]] = 1 - count_tran(data[2279:], key)
    output[key+'_s3'] = tran

#output to csv file.
out_csv = pd.DataFrame(output)
out_csv.to_csv('tran_matrix.csv',index=False)

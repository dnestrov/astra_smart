import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
conn = Connection('192.168.1.7:8000')

#Limits

PSUASTRA=['DIV','BVL','BVUT','BVUB','CS','MC','PSH']
PSUST40=['DIV','BVL','BVUT','BVUB','SOL','MC','PSH']
FONTSIZE=12

def plot_voltages_exp(shotst40,index,t1,t2):
    conn.openTree('st40',shotst40)
    TIMEpsu=conn.get('dim_of(PSU.TF:I)').data()
    iupa=np.where(TIMEpsu > t2)
    iup=iupa[0][0]
    idwa=np.where(TIMEpsu < t1)
    idw=idwa[0][len(idwa[0])-1]
    TIME=TIMEpsu[idw:iup]
    plt.figure('Coil voltages, V')
    for j2 in index-np.array([1]):
        signame='PSU.'+PSUST40[j2]+':V'
        VAR=conn.get(signame)
        plt.plot(TIME,VAR[idw:iup],label=str(PSUST40[j2]+' #'+str(shotst40)))
    conn.closeTree('st40',shotst40)
def plot_voltages_astra(shotastra,run,index):
    conn.openTree('astra',shotastra)
    signame0=run
    TIME=conn.get(signame0+':TIME')
    plt.figure('Coil voltages, V')    
    for j2 in index-np.array([1]):
        signame='PSU.'+PSUASTRA[j2]+':V'
        print(signame0+'.'+signame)
        try:
            VAR=conn.get(signame0+'.'+signame)
            plt.plot(TIME,VAR,label=PSUASTRA[j2]+' #'+str(shotastra)+'@'+signame0)
        except:
            print('ASTRA no signal for '+PSUASTRA[j2] )
            return -1   
    return 1

    conn.closeTree('astra',shotastra)
def plot_voltages_astra_all(shotastra,run,names):
    conn.openTree('astra',shotastra)
    signame0=run
    vac=False
    if run[3] == '0':vac=True 
    TIME=conn.get(signame0+':TIME')
    plt.figure('Coil voltages, V',figsize=(10, 3))
    plt.rc('font', size=FONTSIZE)
    signame='COILS.PSU2PF'
    print(signame0+'.'+signame)
    try:
        VAR=conn.get(signame0+'.'+signame+':V')
        NAME=conn.get(signame0+'.'+signame+':PSU_NAMES')
        for j in range(len(NAME)):
            if NAME[j].strip() == 'SOL':
                NAME[j]='CS'
    except: 
        print('ASTRA no signal for '++str(shotastra)+'@'+signame0)
        return -1
    for j1 in range(len(names)):
        for j2 in range(len(NAME)):
            print(names[j1])
            print(NAME[j2])
            if names[j1].strip() == NAME[j2].strip():
                if vac:
                    plt.plot(TIME[1:],VAR[1:,j2],label=NAME[j2].strip()+' #'+str(shotastra)+'@'+signame0)
                else:
                    print('done')
                    plt.plot(TIME[1:],VAR[1:,j2],label=NAME[j2].strip()+' #'+str(shotastra)+'@'+signame0)                
    conn.closeTree('astra',shotastra)
    return 1

def astra_t1_t2(shotastra,run):
    conn.openTree('astra',shotastra)
    signame0=run
    TIME=conn.get(signame0+':TIME')
    t1=min(TIME)
    t2=max(TIME)
    conn.closeTree('astra',shotastra)
    return t1,t2

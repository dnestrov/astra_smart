import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
shotastra=13000025
run='RUN105'
conn = Connection('192.168.1.7:8000')
col=['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan']
#Limits
TF	=[384,	250]
BVL	=[550,	44]
CS	=[1050,	17.1]
DIV	=[480,	23.1]
BVUT	=[480,	12.5]
BVUB	=[480,	12.5]
BVM	=[918,	13.1]
SXT	=[500,	15]
SXB	=[500,	15]
MCX=0.716
MCY=0.318
PSUASTRA=['DIV','BVL','BVUT','BVUB','CS','MC','MCT','MCB','PSH','TF']
PSUST40=['DIV','BVL','BVUT','BVUB','SOL','MC','MCT','MCB','PSH','TF']
LIMITS=[23.1,44,12.5,12.5,17.1,13.1,15]
FONTSIZE=12
def plot_coilcurrents_exp(shotst40,index,t1,t2,count):
    if count>9: count=0
    conn.openTree('st40',shotst40)
    TIMEpsu=conn.get('dim_of(PSU.TF:I)').data()
    iupa=np.where(TIMEpsu > t2)
    iup=iupa[0][0]
    idwa=np.where(TIMEpsu < t1)
    idw=idwa[0][len(idwa[0])-1]
    TIME=TIMEpsu[idw:iup]
    plt.figure('Coil currents, kA',figsize=(10, 3))
    plt.rc('font', size=FONTSIZE)
    for j2 in index-np.array([1]):
        signame='PSU.'+PSUST40[j2]+':I'
        print(signame)
        try:
            VAR=conn.get(signame)/1000
            plt.plot(TIME,VAR[idw:iup],color=col[count],label=str(PSUST40[j2]+' #'+str(shotst40)))
            count+=1
        except: print('ST40 no signal for '+PSUST40[j2] )
    conn.closeTree('st40',shotst40)
    return count+1
def plot_ipl_exp(shotst40):
    conn.openTree('st40',shotst40)
#    signame0='PFIT.RT_RUN01.RESULTS'
    signame0='PFIT.POST_BEST.RESULTS'
#    TIME=conn.get(signame0+':TIME').data()
#    signame0='EFIT.BEST'
#    TIME=conn.get(signame0+':TIME').data()
#IPL= conn.get(signame0+'.CONSTRAINTS.IP:CVALUE').data()/100000
    plt.figure('Coil currents, kA',figsize=(10, 3))
    plt.rc('font', size=FONTSIZE)
    try:
        TIME=conn.get(signame0+':TIME').data()
        IPL= conn.get(signame0+'.GLOBAL:IP').data()/100000
    except:
        print('No PFIT.POST_BEST current')
        return
    plt.plot(TIME,IPL,label=str('IPL/100kA #'+str(shotst40)))
    conn.closeTree('st40',shotst40)
def plot_coilcurrents_astra(treename,shotastra,run,index,count):
    if count>9: count=0
    conn.openTree(treename,shotastra)
    signame0=run
    vac=False
    if run[3] == '0':vac=True 
    TIME=conn.get(signame0+':TIME')
    plt.figure('Coil currents, kA',figsize=(10, 3))
    plt.rc('font', size=FONTSIZE)
    for j2 in index-np.array([1]):
        signame='PSU.'+PSUASTRA[j2]+':I'
        print(signame0+'.'+signame)
        try:
            VAR=conn.get(signame0+'.'+signame)*1000
            if count>9: count=0
            if vac:
                plt.plot(TIME,VAR,color=col[count],label=PSUASTRA[j2]+' #'+str(shotastra)+'@'+signame0)
            else:
                plt.plot(TIME[1:],VAR[1:],color=col[count],label=PSUASTRA[j2]+' #'+str(shotastra)+'@'+signame0)                
            count+=1
        except: 
            return -1
    conn.closeTree(treename,shotastra)
    return count+1
def plot_coilcurrents_astra_all(treename,shotastra,run,names,count):
    if count>9: count=0
    conn.openTree(treename,shotastra)
    signame0=run
    vac=False
    if run[3] == '0':vac=True 
    TIME=conn.get(signame0+':TIME')
    plt.figure('Coil currents, kA',figsize=(10, 3))
    plt.rc('font', size=FONTSIZE)
    signame='COILS.PSU2PF'
    print(signame0+'.'+signame)
    try:
        VAR=conn.get(signame0+'.'+signame+':I')*1000
        NAME=conn.get(signame0+'.'+signame+':PSU_NAMES')
        for j in range(len(NAME)):
            if NAME[j].strip() == 'SOL':
                NAME[j]='CS'
    except: 
        print('ASTRA no signal for '+str(shotastra)+'@'+signame0)
        return -1
    for j1 in range(len(names)):
        for j2 in range(len(NAME)):
            if names[j1].strip() == NAME[j2].strip():
                if count>9: count=0
                if vac:
                    plt.plot(TIME[1:],VAR[1:,j2],color=col[count],label=NAME[j2].strip()+' #'+str(shotastra)+'@'+signame0)
                else:
                    plt.plot(TIME[1:],VAR[1:,j2],color=col[count],label=NAME[j2].strip()+' #'+str(shotastra)+'@'+signame0)                
                count+=1
    conn.closeTree(treename,shotastra)
    return count+1
def plot_ipl_astra(treename,shotastra,run):
    if treename == 'astra': 
        import read_astra_globals as read
    try:
        TIME,IPL=read.read_glob(shotastra,'IPL',run)
        plt.figure('Coil currents, kA',figsize=(10, 3))
        plt.rc('font', size=FONTSIZE)
        plt.plot(TIME,IPL/100000,linestyle='dashed',label='IPL/100kA #'+str(shotastra)+'@'+run)
    except:print('no IPL data for '+ treename+' '+str(shotastra)+'@'+run)
    if treename == 'spider':
        try:
            conn.openTree(treename,shotastra)
            signame0=run
            TIME=conn.get(signame0+':TIME')
            IPL=conn.get(signame0+'GLOBAL:IPL')
            plt.figure('Coil currents, kA',figsize=(10, 3))
            plt.rc('font', size=FONTSIZE)
            plt.plot(TIME,IPL/100000,linestyle='dashed',label='IPL/100kA '+ treename+' '+str(shotastra)+'@'+run)
        except:print('no IPL data for'+ treename+' '+str(shotastra)+'@'+run)

def astra_t1_t2(shotastra,run):
    treename='ASTRA'
    conn.openTree(treename,shotastra)
    signame0=run
    TIME=conn.get(signame0+':TIME')
    t1=min(TIME)
    t2=max(TIME)
    conn.closeTree(treename,shotastra)
    #return t1,t2
    return t1,0.25

def read_coilcurrents_astra(name,shotastra,run,t1,t2):
    conn.openTree('astra',shotastra)
    signame0=run
    TIME=conn.get(signame0+':TIME')
    iupa=np.where(TIME > t2)
    iup=iupa[0][0]
    idwa=np.where(TIME < t1)
    idw=idwa[0][len(idwa[0])-1]
    signame='PSU.'+name+':I'
    print(signame0+'.'+signame)
    try:
        VAR=conn.get(signame0+'.'+signame)*1000
    except: 
        return -1
    conn.closeTree('astra',shotastra)
    return TIME[idw:iup],VAR[idw:iup]
def read_coilcurrents_exp(name,shotst40,t1,t2):
    conn.openTree('st40',shotst40)
    TIME=conn.get('dim_of(PSU.TF:I)').data()
    iupa=np.where(TIME > t2)
    iup=iupa[0][0]
    idwa=np.where(TIME < t1)
    idw=idwa[0][len(idwa[0])-1]

    signame='PSU.'+name+':I'
    print(signame)
    try:
        VAR=conn.get(signame)/1000
    except: 
        print('ST40 no signal for '+name )
        return 0,0
    conn.closeTree('st40',shotst40)
    return  TIME[idw:iup],VAR[idw:iup]


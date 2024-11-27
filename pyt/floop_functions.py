import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
conn = Connection('192.168.1.7:8000')
col=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf']
def plot_floop_exp(shotst40,name,index,t1,t2):
    conn.openTree('st40',shotst40)
    TIMEmag=conn.get('dim_of(MAG.BEST.FLOOP.L001:PSI)').data()
    iupa=np.where(TIMEmag > t2)
    iup=iupa[0][0]
    idwa=np.where(TIMEmag < t1)
    idw=idwa[0][len(idwa[0])-1]
    TIME=TIMEmag[idw:iup]
    plt.figure(1)
    for count,i in enumerate(index):
        signame='MAG.BEST.FLOOP.L'+name[i][6:9]+':PSI'
        VAR=conn.get(signame)
        color=count-len(col)*int(count/len(col))
        plt.plot(TIME,VAR[idw:iup],col[color],label=name[i]+' #'+str(shotst40))
    conn.closeTree('st40',shotst40)
def read_floop_exp(shotst40,name,t1,t2):
    conn.openTree('st40',shotst40)
    TIMEmag=conn.get('dim_of(MAG.BEST.FLOOP.L001:PSI)').data()
    iupa=np.where(TIMEmag > t2)
    iup=iupa[0][0]
    idwa=np.where(TIMEmag < t1)
    idw=idwa[0][len(idwa[0])-1]
    TIME=TIMEmag[idw:iup]
    signame='MAG.BEST.FLOOP.L'+name+':PSI'
    print(signame)
    VAR=conn.get(signame)
    VAR0=np.mean(VAR[idw:iup])
    conn.closeTree('st40',shotst40)
    return VAR0
def read_floop_exp_all(shotst40,name,t1,t2):
    conn.openTree('st40',shotst40)
    TIMEmag=conn.get('dim_of(MAG.BEST.FLOOP.L001:PSI)').data()
    iupa=np.where(TIMEmag > t2)
    iup=iupa[0][0]
    idwa=np.where(TIMEmag < t1)
    idw=idwa[0][len(idwa[0])-1]
    VAR=np.array([])
    for i in range(0,len(name)):
        signame='MAG.BEST.FLOOP.L'+name[i][6:9]+':PSI'
        PSI=conn.get(signame)
        PSI0=np.mean(PSI[idw:iup])
        VAR=np.append(VAR,PSI0)
    conn.closeTree('st40',shotst40)
    return VAR
def floop_map(shotastra,run,name):
    conn.openTree('astra',shotastra)
    signame='FLOOP.ALL:NAME'
    names=conn.get(run+'.'+signame)
    for i in range(0,len(names)):
        if name.strip() == names[i].strip() : 
            return i
    return 999

def plot_floop_astra(shotastra,run,name,index):
    conn.openTree('astra',shotastra)
    signame0=run
    signame='FLOOP:PSI'
    print(signame0+'.'+signame)
    try:
        TIME=conn.get(signame0+':TIME')
        VAR=conn.get(signame0+'.'+signame)
    except:
        print('no such a run'+run+' or signal '+signame0+'.'+signame+'#'+str(shotastra))
        return
    plt.figure(1)
    for count,i in enumerate(index):
        color=count-len(col)*int(count/len(col))
        plt.plot(TIME[1:],VAR[1:,i],col[color],label=name[i]+' #'+str(shotastra)+'@'+signame0)
    conn.closeTree('astra',shotastra)
def plot_floop_astra_all(shotastra,run,name,index):
    conn.openTree('astra',shotastra)
    signame0=run
    signame='FLOOP.ALL:PSI'
    print(signame0+'.'+signame)
    try:
        TIME=conn.get(signame0+':TIME')
        VAR=conn.get(signame0+'.'+signame)
    except:
        print('no such a run'+run+' or signal '+signame0+'.'+signame+'#'+str(shotastra))
        return
    plt.figure(1)
    for count,i in enumerate(index):
        color=count-len(col)*int(count/len(col))
        plt.plot(TIME[1:],VAR[1:,i],col[color],label=name[i]+' #'+str(shotastra)+'@'+signame0)
    conn.closeTree('astra',shotastra)
def plot_floop_astra_all0(shotastra,run,name,index,count):
    conn.openTree('astra',shotastra)
    signame0=run
    signame='FLOOP.ALL:PSI'
    try:
        TIME=conn.get(signame0+':TIME')
        VAR=conn.get(signame0+'.'+signame)
    except:
        print('no such a run'+run+' or signal '+signame0+'.'+signame+'#'+str(shotastra))
        return
    plt.figure(1)
    color=count-len(col)*int(count/len(col))
    plt.plot(TIME,VAR[:,index],col[color],label=name+' #'+str(shotastra)+'@'+signame0)
    conn.closeTree('astra',shotastra)

def astra_t1_t2(shotastra,run):
    conn.openTree('astra',shotastra)
    signame0=run
    TIME=conn.get(signame0+':TIME')
    t1=min(TIME)
    t2=max(TIME)
    conn.closeTree('astra',shotastra)
    return t1,t2

def read_floop_astra_all(shotastra,run):
    conn.openTree('astra',shotastra)
    signame0=run
    signame='FLOOP.ALL:PSI'
    print(signame0+'.'+signame)
    try:
        TIME=conn.get(signame0+':TIME')
        VAR=conn.get(signame0+'.'+signame)
    except:
        print('no such a run'+run+' or signal '+signame0+'.'+signame+'#'+str(shotastra))
        return 0,0
    return TIME,VAR
    conn.closeTree('astra',shotastra)
def read_floop_tree(treename,shotastra,run):
    conn.openTree(treename,shotastra)
    signame0=run
    signame='FLOOP.ALL:PSI'
    print(signame0+'.'+signame)
    try:
        TIME=conn.get(signame0+':TIME')
        VAR=conn.get(signame0+'.'+signame)
    except:
        print('no such a run'+run+' or signal '+signame0+'.'+signame+'#'+str(shotastra))
        return 0,0
    return TIME,VAR
    conn.closeTree(treename,shotastra)
def plot_floop_efit_m(shot,run,index):
    conn.openTree('EFIT',shot)
    print(run+':TIME')
    TIME=conn.get(run+':TIME')
    signame=run+'.CONSTRAINTS.FLUX:'
    NAMES=conn.get(signame+'NAME')
    VAR=conn.get(signame+'MVALUE')
    for count,i in enumerate(index):
        name=NAMES[i].strip()[2:]
        print(name)
        plt.plot(TIME,2*math.pi*VAR[:,i],col[count],linestyle='dashed',label=name+'EFIT'+str(shot)+'@'+run+' in')
    conn.closeTree('EFIT',shot)
def plot_floop_efit_c(shot,run,index):
    conn.openTree('EFIT',shot)
    print(run+':TIME')
    TIME=conn.get(run+':TIME')
    signame=run+'.CONSTRAINTS.FLUX:'
    NAMES=conn.get(signame+'NAME')
    VAR=conn.get(signame+'CVALUE')
    for count,i in enumerate(index):
        name=NAMES[i].strip()[2:]
        print(name)
        plt.plot(TIME,2*math.pi*VAR[:,i],col[count],linestyle='dashed',label=name+'EFIT'+str(shot)+'@'+run+' in')
    conn.closeTree('EFIT',shot)
def read_RZ(shot):
    conn.openTree('MAG',shot)
    signame0='BEST'
    signame='FLOOP.ALL:'
    print(signame0+'.'+signame)
    try:
        R=conn.get(signame0+'.'+signame+'R')
        Z=conn.get(signame0+'.'+signame+'Z')
    except:
        print('no data FLOOP R,Z in MAG.BEST for'+shot)
        return 0,0
    return R,Z


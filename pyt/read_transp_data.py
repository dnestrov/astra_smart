import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
shotnumber=34011560
runnum='T06' 
conn = Connection('192.168.1.7:8000')
def read_prof(shotnumber,profname,runnum):
    conn.openTree('TRANSP_TEST',shotnumber)
    shot=shotnumber
    signame0=str(runnum)
    TIME=conn.get(signame0+':TIME')
    signame='PROFILES.RHOTOR:'+str(profname)
#    print(signame0+'.'+signame)
    VAR=conn.get(signame0+'.'+signame)
    VAR=np.array(VAR)
    if profname == 'TE': VAR=VAR/1e3
    if profname == 'TI': VAR=VAR/1e3
    if profname == 'TX': VAR=VAR/1e3
    if profname == 'NE': VAR=VAR/1e19
    if profname == 'NI': VAR=VAR/1e19
    if profname == 'NF': VAR=VAR/1e19
    if profname == 'NIZ1': VAR=VAR/1e19
    if profname == 'NIZ2': VAR=VAR/1e19
    if profname == 'NIZ3': VAR=VAR/1e19
    if profname == 'NWN': VAR=VAR/1e19
    if profname == 'NCXN': VAR=VAR/1e19
    conn.closeTree
    return TIME,VAR
def read_glob(shotnumber,name,runnum):
    conn.openTree('TRANSP_TEST',shotnumber)
    shot=shotnumber
    signame0=str(runnum)
    TIME=conn.get(signame0+':TIME')
    print(TIME)
    signame='GLOBAL:'+str(name)
    print(signame0+'.'+signame)
    VAR=conn.get(signame0+'.'+signame)
    print(VAR)
    VAR=np.array(VAR)
    if name == 'TE0': VAR=VAR/1e3
    if name == 'TI0': VAR=VAR/1e3
    if name == 'TX0': VAR=VAR/1e3
    if name == 'NE0': VAR=VAR/1e19
    if name == 'NEL': VAR=VAR/1e19
    if name == 'NEV': VAR=VAR/1e19
    if name[0:2] == 'P_': VAR=VAR/1e6
    if name == 'IP': VAR=VAR/1e6
    conn.closeTree
    return TIME,VAR

def read_prof2exp(shotnumber,runnum):
    conn.openTree('TRANSP_TEST',shotnumber)
    try:
        #TIME=conn.get(runnum+':TIME').data()
        from netCDF4 import Dataset
        path='/home/theory/transp/results/ST40.24/'
        shot=int(shotnumber-int(shotnumber/1e6)*1e6)
        file=path+str(shot)+runnum+'.CDF' 
        f= Dataset(file, "r", format="NETCDF4") 
        TIME=f.variables['TIME3'][:]
    except:
        print('NO TRANSP run for '+str(shotnumber)+'@'+runnum)
        return
    NT=np.shape(TIME)[0]
    pronam=['NE','TE','TI']
    pdenom=[1e19,1000,1000]
    NP=np.shape(pronam)[0]
    signal=runnum+'.PROFILES.RHOTOR:'
    RPOS=conn.get(signal+'R_MID').data()
    Z0=0
    NR=RPOS.shape[1]
    step=10
    dr=4#2 or 0
    print(' ***********Profiles from TRANSP #'+str(shotnumber)+'@'+runnum)
    for i in range(NP):
        proval0=conn.get(signal+pronam[i]).data()/pdenom[i] 
        ASTRAnam=pronam[i]
        for ii in range(NT):
            print('GRIDTYPE 19 NAMEXP '+ASTRAnam+' NTIMES 1 POINTS ','%.0f'%(NR/dr))
            print('%.3f'%TIME[ii])
            print('%.3f'%Z0)
            R1=RPOS[ii,:]
            jj=0
            for j in range(0,NR,dr):
                jj+=1
                print('%.3f'%R1[j],end=' ')
                if jj-step*int(jj/step) == 0:print()
            proval=np.append(proval0[ii,::-1],proval0[ii,:]) 
            jj=0
            for j in range(0,NR,dr): 
                jj+=1
                print('%.3f'%proval[j],end=' ')
                if jj-step*int(jj/step) == 0:print()
    conn.closeTree

def read_glob2exp(shotnumber,runnum):
    conn.openTree('TRANSP_TEST',shotnumber)
    gdedim=[' Edge neutrals, 1e15m-3',' Core neutrals, 1e15m-3']
    glonam=['NWN','NCXN']
    gdenom=[1e15,1e15]
    try:
        TIME=conn.get(runnum+':TIME').data()
        from netCDF4 import Dataset
        path='/home/theory/transp/results/ST40.24/'
        shot=int(shotnumber-int(shotnumber/1e6)*1e6)
        file=path+str(shot)+runnum+'.CDF' 
        f= Dataset(file, "r", format="NETCDF4") 
        TIME3=f.variables['TIME3'][:]
    except:
        print('NO TRANSP run for '+str(shotnumber)+'@'+runnum)
        return

    signal=runnum+'.GLOBAL:'
    #print(signal,glonam[0])
    NP=np.shape(glonam)[0]
    zrdnum=[80,81]
    for i in range(NP):
        signal=runnum+'.GLOBAL:'
        if glonam[i] == 'NWN' or glonam[i] == 'NCXN' :
            signal=runnum+'.PROFILES.RHOTOR:'        
            proval=conn.get(signal+glonam[i]).data()/gdenom[i]
            if glonam[i] == 'NWN':gloval=proval[:,len(proval[0,:])-1] 
            if glonam[i] == 'NCXN':gloval=proval[:,0]
            TIME=TIME3
        else:
            gloval=conn.get(signal+glonam[i]).data()/gdenom[i] 
        NT=np.shape(TIME)[0]
        print(' TRANSP run '+str(shotnumber)+'@'+runnum+' '+glonam[i] + gdedim[i])
        for ii in range(NT):            
                print( 'ZRD'+str(zrdnum[i]),'  %.4f '%TIME[ii],'%.3f'%gloval[ii])
    conn.closeTree


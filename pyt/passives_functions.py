import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
conn = Connection('192.168.1.7:8000')
col=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf']
count=0
shotastra=13011717
run='RUN03' 
RUN=run
time=-0.1  
FONTSIZE=12    
def read_rz(shotastra,RUN):
    conn.openTree('astra',shotastra)
    signame0=RUN
    signame='PASSIVES:'
    try:
        R=conn.get(signame0+'.'+signame+'RP')
        Z=conn.get(signame0+'.'+signame+'ZP')
        try:
            dr=conn.get(signame0+'.'+signame+'DR')
            dz=conn.get(signame0+'.'+signame+'DZ')
        except:
            dr=0
            dz=0
        name=conn.get(signame0+'.'+signame+'NAME')
        return R,Z,dr,dz,name
    except:
        print('no such a run #'+str(shotastra)+'@'+RUN)
        return 0,0,' '
def read_rz_file(machine):
    plt.rc('font', size=FONTSIZE)
    R=np.array([])
    Z=np.array([])
    dr=np.array([])
    dz=np.array([])
    resp=np.array([])
    name=np.array([])
    NAME=np.array([])
    try:
        f = open("exp/equ/"+machine+"/fires.dat", "r")
    except:
        f = open(machine+"/fires.dat", "r")
        
    nl=abs(int(f.readline()))
    ii=1
    for i in range(0,nl):
        aa=f.readline()
        R=np.append(R,float(aa.split()[1].replace('D','E')))
        Z=np.append(Z,float(aa.split()[2].replace('D','E')))
        dr=np.append(dr,float(aa.split()[3].replace('D','E')))
        dz=np.append(dz,float(aa.split()[4].replace('D','E')))
        resp=np.append(resp,float(aa.split()[5].replace('D','E')))
        name=np.append(name,str(aa.split()[7]))
    return R,Z,dr,dz,resp,name
def read_rz_file0(machine):
    plt.rc('font', size=FONTSIZE)
    R=np.array([])
    Z=np.array([])
    dr=np.array([])
    dz=np.array([])
    resp=np.array([])
    name=np.array([])
    NAME=np.array([])
    try:
        f = open("exp/equ/"+machine+"/fires0.dat", "r")
    except:
        print("check if exp/equ/"+machine+"/fires0.dat exists")
        return 0,0,0,0,0,' '
    nl=abs(int(f.readline()))
    ii=1
    for i in range(0,nl):
        aa=f.readline()
        R=np.append(R,float(aa.split()[1].replace('D','E')))
        Z=np.append(Z,float(aa.split()[2].replace('D','E')))
        dr=np.append(dr,float(aa.split()[3].replace('D','E')))
        dz=np.append(dz,float(aa.split()[4].replace('D','E')))
        resp=np.append(resp,float(aa.split()[5].replace('D','E')))
        name=np.append(name,str(aa.split()[7]))
    return R,Z,dr,dz,resp,name
def write_rz_file(machine,R,Z,dr,dz,resp,name):
    f = open("exp/equ/"+machine+"/fires.dat", "w")
    f.write(str(-len(R))+'\n')
    for i in range(0,len(R)): 
        f.write('1 '+str(R[i])+' '+str(Z[i])+' '+str(dr[i])+' '+str(dz[i])+' '+str(resp[i])+' 0 '+name[i]+'\n')
def read_passive_time(name,shotastra,run):
    conn.openTree('astra',shotastra)
    signame0=run
    signame='PASSIVES:'
    try:
        TIME=conn.get(signame0+':TIME')
        I=conn.get(signame0+'.'+signame+'I')
        NAME=conn.get(signame0+'.'+signame+'NAME')
    except:
        print('no such a run '+run+' or signal '+signame0+'.'+signame+'#'+str(shotastra))
        return 0,0

    ind=np.array([])
    nl=len(NAME)
    for i in range(0,nl):
        if NAME[i] == name: ind = np.append(ind,i)
    index=ind.astype(int)
    VAR=np.sum(I[:,index],axis=1)     
    return TIME,VAR


def plot_passives(ax,RP,ZP,dr,dz,name,shotastra,run,time,count):
    conn.openTree('astra',shotastra)
    signame0=run
    signame='PASSIVES:'
    nl=len(name)
    NAME=np.array([])
    NAME=np.append(NAME,name[0])
    for i in range(1,nl):
        if name[i] != name[i-1] : 
            NAME=np.append(NAME,name[i])
    try:
        TIME=conn.get(signame0+':TIME')
        VAR=conn.get(signame0+'.'+signame+'I')
    except:
        print('no such a run '+run+' or signal '+signame0+'.'+signame+'#'+str(shotastra))
        return 0,0,0
    ind=np.where(TIME>=time)[0][0]
    print('ASTRA:',shotastra,'@',run,'time=',TIME[ind])
    ii=0
    CURR=0
    for i in range(0,nl):
        if name[i]!= name[i-1] and i > 1: 
            print(NAME[ii],CURR)
            CURR=0
            ii+=1        
        CURR=CURR+VAR[ind,i]
    print(NAME[ii].strip()[6:],CURR)
    ax.scatter3D(RP,ZP,VAR[ind,:]/dr/dz,zdir='z',c=col[count],marker='.',label='#'+str(shotastra)+'@'+run+',time='+str(TIME[ind])) 
    for i in range(len(RP)):
        ax.plot([RP[i],RP[i]],[ZP[i],ZP[i]],[VAR[ind,i]/dr[i]/dz[i],0],col[count])
    conn.closeTree('astra',shotastra)
    ax.scatter(RP,ZP,RP*0,c='black',marker='x')
    return TIME,VAR
def plot_passives_newshot(ax,RP,ZP,dr,dz,shotastra,run,time,count):
    conn.openTree('astra',shotastra)
    signame0=run
    signame='PASSIVES:'
    try:
        TIME=conn.get(signame0+':TIME')
        VAR=conn.get(signame0+'.'+signame+'I')
    except:
        print('no such a run '+run+' or signal '+signame0+'.'+signame+'#'+str(shotastra))
        return
    ind=np.where(TIME>=time)[0][0]
    print('time=',TIME[ind]) 
    ax.scatter3D(RP,ZP,VAR[ind,:]/dr/dz,zdir='z',c=col[count],marker='.',label='#'+str(shotastra)+'@'+run+',time='+str(TIME[ind])) 
    for i in range(len(RP)):
        ax.plot([RP[i],RP[i]],[ZP[i],ZP[i]],[VAR[ind,i]/dr[i]/dz[i],0],col[count])
    conn.closeTree('astra',shotastra)
    ax.scatter(RP,ZP,RP*0,c='black',marker='x')
    return TIME,VAR
def plot_passives_newtime(ax,TIME,RP,ZP,dr,dz,VAR,time,count):
    ind=np.where(TIME>=time)[0][0]
    print('time=',TIME[ind])      
    ax.scatter3D(RP,ZP,VAR[ind,:]/dr/dz,zdir='z',c=col[count],marker='.',label='#'+str(shotastra)+'@'+run+',time='+str(TIME[ind])) 
    for i in range(len(RP)):
        ax.plot([RP[i],RP[i]],[ZP[i],ZP[i]],[VAR[ind,i]/dr[i]/dz[i],0],col[count])


"""
for i in range(1,len(name)):
    if name[i]!=name[i-1]:
        print(name[i-1].strip()+'","',end='')
deltaR=0.03
R0,Z,dr,dz,resp,name=a.read_rz_file('EFIT')
R=R0*0
for i in range(1,len(name)):
    R[i]=R0[i]
    if name[i]=='DIVPSRT' or name[i]=='DIVPSRB':
        print(i,name[i].strip())
        R[i]=R0[i]+deltaR
a.write_rz_file('EFI2',R,Z,dr,dz,resp,name)


def read_rz():
    plt.rc('font', size=FONTSIZE)
    machin="EFIT"
    R=np.array([])
    Z=np.array([])
    dr=np.array([])
    dz=np.array([])
    resp=np.array([])
    name=np.array([])
    NAME=np.array([])
    try:
        f = open("exp/equ/"+machin+"/fires.dat", "r")
    except:
        f = open(machin+"/fires.dat", "r")
        
    nl=abs(int(f.readline()))
    ii=1
    for i in range(0,nl):
        aa=f.readline()
        R=np.append(R,float(aa.split()[1].replace('D','E')))
        Z=np.append(Z,float(aa.split()[2].replace('D','E')))
        dr=np.append(dr,float(aa.split()[3].replace('D','E')))
        dz=np.append(dz,float(aa.split()[4].replace('D','E')))
        resp=np.append(dz,float(aa.split()[5].replace('D','E')))
        name=np.append(name,str(aa.split()[7]))
    return R,Z,dr,dz,name
def read_rz(shotastra,run):
    conn.openTree('astra',shotastra)
    signame0=run
    signame='PASSIVES:'
    try:
        TIME=conn.get(signame0+':TIME')
        R=conn.get(signame0+'.'+signame+'RP')
        Z=conn.get(signame0+'.'+signame+'ZP')
        NAME=conn.get(signame0+'.'+signame+'NAME')
    except:
        print('no such a run #'+str(shotastra)+'@'+run)
        return 0,0,0,0,' '
    return R,Z,NAME




R,Z,dr,dz,resp,name=a.read_rz_file('FE23')
name1=name
for i in range(0,len(name)-1):
    if name[i] == 'IVC' and R[i] > 0.6:
        name1[i] =name[i] +'_OUT60'
a.write_rz_file('FE23',R,Z,dr,dz,resp,name1)
"""

import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
shotnumber=13311419
runnum='RUN2340' 
conn = Connection('192.168.1.7:8000')
def read_global(shotnumber,name,runnum):
    conn.openTree('EFIT',shotnumber)
    shot=shotnumber
    signame0=str(runnum)
    TIME=conn.get(signame0+':TIME')
    print(TIME)
    signame='GLOBAL:'+str(name)
    print(signame0+'.'+signame)
    VAR=conn.get(signame0+'.'+signame)
    print(VAR)
    VAR=np.array(VAR)
    conn.closeTree
    return TIME,VAR
def read_virial(shotnumber,name,runnum):
    conn.openTree('EFIT',shotnumber)
    shot=shotnumber
    signame0=str(runnum)
    TIME=conn.get(signame0+':TIME')
    print(TIME)
    signame='VIRIAL:'+str(name)
    print(signame0+'.'+signame)
    VAR=conn.get(signame0+'.'+signame)
    print(VAR)
    VAR=np.array(VAR)
    conn.closeTree
    return TIME,VAR
def read_constraints(shotnumber,name,runnum):
    try:
        conn.openTree('EFIT',shotnumber)
    except:print('No Tree for EFIT',shotnumber)
    shot=shotnumber
    signame0=str(runnum)
    try:
        TIME=conn.get(signame0+':TIME')
    except:
        print('No EFIT data',shotnumber,runnum,name)
        return 0,0,0,0,0,0

    signame='CONSTRAINTS.'+str(name)+':'
    print(signame0+'.'+signame)
    CVALUE=conn.get(signame0+'.'+signame+'CVALUE')
    MVALUE=conn.get(signame0+'.'+signame+'MVALUE')
    SIGMA=conn.get(signame0+'.'+signame+'SIGMA')
    WEIGHT=conn.get(signame0+'.'+signame+'WEIGHT')
    CHI=conn.get(signame0+'.'+signame+'CHI')
    NAME=conn.get(signame0+'.'+signame+'NAME')
    CVALUE=np.array(CVALUE)
    MVALUE=np.array(MVALUE)
    SIGMA=np.array(SIGMA)
    WEIGHT=np.array(WEIGHT)
    TIME=np.array(TIME)
    conn.closeTree('EFIT',shotnumber)
    return TIME,CVALUE,MVALUE,SIGMA,WEIGHT,CHI,NAME

def read_CHI(shotnumber,name,runnum):
    try:
        conn.openTree('EFIT',shotnumber)
    except:print('No Tree for EFIT',shotnumber)
    shot=shotnumber
    signame0=str(runnum)
    try:
        TIME=conn.get(signame0+':TIME')
    except:
        print('No EFIT data',shotnumber,runnum,name)
        return 0,0,0,0
    signame='CONSTRAINTS.'+str(name)+':'
    print(signame0+'.'+signame)
    CHI=conn.get(signame0+'.'+signame+'CHI')
    CHI=np.array(CHI)
    conn.closeTree('EFIT',shotnumber)
    return TIME,CHI


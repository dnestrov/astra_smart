import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
conn = Connection('192.168.1.7:8000')
def read_prof(shotnumber,profname,runnum):
    conn.openTree('astra',shotnumber)
    shot=shotnumber
    signame0=str(runnum)
    TIME=conn.get(signame0+':TIME')
    signame='PROFILES.ASTRA:'+str(profname)
#    print(signame0+'.'+signame)
    VAR=conn.get(signame0+'.'+signame)
    VAR=np.array(VAR)
    return TIME,VAR
def read_profPSI(shotnumber,profname,runnum):
    conn.openTree('astra',shotnumber)
    shot=shotnumber
    signame0=str(runnum)
    TIME=conn.get(signame0+':TIME')
    signame='PROFILES.PSI_NORM:'+str(profname)
#    print(signame0+'.'+signame)
    VAR=conn.get(signame0+'.'+signame)
    VAR=np.array(VAR)
    return TIME,VAR



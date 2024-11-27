import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys

#python3 read_st40_astra_coilcurrents.py 8779 13008779 RUN12
#python3 read_st40_astra_coilcurrents.py 8779 13000010 RUN92 
#python3 read_st40_astra_coilcurrents.py 9850 13009850 RUN1006
#python3 read_st40_astra_coilcurrents.py 10820 13010820 RUN01
orig_stdout = sys.stdout
conn = Connection('192.168.1.7:8000')

#shotnumber=360
efitnumber='BEST'
shotst40=int(sys.argv[1])
shotastra=int(sys.argv[2])

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
PSUASTRA=['DIV','BVL','BVUT','BVUB','CS','MC','PSH']
NAMESST40=['BVL','BVUT','BVUB','DIV','MC','PSH','SOL']
NAMESASTRA=['DIV','BVL','BVUT','BVUB','CS']
NAMESST40=['DIV','BVL','BVUT','BVUB','SOL']
LIMITS=[23.1,44,12.5,12.5,17.1,13.1,15]
ind=np.array([])
for j2 in range(0,len(NAMESASTRA)):
    for j1 in range(0,7):
        if NAMESASTRA[j2]==PSUASTRA[j1]:
            ind=np.append(ind,j1)

t1=1
t2=-1
print(ind)
ind=ind.astype(int)
print(ind)
print(LIMITS[ind[0]])
plt.suptitle('Coil currents per turn: #'+str(shotst40)+' vs #'+str(shotastra))
conn.openTree('astra',shotastra)
for j1 in range(3,len(sys.argv)):
    signame0=sys.argv[j1]
    TIME=conn.get(signame0+':TIME')
    t0=min(TIME)
    t1=min(t0,t1)
    t0=max(TIME)
    t2=max(t0,t2)
conn.closeTree('astra',shotastra)

print(signame0)
conn.openTree('st40',shotst40)
TIMEpsu=conn.get('dim_of(PSU.TF:I)').data()
iupa=np.where(TIMEpsu > t2)
iup=iupa[0][0]
idwa=np.where(TIMEpsu < t1)
idw=idwa[0][len(idwa[0])-1]
TIME=TIMEpsu[idw:iup]

print(t1,t2,np.size(TIME))
plt.figure(1)
#plt.suptitle('#'+str(shotst40))
for j2 in range(0,len(NAMESST40)):
    print(j2)
    print(NAMESST40[j2])
    signame='PSU.'+NAMESST40[j2]+':I'
    print(signame)
    VAR=conn.get(signame)/1000
    #plt.figure(j2+1)
    #plt.suptitle(' #'+str(shotst40)+'@'+signame+'  kA')
    plt.plot(TIME,VAR[idw:iup],label=str(NAMESST40[j2]+' #'+str(shotst40)))
    #plt.legend(loc='lower left',fontsize='small')

conn.closeTree('st40',shotst40)
conn.openTree('astra',shotastra)
for j1 in range(3,len(sys.argv)):
    signame0=sys.argv[j1]
    print(signame0)
    TIME=conn.get(signame0+':TIME')
    print(np.size(TIME))
    plt.figure(1)
#    plt.suptitle(' #'+str(shotastra))
    for j2 in range(0,len(NAMESASTRA)):
        signame='PSU.'+NAMESASTRA[j2]+':I'
        print(signame0+'.'+signame)
        VAR=conn.get(signame0+'.'+signame)*1000
        if np.size(VAR) == 1:
            signame='PSU.BVU:I'
            VAR=conn.get(signame0+'.'+signame)*1000
        #plt.figure(j2+1)
        plt.plot(TIME,VAR,label=NAMESASTRA[j2]+' #'+str(shotastra)+'@'+signame0)
        #plt.plot(TIME,np.zeros(np.size(TIME))+float(LIMITS[ind[j2]]),'k',dashes=[2,1])
        #plt.plot(TIME,np.zeros(np.size(TIME))-float(LIMITS[ind[j2]]),'k',dashes=[2,1])
#        plt.legend(loc='upper right',fontsize='small')

conn.closeTree('astra',shotastra)

plt.legend(loc='upper left',fontsize='small')
plt.show()

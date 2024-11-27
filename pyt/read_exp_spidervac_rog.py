#python3 read_exp_spidervac_rog.py 10014 13210014 RUN1
#python3 read_exp_spidervac_rog.py 10009 13210009 RUN1
#python3 read_exp_spidervac_rog.py 10364 13010364 RUN02
#python3 read_exp_spidervac_rog.py 10820 13010820 RUN02 RUN04
import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
orig_stdout = sys.stdout
conn = Connection('192.168.1.7:8000')

#shotnumber=360
efit='BEST'
MAGRUN='BEST'
na=100

shot=int(sys.argv[1])
shotastra=int(sys.argv[2])
"""
shotastra=13210014
shot =10014
signame0='RUN1'
"""
ROGnam=[
    'DIVPSRB',
    'DIVPSRT',
    'HFSPSRB',
    'HFSPSRT',
    'MCB',
    'MCT',
    'GASBFLB',
    'GASBFLT',
    'BVLB',
    'BVLT',
    'DIVB',
    'DIVT',
    'INIVC000',
    'MCWIRE',
    'DIVBWIRE',
    'BVLWIRE'
]

index=[1,2,3,4]
index=[9,10,16]
#index=[1,3,5,7,9,11,13]
#index=[7,8]
#index=[5,6,14]
#index=[14,15,16]
#index=[1,2,4,13]
#index=[5,6,9,10,11,12]
index=[11,12,15]
ng=len(ROGnam)
ni=len(index)
conn.openTree('ST40',shot)
TIMEmag=conn.get('dim_of(MAG.ROG.TFWIRE:I)').data()
jj=0
for j in index-np.array([1]):
    signame='MAG.'+MAGRUN+'.ROG.'+ROGnam[j]+':I'
    signame='MAG.ROG.'+ROGnam[j]+':I'
    print(signame)
    ROG0=conn.get(signame).data()
    if ROGnam[j] == 'DIVT': ROG0=-ROG0
    if ROGnam[j] == 'DIVB': ROG0=-ROG0/10
    if jj==0:
        ROG1=ROG0
    elif jj==1:
        ROG1=np.append([ROG1],[ROG0],axis=0)
    else:
        ROG1=np.append(ROG1,[ROG0],axis=0)
    jj=jj+1

conn.closeTree('st40',shot)
ROG1=ROG1/1000#go to kA
ROG1=ROG1
plt.figure(1)
plt.suptitle('Rogowski signals #'+str(shotastra)+'@'+sys.argv[3]+' #'+str(shot))

nrows=ni
ncols=1
conn.openTree('astra',shotastra)
for signame0 in sys.argv[3:len(sys.argv)]:
    TIME=conn.get(signame0+':TIME')
    jj=0
    for j in index-np.array([1]):
        signame=signame0+'.ROG.'+ROGnam[j]+':I'
        print(signame)
        ROG=conn.get(signame)
        ROG=ROG/1000# go to kA
        ax=plt.subplot(nrows,ncols,jj+1)
        plt.subplots_adjust(hspace=0.7)
        if j == index[0]-1:
            ax.plot(TIME,ROG,label='#'+str(shotastra)+signame0)
        else:
            ax.plot(TIME,ROG)
        jj=jj+1

print(TIME)
n1=np.where(TIMEmag > min(TIME))
n2=np.where(TIMEmag > max(TIME))
print(TIMEmag[n1[0][0]],TIMEmag[n2[0][0]])
jj=0
for j in range(0,ni):
    ax=plt.subplot(nrows,ncols,jj+1)
    plt.subplots_adjust(hspace=0.7)
    if jj == ni-1:
        ax.plot(TIMEmag[n1[0][0]:n2[0][0]],ROG1[j][n1[0][0]:n2[0][0]],'r',label='#'+str(shot))
    else:
        print(j-1)
        print(index[jj])
        ax.plot(TIMEmag[n1[0][0]:n2[0][0]],ROG1[j][n1[0][0]:n2[0][0]],'r')

    plt.title(ROGnam[index[jj]-1],fontsize=10)
    jj=jj+1

legend=ax.legend(loc='upper left',fontsize='small')
conn.closeTree('astra',shotastra)
plt.show()

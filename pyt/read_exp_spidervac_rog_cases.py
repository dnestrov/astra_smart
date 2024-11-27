#python3 read_exp_spidervac_rog.py 10014 13210014 RUN1
#python3 read_exp_spidervac_rog.py 10009 13210009 RUN1
#python3 read_exp_spidervac_rog.py 10364 13010364 RUN02
#python3 read_exp_spidervac_rog_cases.py 10820 13010820 MC RUN01
#python3 read_exp_spidervac_rog_cases.py 10820 13010820 BVL RUN02 RUN04
#python3 read_exp_spidervac_rog_cases.py 10820 13010820 DIV RUN02 RUN04
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
CASE=str(sys.argv[3])
turns=[11,16,28] 
coils=['MC','BVL','DIV']
ROGnam=['B','T','WIRE']
polar=1
if CASE == 'MC':
    index=1
elif CASE == 'BVL':
    index=2
elif CASE == 'DIV':
    index=3
    polar=-1
    ROGnam[2]='BWIRE'
else:
    print('No such a case:',CASE)
    sys.exit()

conn.openTree('ST40',shot)
TIMEmag=conn.get('dim_of(MAG.ROG.TFWIRE:I)').data()
jj=0
signame='MAG.ROG.'+CASE+ROGnam[2]+':I'
print(signame)
wire0=conn.get(signame).data()
for j in range(0,2):
    signame='MAG.ROG.'+CASE+ROGnam[j]+':I'
    print(signame,turns[index-1])
    ROG0=polar*conn.get(signame).data()
    if index==3 and j==0: ROG0=ROG0/10
    ROG0=(ROG0-wire0*turns[index-1])/1000#go to kA
#    ROG0=ROG0/1000#go to kA
    if jj==0:
        ROG1=ROG0
    elif jj==1:
        ROG1=np.append([ROG1],[ROG0],axis=0)
    else:
        ROG1=np.append(ROG1,[ROG0],axis=0)
    jj=jj+1

conn.closeTree('st40',shot)
plt.figure(1)
plt.suptitle('Rogowski signals #'+str(shotastra)+'@'+sys.argv[3]+' #'+str(shot))

nrows=3
ncols=1
conn.openTree('astra',shotastra)
for signame0 in sys.argv[4:len(sys.argv)]:
    print(signame0)
    TIME=conn.get(signame0+':TIME')
    signame=signame0+'.ROG.'+CASE+ROGnam[2]+':I'
    print(signame)
    wire=conn.get(signame)
    ax=plt.subplot(nrows,ncols,3)
    ax.plot(TIME,wire/1000,label='#'+str(shotastra)+signame0)
    for j in range(0,2):
        signame=signame0+'.ROG.'+CASE+ROGnam[j]+':I'
        print(signame)
        ROG=conn.get(signame)
        ROG=(ROG-wire*turns[index-1])/1000# go to kA

        plt.subplots_adjust(hspace=0.7)
        ax=plt.subplot(nrows,ncols,j+1)
        ax.plot(TIME,ROG,label='#'+str(shotastra)+signame0)
n1=np.where(TIMEmag > min(TIME))
n2=np.where(TIMEmag > max(TIME))
plt.subplots_adjust(hspace=0.7)
for j in range(0,2):
    ax=plt.subplot(nrows,ncols,j+1)
    ax.plot(TIMEmag[n1[0][0]:n2[0][0]],ROG1[j][n1[0][0]:n2[0][0]],'r',label='#'+str(shot))
    plt.title('Rogowski cases current in '+CASE+ROGnam[j],fontsize=10)

ax=plt.subplot(nrows,ncols,3)
ax.plot(TIMEmag[n1[0][0]:n2[0][0]],wire0[n1[0][0]:n2[0][0]]/1000,'r',label='#'+str(shot))
plt.title('Rogowski wire current '+CASE+ROGnam[2],fontsize=10)

legend=ax.legend(loc='upper left',fontsize='small')
conn.closeTree('astra',shotastra)
plt.show()

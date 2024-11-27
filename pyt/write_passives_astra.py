import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
#python3 pyt/write_passives_astra.py FE23 13010820 RUN01 0.0095 FEN
#python3 pyt/write_passives_astra.py P2.3 13011560 RUN01 0.0095 ST40

machin=str(sys.argv[1])
CASE=str(sys.argv[5])
if machin == 'SV4_' : 
  PSUST80=['P1','P2','P3','P4','P5','P6','P7','P8','VCCL','VCCU','SOL','P9'] # S
if machin == 'V402' : 
  PSUST80=['P1','P4','P5','P6','P7','SOL'] 
if machin == 'V403' : 
  PSUST80=['SOL','P1','P2','P4','P5','P6','P8'] 
if machin == 'SV3_' or machin == 'SV31' :
  PSUST80=['P1','P2','P3','P4','P5','P6','P7','P8','VCCL','VCCU','SOL']# SV3_
PSUST40=['DIV','BVL','BVUT','BVUB','CS','MC','PSH' ]
PSUFEN=['MC','PSH','DIV','BVL','BVUT','BVUB','CS' ]
MW=1
if CASE == 'ST40' :
  PSU=PSUST40
elif  CASE == 'FEN' :
  PSU=PSUFEN
elif  CASE == 'ST80' :
  PSU=PSUST80

conn = Connection('192.168.1.7:8000')

machin=str(sys.argv[1])
shot=int(sys.argv[2])
run=str(sys.argv[3])
time=float(sys.argv[4])
#machin='P2.3'
#shot=13000040
#run='RUN298'
#time=0.06
#machin='SV2_'
#shot=13000033
#run='RUN21'
#time=0.2

conn.openTree('ASTRA',shot)
signame=run
TIME=conn.get(signame+':TIME')
iupa=np.where(TIME > time)
if np.any(iupa):
  iup=iupa[0][0]
else:
  iup=len(TIME)-1
idwa=np.where(TIME <= time)
idw=idwa[0][len(idwa[0])-1]
dt0=TIME[iup]-TIME[idw]
signame=run+'.PASSIVES'
print(signame+':I')
I_PASS=conn.get(signame+':I')
signame=run+'.PSU.'
I_PF=np.array([])
for j in range(len(PSU)):
  print(signame+PSU[j]+':I')
  I=conn.get(signame+PSU[j]+':I')
  if np.any(iupa):
    VAR=I[idw]+(I[iup]-I[idw])/dt0*(time-TIME[idw])
  else:
    VAR=I[iup]
  I_PF=np.append(I_PF,VAR)
conn.closeTree('ASTRA',shot)
print(len(I_PF))
file=open('exp/equ/'+machin+'/currents.dat','w')
#file=open('currents.wr','w')
npf=len(I_PF)
if CASE == 'FEN':npf=npf+1
npass=len(I_PASS[0,:])
file.write(str(npf))
file.write('  ')
file.write(str(npf+npass))
file.write('\n')
if CASE == 'FEN':file.write('0.0 ')
for i in range(0,len(I_PF)):
  file.write(format(float(I_PF[i]/MW),"13.4e"))
  print(format(float(I_PF[i]/MW),"6.3f"),end=' ')
  if i+1 == int((i+1)/3)*3:file.write('\n')
file.write('\n')
print('\n')
print(len(I_PASS[0,:]))
for i in range(0,len(I_PASS[0,:])):
  if np.any(iupa):
    VAR=I_PASS[idw,i]+(I_PASS[iup,i]-I_PASS[idw,i])/dt0*(time-TIME[idw])
  else:
    VAR=I_PASS[iup,i]
  print(format(float(VAR[0]/MW),"10.3e"),end=' ')
  file.write(format(float(VAR[0]/MW),"13.4e"))
  if i+1 == int((i+1)/3)*3:file.write('\n')
file.write('\n')
print('\n')
file.close()

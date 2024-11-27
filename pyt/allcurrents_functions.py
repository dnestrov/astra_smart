import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
sys.path.append("/home/alexei.dnestrovskij/astra_project/astra_work/pyt")
import passives_EFIT as e
import coilcurrents_functions as c
#python3 pyt/write_passives_astra.py FE23 13010820 RUN01 0.0095 FEN
#python3 pyt/write_passives_astra.py P2.3 13011560 RUN01 0.0095 ST40
PSUST40=['DIV','BVL','BVUT','BVUB','CS','MC','PSH' ]
PSUFEN=['MC','PSH','DIV','BVL','BVUT','BVUB','CS' ]
MW=1
shotelmag=206
conn = Connection('192.168.1.7:8000')
def write_cur(treename,vac,machin,shot,run,time,zeros):
  CASE='ST40'
  PSU=PSUST40
  l=len(machin)
  if machin[l-4:l] == 'FE23' or machin[l-4:l] == 'EFSO' :
    PSU=PSUFEN
    CASE='FEN'
  conn.openTree(treename,shot)
  signame0=run
  if treename == 'SOPHIA': 
    if vac:
      signame0=run+'.VACUUM'
    else:
      signame0=run+'.PLASMA'      
  try:
    print(signame0)
    TIME=conn.get(signame0+':TIME')
  except:
    print('no such a run '+run)
    return
  iupa=np.where(TIME > time)
  if np.any(iupa):
    iup=iupa[0][0]
  else:
    iup=len(TIME)-1
  idwa=np.where(TIME <= time)
  idw=idwa[0][len(idwa[0])-1]
  dt0=TIME[iup]-TIME[idw]
  signame=signame0+'.PASSIVES'
  print(signame+':I')
  I_PASS=conn.get(signame+':I')
  if zeros:I_PASS=0*I_PASS
  signame=signame0+'.PSU.'
  I_PF=np.array([])
  try:
    signame=signame0+'.PSU.'
    for j in range(len(PSU)):
      print(signame+PSU[j]+':I')
      I=conn.get(signame+PSU[j]+':I')
      if np.any(iupa):
        VAR=I[idw]+(I[iup]-I[idw])/dt0*(time-TIME[idw])
      else:
        VAR=I[iup]
      I_PF=np.append(I_PF,VAR)
  except:
    signame='COILS.PSU2PF'
    print(signame0+'.'+signame+':I')
    IPSU=conn.get(signame0+'.'+signame+':I')
    NAME=conn.get(signame0+'.'+signame+':PSU_NAMES')
    for j1 in range(len(PSU)):
      for j2 in range(len(NAME)):
        if PSU[j1].strip() == NAME[j2].strip():
          I=IPSU[:,j2]
          if np.any(iupa):
            VAR=I[idw]+(I[iup]-I[idw])/dt0*(time-TIME[idw])
          else:
            VAR=I[iup]
      I_PF=np.append(I_PF,VAR)
  conn.closeTree(treename,shot)
  print(len(I_PF))
  file=open(machin+'/currents.dat','w')
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
def write_EFIT_cur(machin,shotefit,runefit,timeefit):
  try:
    Re
  except:
    Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
  index=np.array([])
  for i in range(0,13):index=np.append(index,i)
  ivc=True
  PASS=e.read_passives(VAR,ivc,index,shotefit,runefit,timeefit)
  CURR=e.read_active(shotefit,runefit,timeefit)
  filename=machin+'/currents.dat'
  fw=open(filename,'w') 
  fw.write(str(len(CURR))+'  '+str(len(CURR)+len(PASS))+'\n')
  for j in range(0,len(CURR)): 
    fw.write(str(CURR[j])+'   ') 
    if j>0 and j == int(j/3)*3:fw.write('\n')
  fw.write('\n')
  for j in range(0,len(PASS)): 
    fw.write(str(PASS[j])+'   ') 
    if j+1 == int((j+1)/3)*3:fw.write('\n')
  fw.close()
def write_EFIT_cur_1192(machin,shotefit,runefit,timeefit):
  try:
    Re
  except:
    Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
  index=np.array([])
  for i in range(0,13):index=np.append(index,i)
  ivc=True
  PASS=e.read_passives(VAR,ivc,index,shotefit,runefit,timeefit)
  CURR=e.read_active364(shotefit,runefit,timeefit)
  filename=machin+'/currents.dat'
  fw=open(filename,'w') 
  fw.write(str(' 1 '+str(1+len(CURR)+len(PASS))+'\n') )#1 1193
  fw.write(str(' 0 \n')) # 0 - just one current in coil.dat
  for j in range(0,len(CURR)): 
    fw.write(str(CURR[j])+'   ') 
    if j == int(j/3)*3:fw.write('\n')
  fw.write('\n')
  for j in range(0,len(PASS)): 
    fw.write(str(PASS[j])+'   ') 
    if j+1 == int((j+1)/3)*3:fw.write('\n')
  fw.close()


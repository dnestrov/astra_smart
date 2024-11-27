import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import sys
import read_astra_profs as read
shotnum=13011560
shotastra=shotnum
profname='TE'
prof=profname
run='RUN605' 
RUN=run
time1=0.07
time2=0.08
def plot_fill(shotnum,profname,run,time1,time2):
               print(shotnum,profname,run)
               if profname=='Q':
                              TIME,VAR=read.read_profPSI(shotnum,profname,run)
               else:
                              TIME,VAR=read.read_prof(shotnum,profname,run)
               TIME,X=read.read_prof(shotnum,'RHO',run)
               ind=np.where((TIME-time1)*(TIME-time2) < 0)               
               if np.array(ind).shape[1] == 0:
                              print(run,'no profile for this time ',time1,'<t<',time2)
               else:
                              t1=np.array(ind).astype(int)[0,0] 
                              t2=np.array(ind).astype(int)[0,len(ind[0])-1]
                              nr=len(X)
                              print(t1,t2,nr)
                              for ntime in range(t1,t2):                                            
                                             #print(ntime)
                                             VARmax=0+VAR[ntime,:]     
                                             VARmin=0+VAR[ntime,:]     

                                             #print(VAR[ntime,:])
                                             #XN=np.sqrt((X[ntime,:]-X[ntime,0])/(X[ntime,nr-1]-X[ntime,0]))
                                             XN=X/X[nr-1]
                                             for i in range(0,nr):
                                                            VARmax[i]=max(VAR[t1:t2,i])   
                                                            VARmin[i]=min(VAR[t1:t2,i])   
               plt.fill_between(XN,VARmin,VARmax,color='red',alpha=0.2)
               plt.plot(XN,VAR[t1,:],label=profname+'-'+str(shotnum)+'@'+run)
               plt.plot(XN,VAR[t2,:])
def read_prof_rho(shotnum,profname,run,time1,time2):
               print(shotnum,profname,run)
               try:
                              if profname=='Q':
                                             TIME,VAR=read.read_profPSI(shotnum,profname,run)
                              else:
                                             TIME,VAR=read.read_prof(shotnum,profname,run)
               except:
                              print('No ASTRA data for '+profname)
                              return 0,0,0,0,0
               TIME,X=read.read_prof(shotnum,'RHO',run)
               ind=np.where((TIME-time1)*(TIME-time2) < 0)               
               if np.array(ind).shape[1] == 0:
                              print(run,'no profile for this time ',time1,'<t<',time2)
                              return 0,0,0,0,0
               else:
                              t1=np.array(ind).astype(int)[0,0] 
                              t2=np.array(ind).astype(int)[0,len(ind[0])-1]
                              nr=len(X)
                              print(t1,t2,nr)
                              XN=X/X[nr-1]                                            
                              VARmax=0*VAR[t1,:]     
                              VARmin=0*VAR[t1,:]     
                              for i in range(0,nr):
                                             VARmax[i]=max(VAR[t1:t2,i])   
                                             VARmin[i]=min(VAR[t1:t2,i])   
               return XN,VAR[t1,:],VAR[t2,:],VARmin,VARmax
def read_prof_R(shotnum,profname,run,time1,time2):
               print(shotnum,profname,run)
               try:
                              if profname=='Q':
                                             TIME,VAR=read.read_profPSI(shotnum,profname,run)
                              else:
                                             TIME,VAR=read.read_prof(shotnum,profname,run)
               except:
                              print('No ASTRA data for '+profname)
                              return 0,0,0,0

               TIME,RMID=read.read_prof(shotnum,'RMID',run)
               TIME,RMINOR=read.read_prof(shotnum,'RMINOR',run)
               ind=np.where((TIME-time1)*(TIME-time2) < 0)               
               if np.array(ind).shape[1] == 0:
                              print(run,'no profile for this time ',time1,'<t<',time2)
                              return 0,0,0,0
               else:
                              t1=np.array(ind).astype(int)[0,0] 
                              t2=np.array(ind).astype(int)[0,len(ind[0])-1]
               X=RMID-RMINOR
               Y=RMID+RMINOR
               R1=np.append(X[t1,::-1],Y[t1,:])  
               R2=np.append(X[t2,::-1],Y[t2,:])
               VAR1=np.append(VAR[t1,::-1],VAR[t1,:])
               VAR2=np.append(VAR[t2,::-1],VAR[t2,:])
               return R1,R2,VAR1,VAR2
def read_calc_rho(shotnum,profname,run,time1,time2):
               print(shotnum,profname,run)
               if profname=='DVOL': 
                              try:
                                             TIME,VOL=read.read_prof(shotnum,'VOL',run)
                                             VAR=np.diff(VOL)
                              except:
                                             print('No ASTRA data for '+profname)
                                             return 0,0,0,0,0
               if profname=='PRESSTH': 
                              try:
                                             TIME,NE=read.read_prof(shotnum,'NE',run)
                                             TIME,NI=read.read_prof(shotnum,'NI',run)
                                             TIME,TE=read.read_prof(shotnum,'TE',run)
                                             TIME,TI=read.read_prof(shotnum,'TI',run)
                                             VAR=NE*TE+NI*TI
                              except:
                                             print('No ASTRA data for '+profname)
                                             return 0,0,0,0,0
               if profname=='PRESSE': 
                              try:
                                             TIME,NE=read.read_prof(shotnum,'NE',run)
                                             TIME,TE=read.read_prof(shotnum,'TE',run)
                                             VAR=NE*TE
                              except:
                                             print('No ASTRA data for '+profname)
                                             return 0,0,0,0,0
               TIME,X=read.read_prof(shotnum,'RHO',run)
               ind=np.where((TIME-time1)*(TIME-time2) < 0)               
               if np.array(ind).shape[1] == 0:
                              print(run,'no profile for this time ',time1,'<t<',time2)
                              return 0,0,0,0,0
               else:
                              t1=np.array(ind).astype(int)[0,0] 
                              t2=np.array(ind).astype(int)[0,len(ind[0])-1]
                              nr=len(X)
                              print(t1,t2,nr)
                              XN=X/X[nr-1]
                              VARmax=0*VAR[t1,:]     
                              VARmin=0*VAR[t1,:]     
                              for i in range(0,nr):
                                             VARmax[i]=max(VAR[t1:t2,i])   
                                             VARmin[i]=min(VAR[t1:t2,i])   
               if profname=='DVOL': XN=XN[:nr-1]               
               return XN,VAR[t1,:],VAR[t2,:],VARmin,VARmax

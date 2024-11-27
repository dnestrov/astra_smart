import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import sys
import read_transp_data as transp
shotnum=46011560
shottransp=shotnum
profname='TE'
prof=profname
run='K01' 
RUN=run
time1=0.07
time2=0.08
def read_prof_rho(shotnum,profname,run,time1,time2):
               print(shotnum,profname,run)
               try:
                              TIME,VAR=transp.read_prof(shotnum,profname,run)
               except:
                              print('No TRANSP data for '+profname)
                              return 0,0,0,0,0
               TIME,X=transp.read_prof(shotnum,'RHOTOR',run)
               ind=np.where((TIME-time1)*(TIME-time2) < 0)               
               if np.array(ind).shape[1] == 0:
                              print(run,'no profile for this time ',time1,'<t<',time2)
               else:
                              t1=np.array(ind).astype(int)[0,0] 
                              t2=np.array(ind).astype(int)[0,len(ind[0])-1]
                              nr=len(X[0])
                              XN=X[0]/X[0,nr-1]
                              print(t1,t2,nr)
                              VARmax=0*VAR[t1,:]     
                              VARmin=0*VAR[t1,:]     
                              for i in range(0,nr):
                                             VARmax[i]=max(VAR[t1:t2,i])   
                                             VARmin[i]=min(VAR[t1:t2,i])   
               return XN,VAR[t1,:],VAR[t2,:],VARmin,VARmax
def read_prof_R(shotnum,profname,run,time1,time2):
               print(shotnum,profname,run)
               try:
                              TIME,VAR=transp.read_prof(shotnum,profname,run)
               except:
                              print('No TRANSP data for '+profname)
                              return 0,0,0,0
               TIME,RMID=transp.read_prof(shotnum,'R_MID',run)
               ind=np.where((TIME-time1)*(TIME-time2) < 0)               
               if np.array(ind).shape[1] == 0:
                              print(run,'no profile for this time ',time1,'<t<',time2)
                              return 0,0,0,0
               else:
                              t1=np.array(ind).astype(int)[0,0] 
                              t2=np.array(ind).astype(int)[0,len(ind[0])-1]

               R1=RMID[t1,:] 
               R2=RMID[t2,:] 
               VAR1=np.append(VAR[t1,::-1],VAR[t1,:])
               VAR2=np.append(VAR[t2,::-1],VAR[t2,:])
               return R1,R2,VAR1,VAR2
def read_glob(shotnum,name,run):
               print(shotnum,name,run)
               try:
                              TIME,VAR=transp.read_glob(shotnum,name,run)
               except:
                              print('No TRANSP data for '+name)
                              return 0,0
               return TIME,VAR
def read_calc_rho(shotnum,profname,run,time1,time2):
               print(shotnum,profname,run)
               if profname=='VOL': 
                              try:
                                             TIME,VOLUME=transp.read_prof(shotnum,'VOLUME',run)
                                             VAR=VOLUME/10
                              except:
                                             print('No TRANSP data for '+profname)
                                             return 0,0,0,0,0
               else:
                              print('No TRANSP data for '+profname)
                              return 0,0,0,0,0                               
               TIME,X=transp.read_prof(shotnum,'RHOTOR',run)
               ind=np.where((TIME-time1)*(TIME-time2) < 0)               
               if np.array(ind).shape[1] == 0:
                              print(run,'no profile for this time ',time1,'<t<',time2)
               else:
                              t1=np.array(ind).astype(int)[0,0] 
                              t2=np.array(ind).astype(int)[0,len(ind[0])-1]
                              nr=len(X[0])
                              XN=X[0]/X[0,nr-1]
                              print(t1,t2,nr)
                              if t1 == t2 :
                                       VARmax[:]= VAR[t1,:]     
                                       VARmin[:]= VAR[t1,:]
                              else:
                                             VARmax=0*VAR[t1,:]     
                                             VARmin=0*VAR[t1,:]  
                                             for i in range(0,nr):
                                                            VARmax[i]=max(VAR[t1:t2,i])   
                                                            VARmin[i]=min(VAR[t1:t2,i])   
               if profname=='VOL':
                     VAR[t1,:]=np.cumsum(VAR[t1,:])
                     VAR[t2,:]=np.cumsum(VAR[t2,:])
                     VARmin=np.cumsum(VARmin)
                     VARmax=np.cumsum(VARmax)
                     
               return XN,VAR[t1,:],VAR[t2,:],VARmin,VARmax


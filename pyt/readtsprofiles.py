from MDSplus import *
import sys
import numpy as np
import math
conn = Connection('192.168.1.7:8000')
def ts(shotnumber,runnum,time1,time2,t1,t2,filt):
    step=10
    Z0=0 #  vertical shift od the chord
    TSnam=['NE','TE']
    pdenom=[1e19,1000]
    NP=np.shape(TSnam)[0]
    conn.openTree('ST40',shotnumber)
    signame='TS.'+runnum
    try:
        TIME=conn.get(signame+':TIME')
        signame1='PPTS.BEST.GLOBAL:BAD_MA'
        BAD_MA=conn.get(signame1)
    except:
        print(' No data')
        return
    R=conn.get(signame+':R')
    NT=TIME.shape[0]
    NR=R.shape[0]
    for i in range(NP):
        proval=conn.get(signame+'.PROFILES:'+TSnam[i])/pdenom[i]
        for ii in range(NT):
            R1=np.array([])
            TS1=np.array([])
            for iii in range(NR-1,0,-1):
                if math.isnan(proval[ii][iii]) != True :
                #print(TIME[ii],R[iii],proval[ii][iii])
                    R1=np.append(R1,R[iii])
                    TS1=np.append(TS1,proval[ii][iii])
                NR1=R1.shape[0]
            if NR1 > 1  and TIME[ii] <= time2 and TIME[ii] >= time1 :
                if (TIME[ii] - t1)*(TIME[ii] - t2)<=0.0 and TSnam[i] == 'NE' or BAD_MA[ii] == 0:
                    print(' GRIDTYPE 19 NAMEXP '+TSnam[i]+' NTIMES 1 POINTS ','%.0f'%NR1,' FILTER ','%.3f'%filt)
                else:
                    print('GRIDTYPE 19 NAMEXP '+TSnam[i]+' NTIMES 1 POINTS ','%.0f'%NR1,' FILTER ','%.3f'%filt)
                print('%.3f'%TIME[ii])
                print('%.3f'%Z0)
                for j in range(0,NR1,step):
                    for jj in range(0,step): 
                        if j+jj < NR1 : print('%.3f'%R1[j+jj],end=' ')

                    print()
                for j in range(0,NR1,step):
                        for jj in range(0,step): 
                            if j+jj < NR1 : print('%.3f'%TS1[j+jj],end=' ')
                        print()

def tsHFS(shotnumber,runnum,time1,time2,t1,t2,TIMEefit,RMAG):
    step=10
    Z0=0 #  vertical shift od the chord
    TSnam=['NE','TE']
    pdenom=[1e19,1000]
    NP=np.shape(TSnam)[0]
    conn.openTree('ST40',shotnumber)
    signame='TS.'+runnum
    try:
        TIME=conn.get(signame+':TIME')
    except:
        print(' No data')
        return
    R=conn.get(signame+':R')
    NT=TIME.shape[0]
    NR=R.shape[0]
    for i in range(NP):
        proval=conn.get(signame+'.PROFILES:'+TSnam[i])/pdenom[i]
        for ii in range(NT):
            R1=np.array([])
            TS1=np.array([])
            it=np.where(TIMEefit > TIME[ii])
            if [[]] == np.array(it).tolist():
#                print(TIME[ii])
                continue
            it0=it[0][0]
            R0=RMAG[it0]
            for iii in range(NR-1,0,-1):
                if math.isnan(proval[ii][iii]) != True  and R[iii] <= R0 :
                #print(TIME[ii],R[iii],proval[ii][iii])
                    R1=np.append(R1,R[iii])
                    TS1=np.append(TS1,proval[ii][iii])
                NR1=R1.shape[0]
            if NR1 > 1  and TIME[ii] <= time2 and TIME[ii] >= time1:
                if (TIME[ii] - t1)*(TIME[ii] - t2)<=0.0:
                    print(' GRIDTYPE 19 NAMEXP '+TSnam[i]+' NTIMES 1 POINTS ','%.0f'%NR1)
                else:
                    print('GRIDTYPE 19 NAMEXP '+TSnam[i]+' NTIMES 1 POINTS ','%.0f'%NR1)
                print('%.3f'%TIME[ii])
                print('%.3f'%Z0)
                for j in range(0,NR1,step):
                    for jj in range(0,step): 
                        if j+jj < NR1 : print('%.3f'%R1[j+jj],end=' ')

                    print()
                for j in range(0,NR1,step):
                        for jj in range(0,step): 
                            if j+jj < NR1 : print('%.3f'%TS1[j+jj],end=' ')
                        print()

def tsLFS(shotnumber,runnum,time1,time2,t1,t2,TIMEefit,RMAG):
    step=10
    Z0=0 #  vertical shift od the chord
    TSnam=['NE','TE']
    pdenom=[1e19,1000]
    NP=np.shape(TSnam)[0]
    conn.openTree('ST40',shotnumber)
    signame='TS.'+runnum
    try:
        TIME=conn.get(signame+':TIME')
    except:
        print(' No data')
        return
    R=conn.get(signame+':R')
    NT=TIME.shape[0]
    NR=R.shape[0]
    for i in range(NP):
        proval=conn.get(signame+'.PROFILES:'+TSnam[i])/pdenom[i]
        for ii in range(NT):
            R1=np.array([])
            TS1=np.array([])
            it=np.where(TIMEefit > TIME[ii])
            if [[]] == np.array(it).tolist():
#                print(TIME[ii])
                continue
            it0=it[0][0]
            R0=RMAG[it0]
            for iii in range(NR-1,0,-1):
                if math.isnan(proval[ii][iii]) != True  and R[iii] >= R0 :
                #print(TIME[ii],R[iii],proval[ii][iii])
                    R1=np.append(R1,R[iii])
                    TS1=np.append(TS1,proval[ii][iii])
                NR1=R1.shape[0]
            if NR1 > 1  and TIME[ii] <= time2 and TIME[ii] >= time1:
                if (TIME[ii] - t1)*(TIME[ii] - t2)<=0.0:
                    print(' GRIDTYPE 19 NAMEXP '+TSnam[i]+' NTIMES 1 POINTS ','%.0f'%NR1)
                else:
                    print('GRIDTYPE 19 NAMEXP '+TSnam[i]+' NTIMES 1 POINTS ','%.0f'%NR1)
                print('%.3f'%TIME[ii])
                print('%.3f'%Z0)
                for j in range(0,NR1,step):
                    for jj in range(0,step): 
                        if j+jj < NR1 : print('%.3f'%R1[j+jj],end=' ')

                    print()
                for j in range(0,NR1,step):
                        for jj in range(0,step): 
                            if j+jj < NR1 : print('%.3f'%TS1[j+jj],end=' ')
                        print()

  

            

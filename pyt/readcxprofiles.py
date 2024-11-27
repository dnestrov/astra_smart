from MDSplus import *
import sys
import numpy as np
import math
conn = Connection('192.168.1.7:8000')
def cxmean(shotnumber,runnum):
    step=10
    Z0=0 #  vertical shift od the chord
    CXnam=['TI','VTOR']
    pdenom=[1000,1000]
    NP=np.shape(CXnam)[0]
    conn.openTree('ST40',shotnumber)
    signame='CXFF_PI.'+runnum
#    print(signame)
    TIME=conn.get(signame+':TIME')
    R=conn.get(signame+':R')
    NT=TIME.shape[0]
    NR=R.shape[0]
    ARR=np.array([])
    T=np.array([])
    for i in range(NP):
        CXT=np.array([])
        TIMECX=np.array([])
        proval=conn.get(signame+'.PROFILES:'+CXnam[i])/pdenom[i]
        for ii in range(NT):
            R1=np.array([])
            CX1=np.array([])
            for iii in range(NR-1,0,-1):
                if math.isnan(proval[ii][iii]) != True and proval[ii][iii] != 0 :
                #print(TIME[ii],R[iii],proval[ii][iii])
                    R1=np.append(R1,R[iii])
                    CX1=np.append(CX1,proval[ii][iii])
                NR1=R1.shape[0]
            CX0=np.mean([CX1])
            if math.isnan(CX0) != True and CX0 != 0 :
                CXT=np.append(CX0,CXT)
                TIMECX=np.append(TIMECX,TIME[ii])
#        print(CXnam[i])
#        print(TIMECX)
#        print(CXT)
        if i == 0:
            ARR=CXT
            T=TIMECX
        elif i == 1:
            ARR=np.append([ARR],[CXT],axis=0)
            T=np.append([T],[TIMECX],axis=0)
        else:
            ARR=np.append(ARR,[CXT],axis=0)
            T=np.append(T,[TIMECX],axis=0)
    return T,ARR
def cxmax(shotnumber,runnum):
    step=10
    Z0=0 #  vertical shift od the chord
    CXnam=['TI','VTOR']
    pdenom=[1000,1000]
    NP=np.shape(CXnam)[0]
    conn.openTree('ST40',shotnumber)
    signame='CXFF_PI.'+runnum
#    print(signame)
    TIME=conn.get(signame+':TIME')
    R=conn.get(signame+':R')
    NT=TIME.shape[0]
    NR=R.shape[0]
    ARR=np.array([])
    T=np.array([])
    for i in range(NP):
        CXT=np.array([])
        TIMECX=np.array([])
        proval=conn.get(signame+'.PROFILES:'+CXnam[i])/pdenom[i]
        for ii in range(NT):
            R1=np.array([])
            CX1=np.array([])
            for iii in range(NR-1,0,-1):
                if math.isnan(proval[ii][iii]) != True and proval[ii][iii] != 0 :
                #print(TIME[ii],R[iii],proval[ii][iii])
                    R1=np.append(R1,R[iii])
                    CX1=np.append(CX1,proval[ii][iii])
                NR1=R1.shape[0]
            CX0=max(proval[ii][:])
            if math.isnan(CX0) != True and CX0 != 0 :
                CXT=np.append(CX0,CXT)
                TIMECX=np.append(TIMECX,TIME[ii])
#        print(CXnam[i])
#        print(TIMECX)
#        print(CXT)
        if i == 0:
            ARR=CXT
            T=TIMECX
        elif i == 1:
            ARR=np.append([ARR],[CXT],axis=0)
            T=np.append([T],[TIMECX],axis=0)
        else:
            ARR=np.append(ARR,[CXT],axis=0)
            T=np.append(T,[TIMECX],axis=0)
    return T,ARR


def cx19TWS(shotnumber,runnum,time2,CXnam):
    step=10
    Z0=0 #  vertical shift od the chord
    pdenom=[1000,1000]
    NP=1
    conn.openTree('ST40',shotnumber)
    signame='CXFF_TWS_C.'+runnum
    #print(signame)
    try:
        TIME=conn.get(signame+':TIME')
    except:
        print(' No CX TWS data for '+CXnam+'#'+str(shotnumber))
        return
    R=conn.get(signame+':R')
    NT=TIME.shape[0]
    NR=R.shape[0]
    for i in range(NP):
        proval=conn.get(signame+'.PROFILES:'+CXnam)/pdenom[i]
        print(' data from '+signame+'.PROFILES:'+CXnam)
        for ii in range(NT):
            R1=np.array([])
            CX1=np.array([])
            for iii in range(NR-1,-1,-1):
#                print(iii,TIME[ii],R[iii],proval[ii][iii])
                if math.isnan(proval[ii][iii]) != True and proval[ii][iii] != 0 :
                    R1=np.append(R1,R[iii])
                    CX1=np.append(CX1,proval[ii][iii])
                NR1=R1.shape[0]
            if NR1 > 1  and TIME[ii] <= time2:
                print('GRIDTYPE 19 NAMEXP '+CXnam+' NTIMES 1 POINTS ','%.0f'%NR1)
                print('%.3f'%TIME[ii])
                print('%.3f'%Z0)
                for j in range(0,NR1,step):
                    for jj in range(0,step): 
                        if j+jj < NR1 : print('%.3f'%R1[j+jj],end=' ')

                    print()
                for j in range(0,NR1,step):
                        for jj in range(0,step): 
                            if j+jj < NR1 : print('%.3f'%CX1[j+jj],end=' ')
                        print()
def cx19PI(shotnumber,runnum,time2,CXnam):
    step=10
    Z0=0 #  vertical shift od the chord
    pdenom=[1000,1000]
    NP=1
    conn.openTree('ST40',shotnumber)
    signame='CXFF_PI.'+runnum
    #print(signame)
    try:
        TIME=conn.get(signame+':TIME')
    except:
        print(' No CX PI data for '+CXnam+'#'+str(shotnumber))
        return
    R=conn.get(signame+':R')
    NT=TIME.shape[0]
    NR=R.shape[0]
    for i in range(NP):
        proval=conn.get(signame+'.PROFILES:'+CXnam)/pdenom[i]
        print(' data from '+signame+'.PROFILES:'+CXnam)
        for ii in range(NT):
            R1=np.array([])
            CX1=np.array([])
            for iii in range(NR-1,0,-1):
                if math.isnan(proval[ii][iii]) != True and proval[ii][iii] != 0 :
                #print(TIME[ii],R[iii],proval[ii][iii])
                    R1=np.append(R1,R[iii])
                    CX1=np.append(CX1,proval[ii][iii])
                NR1=R1.shape[0]
            if NR1 > 1  and TIME[ii] <= time2:
                print('GRIDTYPE 19 NAMEXP '+CXnam+' NTIMES 1 POINTS ','%.0f'%NR1)
                print('%.3f'%TIME[ii])
                print('%.3f'%Z0)
                for j in range(0,NR1,step):
                    for jj in range(0,step): 
                        if j+jj < NR1 : print('%.3f'%R1[j+jj],end=' ')

                    print()
                for j in range(0,NR1,step):
                        for jj in range(0,step): 
                            if j+jj < NR1 : print('%.3f'%CX1[j+jj],end=' ')
                        print()

            

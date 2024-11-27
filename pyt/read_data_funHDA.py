import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
glonam=['NE0','NEV','TE0','TEV','TI0','TIV','WTH','ZEFF']
gdenom=[1e19,1e19,1000,1000,1000,1000,1000,1]
NG=np.shape(glonam)[0]
conn = Connection('192.168.1.7:8000')

def read_HDA_glob(shotnumber,runnum):
    conn.openTree('HDA',shotnumber)
    TIME=conn.get(runnum+':TIME').data()
    NT=np.shape(TIME)[0]
    signal=runnum+'.GLOBAL:'
    #print(signal,glonam[0])
    for i in range(NG):
        signal+glonam[i]
        gloval=conn.get(signal+glonam[i]).data()/gdenom[i] 
        print(' HDA@'+runnum+' '+glonam[i] )
        for ii in range(NT): 
            if math.isnan(gloval[ii]) != True :
                print( 'ZRD'+str(40+i),'  %.4f '%TIME[ii],'%.3f'%gloval[ii])
def read_HDA_prof(shotnumber,runnum):
    conn.openTree('HDA',shotnumber)
    TIME=conn.get(runnum+':TIME').data()
    NT=np.shape(TIME)[0]
    pronam=['NE','NI','TE','TI','ZEFF']
    pdenom=[1e19,1e19,1000,1000,1]
    NP=np.shape(pronam)[0]
    signal=runnum+'.PROFILES.R_MIDPLANE:'
    RPOS=conn.get(signal+'RPOS').data()
    ZPOS=conn.get(signal+'ZPOS').data()
    NR=np.shape(RPOS)[0]
    step=10
    print(' ***********Profiles from HDA@'+runnum+'tree ***************')
    for i in range(NP):
        proval=conn.get(signal+pronam[i]).data()/pdenom[i] 
        ASTRAnam=pronam[i]
        if ASTRAnam == 'NI':  ASTRAnam='NIX'
        if ASTRAnam == 'ZEFF':  ASTRAnam='ZEFX'
        k=np.array([])
        #    for ii in range(NT):
        #        if math.isnan( proval[ii][0]) == True or proval[ii][0] == 0 :k=np.append(k,ii)
        #    NT1=NT-len(k)
        if len(k) == 0 : k=np.append(k,999)
        print('GRIDTYPE 20 NAMEXP '+ASTRAnam+' NTIMES ','%.0f'%NT,' POINTS ','%.0f'%NR)
        for ii in range(NT): 
            for kk in range(0,len(k)): 
                if ii != k[kk]:
                    print( '%.3f'%TIME[ii], end = ' ')
            print()
        for j in range(0,NR,step): 
            for jj in range(0,step): 
                if j+jj < NR :print( '%.3f'%RPOS[j+jj],end=' ')
            print()
        for j in range(0,NR,step): 
            for jj in range(0,step): 
                if j+jj < NR :print( '%.3f'%ZPOS[j+jj],end=' ')
            print()

        for ii in range(NT):
            for kk in range(0,len(k)): 
                if ii != k[kk]:
                    for j in range(0,NR,step):
                        for jj in range(0,step): 
                            if j+jj < NR : print('%.3f'%proval[ii][j+jj],end=' ')
                        print()


    imp=np.array([])
    try:
        imp=np.append(imp,conn.get(runnum+'.METADATA:IMPURITY1'))
    except:
        print('END')
        print(' No impurity in HDA@'+runnum)
        sys.exit()

    imp=np.append(imp,conn.get(runnum+'.METADATA:IMPURITY2'))
    imp=np.append(imp,conn.get(runnum+'.METADATA:IMPURITY3'))

    for i in range(0,3):
        if imp[i] == 'c':
            HDAnam = 'NIZ'+str(i+1)
            ASTRAnam='CAR61X'
            proval=conn.get(signal+HDAnam).data()/1.e19
            print(' Carbon density from HDA@'+runnum+', 10^16/m^3')
            print('GRIDTYPE 20 NAMEXP '+ASTRAnam+' NTIMES ','%.0f'%NT,' POINTS ','%.0f'%NR+' FACTOR 0.001')
            for ii in range(NT): 
                print( '%.3f'%TIME[ii], end = ' ')
            print()
            for j in range(0,NR,step): 
                for jj in range(0,step): 
                    if j+jj < NR :print( '%.3f'%RPOS[j+jj],end=' ')
                print()
            for j in range(0,NR,step): 
                for jj in range(0,step): 
                    if j+jj < NR :print( '%.3f'%ZPOS[j+jj],end=' ')
                print()
            for ii in range(NT):
                for j in range(0,NR,step):
                    for jj in range(0,step): 
                        if j+jj < NR : print('%.3f'%(proval[ii][j+jj]*1000),end=' ')
                    print()

    for i in range(0,3):
        if imp[i] == 'ar':
            HDAnam = 'NIZ'+str(i+1)
            ASTRAnam='CAR62X'
            proval=conn.get(signal+HDAnam).data()/1.e19
            print(' Argon density from HDA@'+runnum+', 10^16/m^3')
            print('GRIDTYPE 20 NAMEXP '+ASTRAnam+' NTIMES ','%.0f'%NT,' POINTS ','%.0f'%NR+' FACTOR 0.001')
            for ii in range(NT): 
                print( '%.3f'%TIME[ii], end = ' ')
            print()
            for j in range(0,NR,step): 
                for jj in range(0,step): 
                    if j+jj < NR :print( '%.3f'%RPOS[j+jj],end=' ')
                print()
            for j in range(0,NR,step): 
                for jj in range(0,step): 
                    if j+jj < NR :print( '%.3f'%ZPOS[j+jj],end=' ')
                print()
            for ii in range(NT):
                for j in range(0,NR,step):
                    for jj in range(0,step): 
                        if j+jj < NR : print('%.3f'%(proval[ii][j+jj]*1000),end=' ')
                    print()

    for i in range(0,3):
        if imp[i] == 'he':
            HDAnam = 'NIZ'+str(i+1)
            ASTRAnam='CAR63X'
            proval=conn.get(signal+HDAnam).data()/1.e19
            print(' Helium density from HDA@'+runnum+', 10^16/m^3')
            print('GRIDTYPE 20 NAMEXP '+ASTRAnam+' NTIMES ','%.0f'%NT,' POINTS ','%.0f'%NR+' FACTOR 0.001')
            for ii in range(NT): 
                print( '%.3f'%TIME[ii], end = ' ')
            print()
            for j in range(0,NR,step): 
                for jj in range(0,step): 
                    if j+jj < NR :print( '%.3f'%RPOS[j+jj],end=' ')
                print()
            for j in range(0,NR,step): 
                for jj in range(0,step): 
                    if j+jj < NR :print( '%.3f'%ZPOS[j+jj],end=' ')
                print()
            for ii in range(NT):
                for j in range(0,NR,step):
                    for jj in range(0,step): 
                        if j+jj < NR : print('%.3f'%(proval[ii][j+jj]*1000),end=' ')
                    print()


import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
#glonam=['NE0','NEV','TE0','TEV','TI0','TIV','WTH','ZEFF']
glonam=['NE0','TE0','TI0','WTH','NNEUTR0','NNEUTRB']
gdenom=[1e19,1000,1000,1000,1e17,1e17]
gdedim=['1e19m-3','keV','keV','kJ','1e17m-3','1e17m-3']
NG=np.shape(glonam)[0]
conn = Connection('192.168.1.7:8000')

def read_BDA_glob(shotnumber,runnum):
    conn.openTree('st40',shotnumber)
    try:
        TIME=conn.get(runnum+':TIME').data()
    except:
        return
    NT=np.shape(TIME)[0]
    signal=runnum+'.GLOBAL:'
    #print(signal,glonam[0])
    for i in range(NG):
        signal+glonam[i]
        gloval=conn.get(signal+glonam[i]).data()/gdenom[i] 
        print(' '+runnum+' '+glonam[i] + ','+ gdedim[i])
        for ii in range(NT): 
            if math.isnan(gloval[ii]) != True :
                print( 'ZRD'+str(40+i),'  %.4f '%TIME[ii],'%.3f'%gloval[ii])
def read_BDA_prof(shotnumber,runnum):
    conn.openTree('st40',shotnumber)
    try:
        TIME=conn.get(runnum+':TIME').data()
    except:
        return
    NT=np.shape(TIME)[0]
    pronam=['NE','NI','TE','TI','ZEFF']
    pdenom=[1e19,1e19,1000,1000,1]
    NP=np.shape(pronam)[0]
    signal=runnum+'.PROFILES.R_MIDPLANE:'
    RPOS=conn.get(signal+'RPOS').data()
    ZPOS=conn.get(signal+'ZPOS').data()
    NR=np.shape(RPOS)[0]
    step=10
    print(' ***********Profiles from '+runnum+'  tree ***************')
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
                            if j+jj < NR :
                                if pronam[i] == 'NI':
                                    if math.isnan( proval[ii][0][j+jj]) == True:
                                        print('0.000',end=' ')
                                    else:
                                        print('%.3f'%proval[ii][0][j+jj],end=' ')
                                else:
                                    if math.isnan( proval[ii][j+jj]) == True:
                                        print('0.000',end=' ')
                                    else:
                                        print('%.3f'%proval[ii][j+jj],end=' ')
                        print()


    imp=np.array([])
    try:
        imp=conn.get(runnum+':ELEMENT')
    except:
        print('END')
        print(' No impurity in '+runnum)
        sys.exit()


    AstraImpnames=['CAR61X','CAR62X','CAR63X','CAR64X']
    nam = 'NI'
    proval=conn.get(signal+nam).data()/1.e19
    for count,name in enumerate(imp[1:]):
        if name == 'c ':impname='Carbon'
        if name == 'ar':impname='Argon'
        if name == 'he':impname='Helium'
        ASTRAnam=AstraImpnames[count]
        print(' '+impname+' density from '+runnum+', 10^16/m^3')
        print('GRIDTYPE 20 NAMEXP '+AstraImpnames[count]+' NTIMES ','%.0f'%NT,' POINTS ','%.0f'%NR+' FACTOR 0.001')
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
                    if j+jj < NR :
                        if math.isnan( proval[ii][count+1][j+jj]) == True:
                            print('0.000',end=' ')
                        else:
                            print('%.3f'%(proval[ii][count+1][j+jj]*1000),end=' ')
                print()



#import matplotlib.pyplot as plt
from MDSplus import *
import math
import sys
import numpy as np
from scipy import interpolate
import readcxprofiles as readcx
from Signals import *
#python3 get_data_shotlist.py


#shotlist=shotshda
efitrun='RUN02'
efitrun='RUN01'
#efitrun='BEST'
SMMH1RUN='_SCALE.BEST'
SMMH1RUN='.BEST'
sigsmm='INTERFEROM.SMMH1'+SMMH1RUN+'.LINE_AV:NE'
#sigsmm='SMMH'+SMMH1RUN+'.GLOBAL:NE_INT'
sigsmm='TS.BEST.GLOBAL:SMM_NEL'
sigRFX='NBI.RFX.RUN1:PINJ'
#sigRFX='RFX.BEST:POWER'
sigHNBI='NBI.HNBI1.RUN1:PINJ'
#sigHNBI='HNBI1.BEST:POWER'


conn = Connection('192.168.1.7:8000')
TOREAD=['WDIA','NEL','TISX','TIerr','TESX','TEerr','BTOR','IPL','RGEO','AMIN','RFX','HNBI','Te0TS','TImaxPI','err','VmaxPI','err','TImaxTWS','err','VmaxTWS']

print('{0:7}'.format('shot'),end=' ')
for n in range(0,len(TOREAD)):    
    print('{0:7}'.format(TOREAD[n]),end=' ')
print()
def get_IPL_pfit(shot):
    conn.openTree('ST40',shot)
    signame0='PFIT.POST_BEST.RESULTS'
    TIME=conn.get(signame0+':TIME').data()
    IPL= conn.get(signame0+'.GLOBAL:IP').data()/1e6
    return 'ok',TIME,IPL
def get_EFIT_global(shot,name,run):
    conn.openTree('ST40',shot)
    signal='EFIT.'+run
    try:
        TIME=conn.get(signal+':TIME')
    except:
        return 'EFIT error',-999,-999
    if name == 'RGEOEF':    sigefit=signal+'.GLOBAL:RGEO'
    if name == 'RMAGEF':    sigefit=signal+'.GLOBAL:RMAG'
    if name == 'AMINEF':    sigefit=signal+'.GLOBAL:CR0'
    if name == 'WDIAEF':    sigefit=signal+'.VIRIAL:WDIA'
    if name == 'LI3MEF':    sigefit=signal+'.VIRIAL:LI3M'
    if name == 'BTPMEF':    sigefit=signal+'.VIRIAL:BTPM'
    if name == 'BTTMEF':    sigefit=signal+'.VIRIAL:BTTM'
    if name == 'SH_EF': 
            RGEO=conn.get(signal+'.GLOBAL:RGEO')
            RMAG=conn.get(signal+'.GLOBAL:RMAG')
            return 'ok',TIME,RMAG-RGEO
    if name == 'IN_EF' :
            RGEO=conn.get(signal+'.GLOBAL:RGEO')
            AMIN=conn.get(signal+'.GLOBAL:CR0')
            return 'ok',TIME,RGEO-AMIN
    if name == 'OUT_EF' :
            RGEO=conn.get(signal+'.GLOBAL:RGEO')
            AMIN=conn.get(signal+'.GLOBAL:CR0')
            return 'ok',TIME,RGEO+AMIN
    if name == 'BTOREF': 
        try:
            RGEO=conn.get(signal+'.GLOBAL:RGEO')
            BTOR=conn.get(signal+'.GLOBAL:BTVAC')
            BTOR=BTOR*0.5/RGEO
            return 'ok',TIME,BTOR
        except:return 'No EFIT name: GLOBAL:',-999,-999
    try:
        VAR=conn.get(sigefit)
    except:
        return 'No EFIT name: GLOBAL:',-999,-999
    return 'ok',TIME,VAR
def get_EFIT_virial(shot,name,run):
    conn.openTree('ST40',shot)
    signal='EFIT.'+run
    try:
        print(signal+':TIME')
        TIME=conn.get(signal+':TIME')
    except:
        return 'EFIT error',-999,-999
    sigefit=signal+'.GLOBAL:'+name
    try:
        VAR=conn.get(signal+'.VIRIAL:'+name)
    except:
        return 'No EFIT name VIRIAL:',name,-999
    return 'ok',TIME,VAR
def get_TWS_data(shot,name):
    conn.openTree('ST40',shot)
    time=np.array([]) 
    timax=np.array([]) 
    vmax=np.array([]) 
    tierr=np.array([]) 
    verr=np.array([]) 
    try:
        t = [0.0, 0.5] 
        sig = Signals(int(shot))
        TIME, r, ti, ti_err = sig.cxrs_tws_c_ti(t)
        _, _, vtor, vtor_err = sig.cxrs_tws_c_vtor(t)        
    except:
        print('TWS error')
        return 'TWS error',-999,-999,-999
    for i in range(0,len(TIME)-1): 
        time=np.append(time,TIME[i])
        timax=np.append(timax,max(ti[i][:]))
        vmax=np.append(vmax,max(vtor[i][:]))
        tierr=np.append(tierr,np.mean(ti_err[i][:]))
        verr=np.append(verr,np.mean(vtor_err[i][:]))
    if name == 'TImaxTWS' : return 'ok',time,timax,tierr
    if name == 'VmaxTWS' :  return 'ok',time,vmax/1e6,verr/1e6
def get_PI_data(shot,name):
    conn.openTree('ST40',shot)
    time=np.array([]) 
    timax=np.array([]) 
    vmax=np.array([]) 
    tierr=np.array([]) 
    verr=np.array([]) 
    try:
        t = [0.0, 0.5] 
        sig = Signals(int(shot))
        TIME, r, ti, ti_err = sig.cxrs_pi_ti(t)
        _, _, vtor, vtor_err = sig.cxrs_pi_vtor(t)        
    except:
        print('PI error')
        return 'PI error',-999,-999,-999
    for i in range(0,len(TIME)-1): 
        time=np.append(time,TIME[i])
        timax=np.append(timax,max(ti[i][:]))
        vmax=np.append(vmax,max(vtor[i][:]))
        tierr=np.append(tierr,np.mean(ti_err[i][:]))
        verr=np.append(verr,np.mean(vtor_err[i][:]))
    if name == 'TImaxPI' : return 'ok',time,timax,tierr
    if name == 'VmaxPI' :  return 'ok',time,vmax/1e6,verr/1e6
def get_TS_1Ddata(shot,name):
    conn.openTree('PPTS',shot)
    runnum='BEST'
    signame=runnum
    TIME=conn.get(signame+':TIME')
    if name == 'RMAGTS':        sigTS=signame+'.GLOBAL:RMAG_TE'
    if name == 'IN_TS':        sigTS=signame+'.GLOBAL:RSEP_HFS'
    if name == 'OUT_TS':        sigTS=signame+'.GLOBAL:RSEP_LFS'
    if name == 'Te0TS':         sigTS=signame+'.GLOBAL:TE_RMAG'
    if name == 'Ne0TS':       sigTS=signame+'.GLOBAL:NE_RMAG'
    if name == 'SH_TS':       
        RMAG=conn.get(signame+'.GLOBAL:RMAG_TE')
        RIN=conn.get(signame+'.GLOBAL:RSEP_HFS')
        ROUT=conn.get(signame+'.GLOBAL:RSEP_LFS')
        TS=RMAG-(RIN+ROUT)/2
        return 'ok',TIME,TS
    try:
        TS=conn.get(sigTS)
    except:
        return 'TS error sigTS',-999,-999
    if name == 'Te0TS': TS=TS/1000
    if name == 'NETS': TS=TS/1e19
    return 'ok',TIME,TS
def get_smm_data(shot):
    conn.openTree('ST40',shot)
    try:
        sigsmm='SMMH'+SMMH1RUN+'.GLOBAL:NE_INT'
        print(sigsmm)
        TIME=conn.get('dim_of('+sigsmm+')').data()
        SMM=conn.get(sigsmm).data()/1e19
    except:
        return 'smm error',-999,-999
    return 'ok',TIME,SMM
def get_XRCS_data(shot,name):
    conn.openTree('ST40',shot)
    try:
        TIME=conn.get('SXR.XRCS.BEST:TIME').data()
    except:
        return 'XRCS error',-999,-999,-999
    VAR=conn.get('SXR.XRCS.BEST.TI_W:TI').data()/1000
    ERR=conn.get('SXR.XRCS.BEST.TI_W:TI_ERR').data()/1000
    ind=np.where(np.isnan(VAR)!= True) 
    TI=VAR[ind]
    TIerr=ERR[ind]
    TIMEti=TIME[ind]
    TIME=conn.get('SXR.XRCS.BEST:TIME').data()
    VAR=conn.get('SXR.XRCS.BEST.TE_KW:TE').data()/1000
    ERR=conn.get('SXR.XRCS.BEST.TE_KW:TE_ERR').data()/1000
    ind=np.where(np.isnan(VAR)!= True) 
    TE=VAR[ind]
    TEerr=ERR[ind]
    TIMEte=TIME[ind]
    if name == 'TISX' : return 'ok',TIMEti,TI,TIerr
    if name == 'TESX' : return 'ok',TIMEte,TE,TEerr
def get_NBI_data(shot,name): 
    conn.openTree('ST40',shot)
    sigRFX='NBI.RFX.RUN1:PINJ'
    sigHNBI='NBI.HNBI1.RUN1:PINJ'
    if int(shot) > 10900: 
        sigRFX='RFX.BEST:POWER'
        sigHNBI='HNBI1.BEST:POWER'
    try:
        RFX=conn.get(sigRFX).data()
        TIMERFX=conn.get('dim_of('+sigRFX+')').data()
    except:
        return 'NO RFX data',-999,-999,-999,-999
    try:
        HNBI=conn.get(sigHNBI).data()
        TIMEHNBI=conn.get('dim_of('+sigHNBI+')').data()
    except:
        return 'NO HNBI data',-999,-999,-999,-999
    if name == 'RFX' : return 'ok',TIMERFX,RFX/1e6,-999,-999
    if name == 'HNBI' : return 'ok',TIMEHNBI,HNBI/1e6,-999,-999
    if name == 'PNB' : return 'ok',TIMERFX,RFX/1e6,TIMEHNBI,HNBI/1e6

 
def get_data(shot1,time1,time2,efitrun):
#    time1=0.06
#    time2=0.09
    j=shot1
    conn.openTree('st40',int(j))
    sigefit='EFIT.'+efitrun
    #if shot1==11227 or shot1==11229:sigefit='EFIT.RUN01'
    sigvirial=sigefit+'.VIRIAL'
    try:
        TIMEefit=conn.get(sigefit+':TIME')
    except:
        return 'EFIT error',-999
    WDIA=conn.get(sigefit+'.VIRIAL:WP')/1e6
    TIMEwdia=TIMEefit
#    WDIA=conn.get('DIALOOP.BEST.GLOBAL:WDIA')
#    TIMEwdia=conn.get('dim_of(DIALOOP.BEST.GLOBAL:WDIA)').data()
    RGEO=conn.get(sigefit+'.GLOBAL:RGEO')
    BTOR=conn.get(sigefit+'.GLOBAL:BTVAC')*0.5/RGEO
    AMIN= conn.get(sigefit+'.GLOBAL:CR0') 
    ELON= conn.get(sigefit+'.GLOBAL:ELON') 
    QEDG=conn.get(sigefit+'.GLOBAL:Q95') 
    BETP= conn.get(sigefit+'.VIRIAL:BTPM') 
    IPL= conn.get(sigefit+'.CONSTRAINTS.IP:MVALUE')
    #if j > 10900:sigsmm='SMMH'+SMMH1RUN+'.GLOBAL:NE_INT'
    try:
        TIMEsmm=conn.get('dim_of('+sigsmm+')').data()
        SMM=conn.get(sigsmm).data()
        SMMerror=0
    except:
        TIMEsmm=0
        SMMerror=1
    TIME1=conn.get('SXR.XRCS.BEST:TIME').data()
    VAR1=conn.get('SXR.XRCS.BEST.TI_W:TI').data()/1000
    ERR1=conn.get('SXR.XRCS.BEST.TI_W:TI_ERR').data()/1000
    ind=np.where(np.isnan(VAR1)!= True) 
    TIexp=VAR1[ind]
    TIerr=ERR1[ind]
    TIMEti=TIME1[ind]
    TIME1=conn.get('SXR.XRCS.BEST:TIME').data()
    VAR1=conn.get('SXR.XRCS.BEST.TE_KW:TE').data()/1000
    ERR1=conn.get('SXR.XRCS.BEST.TE_KW:TE_ERR').data()/1000
    ind=np.where(np.isnan(VAR1)!= True) 
    TEexp=VAR1[ind]
    TEerr=ERR1[ind]
    TIMEte=TIME1[ind]
    if j > 10900:sigRFX='RFX.BEST:POWER'
    try:
        RFX=conn.get(sigRFX).data()
        TIMERFX=conn.get('dim_of('+sigRFX+')').data()
        RFXerror=0
    except:
        TIMERFX=0
        RFXerror=1
    if j > 10900:sigHNBI='HNBI1.BEST:POWER'
    HNBI=conn.get(sigHNBI).data()
    TIMEHNBI=conn.get('dim_of('+sigHNBI+')').data()
    try:
        T,MAX=readcx.cxmax(int(j),'BEST')
        T,ERR=readcx.cxerr(int(j),'BEST')
        errPI=0
    except:
#        print(str(j)+' no CX profiles')
        print('PIcx error')
        errPI=1
    try:
        t = [0.0, 0.5] 
        sig = Signals(int(j))
        TIMEtws, r, ti, ti_err = sig.cxrs_tws_c_ti(t)
        _, _, vtor, vtor_err = sig.cxrs_tws_c_vtor(t)        
        errTWS=0
    except:
#        print(str(j)+' no CX profiles')
        print('TWS error')
        errTWS=1
    try:
        TETS=conn.get(sigTS).data()
    except:
        return 'TS error',-999
    TIMETS=conn.get('dim_of('+sigTS+')').data()
    conn.closeTree('st40',int(j))
    Y=np.array([])
    n1=np.array([])
    n2=np.array([])
    timax=np.array([])
    vmax=np.array([])
    for jj in range(0,11):
        if jj==0:TIME=TIMEefit
        if jj==1:TIME=TIMEsmm
        if jj==2:TIME=TIMEti
        if jj==3:TIME=TIMEte
        if jj==4:TIME=TIMERFX
        if jj==5:TIME=TIMEHNBI
        if jj==6 and errPI == 0:TIME=T[0,:]
        if jj==7 and errPI == 0:TIME=T[1,:]
        if jj==8 and errTWS == 0: TIME=TIMEtws
        if jj==9:TIME=TIMETS
        if jj==10:TIME=TIMEwdia
        ind=np.where((TIME-time1)*(TIME-time2) <= 0)
        try:
            e1=np.array(ind).astype(int)[0,0] 
            e2=np.array(ind).astype(int)[0,len(ind[0])-1]
        except:
            e1=0
            e2=0
        n1=np.append(n1,e1).astype(int)
        n2=np.append(n2,e2).astype(int)
#Conditions:
    jj=2
    #if np.mean(TIexp[n1[jj]:n2[jj]+1]) < 6: return 'TIexp < 6',-999
    if SMMerror==1 or n2[0]==0:
         NEL=-9e19
    else: NEL=np.mean(SMM[n1[1]:n2[1]+1])/np.mean(AMIN[n1[0]:n2[0]+1])/4
    #if NEL < 3.5e19: return 'NEL < 3.5e19',-999
    jj=10
    if n2[jj]==0:
        WD=-999
    else:WD=np.mean(WDIA[n1[jj]:n2[jj]+1])/1000
    Y=np.append(Y,WD)
    jj=1
    Y=np.append(Y,NEL/1e19)
    jj=2
    TI=np.mean(TIexp[n1[jj]:n2[jj]+1])
    TIe=np.mean(TIerr[n1[jj]:n2[jj]+1])
    Y=np.append(Y,TI)
    Y=np.append(Y,TIe)
    jj=3
    TE=np.mean(TEexp[n1[jj]:n2[jj]+1])
    TEe=np.mean(TEerr[n1[jj]:n2[jj]+1])
    Y=np.append(Y,TE)
    Y=np.append(Y,TEe)
    jj=0
    if n2[jj]==0:
        for i in range(0,4):Y=np.append(Y,-999)
    else:
        Y=np.append(Y,np.mean(BTOR[n1[jj]:n2[jj]+1]))
        Y=np.append(Y,np.mean(IPL[n1[jj]:n2[jj]+1])/1e6)
        Y=np.append(Y,np.mean(RGEO[n1[jj]:n2[jj]+1]))
        Y=np.append(Y,np.mean(AMIN[n1[jj]:n2[jj]+1]))
    jj=4
    PNB=0
    if n2[jj] == 0:
        Y=np.append(Y,0)
    else:
        if RFXerror==0:
            Y=np.append(Y,np.mean(RFX[n1[jj]:n2[jj]+1])/1e6)
            PNB=np.mean(RFX[n1[jj]:n2[jj]+1])/1e6
        else:
            Y=np.append(Y,0)
    jj=5
    if n2[jj] == 0:
        Y=np.append(Y,0)
    else:
        Y=np.append(Y,np.mean(HNBI[n1[jj]:n2[jj]+1])/1e6)
    PNB=PNB+np.mean(HNBI[n1[jj]:n2[jj]+1])/1e6
    #if PNB < 1.5 : return 'PNB < 1.5',-999
    Y=np.append(Y,PNB)
    jj=9
    TE=np.mean(TETS[n1[jj]:n2[jj]+1])/1e3
    Y=np.append(Y,TE)
    jj=6
    if n2[jj] == 0 or errPI == 1:
        Y=np.append(Y,0)
        Y=np.append(Y,0)
    else:
        Y=np.append(Y,np.mean(MAX[0,n1[jj]:n2[jj]+1]))
        Y=np.append(Y,np.mean(ERR[0,n1[jj]:n2[jj]+1]))
    jj=7
    if n2[jj] == 0 or errPI == 1:
        Y=np.append(Y,0)
        Y=np.append(Y,0)
    else:
        Y=np.append(Y,np.mean(MAX[1,n1[jj]:n2[jj]+1]))
        Y=np.append(Y,np.mean(ERR[1,n1[jj]:n2[jj]+1]))
    jj=8
    tierr=np.array([]) 
    if n2[jj] == 0 or errTWS == 1:
        Y=np.append(Y,0)
        Y=np.append(Y,0)
        Y=np.append(Y,0)
    else:
        for i in range(0,len(TIMEtws)-1): 
            timax=np.append(timax,max(ti[i][:]))
            vmax=np.append(vmax,max(vtor[i][:]))
            tierr=np.append(tierr,np.mean(ti_err[i][:]))
#        TIMAX=np.mean(timax[n1[jj]:n2[jj]+1])
        TIMAX=max(timax[n1[jj]:n2[jj]+1])
        TIerr=max(tierr[n1[jj]:n2[jj]+1])
        Y=np.append(Y,TIMAX)
        Y=np.append(Y,TIerr)
        Y=np.append(Y,np.mean(vmax[n1[jj]:n2[jj]+1])/1e3)
        Y=np.append(Y,TIMAX-TE)

#    print('{:5}'.format(int(j)),end=' ')
#    for n in range(0,len(TOREAD)):    
#        print('{:7.2f}'.format(Y[n]),end=' ')
#    print()
    return 'ok',Y,TOREAD
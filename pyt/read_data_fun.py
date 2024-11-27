import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
glonam=['NE0','NEV','TE0','TEV','TI0','TIV','WTH','ZEFF']
gdenom=[1e19,1e19,1000,1000,1000,1000,1000,1]
NG=np.shape(glonam)[0]
conn = Connection('192.168.1.7:8000')

def open_conn(shotnumber):
    conn.openTree('st40',shotnumber)

def read_psu(timea):
    na=len(timea)
    SOLV=conn.get('PSU.SOL:V').data()
    DIVV=conn.get('PSU.DIV:V').data()
    BVLV=conn.get('PSU.BVL:V').data()
    BVUBV=conn.get('PSU.BVUB:V').data()
    BVUTV=conn.get('PSU.BVUT:V').data()
    MCV=conn.get('PSU.MC:V').data()
    PSHV=conn.get('PSU.PSH:V').data()
    SOLBEST=conn.get('PSU.SOL:I').data()
    DIVBEST=conn.get('PSU.DIV:I').data()
    BVLBEST=conn.get('PSU.BVL:I').data()
    BVUBBEST=conn.get('PSU.BVUB:I').data()
    BVUTBEST=conn.get('PSU.BVUT:I').data()
    BVUBEST=0.5*(BVUTBEST+BVUBBEST)
    MCBEST=conn.get('PSU.MC:I').data()
    PSHBEST=conn.get('PSU.PSH:I').data()
    TIME=conn.get('dim_of(PSU.SOL:I)').data()
    diva=np.array([])
    bvla=np.array([])
    bvuta=np.array([])
    bvuba=np.array([])
    mca=np.array([])
    psha=np.array([])
    sola=np.array([])
    divva=np.array([])
    bvlva=np.array([])
    bvutva=np.array([])
    bvubva=np.array([])
    mcva=np.array([])
    pshva=np.array([])
    solva=np.array([])    
    for i in range(0,na):   
        iupa=np.where(TIME > timea[i])
        iup=iupa[0][0]
        idwa=np.where(TIME <= timea[i])
        idw=idwa[0][len(idwa[0])-1]
        dt0=TIME[iup]-TIME[idw]
        diva=np.append(diva,DIVBEST[idw]+(DIVBEST[iup]-DIVBEST[idw])/dt0*(timea[i]-TIME[idw])) 
        bvla=np.append(bvla,BVLBEST[idw]+(BVLBEST[iup]-BVLBEST[idw])/dt0*(timea[i]-TIME[idw])) 
        bvuta=np.append(bvuta,BVUTBEST[idw]+(BVUTBEST[iup]-BVUTBEST[idw])/dt0*(timea[i]-TIME[idw]))
        bvuba=np.append(bvuba,BVUBBEST[idw]+(BVUBBEST[iup]-BVUBBEST[idw])/dt0*(timea[i]-TIME[idw]))
        bvua=np.append(bvuba,BVUBEST[idw]+(BVUBEST[iup]-BVUBEST[idw])/dt0*(timea[i]-TIME[idw]))
        mca= np.append(mca,MCBEST[idw]+(MCBEST[iup]- MCBEST[idw])/dt0*(timea[i]-TIME[idw])) 
        psha=np.append(psha,PSHBEST[idw]+(PSHBEST[iup]-PSHBEST[idw])/dt0*(timea[i]-TIME[idw])) 
        sola=np.append(sola,SOLBEST[idw]+(SOLBEST[iup]-SOLBEST[idw])/dt0*(timea[i]-TIME[idw])) 
        divva=np.append(divva,DIVV[idw]+(DIVV[iup]-DIVV[idw])/dt0*(timea[i]-TIME[idw])) 
        bvlva=np.append(bvlva,BVLV[idw]+(BVLV[iup]-BVLV[idw])/dt0*(timea[i]-TIME[idw])) 
        bvutva=np.append(bvutva,BVUTV[idw]+(BVUTV[iup]-BVUTV[idw])/dt0*(timea[i]-TIME[idw])) 
        bvubva=np.append(bvubva,BVUBV[idw]+(BVUBV[iup]-BVUBV[idw])/dt0*(timea[i]-TIME[idw])) 
        pshva=np.append(pshva,PSHV[idw]+(PSHV[iup]-PSHV[idw])/dt0*(timea[i]-TIME[idw])) 
        solva=np.append(solva,SOLV[idw]+(SOLV[iup]-SOLV[idw])/dt0*(timea[i]-TIME[idw])) 
        mcva=np.append(mcva,MCV[idw]+(MCV[iup]-MCV[idw])/dt0*(timea[i]-TIME[idw]))
    return diva,bvla,bvuta,bvuba,mca,psha,sola,divva,bvlva,bvutva,bvubva,mcva,pshva,solva
def read_tfa(timea):
    na=len(timea)
    try:
        TIME=conn.get('dim_of(PSU.TF:I)').data()
        TFBEST=conn.get('PSU.TF:I').data()
    except:
        return np.array([0])
    tfa=np.array([])
    for i in range(0,na):   
        iupa=np.where(TIME > timea[i])
        iup=iupa[0][0]
        idwa=np.where(TIME <= timea[i])
        idw=idwa[0][len(idwa[0])-1]
        dt0=TIME[iup]-TIME[idw]
        tfa=np.append(tfa,TFBEST[idw]+(TFBEST[iup]-TFBEST[idw])/dt0*(timea[i]-TIME[idw]))
    return tfa

def read_comment():
    try:
        COMMENTpre=conn.get('SUMMARY.PRE_COMMENT').data()
        COMMENTpost=conn.get('SUMMARY.POST_COMMENT').data()
    except:
        COMMENTpre='no comment'
        COMMENTpost='no comment'
    return COMMENTpre,COMMENTpost

def read_mag(BEST,timea):
    na=len(timea)
    try:
        UPL=conn.get('MAG.'+BEST+'FLOOP.L016:V').data()
        TIME=conn.get('dim_of(MAG.'+BEST+'FLOOP.L016:V)').data()
    except:
        return np.array([0])
    upla=np.array([])
    for i in range(0,na):   
        iupa=np.where(TIME > timea[i])
        iup=iupa[0][0]
        idwa=np.where(TIME <= timea[i])
        idw=idwa[0][len(idwa[0])-1]
        dt0=TIME[iup]-TIME[idw]
        upla=np.append(upla,UPL[idw]+(UPL[iup]-UPL[idw])/dt0*(timea[i]-TIME[idw]))
    return upla
def read_efit(efitnumber,timea):
    na=len(timea)
    signame0='EFIT.'+str(efitnumber)
    TIME=conn.get(signame0+':TIME')
    ne=np.size(TIME)-1
    signame=signame0+'.CONSTRAINTS'
    IPL=conn.get(signame+'.IP:MVALUE')
    BPefit=-conn.get(signame+'.BP:CVALUE')
    ROG= conn.get(signame+'.ROGC:MVALUE')
    signame=signame0+'.GLOBAL'
    RTOR=conn.get(signame+':RGEO')
    RMAG=conn.get(signame+':RMAG')
    ZGEO = conn.get(signame+':ZGEO') 
    TRIL= conn.get(signame+':TRIL') 
    TRIU= conn.get(signame+':TRIU') 
    TRIA=(TRIL+TRIU)/2
    AMIN= conn.get(signame+':CR0') 
    ELON= conn.get(signame+':ELON') 
    QEDG=conn.get(signame+':Q95') 
    BTOR=conn.get(signame+':BTVAC')
    signame=signame0+'.VIRIAL'
    WMHD=conn.get(signame+':WP') 
    LI3M=conn.get(signame+':LI3M') 
    BETP= conn.get(signame+':BTPM') 
    BETT=conn.get(signame+':BTTM') 
 
    ipla=np.array([])
    triaa=np.array([])
    wmhda=np.array([])
    betpa=np.array([])
    betta=np.array([])
    qedgea=np.array([])
    lia=np.array([])
    rtora=np.array([])
    amina=np.array([])
    elona=np.array([])       
    zgeoa=np.array([])
    r=0;z=0
    for i in range(0,na):   
        iupa=np.where(TIME > timea[i])
        idwa=np.where(TIME <= timea[i])
        if np.size(iupa) == 0: 
            idw=idwa[0][len(idwa[0])-1]    
            iup=idw
        elif np.size(idwa) == 0:
            iup=iupa[0][0]
            idw=iup
        else:
            idw=idwa[0][len(idwa[0])-1]    
            iup=iupa[0][0]
        dt0=TIME[iup]-TIME[idw]
        if dt0 == 0: dt0=1
        ipla=np.append(ipla,IPL[idw]+(IPL[iup]-IPL[idw])/dt0*(timea[i]-TIME[idw]))
        triaa=np.append(triaa,TRIA[idw]+(TRIA[iup]-TRIA[idw])/dt0*(timea[i]-TIME[idw]))
        wmhda=np.append(wmhda,WMHD[idw]+(WMHD[iup]-WMHD[idw])/dt0*(timea[i]-TIME[idw]))
        betpa=np.append(betpa,BETP[idw]+(BETP[iup]-BETP[idw])/dt0*(timea[i]-TIME[idw]))
        betta=np.append(betta,BETT[idw]+(BETT[iup]-BETT[idw])/dt0*(timea[i]-TIME[idw]))
        qedgea=np.append(qedgea,QEDG[idw]+(QEDG[iup]-QEDG[idw])/dt0*(timea[i]-TIME[idw]))
        lia=np.append(lia,LI3M[idw]+(LI3M[iup]-LI3M[idw])/dt0*(timea[i]-TIME[idw]))
        rtora=np.append(rtora,RTOR[idw]+(RTOR[iup]-RTOR[idw])/dt0*(timea[i]-TIME[idw]))
        amina=np.append(amina,AMIN[idw]+(AMIN[iup]-AMIN[idw])/dt0*(timea[i]-TIME[idw]))
        elona=np.append(elona,ELON[idw]+(ELON[iup]-ELON[idw])/dt0*(timea[i]-TIME[idw]))
        zgeoa=np.append(zgeoa,ZGEO[idw]+(ZGEO[iup]-ZGEO[idw])/dt0*(timea[i]-TIME[idw]))
    return ipla,triaa,wmhda,betpa,betta,qedgea,lia,rtora,amina,elona,zgeoa,TIME,RMAG
def read_efitBND(efitnumber,ntheta,timea):
    from scipy import interpolate
    na=len(timea)
    EFITtree='EFIT.'
    signame0=EFITtree+str(efitnumber)
    signame=signame0+'.P_BOUNDARY'
    TIME=conn.get(signame0+':TIME')
    RBND= conn.get(signame+':RBND')
    ZBND= conn.get(signame+':ZBND') 
    for i in range(0,na):   
        iupa=np.where(TIME > timea[i])
        idwa=np.where(TIME <= timea[i])
        if np.size(iupa) == 0: 
            idw=idwa[0][len(idwa[0])-1]    
            iup=idw
        elif np.size(idwa) == 0:
            iup=iupa[0][0]
            idw=iup
        else:
            idw=idwa[0][len(idwa[0])-1]    
            iup=iupa[0][0]
        dt0=TIME[iup]-TIME[idw]
        if dt0 == 0: dt0=1
        for i2 in [idw,iup]:
            rba=RBND[i2,:]
            zba=ZBND[i2,:]
            NR=np.where(zba == 0)[0][2]
            arc=np.array([])
            for j in range(0,NR+1):
                if j==0:arc=np.append(arc,0)
                if j>0:arc=np.append(arc,arc[j-1]+np.sqrt((rba[j]-rba[j-1])**2+(zba[j]-zba[j-1])**2))
            fR=interpolate.InterpolatedUnivariateSpline(arc,rba[0:NR+1],k=3)
            fZ=interpolate.InterpolatedUnivariateSpline(arc,zba[0:NR+1],k=3)
            dl=arc[len(arc)-1]/(ntheta-1)
            length=np.array([])
            for j in range(0,ntheta):
                if j==0:
                    length=np.append(length,0)
                else:
                    length=np.append(length,length[j-1]+dl)

            if i2==idw:
                rdw=fR(length)
                zdw=fZ(length)
            if i2==iup:
                rup=fR(length)
                zup=fZ(length)

        rb=rdw+(rup-rdw)/dt0*(timea[i]-TIME[idw])
        zb=zdw+(zup-zdw)/dt0*(timea[i]-TIME[idw])
        rbnd=np.array([])
        zbnd=np.array([])
        for j in range(0,ntheta):
            rbnd=np.append(rbnd,rb[j])
            zbnd=np.append(zbnd,zb[j])
        if i==0:
            r=rbnd
            z=zbnd
        elif i==1:        
            r=np.append([r],[rbnd])
            z=np.append([z],[zbnd])
        else:        
            r=np.append(r,[rbnd])
            z=np.append(z,[zbnd])
    return r,z
def read_pfit(timea):
    na=len(timea)
    time1=min(timea)
    time2=max(timea)
    signame0='PFIT.POST_BEST.RESULTS'
    signame=signame0+'.GLOBAL'
    TIMEpfit=conn.get(signame0+':TIME').data()
    signame=signame0+'.GLOBAL:'
    RTORpfit= conn.get(signame+'RGEO').data()
    ind=np.array([])
    for i in range(0,len(RTORpfit)):
        if math.isnan(RTORpfit[i]) != True : ind=np.append(ind,i)
    i1=ind.astype(int)
    TIME=TIMEpfit[i1]
    RTOR=RTORpfit[i1]
    time2pfit=max(TIME)
    time0=TIME[(TIME>time1) & (TIME<time2)]
    n0=len(time0)
    IPLpfit= conn.get(signame+'IP').data()
    AMINpfit= conn.get(signame+'AMINOR').data()
    ELONGpfit= conn.get(signame+'KAPPA').data()
    ZGEOpfit= conn.get(signame+'ZGEO').data()
    IPL=IPLpfit[i1]
    AMIN=AMINpfit[i1]
    ELONG=ELONGpfit[i1]
    ZGEO=ZGEOpfit[i1]
    ipla=np.array([])
    rtora=np.array([])
    amina=np.array([])
    elona=np.array([])
    zgeoa=np.array([])
    timepfit=np.array([])
    if len(IPL) == 1:
        IPL=IPL[0] 
        RTOR= RTOR[0]
        AMIN=AMIN[0]
        ELONG= ELONG[0]
        ZGEO= ZGEO[0]
    for i in range(0,na):
        if timea[i] >= time2pfit and timea[i] < min(TIME): break
        try:
            iupa=np.where(TIME > timea[i])
            iup=iupa[0][0]
            idwa=np.where(TIME <= timea[i])
            idw=idwa[0][len(idwa[0])-1]
            dt0=TIME[iup]-TIME[idw]      
            ipla=np.append(ipla,IPL[idw]+(IPL[iup]-IPL[idw])/dt0*(timea[i]-TIME[idw]))
            rtora=np.append(rtora,RTOR[idw]+(RTOR[iup]-RTOR[idw])/dt0*(timea[i]-TIME[idw]))
            amina=np.append(amina,AMIN[idw]+(AMIN[iup]-AMIN[idw])/dt0*(timea[i]-TIME[idw]))
            elona=np.append(elona,ELONG[idw]+(ELONG[iup]-ELONG[idw])/dt0*(timea[i]-TIME[idw]))
            zgeoa=np.append(zgeoa,ZGEO[idw]+(ZGEO[iup]-ZGEO[idw])/dt0*(timea[i]-TIME[idw]))
            timepfit=np.append(timepfit,timea[i])
        except:
            continue 
    return ipla,rtora,amina,elona,zgeoa,timepfit
def read_NBI(ifNBI,timea):
    na=len(timea)
    rfxa=np.array([])
    hnbia=np.array([])
    if ifNBI > 0:
        if ifNBI == 1: signame='NBI.RFX.RUN1:PINJ'
        if ifNBI == 2: signame='RFX.BEST:POWER'
        try:
            SIG=conn.get(signame).data()
            RFXYES=0==0
        except:
            RFXYES=0==1         
        if RFXYES:
            TIME=conn.get('dim_of('+signame+')').data()
            for i in range(0,na):
                iupa=np.where(TIME > timea[i])
                idwa=np.where(TIME <= timea[i])
                if np.size(iupa) == 0: 
                    idw=idwa[0][len(idwa[0])-1]    
                    iup=idw
                elif np.size(idwa) == 0:
                    iup=iupa[0][0]
                    idw=iup
                else:
                    idw=idwa[0][len(idwa[0])-1]    
                    iup=iupa[0][0]
                dt0=TIME[iup]-TIME[idw]
                if dt0 == 0: dt0=1
                rfxa=np.append(rfxa,SIG[idw]+(SIG[iup]-SIG[idw])/dt0*(timea[i]-TIME[idw]))
        if ifNBI == 1: signame='NBI.HNBI1.RUN1:PINJ'
        if ifNBI == 2: signame='HNBI1.BEST:POWER'
        try:
            SIG=conn.get(signame).data()
            HNBIYES=0==0
        except:
            HNBIYES=0==1
        if HNBIYES:
            TIME=conn.get('dim_of('+signame+')').data()
            for i in range(0,na):
                try:
                    iupa=np.where(TIME > timea[i])
                    iup=iupa[0][0]
                    idwa=np.where(TIME <= timea[i])
                    idw=idwa[0][len(idwa[0])-1]
                    dt0=TIME[iup]-TIME[idw]
                    hnbia=np.append(hnbia,SIG[idw]+(SIG[iup]-SIG[idw])/dt0*(timea[i]-TIME[idw]))
                except:
                    hnbia=np.append(hnbia,0)
        if ifNBI == 2:rfxa=rfxa/1e6
        if ifNBI == 2:hnbia=hnbia/1e6
    if ifNBI == -1:
        signame='RAW_NBI.RFX.HV_DAQ.ACCEL:CURRENT'
        try:
            SIG=conn.get(signame).data()
            RFXYES=0==0
        except:
            RFXYES=0==1
        if not np.isnan(SIG).any() and  RFXYES:
            TIME=conn.get('dim_of('+signame+')').data()
            for i in range(0,na):
                try:
                    iupa=np.where(TIME > timea[i]+dt/2)
                    iup=iupa[0][0]
                    idwa=np.where(TIME < timea[i]-dt/2)
                    idw=idwa[0][len(idwa[0])-1]
                    dt0=TIME[iup]-TIME[idw]
                    SIG1=SIG[idw]+(SIG[iup]-SIG[idw])/dt0*(timea[i]-TIME[idw])
                    if SIG1 > 0:
                        rfxa=np.append(rfxa,1)
                    else:
                        rfxa=np.append(rfxa,0)
                except:
                    rfxa=np.append(rfxa,0)

        signame='RAW_NBI.HNBI1.HV_PS:I'
        try:
            SIG=conn.get(signame).data()
            HNBIYES=0==0
        except:
            HNBIYES=0==1
        if not np.isnan(SIG).any() and HNBIYES:
            TIME=conn.get('dim_of('+signame+')').data()
            for i in range(0,na):
                try:
                    iupa=np.where(TIME > timea[i]+dt/2)
                    iup=iupa[0][0]
                    idwa=np.where(TIME < timea[i]-dt/2)
                    idw=idwa[0][len(idwa[0])-1]
                    dt0=TIME[iup]-TIME[idw]
                    SIG1=SIG[idw]+(SIG[iup]-SIG[idw])/dt0*(timea[i]-TIME[idw])
                    if SIG1 > 0:
                        hnbia=np.append(hnbia,1)
                    else:
                        hnbia=np.append(hnbia,0)
                except:
                    hnbia=np.append(hnbia,0)
    return RFXYES,rfxa,HNBIYES,hnbia
def read_Ar(timea):
    na=len(timea)
    signame0='SXR.XRCS.BEST'
    TIME=conn.get(signame0+':TIME').data()
    INTW=conn.get(signame0+'.TE_KW:INT_W').data()
    iupa=np.where(TIME <= timea[na-1])
    idwa=np.where(TIME >= timea[0])
    iup=iupa[0][len(iupa[0])-1]
    idw=idwa[0][0]
    TIMEAR=TIME[idw:iup]
    IAR=INTW[idw:iup]
    return TIMEAR,IAR
def read_NIR(timea):
    na=len(timea)
    signal='INTERFEROM.NIRH1.BEST'
    try:
        DENNIR=conn.get(signal+'.LINE_AV:NE').data()
        NIRYES=0==0
        if math.isnan(DENNIR)==True:
            NIRYES=0==1
            return NIRYES,1
    except:
        NIRYES=0==1
        return NIRYES,1
    if NIRYES:
        #TIME=conn.get('INTERFEROM.NIRH1.BEST:TIME').data()
        TIME=conn.get('dim_of('+signal+'.LINE_AV:NE)').data()
        dennir=np.array([])
        DEN=DENNIR
        print( NIRYES,TIME,DEN)
        for i in range(0,na):   
            iupa=np.where(TIME > timea[i])
            iup=iupa[0][0]
            idwa=np.where(TIME <= timea[i])
            idw=idwa[0][len(idwa[0])-1]
            dt0=TIME[iup]-TIME[idw]
            dennir=np.append(dennir,DEN[idw]+(DEN[iup]-DEN[idw])/dt0*(timea[i]-TIME[idw]))
    return NIRYES,dennir
def read_SMM(timea):
    na=len(timea)
    signal='SMMH.BEST.GLOBAL'
    #signal='INTERFEROM.SMMH1_SCALE.'+SMMH1RUN+'.LINE_INT'
    #signal='INTERFEROM.SMMH1_SCALE.'+SMMH1RUN+'.LINE_INT'
    try:
        DENSMM=conn.get(signal+':NE_INT').data()
        SMMYES=0==0
    except:
        SMMYES=0==1
    if SMMYES:
        TIME=conn.get('dim_of('+signal+':NE_INT)').data()
#        TIME=conn.get(signal+':TIME').data()
        DEN=DENSMM
        dneg=np.where(DENSMM <= 0)
        dpos=np.where(DENSMM > 0)
        DEN[dneg]=min(DENSMM[dpos])
        densmm=np.array([])
        for i in range(0,na):   
            iupa=np.where(TIME > timea[i])
            iup=iupa[0][0]
            idwa=np.where(TIME <= timea[i])
            idw=idwa[0][len(idwa[0])-1]
            dt0=TIME[iup]-TIME[idw]
            densmm=np.append(densmm,DEN[idw]+(DEN[iup]-DEN[idw])/dt0*(timea[i]-TIME[idw])) 
    return SMMYES,densmm
def read_XRCS(shot0,timea):
    try:
        shot=conn.get('SUMMARY:PULSE')
    except:
        print('The ST40 tree is not opened')
        return -999,0,0
    na=len(timea)
    signame0='SXR.XRCS.BEST'
    if shot > shot0:signame0='XRCS.BEST'
    try:
        TIME=conn.get(signame0+':TIME').data()
        if np.isscalar(TIME) and math.isnan(TIME) == True : return -999,0,0
    except:
        return -999,0,0
    if not np.isscalar(TIME):
        signame=signame0+'.TI_W:TI0'
        if shot > shot0: signame=signame0+'.GLOBAL:TI_W'
        TIW=conn.get(signame).data()
        signame=signame0+'.TE_KW:TE0'
        if shot > shot0: signame=signame0+'.GLOBAL:TE_KW'
        TEKW=conn.get(signame).data()
        iupa=np.where(TIME <= timea[na-1])
        idwa=np.where(TIME >= timea[0])
        iup=iupa[0][len(iupa[0])-1]
        idw=idwa[0][0]
        TIMET=TIME[idw:iup]
        TE=TEKW[idw:iup]
        TI=TIW[idw:iup]
    else: return -999,0,0
    return TIMET,TI,TE

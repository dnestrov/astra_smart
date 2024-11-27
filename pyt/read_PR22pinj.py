import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
from scipy import interpolate

#python3 read_PR22pinj.py 10014 0.02 0.15 FE22
#python3 read_PR22pinj.py 10820 0.01 0.1 FE23
#python3 read_PR22pinj.py 10820 0.01 0.1 P2.3
Program_configuration='PR22'
Program_configuration='P2.2'
Program_configuration='FEN1'
Program_configuration=str(sys.argv[4])
if Program_configuration=='FEN1' or Program_configuration=='FE22' or Program_configuration=='FE23':
    fenix=True
    ncoils=8
else:
    fenix=False
    ncoils=7
efitnumber='BEST'
tofile=bool(True)
#tofile=bool(False)
# for #8323
#efitnumber='RUN02'
pfit=0
ifPSU=1 # =1 Coil currents from PSU.PFNAME:I, =0 Coil currents from PSU2PF.I_PSU_BEST
ifWIRE=1 # =1 MC and PSH from ROG.WIRE 
ifNIR=0
ifSMM=0
SMMH1RUN='BEST'
#SMMH1RUN='RUN01'
ifNBI=0 # 2 - NBI.RFX.RUN1:PINJ [MW] ; 3 - RAW_NBI.RFX.HV_DAQ.ACCEL:CURRENT [0.1] 
efit=1
ifTETI=1
ifAr=0
ifSym=0 # 0 BVUT&BVUB; 1 (BVUT+BVUB)/2 
ifBND=0 # 0 - parametric boundary, 1 - by points, NB0 - points number
ntheta=64 # boundary points
mctime0=0.005 # time when MC  currents are set to zero
pshtime0=0.02 # time when PSH currents are set to zero
shotnumber=int(sys.argv[1])
time1=float(sys.argv[2])
time2=float(sys.argv[3])
"""
shotnumber=8478
time1=0.02
time2=0.18
"""
BEST=''
if shotnumber > 10800:BEST='BEST.'
#dt=0.0025
dt=0.005
na=int((time2-time1)/dt)+1

strshot=str(shotnumber)
timea=np.array([])
for i in range(0,na):
    timea=np.append(timea,time1+dt*i)

conn = Connection('192.168.1.7:8000')
conn.openTree('st40',shotnumber)

SOLV=conn.get('PSU.SOL:V').data()
DIVV=conn.get('PSU.DIV:V').data()
BVLV=conn.get('PSU.BVL:V').data()
BVUBV=conn.get('PSU.BVUB:V').data()
BVUTV=conn.get('PSU.BVUT:V').data()
MCV=conn.get('PSU.MC:V').data()
PSHV=conn.get('PSU.PSH:V').data()
TFV=conn.get('PSU.TF:V').data()
if ifPSU == 1 :
    SOLBEST=conn.get('PSU.SOL:I').data()
    DIVBEST=conn.get('PSU.DIV:I').data()
    BVLBEST=conn.get('PSU.BVL:I').data()
    BVUBBEST=conn.get('PSU.BVUB:I').data()
    BVUTBEST=conn.get('PSU.BVUT:I').data()
    MCBEST=conn.get('PSU.MC:I').data()
    PSHBEST=conn.get('PSU.PSH:I').data()
    TFBEST=conn.get('PSU.TF:I').data()
    TIMEpsu=conn.get('dim_of(PSU.SOL:I)').data()
elif ifPSU == 0 :
    IPSUBEST=conn.get('PSU2PF.I_PSU_BEST').data()
    TIMEpsu=conn.get('dim_of(PSU2PF.I_PSU_BEST)').data()
    PSUNAMES=conn.get('PSU2PF.PSU_NAMES').data()
    npsu=np.size(PSUNAMES)
    PFNAMES=conn.get('PSU2PF.PF_NAMES').data()
    ncoils=np.size(PFNAMES)
    PSU2PFTABLE=conn.get('PSU2PF.PSU2PF_TABLE').data()
    for i in range(0,npsu):
        print( i,PSUNAMES[i],npsu)
        if PSUNAMES[i] == b'SOL ':
            SOLBEST=IPSUBEST[i,:] 
        elif PSUNAMES[i] == b'MC  ':
            MCBEST=IPSUBEST[i,:] 
        elif PSUNAMES[i] == b'BVL ':
            BVLBEST=IPSUBEST[i,:] 
        elif PSUNAMES[i] == b'BVUT':
            BVUTBEST=IPSUBEST[i,:] 
        elif PSUNAMES[i] == b'BVUB':
            BVUBBEST=IPSUBEST[i,:] 
        elif PSUNAMES[i] == b'DIV ':
            DIVBEST=IPSUBEST[i,:] 
        elif PSUNAMES[i] == b'PSH ':
            PSHBEST=IPSUBEST[i,:] 
    TFBEST=conn.get('PSU2PF:I_TF').data()

BVUBEST=0.5*(BVUTBEST+BVUBBEST)
#BVUTBEST=BVUBEST
#BVUBBEST=BVUBEST
TFWIRE=conn.get('MAG.'+BEST+'ROG.TFWIRE:I').data()
MCWIRE=conn.get('MAG.'+BEST+'ROG.MCWIRE:I').data()
PSHBWIRE=conn.get('MAG.'+BEST+'ROG.PSHBWIRE:I').data()
PSHTWIRE=conn.get('MAG.'+BEST+'ROG.PSHTWIRE:I').data()
UPL=conn.get('MAG.'+BEST+'FLOOP.L016:V').data()
COMMENTpre=conn.get('SUMMARY.PRE_COMMENT').data()
COMMENTpost=conn.get('SUMMARY.POST_COMMENT').data()
TIMEmag=conn.get('dim_of(MAG.'+BEST+'FLOOP.L016:V)').data()
diva=np.array([])
bvla=np.array([])
bvuta=np.array([])
bvuba=np.array([])
bvua=np.array([])
mca=np.array([])
psha=np.array([])
sola=np.array([])
tfa=np.array([])
divva=np.array([])
bvlva=np.array([])
bvutva=np.array([])
bvubva=np.array([])
mcva=np.array([])
pshva=np.array([])
solva=np.array([])

TIME=TIMEpsu
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
    tfa=np.append(tfa,TFBEST[idw]+(TFBEST[iup]-TFBEST[idw])/dt0*(timea[i]-TIME[idw]))
    divva=np.append(divva,DIVV[idw]+(DIVV[iup]-DIVV[idw])/dt0*(timea[i]-TIME[idw])) 
    bvlva=np.append(bvlva,BVLV[idw]+(BVLV[iup]-BVLV[idw])/dt0*(timea[i]-TIME[idw])) 
    bvutva=np.append(bvutva,BVUTV[idw]+(BVUTV[iup]-BVUTV[idw])/dt0*(timea[i]-TIME[idw])) 
    bvubva=np.append(bvubva,BVUBV[idw]+(BVUBV[iup]-BVUBV[idw])/dt0*(timea[i]-TIME[idw])) 
    pshva=np.append(pshva,PSHV[idw]+(PSHV[iup]-PSHV[idw])/dt0*(timea[i]-TIME[idw])) 
    solva=np.append(solva,SOLV[idw]+(SOLV[iup]-SOLV[idw])/dt0*(timea[i]-TIME[idw])) 
    mcva=np.append(mcva,MCV[idw]+(MCV[iup]-MCV[idw])/dt0*(timea[i]-TIME[idw]))  
    if timea[i] > mctime0:  mca[i]=0
    if timea[i] > pshtime0:  psha[i]=0

upla=np.array([])
#tfwirea=np.array([])
mcwirea=np.array([])
pshbwirea=np.array([])
pshtwirea=np.array([])
TIME=TIMEmag
for i in range(0,na):   
    iupa=np.where(TIME > timea[i])
    iup=iupa[0][0]
    idwa=np.where(TIME <= timea[i])
    idw=idwa[0][len(idwa[0])-1]
    dt0=TIME[iup]-TIME[idw]
    upla=np.append(upla,UPL[idw]+(UPL[iup]-UPL[idw])/dt0*(timea[i]-TIME[idw]))
#    tfwirea=np.append(tfwirea,TFWIRE[idw]+(TFWIRE[iup]-TFWIRE[idw])/dt0*(timea[i]-TIME[idw]))
    mcwirea=np.append(mcwirea,MCWIRE[idw]+(MCWIRE[iup]-MCWIRE[idw])/dt0*(timea[i]-TIME[idw]))
    pshbwirea=np.append(pshbwirea,PSHBWIRE[idw]+(PSHBWIRE[iup]-PSHBWIRE[idw])/dt0*(timea[i]-TIME[idw]))
    pshtwirea=np.append(pshtwirea,PSHTWIRE[idw]+(PSHTWIRE[iup]-PSHTWIRE[idw])/dt0*(timea[i]-TIME[idw]))
if pfit == 1:
    signame0='PFIT.POST_BEST.RESULTS'
    signame=signame0+'.GLOBAL'
#    TIMEpfit=conn.get('dim_of('+signame+':IP)').data()
    TIMEpfit=conn.get(signame0+':TIME').data()
    TIME=TIMEpfit
    print(TIME)
    time0=TIME[(TIME>time1) & (TIME<time2)]
    n0=len(time0)
    signame=signame0+'.GLOBAL:'
    IPL= conn.get(signame+'IP').data()
    RTOR= conn.get(signame+'RGEO').data()
    AMIN= conn.get(signame+'AMINOR').data()
    ELONG= conn.get(signame+'KAPPA').data()
    ipla=np.array([])
    rtora=np.array([])
    amina=np.array([])
    elona=np.array([])
    if len(IPL) == 1:
        IPL=IPL[0] 
        RTOR= RTOR[0]
        AMIN=AMIN[0]
        ELONG= ELONG[0]
    for i in range(0,na):
        iupa=np.where(TIME > timea[i])
        iup=iupa[0][0]
        idwa=np.where(TIME <= timea[i])
        idw=idwa[0][len(idwa[0])-1]
        dt0=TIME[iup]-TIME[idw]
        ipla=np.append(ipla,IPL[idw]+(IPL[iup]-IPL[idw])/dt0*(timea[i]-TIME[idw]))
        rtora=np.append(rtora,RTOR[idw]+(RTOR[iup]-RTOR[idw])/dt0*(timea[i]-TIME[idw]))
        amina=np.append(amina,AMIN[idw]+(AMIN[iup]-AMIN[idw])/dt0*(timea[i]-TIME[idw]))
        elona=np.append(elona,ELONG[idw]+(ELONG[iup]-ELONG[idw])/dt0*(timea[i]-TIME[idw]))
if ifNBI == 1:
    signame='NBI.RFX.RUN1:PINJ'
    SIG=conn.get(signame).data()
    TIME=conn.get('dim_of('+signame+')').data()
    rfxa=np.array([])
    for i in range(0,na):
        iupa=np.where(TIME > timea[i])
        iup=iupa[0][0]
        idwa=np.where(TIME <= timea[i])
        idw=idwa[0][len(idwa[0])-1]
        dt0=TIME[iup]-TIME[idw]
        rfxa=np.append(rfxa,SIG[idw]+(SIG[iup]-SIG[idw])/dt0*(timea[i]-TIME[idw]))


    signame='NBI.HNBI1.RUN1:PINJ'
    SIG=conn.get(signame).data()
    TIME=conn.get('dim_of('+signame+')').data()
    hnbia=np.array([])
    print(TIME)
    for i in range(0,na):
        print(i,timea[i])
        iupa=np.where(TIME > timea[i])
        iup=iupa[0][0]
        idwa=np.where(TIME <= timea[i])
        idw=idwa[0][len(idwa[0])-1]
        dt0=TIME[iup]-TIME[idw]
        hnbia=np.append(hnbia,SIG[idw]+(SIG[iup]-SIG[idw])/dt0*(timea[i]-TIME[idw]))

if ifNBI == 2:
    signame='NBI.RFX.RUN1:PINJ'
    try:
        SIG=conn.get(signame).data()
        RFXYES=0==0
    except:
        RFXYES=0==1
         
    if RFXYES:
        TIME=conn.get('dim_of('+signame+')').data()
        rfxa=np.array([])
        for i in range(0,na):
            iupa=np.where(TIME > timea[i])
            iup=iupa[0][0]
            idwa=np.where(TIME <= timea[i])
            idw=idwa[0][len(idwa[0])-1]
            dt0=TIME[iup]-TIME[idw]
            rfxa=np.append(rfxa,SIG[idw]+(SIG[iup]-SIG[idw])/dt0*(timea[i]-TIME[idw]))
    signame='NBI.HNBI1.RUN1:PINJ'
    try:
        SIG=conn.get(signame).data()
        HNBIYES=0==0
    except:
        HNBIYES=0==1
    if HNBIYES:
        TIME=conn.get('dim_of('+signame+')').data()
        hnbia=np.array([])
        print(TIME)
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

if ifNBI == 3:
    signame='RAW_NBI.RFX.HV_DAQ.ACCEL:CURRENT'
    print(signame)
    try:
        SIG=conn.get(signame).data()
        RFXYES=0==0
        print(SIG)
    except:
        RFXYES=0==1
    if not np.isnan(SIG).any() and  RFXYES:
        TIME=conn.get('dim_of('+signame+')').data()
        rfxa=np.array([])
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
        hnbia=np.array([])
        print(TIME)
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

if ifAr == 1:
#SXR.XRCS.BEST.TE_KW:INT_W
    signame0='SXR.XRCS.BEST'
    TIME=conn.get(signame0+':TIME').data()
    INTW=conn.get(signame0+'.TE_KW:INT_W').data()
    iupa=np.where(TIME <= timea[na-1])
    idwa=np.where(TIME >= timea[0])
    iup=iupa[0][len(iupa[0])-1]
    idw=idwa[0][0]
    TIMEAR=TIME[idw:iup]
    IAR=INTW[idw:iup]


if ifNIR == 1:
    DENNIR=conn.get('INTERFEROM.NIRH1.BEST.LINE_AV:NE').data()
    TIMENIR=conn.get('INTERFEROM.NIRH1.BEST:TIME').data()
    dennir=np.array([])
    TIME=TIMENIR
    DEN=DENNIR
    for i in range(0,na):   
        iupa=np.where(TIME > timea[i])
        iup=iupa[0][0]
        idwa=np.where(TIME <= timea[i])
        idw=idwa[0][len(idwa[0])-1]
        dt0=TIME[iup]-TIME[idw]
        dennir=np.append(dennir,DEN[idw]+(DEN[iup]-DEN[idw])/dt0*(timea[i]-TIME[idw]))
    print(dennir)

if ifSMM == 1:
    try:
        #DENSMM=conn.get('INTERFEROM.SMMH1_SCALE.'+SMMH1RUN+'.LINE_INT:NE_EFIT').data()
        DENSMM=conn.get('INTERFEROM.SMMH1.'+SMMH1RUN+'.LINE_INT:NE').data()
        print(DENSMM)
        SMMYES=0==0
    except:
        SMMYES=0==1
    if SMMYES:
        TIME=conn.get('INTERFEROM.SMMH1.'+SMMH1RUN+':TIME').data()
        DEN=DENSMM
        dneg=np.where(DENSMM <= 0)
        dpos=np.where(DENSMM > 0)
        DEN[dneg]=min(DENSMM[dpos])
        densmm=np.array([])
        print(TIME)
        for i in range(0,na):   
            iupa=np.where(TIME > timea[i])
            iup=iupa[0][0]
            idwa=np.where(TIME <= timea[i])
            idw=idwa[0][len(idwa[0])-1]
            dt0=TIME[iup]-TIME[idw]
            densmm=np.append(densmm,DEN[idw]+(DEN[iup]-DEN[idw])/dt0*(timea[i]-TIME[idw])) 
        print(DENSMM) 

if ifTETI == 1:
    signame0='SXR.XRCS.BEST'
    TIME=conn.get(signame0+':TIME').data()
    if not np.isscalar(TIME):
        TIW=conn.get(signame0+'.TI_W:TI0').data()
        TEKW=conn.get(signame0+'.TE_KW:TE0').data()
        iupa=np.where(TIME <= timea[na-1])
        idwa=np.where(TIME >= timea[0])
        iup=iupa[0][len(iupa[0])-1]
        idw=idwa[0][0]
        TIMET=TIME[idw:iup]
        TE=TEKW[idw:iup]
        TI=TIW[idw:iup]

if efit == 1:
    signame0='EFIT.'+str(efitnumber)
    print(signame0)
    TIME=conn.get(signame0+':TIME')
    ne=np.size(TIME)-1
    signame=signame0+'.CONSTRAINTS'
    IPL=conn.get(signame+'.IP:MVALUE')
    BPefit=-conn.get(signame+'.BP:CVALUE')
    ROG= conn.get(signame+'.ROGC:MVALUE')
    MCRG=(ROG[:,0]+ROG[:,1])/2
    BVLR=(ROG[:,2]+ROG[:,3])/2
    signame=signame0+'.GLOBAL'
    RTOR=conn.get(signame+':RGEO')
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
    if ifBND == 1: 
        signame=signame0+'.P_BOUNDARY'
        RBND= conn.get(signame+':RBND')
        ZBND= conn.get(signame+':ZBND') 
 
    ipla=np.array([])
    rtora=np.array([])
    zgeoa=np.array([])
    amina=np.array([])
    elona=np.array([])
    triaa=np.array([])
    wmhda=np.array([])
    betpa=np.array([])
    betta=np.array([])
    qedgea=np.array([])
    lia=np.array([])
    mcrga=np.array([])
    bvlra=np.array([])
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
        if ifBND == 1: 
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

        ipla=np.append(ipla,IPL[idw]+(IPL[iup]-IPL[idw])/dt0*(timea[i]-TIME[idw]))
        rtora=np.append(rtora,RTOR[idw]+(RTOR[iup]-RTOR[idw])/dt0*(timea[i]-TIME[idw]))
        zgeoa=np.append(zgeoa,ZGEO[idw]+(ZGEO[iup]-ZGEO[idw])/dt0*(timea[i]-TIME[idw]))
        amina=np.append(amina,AMIN[idw]+(AMIN[iup]-AMIN[idw])/dt0*(timea[i]-TIME[idw]))
        elona=np.append(elona,ELON[idw]+(ELON[iup]-ELON[idw])/dt0*(timea[i]-TIME[idw]))
        triaa=np.append(triaa,TRIA[idw]+(TRIA[iup]-TRIA[idw])/dt0*(timea[i]-TIME[idw]))
        wmhda=np.append(wmhda,WMHD[idw]+(WMHD[iup]-WMHD[idw])/dt0*(timea[i]-TIME[idw]))
        betpa=np.append(betpa,BETP[idw]+(BETP[iup]-BETP[idw])/dt0*(timea[i]-TIME[idw]))
        betta=np.append(betta,BETT[idw]+(BETT[iup]-BETT[idw])/dt0*(timea[i]-TIME[idw]))
        qedgea=np.append(qedgea,QEDG[idw]+(QEDG[iup]-QEDG[idw])/dt0*(timea[i]-TIME[idw]))
        lia=np.append(lia,LI3M[idw]+(LI3M[iup]-LI3M[idw])/dt0*(timea[i]-TIME[idw]))
        mcrga=np.append(mcrga,MCRG[idw]+(MCRG[iup]-MCRG[idw])/dt0*(timea[i]-TIME[idw])) 
        bvlra=np.append(bvlra,BVLR[idw]+(BVLR[iup]-BVLR[idw])/dt0*(timea[i]-TIME[idw])) 


nefit=i
R0=np.mean(rtora)
shif=rtora-R0
#btora=tfa/5/R0/1e6*23
btora=tfa/5/R0/1e6*24
#btorefita=tfwirea/5/R0/1e6*24

import sys
orig_stdout = sys.stdout
#f = open('st40_'+strshot+'_'+efitnumber,'w')
f = open('exp/st40_'+strshot+'_'+Program_configuration,'w')
if tofile:sys.stdout = f

print( Program_configuration,' #',strshot)
print( ' Pre:',COMMENTpre)
print( ' Post:',COMMENTpost)
if efit ==1:
    print( ' EFIT geometry')
else:
    print( ' PFIT geometry')
    nefit=na
    
print( ' Name	Time	Value	Error')
print( 'NA1             65')
print( 'AB              0.3')
print( 'AWALL           0.3')
for i in range(nefit): print( 'UPDWN  ','%.4f '%timea[i],'%.3f'%zgeoa[i])
print( 'RTOR           ','%.3f'%R0)
for i in range(nefit): print( 'SHIFT  ','%.4f '%timea[i],'%.3f'%shif[i])
for i in range(nefit): print( 'ABC    ','%.4f '%timea[i],'%.3f'%amina[i])
print( 'ELONM           1.6')
for i in range(nefit): print( 'ELONG  ','%.4f '%timea[i],'%.3f'%elona[i])
for i in range(nefit): print( 'IPL    ','%.4f '%timea[i],'%.3f'%(ipla[i]*1.e-6))
#print( ' BTOR from MAG.ROG.TFWIRE,T')
#for i in range(nefit): print( 'BTOR   ','%.4f '%timea[i],'%.3f'%btorefita[i])
print( ' BTOR  from TF')
for i in range(nefit): print( 'BTOR   ','%.4f '%timea[i],'%.3f'%btora[i])
if efit == 1:
    print( 'TRICH           0.6')
    print( ' Triangularity up-down symmetrized')
    for i in range(nefit): print( 'TRIAN  ','%.4f '%timea[i],'%.3f'%triaa[i])
    print( ' Beta pol')
    for i in range(nefit): print( 'ZRD1   ','%.4f '%timea[i],'%.3f'%betpa[i])
    print( ' Beta')
    for i in range(nefit): print( 'ZRD2   ','%.4f '%timea[i],'%.3f'%betta[i])
    print( ' qedge')
    for i in range(nefit): print( 'ZRD3   ','%.4f '%timea[i],'%.3f'%qedgea[i])
    print( ' W EFIT,kJ')
    for i in range(nefit): print( 'ZRD4   ','%.4f '%timea[i],'%.3f'%(wmhda[i]/1.e3))
    print( ' li internal inductance')
    for i in range(nefit): print( 'ZRD5   ','%.4f '%timea[i],'%.3f'%lia[i])

print( ' UEXT loop voltage,V')
for i in range(na): print( 'ZRD6   ','%.4f '%timea[i],'%.3f'%upla[i])

if ifPSU==0: print( ' DIV,kA, from PSU2PF.I_PSU_BEST')
if ifPSU==1: print( ' DIV,kA, from PSU.DIV:I')
for i in range(na): print( 'ZRD7   ','%.4f '%timea[i],'%.3f'%(diva[i]/1.e3))
if ifPSU==0: print( ' BVL,kA, from PSU2PF.I_PSU_BEST')
if ifPSU==1: print( ' BVL,kA, from PSU.BVL:I')
for i in range(na): print( 'ZRD8   ','%.4f '%timea[i],'%.3f'%(bvla[i]/1.e3))
if ifPSU==0: print( ' BVUT,kA, from PSU2PF.I_PSU_BEST')
if ifPSU==1: print( ' BVUT,kA, from PSU.BVUT:I')
for i in range(na): print( 'ZRD9   ','%.4f '%timea[i],'%.3f'%(bvuta[i]/1.e3))
if ifPSU==0: print( ' BVUB,kA, from PSU2PF.I_PSU_BEST')
if ifPSU==1: print( ' BVUB,kA, from PSU.BVUB:I')
for i in range(na): print( 'ZRD10  ','%.4f '%timea[i],'%.3f'%(bvuba[i]/1.e3))
if ifPSU==0: print( ' SOL,kA, from PSU2PF.I_PSU_BEST')
if ifPSU==1: print( ' SOL,kA, from PSU.SOL:I')
for i in range(na): print( 'ZRD11  ','%.4f '%timea[i],'%.3f'%(sola[i]/1.e3))
if ifWIRE == 0:
    if ifPSU==0: print( ' MC,kA, from PSU2PF.I_PSU_BEST')
    if ifPSU==1: print( ' MC,kA, from PSU.MC:I')
    for i in range(na): print( 'ZRD12   ','%.4f '%timea[i],'%.3f'%(mca[i]/1.e3))
    if ifPSU==0: print( ' PUSHER,kA, from PSU2PF.I_PSU_BEST')
    if ifPSU==1: print( ' PUSHER,kA, from PSU.PSH:I')
    for i in range(na): print( 'ZRD13  ','%.4f '%timea[i],'%.3f'%(psha[i]/1.e3))
if ifWIRE == 1:
    print( ' MC,kA, from MAG.ROG.MCWIRE:I')
    for i in range(na): print( 'ZRD12   ','%.4f '%timea[i],'%.3f'%(mcwirea[i]/1.e3))
    print( ' PUSHER TOP,kA, from  MAG.ROG.PSHTWIRE:I')
    for i in range(na): print( 'ZRD13  ','%.4f '%timea[i],'%.3f'%(pshtwirea[i]/1.e3))
    print( ' PUSHER BOT,kA, from  MAG.ROG.PSHBWIRE:I')
    for i in range(na): print( 'ZRD13  ','%.4f '%timea[i],'%.3f'%(pshbwirea[i]/1.e3))
    print( ' PUSHER mean(up,down),kA, from  MAG.ROG.PSHTWIRE:I and MAG.ROG.PSHBWIRE:I')
    for i in range(na): print( 'ZRD13  ','%.4f '%timea[i],'%.3f'%((pshtwirea[i]+pshbwirea[i])/2.e3))
 
if ifTETI==1:
    print( ' Electron temperature SXR.XRCS.BEST.TE_KW:TE0')
    for i in range(len(TIMET)): 
        if math.isnan(TE[i]) != True : 
            print( 'ZRD14  ','%.4f '%TIMET[i],'%.3f'%(TE[i]/1000))
    print( ' Ion temperature SXR.XRCS.BEST.TI_W:TI0')
    for i in range(len(TIMET)): 
        if math.isnan(TI[i]) != True :  
            print( 'ZRD15  ','%.4f '%TIMET[i],'%.3f'%(TI[i]/1000))

if ifSMM == 1:
    if SMMYES:
        print( ' Chord averaged density SMM, 10^19 m^-2')
        for i in range(na): print( 'ZRD20  ','%.4f '%timea[i],'%.3f'%(densmm[i]/1e19))
elif ifNIR == 1:
    print( ' Chord averaged density NIR, 10^19 m^-2')
    for i in range(na): print( 'ZRD20  ','%.4f '%timea[i],'%.3f'%(dennir[i]/1e19))
else:
    print( ' Chord averaged density no signal')
    print( 'ZRD20  ','%.4f '%time1,' 1.0')

if ifNBI == 1:
    print( ' RFX beam')
    for i in range(na): print( 'ZRD60  ','%.4f '%timea[i],'%.3f'%(rfxa[i]))
    print( ' HNBI beam')
    for i in range(na): print( 'ZRD70  ','%.4f '%timea[i],'%.3f'%(hnbia[i]))
if ifNBI == 2 :
    if RFXYES:
        print( ' RFX beam, PINJ, MW')
        for i in range(na): print( 'ZRD60  ','%.4f '%timea[i],'%.3f'%(rfxa[i]))
    if HNBIYES:
        print( ' HNBI beam, PINJ, MW')
        for i in range(na): print( 'ZRD70  ','%.4f '%timea[i],'%.3f'%(hnbia[i]))
if ifNBI == 3:
    if RFXYES:
        print( ' RFX beam, yes/no')
        for i in range(na): print( 'ZRD60  ','%.4f '%timea[i],'%.3f'%(rfxa[i]))
    if HNBIYES:
        print( ' HNBI beam, yes/no')
        for i in range(na): print( 'ZRD70  ','%.4f '%timea[i],'%.3f'%(hnbia[i]))

if ifAr==1:
    print( ' Argon line emission SXR.XRCS.BEST.TE_KW:INT_W')
    for i in range(len(TIMEAR)): 
        if math.isnan(IAR[i]) != True : 
            print( 'ZRD51  ','%.4f '%TIMEAR[i],'%.3f'%(IAR[i]))
if ifBND == 1: 
    print('NAMEXP BND NTIMES ','%.0f'%na,' POINTS ','%.0f'%(ntheta-1))
    for i in range(na): print( '%.4f'%timea[i],end=' ')
    print( )
    for j in range(ntheta-1): 
        for i in range(0,na):
            print('%.4f '%r[ntheta*i+j],end=' ')
            if int(i/10) == i/10 and i != 0: print()
        print()
        for i in range(0,na):
            print('%.4f '%z[ntheta*i+j],end=' ')
            if int(i/10) == i/10 and i != 0: print()
        print()

 
if fenix:
    print( ' current[MA] in coils:IPL MC  PSH DIV BVL BVUT BVUB SOL  ')
else:    
    print( ' current[MA] in coils:DIV BVL BVUT BVUB SOL  MC  PSH ')
print( ' see coil.dat & coilres.dat in PR22')
print('NAMEXP CCOIL NTIMES ','%.0f'%na,' POINTS ','%.0f'%ncoils)
for i in range(na): 
    print( '%.4f'%timea[i],end=' ')
    if int(i/10) == i/10 and i != 0: print()

print( )
if fenix :
    for i in range(na): print(\
                              '0.0 ',\
                              '%.3e'%(mca[i]/1.e6),\
                              '%.3e'%(psha[i]/1.e6),\
                              '%.3e'%(diva[i]/1.e6),\
                              '%.3e'%(bvla[i]/1.e6),\
                              '%.3e'%(bvua[i]/1.e6),\
                              '%.3e'%(bvua[i]/1.e6),\
                              '%.3e'%(sola[i]/1.e6))
else:
    if ifSym == 1:
        for i in range(na): print(\
                              '%.3e'%(diva[i]/1.e6),\
                              '%.3e'%(bvla[i]/1.e6),\
                              '%.3e'%(bvua[i]/1.e6),\
                              '%.3e'%(bvua[i]/1.e6),\
                              '%.3e'%(sola[i]/1.e6),\
                              '%.3e'%(mca[i]/1.e6),\
                              '%.3e'%(psha[i]/1.e6))
    else:
        for i in range(na):    print(\
                                 '%.3e'%(diva[i]/1.e6),\
                                 '%.3e'%(bvla[i]/1.e6),\
                                 '%.3e'%(bvuta[i]/1.e6),\
                                 '%.3e'%(bvuba[i]/1.e6),\
                                 '%.3e'%(sola[i]/1.e6),\
                                 '%.3e'%(mca[i]/1.e6),\
                                 '%.3e'%(psha[i]/1.e6))
print('NAMEXP VCOIL NTIMES ','%.0f'%na,'  POINTS ','%.0f'%ncoils)
for i in range(na): print( '%.4f'%timea[i],end=' ')
print( )
if fenix:
    for i in range(na): print(\
                              '0.0 ',\
                              '%.3e'%mcva[i],\
                              '%.3e'%pshva[i],\
                              '%.3e'%divva[i],\
                              '%.3e'%bvlva[i],\
                              '%.3e'%bvutva[i],\
                              '%.3e'%bvubva[i],\
                              '%.3e'%solva[i])
else:
    for i in range(na): print(\
                              '%.3e'%divva[i],\
                              '%.3e'%bvlva[i],\
                              '%.3e'%bvutva[i],\
                              '%.3e'%bvubva[i],\
                              '%.3e'%solva[i],\
                              '%.3e'%mcva[i],\
                              '%.3e'%pshva[i])
print( 'END')
sys.stdout = orig_stdout
f.close()

#plt.figure()s
#plt.scatter(timea,ipla)
#plt.show()

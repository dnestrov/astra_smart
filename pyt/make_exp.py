from MDSplus import *
import numpy as np
import math
import sys
import read_data_fun as read
conn = Connection('192.168.1.7:8000')
shotxrcs=12000 # shot number to start new XRCS tree
time1=0.01;time2=0.2;shotnumber=13311419;strshot=str(shotnumber);Program_configuration='P2.3'
efitnumber='RUN2120';ntheta=64;
def printout(shotnumber,time1,time2,t1,t2,Program_configuration,efit,efitnumber,pfit,ifBND,ntheta,ifPSU,ifNIR,ifSMM,ifNBI,ifXRCS,ifAr,ifSym,ifTWSTi,ifTWSVtor,ifPITi,ifPIVtor,ifTS,ifTSHFS,ifTSLFS,filt,ifHDA,runHDA,ifBDA,bdarange,ifTRANSP,shotT,runT,tofile):
    runts='BEST'
    #runts='RUN03'
    runTWS='BEST'
    runPI='BEST'
#    tofile=bool(False)
    BEST=''
    if shotnumber > 10800:BEST='BEST.'
    #dt=0.0025
    dt=0.005
    na=int((time2-time1)/dt)+1
    
    strshot=str(shotnumber)
    timea=np.array([])
    for i in range(0,na):
        timea=np.append(timea,time1+dt*i)
        
    if Program_configuration=='FE23' or Program_configuration=='P238' or Program_configuration=='V238':
        fenix=True
        ncoils=8
    elif Program_configuration=='MCT_':
        fenix=False
        ncoils=8
    else:
        fenix=False
        ncoils=7
    if  Program_configuration=='P238':
        ifPSU=1;ifNIR=0;ifSMM=0;ifNBI=0;efit=0;pfit=0
        ifAr=0;ifSym=0;ifBND=0;ifTS=0;ifTSHFS=0;ifTSLFS=0
        ifTWSTi=0;ifTWSVtor=0;ifPITi=0;ifPIVtor=0;ifXRCS=0

    read.open_conn(shotnumber)
    COMMENTpre,COMMENTpost=read.read_comment()  
    upla=read.read_mag(BEST,timea)
    tfa=read.read_tfa(timea)
    if ifPSU==1:
        diva,bvla,bvuta,bvuba,mca,psha,sola,divva,bvlva,bvutva,bvubva,mcva,pshva,solva=read.read_psu(timea)
    if pfit==1:
        iplpf,rtorpf,aminpf,elonpf,zgeopf,timepfit=read.read_pfit(timea)
        npfit=len(timepfit)
    if ifNBI != 0:RFXYES,rfxa,HNBIYES,hnbia=read.read_NBI(ifNBI,timea)
    if efit==1:
        ipla,triaa,wmhda,betpa,betta,qedgea,lia,rtora,amina,elona,zgeoa,TIMEefit,RMAG=read.read_efit(efitnumber,timea)
    if ifBND==1:
        r,z=read.read_efitBND(efitnumber,ntheta,timea)
    ind=np.array([])
    if efit ==1 and  pfit ==0:
        ngeo=na
        timegeo=timea
        zgeo=zgeoa
        elon=elona
        ipl=ipla
        for i in range(0,len(rtora)):
            if math.isnan(rtora[i]) != True : ind=np.append(ind,i)
        R0=np.mean(rtora[ind.astype(int)])
        shif=rtora-R0
        amin=amina
    if pfit ==1:
        print( ' PFIT geometry (a,shif,elon,updwn) and current (ipl)')
        ngeo=npfit
        timegeo=timepfit
        zgeo=zgeopf
        elon=elonpf
        ipl=iplpf
        for i in range(0,len(rtorpf)):
            if math.isnan(rtorpf[i]) != True : ind=np.append(ind,i)
        R0=np.mean(rtorpf[ind.astype(int)])
        shif=rtorpf-R0
        amin=aminpf

    if efit ==0 and  pfit ==0:#i.e. for vacuum shot P238
        index=timea/timea
        R0=0.44
        zgeo=0*index
        shif=0*index
        elon=1*index
        amin=0.22*index
        ipl=500000*index
        tfa=150000*index
        print(amin)
        ngeo=na
        timegeo=timea
    btor=tfa/5/R0/1e6*24
    orig_stdout = sys.stdout
    if shotnumber < 10000 :
        filename='exp/st40_0'+strshot
    else:
        filename='exp/st40_'+strshot
    if ifBND == 1:filename=filename+'BND'
    if ifTS == 1 : filename=filename+'ts'
    if ifTSHFS == 1: filename=filename+'tsH'
    if ifTSLFS == 1: filename=filename+'tsL'
    if ifTS == 1 and runts[0:3] == 'RUN':filename=filename+runts[3:5]
    if ifHDA == 1: filename=filename+'HDA'+runHDA
    if ifBDA == 1: filename=filename+'BDA'
    if ifTRANSP == 1: filename=filename+'TR'+runT
    if ifTWSTi == 1 or ifTWSVtor == 1: filename=filename+'TWS'
    if ifPITi == 1 or ifPIVtor == 1 : filename=filename+'PI'
    if pfit == 1: filename=filename+'pfit'
    if efitnumber[0:3] == 'RUN': filename=filename+'efit'+efitnumber[3:5]
    filename=filename+Program_configuration
    print(filename)
    if tofile:    
        f = open(filename,'w')
        sys.stdout = f
    if ifHDA == 0 and ifBDA == 0 and ifTRANSP == 0: 
        print( Program_configuration,' #',strshot)
        print( ' Pre:',COMMENTpre)
        print( ' Post:',COMMENTpost)
    if ifHDA == 1 :
        print( Program_configuration)
        print( 'HDA profiles from #'+str(shotnumber+25000000)+'@'+runHDA)
        print( Program_configuration,' #',strshot)
    if ifBDA == 1 :
        print( Program_configuration)
        print( ' BDA profiles from #'+str(shotnumber+bdarange)+'@BEST')
    if ifTRANSP == 1: 
        print( Program_configuration)
        print( ' TRANSP profiles from #'+str(shotT)+'@'+runT)
    print( ' EFIT geometry @'+efitnumber)
    print( ' Name	Time	Value	Error')
    print( 'NA1             65')
    print( 'AB              0.35')
    print( 'AWALL           0.35')
    for i in range(ngeo): print( 'UPDWN  ','%.4f '%timegeo[i],'%.3f'%zgeo[i])
    print( 'RTOR           ','%.3f'%R0)
    for i in range(ngeo): print( 'SHIFT  ','%.4f '%timegeo[i],'%.3f'%shif[i])
    for i in range(ngeo): print( 'ABC    ','%.4f '%timegeo[i],'%.3f'%amin[i])
    print( 'ELONM           1.9')
    for i in range(ngeo): print( 'ELONG  ','%.4f '%timegeo[i],'%.3f'%elon[i])
    for i in range(ngeo): print( 'IPL    ','%.4f '%timegeo[i],'%.3f'%(ipl[i]*1.e-6))
    if tfa[0] != 0:
        print( ' BTOR  from TF')
        for i in range(na): print( 'BTOR   ','%.4f '%timegeo[i],'%.3f'%btor[i])
    if efit == 1:
        print( ' EFIT data from TRIAN to li')
        print( 'TRICH           0.6')
        print( ' Triangularity up-down symmetrized')
        for i in range(na): print( 'TRIAN  ','%.4f '%timea[i],'%.3f'%triaa[i])
        print( ' Beta pol')
        for i in range(na): print( 'ZRD1   ','%.4f '%timea[i],'%.3f'%betpa[i])
        print( ' Beta')
        for i in range(na): print( 'ZRD2   ','%.4f '%timea[i],'%.3f'%betta[i])
        print( ' qedge')
        for i in range(na): print( 'ZRD3   ','%.4f '%timea[i],'%.3f'%qedgea[i])
        print( ' W EFIT,kJ')
        for i in range(na): print( 'ZRD4   ','%.4f '%timea[i],'%.3f'%(wmhda[i]/1.e3))
        print( ' li internal inductance')
        for i in range(na): print( 'ZRD5   ','%.4f '%timea[i],'%.3f'%lia[i])

    if upla[0] != 0:
        print( ' UEXT loop voltage from MAG.L016, V')
        for i in range(na): print( 'ZRD6   ','%.4f '%timea[i],'%.3f'%upla[i])

    if ifPSU==1: 
        print( ' DIV,kA, from PSU.DIV:I')
        for i in range(na): print( 'ZRD7   ','%.4f '%timea[i],'%.3f'%(diva[i]/1.e3))
        print( ' BVL,kA, from PSU.BVL:I')
        for i in range(na): print( 'ZRD8   ','%.4f '%timea[i],'%.3f'%(bvla[i]/1.e3))
        print( ' BVUT,kA, from PSU.BVUT:I')
        for i in range(na): print( 'ZRD9   ','%.4f '%timea[i],'%.3f'%(bvuta[i]/1.e3))
        print( ' BVUB,kA, from PSU.BVUB:I')
        for i in range(na): print( 'ZRD10  ','%.4f '%timea[i],'%.3f'%(bvuba[i]/1.e3))
        print( ' SOL,kA, from PSU.SOL:I')
        for i in range(na): print( 'ZRD11  ','%.4f '%timea[i],'%.3f'%(sola[i]/1.e3))
        
    if ifXRCS==1:
        TIMET,TI,TE=read.read_XRCS(shotxrcs,timea)
        if np.isscalar(TIMET) and TIMET == -999: 
            print(' No XRCS data')
        else:
            if shotnumber <= shotxrcs:
                print( ' Electron temperature SXR.XRCS.BEST.TE_KW:TE0')
            else:
                print( ' Electron temperature XRCS.BEST.GLOBAL:TE_KW')
            for i in range(len(TIMET)): 
                if math.isnan(TE[i]) != True : 
                    print( 'ZRD14  ','%.4f '%TIMET[i],'%.3f'%(TE[i]/1000))
            if shotnumber <= shotxrcs:
                print( ' Ion temperature SXR.XRCS.BEST.TI_W:TI0')
            else:
                print( ' Ion temperature XRCS.BEST.GLOBAL:TI_W')                
            for i in range(len(TIMET)): 
                if math.isnan(TI[i]) != True :  
                    print( 'ZRD15  ','%.4f '%TIMET[i],'%.3f'%(TI[i]/1000))

    if ifSMM == 1:
        SMMYES,densmm=read.read_SMM(timea)
        if SMMYES:
            print( ' Chord averaged density SMM, 10^19 m^-2')
            for i in range(na): print( 'ZRD20  ','%.4f '%timea[i],'%.3f'%(densmm[i]/1e19))
        else:
            print( ' Chord averaged density no SMM signal')
            print( 'ZRD20  ','%.4f '%time1,' 1.0')
    if ifNIR == 1:
        NIRYES,dennir=read.read_NIR(timea)
        if NIRYES:
            print( ' Chord averaged density NIR, 10^19 m^-2')
            for i in range(na): print( 'ZRD20  ','%.4f '%timea[i],'%.3f'%(dennir[i]/1e19))
        else:
            print( ' Chord averaged density no NIR signal')
            print( 'ZRD20  ','%.4f '%time1,' 1.0')

    if ifNBI > 0 :
        if RFXYES:
            print( ' RFX beam, PINJ, MW')
            for i in range(na): print( 'ZRD60  ','%.4f '%timea[i],'%.3f'%(rfxa[i]))
        if HNBIYES:
            print( ' HNBI beam, PINJ, MW')
            for i in range(na): print( 'ZRD70  ','%.4f '%timea[i],'%.3f'%(hnbia[i]))
    if ifNBI == -1:
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

    if ifHDA == 1:
        import read_data_funHDA as hda
        hda.read_HDA_glob(shotnumber+25000000,runHDA)
        hda.read_HDA_prof(shotnumber+25000000,runHDA)
    if ifBDA == 1:
        import read_data_funBDA as bda
        bda.read_BDA_glob(shotnumber+bdarange,'BDA.BEST')
        bda.read_BDA_prof(shotnumber+bdarange,'BDA.BEST')
    if ifTRANSP == 1:
        import read_transp_data as transp
        transp.read_glob2exp(shotT,runT)
        transp.read_prof2exp(shotT,runT)
    if ifTS == 1:
        import readtsprofiles as readts
        print(' All points from TS data @'+runts)
        readts.ts(shotnumber,runts,time1,time2,t1,t2,filt)
    if ifTSHFS == 1 and efit == 1:
        import readtsprofiles as readts
        print(' HFS points from TS data @'+runts)
        readts.tsHFS(shotnumber,runts,time1,time2,t1,t2,TIMEefit,RMAG)
    if ifTSLFS == 1 and efit == 1:
        import readtsprofiles as readts
        print(' LFS points from TS data @'+runts)
        readts.tsLFS(shotnumber,runts,time1,time2,t1,t2,TIMEefit,RMAG)
    if ifTWSTi == 1:
        import readcxprofiles as readcx
        readcx.cx19TWS(shotnumber,runTWS,time2,'TI')
    if ifTWSVtor == 1:
        import readcxprofiles as readcx
        readcx.cx19TWS(shotnumber,runTWS,time2,'VTOR')
    if ifPITi == 1:
        import readcxprofiles as readcx
        readcx.cx19PI(shotnumber,runPI,time2,'TI')
    if ifPIVtor == 1:
        import readcxprofiles as readcx
        readcx.cx19PI(shotnumber,runPI,time2,'VTOR')
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

    if ifPSU==1: 
        if fenix:
            print( ' current[MA] in coils:IPL MC  PSH DIV BVL BVUT BVUB SOL  ')
        else:
            if ncoils==8:    
                print( ' current[MA] in coils:DIV BVL BVUT BVUB SOL  MCT MCB  PSH ')
            if ncoils==7:        
                print( ' current[MA] in coils:DIV BVL BVUT BVUB SOL  MC  PSH ')
        print( ' see coil.dat & coilres.dat in exp/equ/'+Program_configuration)
        print('NAMEXP CCOIL NTIMES ','%.0f'%na,' POINTS ','%.0f'%ncoils)
        for i in range(na): 
            print( '%.4f'%timea[i],end=' ')
            if int(i/10) == i/10 and i != 0: print()
        print( )
        if fenix :
            if ifSym == 1:
                bvua=0.5*(bvuba+bvuta)
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
                for i in range(na): print(\
                                          '0.0 ',\
                                          '%.3e'%(mca[i]/1.e6),\
                                          '%.3e'%(psha[i]/1.e6),\
                                          '%.3e'%(diva[i]/1.e6),\
                                          '%.3e'%(bvla[i]/1.e6),\
                                          '%.3e'%(bvuta[i]/1.e6),\
                                          '%.3e'%(bvuba[i]/1.e6),\
                                          '%.3e'%(sola[i]/1.e6))
        else:
            if ifSym == 1:
                bvua=0.5*(bvuba+bvuta)
                for i in range(na): print(\
                                          '%.3e'%(diva[i]/1.e6),\
                                          '%.3e'%(bvla[i]/1.e6),\
                                          '%.3e'%(bvua[i]/1.e6),\
                                          '%.3e'%(bvua[i]/1.e6),\
                                          '%.3e'%(sola[i]/1.e6),\
                                          '%.3e'%(mca[i]/1.e6),\
                                          '%.3e'%(psha[i]/1.e6))
            else:
                  for i in range(na): print(\
                                          '%.3e'%(diva[i]/1.e6),\
                                          '%.3e'%(bvla[i]/1.e6),\
                                          '%.3e'%(bvuta[i]/1.e6),\
                                          '%.3e'%(bvuba[i]/1.e6),\
                                          '%.3e'%(sola[i]/1.e6),\
                                          '%.3e'%(mca[i]/1.e6),\
                                          '%.3e'%(psha[i]/1.e6))
        print('NAMEXP VCOIL NTIMES ','%.0f'%na,'  POINTS ','%.0f'%ncoils)
        for i in range(na): 
            print( '%.4f'%timea[i],end=' ')
            if int(i/10) == i/10 and i != 0: print()
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
            if ncoils == 7:
                for i in range(na): print(\
                                      '%.3e'%divva[i],\
                                      '%.3e'%bvlva[i],\
                                      '%.3e'%bvutva[i],\
                                      '%.3e'%bvubva[i],\
                                      '%.3e'%solva[i],\
                                      '%.3e'%mcva[i],\
                                      '%.3e'%pshva[i])
            if ncoils == 8:
                for i in range(na): print(\
                                      '%.3e'%divva[i],\
                                      '%.3e'%bvlva[i],\
                                      '%.3e'%bvutva[i],\
                                      '%.3e'%bvubva[i],\
                                      '%.3e'%solva[i],\
                                      '%.3e'%mcva[i],\
                                      '%.3e'%mcva[i],\
                                       '%.3e'%pshva[i])
    print( 'END')
    if tofile:    
        sys.stdout = orig_stdout
        f.close()



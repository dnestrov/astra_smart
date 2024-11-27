import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
conn = Connection('192.168.1.7:8000')
def calc_global(shotnumber,globname,RUN):
    conn.openTree('astra',shotnumber)
    TIME=0;glob=0
    dashed=False
    try:
        TIME=conn.get(RUN+':TIME')
    except:
      print('Empty run:'+str(shotnumber),RUN)
      return 0,0
    signame=RUN+'.GLOBAL:'
    if str(globname) =='X-points':
        try:
            glob=conn.get(RUN+'.P_BOUNDARY.XPOINTS:ACTIVE')
        except:
            print('Empty run or variable:'+str(shotnumber),globname,RUN)
            return 0,0
    if str(globname) == 'LIMACT' :
        try:
            glob=conn.get(RUN+'.P_BOUNDARY.LIMITER.PLASMA:ACTIVE')   
        except:
            print('Empty run or variable:'+str(shotnumber),globname,RUN)
            return 0,0
    if str(globname) == 'TAUGLOB' :
        try:
            VAR1=conn.get(RUN+'.GLOBAL:TAUE')
            VAR2=conn.get(RUN+'.GLOBAL:HGLOB')
            glob=VAR1/VAR2       
        except:
            print('Empty run or variable:'+str(shotnumber),globname,RUN)
            return 0,0
    if str(globname) =='BGEO':
        BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
        RGEO=conn.get(RUN+'.GLOBAL:RGEO')
        glob=BTOR*0.5/RGEO
    if str(globname) =='TauNE065':
        TAUE=conn.get(RUN+'.GLOBAL:TAUE')
        NEL=conn.get(RUN+'.GLOBAL:NEL')/1e19
        glob=TAUE/NEL**0.65
    if str(globname) =='Tau20':
        try:
            ABC=conn.get(RUN+'.GLOBAL:CR0')
            ELON=conn.get(RUN+'.GLOBAL:ELON')
            BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
            RGEO=conn.get(RUN+'.GLOBAL:RGEO')
            BTOR=BTOR*0.5/RGEO
            IPL=conn.get(RUN+'.GLOBAL:IPL')/1e6
            NEL=conn.get(RUN+'.GLOBAL:NEL')
            TRIL=conn.get(RUN+'.GLOBAL:TRIL')
            TRIU=conn.get(RUN+'.GLOBAL:TRIU')
            TRI=0.5*(TRIL+TRIU)
            try:
                M=conn.get(RUN+'.INPUT.CONST:AMJ')
            except: M=2
            P_OH=conn.get(RUN+'.GLOBAL:P_OH')
            P_AUX=conn.get(RUN+'.GLOBAL:P_AUX')
            P_RAD=conn.get(RUN+'.GLOBAL:P_RAD')
            P_TOT=(P_OH+P_AUX-P_RAD)/1e6
            print(np.mean(IPL),np.mean(BTOR),np.mean(NEL),np.mean(P_TOT),np.mean(RGEO),np.mean(TRI),np.mean(ELON),np.mean(ABC),np.mean(M))
            glob=0.053*IPL**0.98*BTOR**0.22*NEL**0.24*P_TOT**-0.669*RGEO**1.71
            glob=glob*(1+TRI)**0.36*ELON**0.8*(RGEO/ABC)**0.35*M**0.2
        except:
            print('Empty run or variable:'+str(shotnumber),globname,RUN)
            return 0,0
 
    if str(globname) =='H20':
        try:
            ABC=conn.get(RUN+'.GLOBAL:CR0')
            ELON=conn.get(RUN+'.GLOBAL:ELON')
            BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
            RGEO=conn.get(RUN+'.GLOBAL:RGEO')
            BTOR=BTOR*0.5/RGEO
            IPL=conn.get(RUN+'.GLOBAL:IPL')/1e6
            NEL=conn.get(RUN+'.GLOBAL:NEL')
            TRIL=conn.get(RUN+'.GLOBAL:TRIL')
            TRIU=conn.get(RUN+'.GLOBAL:TRIU')
            TRI=0.5*(TRIL+TRIU)
            TAUE=conn.get(RUN+'.GLOBAL:TAUE')
            try:
                M=conn.get(RUN+'.INPUT.CONST:AMJ')
            except: M=2
            P_OH=conn.get(RUN+'.GLOBAL:P_OH')
            P_AUX=conn.get(RUN+'.GLOBAL:P_AUX')
            P_RAD=conn.get(RUN+'.GLOBAL:P_RAD')
            P_TOT=(P_OH+P_AUX-P_RAD)/1e6
            glob=0.053*IPL**0.98*BTOR**0.22*NEL**0.24*P_TOT**-0.669*RGEO**1.71
            glob=glob*(1+TRI)**0.36*ELON**0.8*(RGEO/ABC)**0.35*M**0.2
            glob=TAUE/glob
        except:
            print('Empty run or variable:'+str(shotnumber),globname,RUN)
            return 0,0
 
    if str(globname) == 'PLH':
        ABC=conn.get(RUN+'.GLOBAL:CR0')
        ELON=conn.get(RUN+'.GLOBAL:ELON')
        BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
        RGEO=conn.get(RUN+'.GLOBAL:RGEO')
        BTOR=BTOR*0.5/RGEO
        IPL=conn.get(RUN+'.GLOBAL:IPL')/1e6
        NEL=conn.get(RUN+'.GLOBAL:NEL')/1e19
        S=(2*math.pi)**2*ABC*RGEO*np.sqrt((1+ELON**2)/2.)
        YA=RGEO/ABC
        beff=np.sqrt((BTOR*YA/(YA+1))**2+(IPL/5./ABC*(1+1/YA))**2)
        plh=0.06*(0.1*NEL)**.7*beff**0.7*S**0.9
        FACTOR=0.1*YA/(1-np.sqrt(2./(1.+YA)))
        gamma=1.0
        glob=plh*FACTOR**gamma
    if str(globname) == 'PTOT_ABS':
        P_OH=conn.get(RUN+'.GLOBAL:P_OH')
        P_AUX=conn.get(RUN+'.GLOBAL:P_AUX')
        P_RAD=conn.get(RUN+'.GLOBAL:P_RAD')
        glob=(P_OH+P_AUX-P_RAD)/1e6
    if str(globname) == 'FULLNEUT' :
        try:
            VAR1=conn.get(RUN+'.GLOBAL:BTNEUT')
            VAR2=conn.get(RUN+'.GLOBAL:BBNEUT')
            VAR3=conn.get(RUN+'.GLOBAL:DDNEUT')
            glob=VAR1+VAR2+VAR3     
        except:
            print('Empty run or variable:'+str(shotnumber),globname,RUN)
            return 0,0

    if str(globname) == 'FFAST':
        glob=conn.get(RUN+'.GLOBAL:FTHERM')
        glob=1-glob
    if str(globname) == 'FCD':
        FBS=conn.get(RUN+'.GLOBAL:F_BS')
        FNI=conn.get(RUN+'.GLOBAL:F_NI')
        glob=FBS+FNI
    if str(globname) == 'Ni0Ti0TauE':                    
        TAUE=conn.get(RUN+'.GLOBAL:TAUE')
        TI0=conn.get(RUN+'.GLOBAL:TI0')
        import read_astra_profs as readpr
        TIME,NI=readpr.read_prof(shotnumber,'NI',RUN)       
        glob=NI[:,0]*TI0/1000*TAUE*1.e19
    if str(globname) == 'Ne0Ti0TauE':
        TAUE=conn.get(RUN+'.GLOBAL:TAUE')
        TI0=conn.get(RUN+'.GLOBAL:TI0')
        NE0=conn.get(RUN+'.GLOBAL:EN0')
        glob=NI0*TI0/1000*TAUE*1.e19
    if str(globname) == 'TauE_tot':
        FTHERM=conn.get(RUN+'.GLOBAL:FTHERM')
        TAUE=conn.get(RUN+'.GLOBAL:TAUE')
        glob=TAUE/FTHERM
    if str(globname) == 'NUSTARI':
        ABC=conn.get(RUN+'.GLOBAL:CR0')
        ELON=conn.get(RUN+'.GLOBAL:ELON')
        BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
        RGEO=conn.get(RUN+'.GLOBAL:RGEO')
        BTOR=BTOR*0.5/RGEO
        IPL=conn.get(RUN+'.GLOBAL:IPL')
        NEV=conn.get(RUN+'.GLOBAL:NEV')
        ZEFAV=conn.get(RUN+'.GLOBAL:ZEFAV')
        TIV=conn.get(RUN+'.GLOBAL:TIV')
        QENG=5*ABC**2*ELON*BTOR/RGEO/IPL*1e6
        glob=0.01*NEV*0.1*QENG*RGEO*ZEFAV*np.sqrt((RGEO/ABC)**3)/TIV**2
    if str(globname) == 'NUSTARE':
        ABC=conn.get(RUN+'.GLOBAL:CR0')
        ELON=conn.get(RUN+'.GLOBAL:ELON')
        BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
        RGEO=conn.get(RUN+'.GLOBAL:RGEO')
        BTOR=BTOR*0.5/RGEO
        IPL=conn.get(RUN+'.GLOBAL:IPL')
        NEV=conn.get(RUN+'.GLOBAL:NEV')
        ZEFAV=conn.get(RUN+'.GLOBAL:ZEFAV')
        TEV=conn.get(RUN+'.GLOBAL:TEV')
        QENG=5*ABC**2*ELON*BTOR/RGEO/IPL*1e6
        glob=0.01*NEV*0.1*QENG*RGEO*ZEFAV*np.sqrt((RGEO/ABC)**3)/TEV**2

    if str(globname) == 'RHOSTAR':
        AMJ=1
        if  shot > 9700: AMJ=2
        BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
        RGEO=conn.get(RUN+'.GLOBAL:RGEO')
        BTOR=BTOR*0.5/RGEO
        ABC=conn.get(RUN+'.GLOBAL:CR0')
        TIV=conn.get(RUN+'.GLOBAL:TIV')
        glob=0.0032*np.sqrt(AMJ*TIV)/ABC/BTOR
    if str(globname) == 'BTauE':
        BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
        RGEO=conn.get(RUN+'.GLOBAL:RGEO')
        BTOR=BTOR*0.5/RGEO
        TAUE=conn.get(RUN+'.GLOBAL:TAUE')
        glob=BTOR*TAUE
    if str(globname) == 'BTauETOT':
        BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
        RGEO=conn.get(RUN+'.GLOBAL:RGEO')
        BTOR=BTOR*0.5/RGEO
        TAUE=conn.get(RUN+'.GLOBAL:TAUE')
        FTHERM=conn.get(RUN+'.GLOBAL:FTHERM')
        glob=BTOR*TAUE/FTHERM
    if str(globname) == 'IP':
        glob=conn.get(RUN+'.GLOBAL:IPL')
        dashed=True
    if str(globname) == 'RIP':
        glob=conn.get(RUN+'.GLOBAL:IPL')
        glob=glob*conn.get(RUN+'.GLOBAL:RC')
        dashed=True
    if str(globname) == 'R_IP':
        glob=conn.get(RUN+'.GLOBAL:RC')
        dashed=True
    if str(globname) == 'ZIP':
        glob=conn.get(RUN+'.GLOBAL:IPL')
        glob=glob*conn.get(RUN+'.GLOBAL:ZC')
        dashed=True
    if str(globname) == 'Z_IP':
        glob=conn.get(RUN+'.GLOBAL:ZC')
        #dashed=True
    if str(globname) == 'TEA':
        import read_astra_profs as readpr
        TIME,TE=readpr.read_prof(shotnumber,'TE',RUN)
        glob=TE[:,len(TE[0,:])-1]
    if str(globname) == 'NEA':
        import read_astra_profs as readpr
        TIME,NE=readpr.read_prof(shotnumber,'NE',RUN)
        glob=NE[:,len(NE[0,:])-1]
    if str(globname) == 'TIA':
        import read_astra_profs as readpr
        TIME,TI=readpr.read_prof(shotnumber,'TI',RUN)
        glob=TI[:,len(TI[0,:])-1]

    if dashed: 
        plt.plot(TIME,glob,linestyle='--',label=globname+'-'+str(shotnumber)+'@'+RUN)
    else:
        plt.plot(TIME,glob,label=globname+'-'+str(shotnumber)+'@'+RUN)
    return TIME,glob

def read_global(shotnumber,globname,signame0):
    conn.openTree('astra',shotnumber)
    try:
        TIME=conn.get(signame0+':TIME')
    except:
      print('Empty run:'+str(shotnumber),signame0)
      return 0,0
    signame='GLOBAL:'+str(globname)
    try:
        VAR=conn.get(signame0+'.'+signame)
    except:
      print('Empty run or variable:'+str(shotnumber),globname,signame0)
      return 0,0
    if str(globname) == 'IPL':VAR=VAR/1e6
    if str(globname) == 'NEL':VAR=VAR/1e19
    if str(globname) == 'TE0':VAR=VAR/1e3
    if str(globname) == 'TI0':VAR=VAR/1e3
    if str(globname) == 'VTOR0':VAR=VAR/1e6
    if globname[0:2] == 'P_':VAR=VAR/1e6
    if str(globname) == 'PABS':VAR=VAR/1e6
    if str(globname) == 'PBO':VAR=VAR/1e6
    if str(globname) == 'PCX':VAR=VAR/1e6
    if str(globname) == 'PNB':VAR=VAR/1e6
    if str(globname) == 'PSH':VAR=VAR/1e6
    if str(globname) == 'PTH':VAR=VAR/1e6
#    plt.suptitle(signame0+'@'+signame) 
    if str(globname) != 'gamma' :
        plt.plot(TIME,VAR,label=globname+'-'+str(shotnumber)+'@'+signame0)
        #plt.plot(TIME,VAR,label=str(shotnumber-13000000))
    else:
        plt.semilogy(TIME[0:len(VAR)],VAR,label=str(shotnumber)+'@'+signame0)
    #plt.plot.set_yscale('log')
    #plt.legend(loc='upper left',fontsize='small')
    return TIME,VAR

def read_glob(shotnumber,globname,runnum):
    conn.openTree('astra',shotnumber)
    shot=shotnumber
    signame0=str(runnum)                              
    TIME=conn.get(signame0+':TIME')
    signame='GLOBAL:'+str(globname)
    VAR=conn.get(signame0+'.'+signame)
    return TIME,VAR
def plot_globXY(shots,rang,RUN,globnameX,mdsX,globnameY,mdsY,time1,time2):
    mds=[mdsX,mdsY]
    for shot in shots:
        try:
            conn.openTree('astra',rang+shot)
        except:
            print('No '+str(rang+shot)+' shot in astra tree')
            continue
        try:
            TIME=conn.get(RUN+':TIME')
            n1,n2=get_time(TIME,time1,time2)
        except:
            print('No '+RUN+' for shot:',rang+shot)
            continue
        for count,globname in enumerate([globnameX,globnameY]):
            if mds[count]:
                signame='GLOBAL:'+str(globname)
                glob=conn.get(RUN+'.'+signame)
                if str(globname) == 'IPL':glob=glob/1e6
                if str(globname) == 'NEL':glob=glob/1e19
                if str(globname) == 'TE0':glob=glob/1e3
                if str(globname) == 'TI0':glob=glob/1e3
                if str(globname) == 'VTOR0':glob=glob/1e6
                if globname[0:2] == 'P_':glob=glob/1e6
                if str(globname) == 'PABS':VAR=VAR/1e6
                if str(globname) == 'PBO':VAR=VAR/1e6
                if str(globname) == 'PCX':VAR=VAR/1e6
                if str(globname) == 'PNB':VAR=VAR/1e6
                if str(globname) == 'PSH':VAR=VAR/1e6
                if str(globname) == 'PTH':VAR=VAR/1e6
            else:
                if str(globname) == 'FFAST':
                    glob=conn.get(RUN+'.GLOBAL:FTHERM')
                    glob=1-glob
                if str(globname) == 'FCD':
                    FBS=conn.get(RUN+'.GLOBAL:F_BS')
                    FNI=conn.get(RUN+'.GLOBAL:F_NI')
                    glob=FBS+FNI
                if str(globname) == 'Ni0Ti0TauE':                    
                    TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                    TI0=conn.get(RUN+'.GLOBAL:TI0')
                    import read_astra_profs as readpr
                    TIME,NI=readpr.read_prof(shot+rang,'NI',RUN)       
                    glob=NI[:,0]*TI0/1000*TAUE*1.e19
                if str(globname) == 'Ne0Ti0TauE':
                    TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                    TI0=conn.get(RUN+'.GLOBAL:TI0')
                    NE0=conn.get(RUN+'.GLOBAL:EN0')
                    glob=NI0*TI0/1000*TAUE*1.e19
                if str(globname) == 'TauE_tot':
                    FTHERM=conn.get(RUN+'.GLOBAL:FTHERM')
                    TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                    glob=TAUE/FTHERM
                if str(globname) == 'NUSTARI':
                    ABC=conn.get(RUN+'.GLOBAL:CR0')
                    ELON=conn.get(RUN+'.GLOBAL:ELON')
                    BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                    RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                    BTOR=BTOR*0.5/RGEO
                    IPL=conn.get(RUN+'.GLOBAL:IPL')
                    NEV=conn.get(RUN+'.GLOBAL:NEV')
                    ZEFAV=conn.get(RUN+'.GLOBAL:ZEFAV')
                    TIV=conn.get(RUN+'.GLOBAL:TIV')
                    QENG=5*ABC**2*ELON*BTOR/RGEO/IPL*1e6
                    glob=0.01*NEV*0.1*QENG*RGEO*ZEFAV*np.sqrt((RGEO/ABC)**3)/TIV**2
                if str(globname) == 'NUSTARE':
                    ABC=conn.get(RUN+'.GLOBAL:CR0')
                    ELON=conn.get(RUN+'.GLOBAL:ELON')
                    BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                    RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                    BTOR=BTOR*0.5/RGEO
                    IPL=conn.get(RUN+'.GLOBAL:IPL')
                    NEV=conn.get(RUN+'.GLOBAL:NEV')
                    ZEFAV=conn.get(RUN+'.GLOBAL:ZEFAV')
                    TEV=conn.get(RUN+'.GLOBAL:TEV')
                    QENG=5*ABC**2*ELON*BTOR/RGEO/IPL*1e6
                    glob=0.01*NEV*0.1*QENG*RGEO*ZEFAV*np.sqrt((RGEO/ABC)**3)/TEV**2
                if str(globname) == 'RHOSTAR':
                    AMJ=1
                    if  shot > 9700: AMJ=2
                    BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                    RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                    BTOR=BTOR*0.5/RGEO
                    ABC=conn.get(RUN+'.GLOBAL:CR0')
                    TIV=conn.get(RUN+'.GLOBAL:TIV')
                    glob=0.0032*np.sqrt(AMJ*TIV)/ABC/BTOR
                if str(globname) == 'BTauE':
                    BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                    RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                    BTOR=BTOR*0.5/RGEO
                    TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                    glob=BTOR*TAUE
                if str(globname) == 'BTauETOT':
                    BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                    RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                    BTOR=BTOR*0.5/RGEO
                    TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                    FTHERM=conn.get(RUN+'.GLOBAL:FTHERM')
                    glob=BTOR*TAUE/FTHERM
                    
            print(rang+shot,globname,np.mean(glob[n1:n2]))
            if globname == globnameX: globX=np.mean(glob[n1:n2])
            if globname == globnameY: globY=np.mean(glob[n1:n2])
                
        plt.annotate(shot,(globX,globY),xytext=(globX,globY))
        if shot == shots[0]:
            plt.plot(globX,globY,'bx',label='ASTRA@'+RUN)
        else:
            plt.plot(globX,globY,'bx')
def get_glob(shots,rang,RUN,globname,mds,time1,time2):
    var=np.array([])
    for shot in shots:
        ok=True
        try:
            conn.openTree('astra',rang+shot)
        except:
            print('No '+str(rang+shot)+' shot in astra tree')
            ok=False
            var=np.append(var,0)
            continue
        try:
            TIME=conn.get(RUN+':TIME')
            n1,n2=get_time(TIME,time1,time2)
            ok=True
        except:
            print('No '+RUN+' for shot:',rang+shot)
            var=np.append(var,0)
            ok=False
            continue
        if mds:
            signame='GLOBAL:'+str(globname)
            glob=conn.get(RUN+'.'+signame)
            if str(globname) == 'IPL':glob=glob/1e6
            if str(globname) == 'NEL':glob=glob/1e19
            if str(globname) == 'TE0':glob=glob/1e3
            if str(globname) == 'TI0':glob=glob/1e3
            if str(globname) == 'VTOR0':glob=glob/1e3
            if globname[0:1] == 'P':glob=glob/1e6
        else:
            signame=RUN+'.'+'GLOBAL:'
            if str(globname) == 'TAUGLOB' :
                VAR1=conn.get(RUN+'.GLOBAL:TAUE')
                VAR2=conn.get(RUN+'.GLOBAL:HGLOB')
                glob=VAR1/VAR2       
            if str(globname) == 'FULLNEUT' :
                VAR1=conn.get(RUN+'.GLOBAL:BTNEUT')
                VAR2=conn.get(RUN+'.GLOBAL:BBNEUT')
                VAR3=conn.get(RUN+'.GLOBAL:DDNEUT')
                glob=VAR1+VAR2+VAR3     
            if str(globname) =='TauNE065':
                TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                NEL=conn.get(RUN+'.GLOBAL:NEL')/1e19
                glob=TAUE/NEL**0.65
            if str(globname) =='BGEO':
                BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                glob=BTOR*0.5/RGEO
            if str(globname) =='Tau20':
                try:
                    ABC=conn.get(RUN+'.GLOBAL:CR0')
                    ELON=conn.get(RUN+'.GLOBAL:ELON')
                    BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                    RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                    BTOR=BTOR*0.5/RGEO
                    IPL=conn.get(RUN+'.GLOBAL:IPL')/1e6
                    NEL=conn.get(RUN+'.GLOBAL:NEL')/1e19
                    TRIL=conn.get(RUN+'.GLOBAL:TRIL')
                    TRIU=conn.get(RUN+'.GLOBAL:TRIU')
                    TRI=0.5*(TRIL+TRIU)
                    try:
                        M=conn.get(RUN+'.INPUT.CONST:AMJ')
                    except: M=2
                    P_OH=conn.get(RUN+'.GLOBAL:P_OH')
                    P_AUX=conn.get(RUN+'.GLOBAL:P_AUX')
                    P_RAD=conn.get(RUN+'.GLOBAL:P_RAD')
                    P_TOT=(P_OH+P_AUX-P_RAD)/1e6
                    print(np.mean(IPL),np.mean(BTOR),np.mean(NEL),np.mean(P_TOT),np.mean(RGEO),np.mean(TRI),np.mean(ELON),np.mean(ABC),np.mean(M))
                    glob=0.053*IPL**0.98*BTOR**0.22*NEL**0.24*P_TOT**-0.669*RGEO**1.71
                    glob=glob*(1+TRI)**0.36*ELON**0.8*(RGEO/ABC)**0.35*M**0.2
                except:
                    print('Empty run or variable:'+str(shotnumber),globname,RUN)
 

            if str(globname) =='H20':
                try:
                    ABC=conn.get(RUN+'.GLOBAL:CR0')
                    ELON=conn.get(RUN+'.GLOBAL:ELON')
                    BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                    RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                    BTOR=BTOR*0.5/RGEO
                    IPL=conn.get(RUN+'.GLOBAL:IPL')/1e6
                    NEL=conn.get(RUN+'.GLOBAL:NEL')/1e19
                    TRIL=conn.get(RUN+'.GLOBAL:TRIL')
                    TRIU=conn.get(RUN+'.GLOBAL:TRIU')
                    TRI=0.5*(TRIL+TRIU)
                    TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                    try:
                        M=conn.get(RUN+'.INPUT.CONST:AMJ')
                    except: M=2
                    P_OH=conn.get(RUN+'.GLOBAL:P_OH')
                    P_AUX=conn.get(RUN+'.GLOBAL:P_AUX')
                    P_RAD=conn.get(RUN+'.GLOBAL:P_RAD')
                    P_TOT=(P_OH+P_AUX-P_RAD)/1e6
                    glob=0.053*IPL**0.98*BTOR**0.22*NEL**0.24*P_TOT**-0.669*RGEO**1.71
                    glob=glob*(1+TRI)**0.36*ELON**0.8*(RGEO/ABC)**0.35*M**0.2
                    glob=TAUE/glob
                except:
                    print('Empty run or variable:'+str(shotnumber),globname,RUN) 
            if str(globname) == 'PLH':
                    ABC=conn.get(RUN+'.GLOBAL:CR0')
                    ELON=conn.get(RUN+'.GLOBAL:ELON')
                    BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                    RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                    BTOR=BTOR*0.5/RGEO
                    IPL=conn.get(RUN+'.GLOBAL:IPL')/1e6
                    NEL=conn.get(RUN+'.GLOBAL:NEL')/1e19
                    S=(2*math.pi)**2*ABC*RGEO*np.sqrt((1+ELON**2)/2.)
                    YA=RGEO/ABC
                    beff=np.sqrt((BTOR*YA/(YA+1))**2+(IPL/5./ABC*(1+1/YA))**2)
                    plh=0.06*(0.1*NEL)**.7*beff**0.7*S**0.9
                    FACTOR=0.1*YA/(1-np.sqrt(2./(1.+YA)))
                    gamma=1.0
                    glob=plh*FACTOR**gamma
            if str(globname) == 'PTOT_ABS':
                P_OH=conn.get(RUN+'.GLOBAL:P_OH')
                P_AUX=conn.get(RUN+'.GLOBAL:P_AUX')
                P_RAD=conn.get(RUN+'.GLOBAL:P_RAD')
                glob=(P_OH+P_AUX-P_RAD)/1e6
            if str(globname) == 'SH_AS':
                glob=conn.get(RUN+'.GLOBAL:RMAG')
                glob=glob-conn.get(RUN+'.GLOBAL:RGEO')
            if str(globname) == 'FFAST':
                glob=conn.get(RUN+'.GLOBAL:FTHERM')
                glob=1-glob
            if str(globname) == 'FCD':
                FBS=conn.get(RUN+'.GLOBAL:F_BS')
                FNI=conn.get(RUN+'.GLOBAL:F_NI')
                glob=FBS+FNI
            if str(globname) == 'Ni0Ti0TauE':                    
                TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                TI0=conn.get(RUN+'.GLOBAL:TI0')
                import read_astra_profs as readpr
                TIME,NI=readpr.read_prof(shot+rang,'NI',RUN)       
                glob=NI[:,0]*TI0/1000*TAUE*1.e19
            if str(globname) == 'Ne0Ti0TauE':
                TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                TI0=conn.get(RUN+'.GLOBAL:TI0')
                NE0=conn.get(RUN+'.GLOBAL:EN0')
                glob=NI0*TI0/1000*TAUE*1.e19
            if str(globname) == 'TauE_tot':
                FTHERM=conn.get(RUN+'.GLOBAL:FTHERM')
                TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                glob=TAUE/FTHERM
            if str(globname) == 'NUSTARI':
                ABC=conn.get(RUN+'.GLOBAL:CR0')
                ELON=conn.get(RUN+'.GLOBAL:ELON')
                BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                BTOR=BTOR*0.5/RGEO
                IPL=conn.get(RUN+'.GLOBAL:IPL')
                NEV=conn.get(RUN+'.GLOBAL:NEV')
                ZEFAV=conn.get(RUN+'.GLOBAL:ZEFAV')
                TIV=conn.get(RUN+'.GLOBAL:TIV')
                QENG=5*ABC**2*ELON*BTOR/RGEO/IPL*1e6
                glob=0.01*NEV*0.1*QENG*RGEO*ZEFAV*np.sqrt((RGEO/ABC)**3)/TIV**2
            if str(globname) == 'NUSTARE':
                ABC=conn.get(RUN+'.GLOBAL:CR0')
                ELON=conn.get(RUN+'.GLOBAL:ELON')
                BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                BTOR=BTOR*0.5/RGEO
                IPL=conn.get(RUN+'.GLOBAL:IPL')
                NEV=conn.get(RUN+'.GLOBAL:NEV')
                ZEFAV=conn.get(RUN+'.GLOBAL:ZEFAV')
                TEV=conn.get(RUN+'.GLOBAL:TEV')
                QENG=5*ABC**2*ELON*BTOR/RGEO/IPL*1e6
                glob=0.01*NEV*0.1*QENG*RGEO*ZEFAV*np.sqrt((RGEO/ABC)**3)/TEV**2
            if str(globname) == 'RHOSTAR':
                AMJ=1
                if  shot > 9700: AMJ=2
                BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                BTOR=BTOR*0.5/RGEO
                ABC=conn.get(RUN+'.GLOBAL:CR0')
                TIV=conn.get(RUN+'.GLOBAL:TIV')
                glob=0.0032*np.sqrt(AMJ*TIV)/ABC/BTOR
            if str(globname) == 'BTauE':
                BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                BTOR=BTOR*0.5/RGEO
                TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                glob=BTOR*TAUE
            if str(globname) == 'BTauETOT':
                BTOR=conn.get(RUN+'.GLOBAL:BTVAC')
                RGEO=conn.get(RUN+'.GLOBAL:RGEO')
                BTOR=BTOR*0.5/RGEO
                TAUE=conn.get(RUN+'.GLOBAL:TAUE')
                FTHERM=conn.get(RUN+'.GLOBAL:FTHERM')
                glob=BTOR*TAUE/FTHERM
                    
        print(rang+shot,globname,np.mean(glob[n1:n2]))
        var=np.append(var,np.mean(glob[n1:n2]))
    return var
def get_time(TIME,time1,time2):
        ind=np.where((TIME-time1)*(TIME-time2) <= 0)
        try:
            n1=np.array(ind).astype(int)[0,0] 
            n2=np.array(ind).astype(int)[0,len(ind[0])-1]
        except:
            n1=0
            n2=0
        return n1,n2




# Script for creating the model tree for ST40 EQUIL tree
# Alexei -- 07/2019
# Peter Buxton -- added username and checks before deleting -- Feb / 2021
# Peter Buxton -- added  copy_runs and warning_message  -- Feb / 2021
#/home/alexei.dnestrovskij/mdsplus/DB_nodes/Python_Scripts
from MDSplus import *
from numpy import *
import numpy as np
import mdsHelpers as mh
from imp import reload
reload(mh)
import getpass
user = getpass.getuser()
MDSplus_IP_address = '192.168.1.7:8000'  # smaug IP address
CONSTRAINTS=[
"FLUX","Poloidal flux in loops, Wb ",
"BP","Poloidal field in probes, T",
"PFC_DOF","Current in coils, A",
"ROGC","Current in Rogowski coils, A",
"ULOOP","Voltage in loops, V",
"DF","Diamagnetic flux, Wb",
"IP","Plasma current, A",
"PRESSURE","Pressure, Pa"]
GLOBAL=[
"IPL ","Plasma current,        MA",
"BTVAC","BT_vacuum at R=0.5m, T",
"DF  ","simulated diamagnetic flux,  Wb",
"CR0 ","MINOR RAD=(Rmax-Rmin)/2, m",
"RGEO","MAJOR R = (Rmax+Rmin)/2, m",
"ZGEO","Geom vertical position, m ",
"RC","Current density center R_IP, m ",
"ZC","Current density center Z_IP, m ",
"ELON","ELONGATION BOUNDARY     ",
"TRIL","LOWER TRIANGULARITY     ",
"TRIU","UPPER TRIANGULARITY     ",
"SQL","LOWER SQUARENESS         ",
"SQU","UPPER SQUARENESS         ",
"SQ","SQUARENESS         ",
"QWL ","Q(PSI) AT the LCFS      ",
"Q95 ","Q(PSI) AT 95% of full poloidal flux inside LCFS",
"TE0 ","Central electron temp, keV",
"TI0 ","Central ion temp, keV",
"NE0 ","Central electron density, 10E19m^-3 ",
"NEL ","Line aver electron density 10E19m^-3 ",
"NEV ","Volume aver electron density 10E19m^-3 ",
"TEV ","Volume aver electron temp, keV",
"TIV ","Volume aver ion temp, keV",
"TAUE","Energy confinement time, s ",
"P_OH","Total Ohmic power, W",
"IEXC","Ion-electron exchange power, W",
"UPL ","Loop Voltage,V          ",
"WTH ","Total energy, J       ",
"LI1","Normalised internal inductance, li(1)",
"LI2","Normalised internal inductance, li(2)",
"LI3","Normalised internal inductance, li(3)",
"BETAP1","Poloidal beta, betaP(1)",
"BETAP2","Poloidal beta, betaP(2)",
"BETAP3","Poloidal beta, betaP(3)",
"BetT","Toroidal beta           ",
"BetN","Beta normalized  ",
"Hoh","Neo-alcator H-factor",
"H98","ITER IPB(y,2) H-factor",
"HNSTX","NSTX scaling H-factor",
"HPB","Peter Buxton H-factor",
"HGLOB","Globus-M2 FEC2020 H-factor",
"HLMOD","L-mode scaling P.Yushmanov et al.NF(1990)1999 H-factor",
"ZEFF","Z effective at the plasma center",
"Res","Total plasma resistance Qj/Ipl^2, Ohm",
"Rmag","Magnetic axis hor position, m",
"Zmag","Magnetic axis vert position, m",
"Vol","Plasma volume, m^3",
"ROC","Effective plasma radius, m",
"P_NBI_E","Total power from NBI to electrons, W",
"P_NBI_I","Total power from NBI to ions, W",
"P_RF","Total RF power to electrons,W",
"I_BS","Total bootstrap current,MA",
"F_BS","Bootstrap current fraction",
"I_NBI","Total NB driven current,MA",
"NBI_NAMES","NBI names, RFX,HNBI1=00,01,10,11",
"I_RF","Total RF driven current,MA",
"I_OH","Total Ohmic current,MA",
"F_NI","Non-inductive current fraction",
"P_FUS_THERM","Thermal fusion power,W",
"P_FUS_TOT","Total fusion power: thermal+NBI,W",
"P_AUX","Total external heating power,W",
"Q_FUS","Fusion energy gain",
"P_TOT_E","Total alpha power to electrons,W",
"P_TOT_I","Total alpha power to ions,W",
"I_ICR","Total ICR driven current,MA",
"FBND","boundary poloidal flux,Wb",
"FAXS","axis poloidal flux,Wb",
"QE","electron power flux through LCFS, W",
"QI","ion power flux through LCFS, W",
"QN","electron flux through LCFS, 10^19/s",
"STOT","Total electron source, 10^19/s",
"SPEL","Pellet electron source, 10^19/s",
"SWALL","Boundary electron source, 10^19/s",
"SBM","Neutral beam electron source, 10^19/s",
"NNCL","Wall cold neutral density, 10^19/m^3",
"NCXN0","Halo neutrals on axis, 10^19/m3",
"TAUP","Particle confinement time ,s",
"GAMMA","KINX growth rate, 1/s",
"VTOR0","Central toroidal velocity, m/s",
"TORQ","Total torque from NB, N*m",
"TORQ_BE","Collisional to electron torque from NB, N*m",
"TORQ_BI","Collisional to ions torque from NB, N*m",
"TORQ_BTH","Beam thermalisation torquefrom NB, N*m",
"TORQ_JXB","JXB torque from NB, N*m",
"TORQ_BCX","CX losses torque from NB, N*m",
"TAU_PHI","Momentum confinement time, s",
"TOTNEUT","total neutrons from as_nubeam_neutot_out, 1/s",
"BTNEUT","beam-target neutrons from as_nubeam_neutot_out, 1/s",
"BBNEUT","beam-beam neutrons from as_nubeam_neutot_out, 1/s",
"DDNEUT","plasma-plasma DD neutron flux, 1/s",
"DTNEUT"," neutron rate from D-T reaction in plasma, 1/s",
"INTNEUT","time integrated neutron yield, -",
"Ftherm","Thermal energy fraction, -",
"P_RAD","Radiated power, W",
"Pabs"," Absorbed power, W",
"Pnb"," Injected beam power, W",
"Pth"," Beam power thermalising into plasma, W",
"dPdt"," dW_fast/dt, W",
"Pbo"," Bad orbit loss power, W",
"Psh"," Shine through power loss, W",
"Pcx"," Charge exchange loss, W",
"ERFX","RFX:beam energy, kV",
"FULLRFX","RFX:fraction of beam current at full energy, -",
"HALFRFX","RFX:fraction of beam current at half energy, -",
"EHNBI","HNBI:beam energy, kV",
"FULLHNBI","HNBI:fraction of beam current at full energy, -",
"HALFHNBI","HNBI:fraction of beam current at half energy, -",
"Q0","central q, -",
"NFASTV","Volume averaged fast ion density from NUBEAM, 10^19/m^3",
"ZEFAV","Volume averaged effective charge, -",
"NIZ1AV","Volume averaged impurity 1 density, 10^19/m^3",
"NIZ2AV","Volume averaged impurity 2 density, 10^19/m^3",
"NIZ3AV","Volume averaged impurity 3 density, 10^19/m^3",
"HQ1","HQ1 vertical position of q=1 surface relative to midplane, m",
"BgBFACTORe","BgB model factor for electron heat conductivity,-",
"BgBFACTORi","BgB model factor for ion heat conductivity,-",
"Wtherm","Plasma thermal energy,J",
"Wfast","Fast particle energy,J",
"P_ICR"," ICR power to ions,W",
"BANGLE","Angle of magnetic field line to toroidal direction (grad(phi)), Degree"]
PROFILES=[
"RHO","rho - toroidal flux coordinate, m",    
"TE","Electron temperature, keV",    
"NE","Electron density, 10^19 m^-3",    
"NI","Main ion density, 10^19 m^-3",    
"TI","Ion temperature, keV",    
"ZEFF","Effective ion charge",
"QNBE","Beam power density to electrons, MW/m3",
"QNBI","Beam power density to ions, MW/m3",
"Q_OH","Ohmic heating power profile, MW/m3",
"Q_EI","Electron-ion heat exchange due to Coulomb collisions, MW/m3",
"STOT","Total electron source,10^19/s/m3",
"CHI_E","Total electron heat conductivity, m^2/s",
"CHI_I","Total ion heat conductivity, m^2/s",
"CHI_E_ANOM","anomalous electron heat conductivity, m^2/s",
"CHI_I_ANOM","anomalous ion heat conductivity, m^2/s",
"CHI_E_NEO","neoclassical electron heat conductivity, m^2/s",
"CHI_I_NEO","neoclassical ion heat conductivity, m^2/s",
"DIFF","diffusion coefficient, m^2/s",
"DIFF_ANOM","anomalous diffusion coefficient, m^2/s",
"QE","electron power flux, MW",
"QI","ion power flux, MW",
"QN","total electron flux, 10^19/s",
"PEGN","electron convective heat flux, MW",
"PIGN","ion convective heat flux, MW",
"CC","Parallel current conductivity, 1/(Ohm*m)",
"ELON","Elongation profile",
"TRI","Triangularity (up/down symmetrized) profile",
"RMID","Centre of flux surfaces, m",
"RMINOR","minor radius, m",
"N_D","Deuterium density,10E19/m3",
"N_T","Tritium density	,10E19/m3",
"T_D","Deuterium temperature,keV",
"T_T","Tritium temperature,keV",
"Q_RF","RF power density to electron,MW/m3",
"Q_ALPHA_E","Alpha power density to electrons,MW/m3",
"Q_ALPHA_I","Alpha power density to ions,MW/m3",
"J_NBI","NB driven current density,MA/m2",
"J_RF"," EC driven current density,MA/m2",
"J_BS","Bootstrap current density,MA/m2",
"J_OH","Ohmic current density,MA/m2",
"J_TOT","Total current density,MA/m2",
"Q_ICR","ICRH power density to ions,MW/m3",
"J_ICR","ICR current density,MA/m2", 
"PSIN","Normalized poloidal flux -",
"SBM","Particle source from beam, 10^19/m^3/s ",
"SPEL","Particle source from pellets, 10^19/m^3/s",
"SWALL","Particle source from wall neutrals, 10^19/m^3/s",
"OMEGA_TOR","Toroidal rotation frequency, 1/s",
"TORQ_DEN","Total torque density from NB, N*m/m3",
"TORQ_DEN_BE","Collisional to electron torque density from NB, N*m/m3",
"TORQ_DEN_BI","Collisional to ions torque density from NB, N*m/m3",
"TORQ_DEN_BTH","Beam thermalisation torque density from NB, N*m/m3",
"TORQ_DEN_JXB","JXB torque density from NB, N*m/m3",
"TORQ_DEN_BCX","CX losses torque density from NB, N*m/m3",
"CHI_PHI","Momentum transport coefficient, m2/s",
"QRAD","Radiated power density, MW/m3",
"NF","Fast ion density profile from NUBEAM, 10^19/m^3",
"NIZ1","Impurity 1 density profile, 10^19/m^3",
"NIZ2","Impurity 2 density profile, 10^19/m^3",
"NIZ3","Impurity 3 density profile, 10^19/m^3",
"ZIM1","Impurity 1 mean charge profile, ",
"ZIM2","Impurity 2 mean charge profile, ",
"ZIM3","Impurity 3 mean charge profile, ",
"DAN_IMP1","Impurity 1 anomalous diffusion profile, m^2/s",
"DAN_IMP2","Impurity 2 anomalous diffusion profile, m^2/s",
"DAN_IMP3","Impurity 3 anomalous diffusion profile, m^2/s",
"VAN_IMP1","Impurity 1 anomalous convection velocity profile, m/s",
"VAN_IMP2","Impurity 2 anomalous convection velocity profile, m/s",
"VAN_IMP3","Impurity 3 anomalous convection velocity profile, m/s",
"DNEO_IMP1","Impurity 1 neoclassical diffusion profile, m^2/s",
"DNEO_IMP2","Impurity 2 neoclassical diffusion profile, m^2/s",
"DNEO_IMP3","Impurity 3 neoclassical diffusion profile, m^2/s",
"VNEO_IMP1","Impurity 1 anomalous convection velocity profile, m/s",
"VNEO_IMP2","Impurity 2 anomalous convection velocity profile, m/s",
"VNEO_IMP3","Impurity 3 anomalous convection velocity profile, m/s",
"PBLON","Parallel pressure, Pa",
"PBPER","Perpendicular pressure, Pa",
"WF","Fast particle energy profile,MJ/m3",
"VAN","Pinch velocity,m/s",
"DNEO","Neoclassical diffusivity,m^2/s",
"VNEO","Neoclassical pinch,m/s",
"VR","dVolume/dRHO, m^2",
"PSI","Poloidal flux on ASTRA mesh, Wb",
"NN"," Neutral density, 10^19/m3",
"NCXN"," Hqlo neutral density, 10^19/m3",
"UPL"," Loop voltage, V",
"SURF","Flux surface area,m^2",
"VOL","Flux surface  volume,m^3"]

def tree(t,run,descriptions,tree):
    if tree == 'ASTRA':
        t.deleteNode(run)
        t.setDefault( mh.createNode(t,run,"STRUCTURE",descriptions[0]) )
        node = t.getDefault()
        ok=True
    if tree == 'SOPHIA':
        print(run)
        t.setDefault(run) 
        try:
            print('01')
            print(t.getNode('ASTRA'))
            t.setDefault(t.getNode('ASTRA'))
            print('02')
            ok=False
            return ok
        except:
            print('03')
            t.setDefault( mh.createNode(t,"ASTRA", "STRUCTURE",descriptions[0]))
            ok=True
        node = t.getDefault()
    t.addNode("CODE_VERSION", "STRUCTURE")
    n = t.addNode("CODE_VERSION:USER", "TEXT")
    n.putData(user)
    n= mh.createNode(t,"TIME","NUMERIC",  "time vector");
    n= mh.createNode(t,"DATE","TEXT",  "Date and time of calculation");

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"INPUT","STRUCTURE","Input parameters") )
    defaultNode = t.getDefault();
    n= mh.createNode(t,"CODE_FILES","NUMERIC",  "astra run zipped files");
    t.setDefault( mh.createNode(t,"CONST","STRUCTURE","global parameters") )
    n = mh.createNode(t,"AIM1","NUMERIC","Impurity 1 ions atom mass/Mp");    
    n = mh.createNode(t,"AIM2","NUMERIC","Impurity 2 ions atom mass/Mp");    
    n = mh.createNode(t,"AIM3","NUMERIC","Impurity 3 ions atom mass/Mp");    
    n = mh.createNode(t,"ZNUM1","NUMERIC","Impurity 1 atomic number");    
    n = mh.createNode(t,"ZNUM2","NUMERIC","Impurity 2 atomic number");    
    n = mh.createNode(t,"ZNUM3","NUMERIC","Impurity 3 atomic number");    
    n = mh.createNode(t,"AMJ","NUMERIC","Main ions atom mass/Mp");    
    n = mh.createNode(t,"ZMJ","NUMERIC","Main ion charge");    

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"GLOBAL","STRUCTURE","Global parameters") )  
    for i in range(int(len(GLOBAL)/2)):
        #print(GLOBAL[2*i]+','+GLOBAL[2*i+1])
        n = mh.createNode(t,GLOBAL[2*i],"SIGNAL",GLOBAL[2*i+1]); 

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"BPPROBE","STRUCTURE","probe signals"))
    t.setDefault( mh.createNode(t,"ALL","STRUCTURE","all in one"))
    n = mh.createNode(t,"B","SIGNAL","Poloidal magnetic field, T");    
    n = mh.createNode(t,"R","NUMERIC","R position, M");    
    n = mh.createNode(t,"Z","NUMERIC","Z position, M");    
    n = mh.createNode(t,"ANGLE","NUMERIC","Angle, rad");    
    n = mh.createNode(t,"NAME","TEXT","Probe name");    

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"FLOOP","STRUCTURE","probe signals"))
    t.setDefault( mh.createNode(t,"ALL","STRUCTURE","all in one"))
    n = mh.createNode(t,"PSI","SIGNAL","Poloidal magnetic field, Wb");    
    n = mh.createNode(t,"V","SIGNAL","Loop voltage, V");    
    n = mh.createNode(t,"R","NUMERIC","R position, M");    
    n = mh.createNode(t,"Z","NUMERIC","Z position, M");    
    n = mh.createNode(t,"NAME","TEXT","Probe name");    

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"PASSIVES","STRUCTURE","PASSIVE FILAMENTS"))
    n = mh.createNode(t,"INDEX","NUMERIC","x vector(i) = i");       
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"RP","NUMERIC","R filament position, M");    
    n = mh.createNode(t,"ZP","NUMERIC","Z filament position, M");    
    n = mh.createNode(t,"DR","NUMERIC","DR for filament, M");    
    n = mh.createNode(t,"DZ","NUMERIC","DZ for filament, M");    
    n = mh.createNode(t,"RESP","NUMERIC","filament resistance, Ohm");    
    n = mh.createNode(t,"NAME","TEXT","filament name"); 
   
    t.setDefault(node)
    t.setDefault( mh.createNode(t,"CONSTRAINTS","STRUCTURE","") )
    C=t.getDefault()
    
    for i in range(int(len(CONSTRAINTS)/2)):
        t.setDefault(mh.createNode(t,CONSTRAINTS[2*i],"STRUCTURE",CONSTRAINTS[2*i+1])) 
        n = mh.createNode(t,"CVALUE","SIGNAL","simulated");    
        n = mh.createNode(t,"MVALUE","SIGNAL","experimental");    
        n = mh.createNode(t,"WEIGHT","SIGNAL","");    
        n = mh.createNode(t,"NAME","TEXT","");    
        t.setDefault(C)

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"PSI2D","STRUCTURE","2D psi") )    
    n = mh.createNode(t,"RGRID","NUMERIC","Major radius coordinate m");    
    n = mh.createNode(t,"ZGRID","NUMERIC","Vertical coordinate m");    
    n = mh.createNode(t,"PSI","SIGNAL","Poloidal flux W");    

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"COILS","STRUCTURE","PF coils") )
    n = mh.createNode(t,"R","NUMERIC","R, m");      
    n = mh.createNode(t,"Z","NUMERIC","Z, m");      
    n = mh.createNode(t,"DR","NUMERIC","DR, m");      
    n = mh.createNode(t,"DZ","NUMERIC","DZ, m");      
    n = mh.createNode(t,"TURNS","NUMERIC","Number of turns per coil");      
    n = mh.createNode(t,"PF_NAMES","TEXT","PF coils name")
    t.setDefault( mh.createNode(t,"PSU2PF","STRUCTURE","PSU connections") )
    n = mh.createNode(t,"PSU_NAMES","TEXT","PSU name")
    n = mh.createNode(t,"I","SIGNAL","PSU currents, A");      
    n = mh.createNode(t,"V","SIGNAL","Voltage, V");      
    n = mh.createNode(t,"PSU2PF_TABLE","NUMERIC","Connection MATRIX: coil number x psu number");

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"PROFILES","STRUCTURE","Profiles") )
    P=t.getDefault()
    t.setDefault( mh.createNode(t,"PSI_NORM","STRUCTURE","Profiles on flux surfaces") )    
    n = mh.createNode(t,"XPSN","NUMERIC","x vector -sqrt(fi_normalized)");
    n = mh.createNode(t,"Q","SIGNAL","Q_PROFILE(PSI_NORM)");
    n = mh.createNode(t,"P","SIGNAL","PRESSURE(PSI_NORM)");
    n = mh.createNode(t,"PSI","SIGNAL","PSI");
    n = mh.createNode(t,"PPRIME","SIGNAL","PPRIME");
    n = mh.createNode(t,"FFPRIME","SIGNAL","FFPRIME");
    n = mh.createNode(t,"FTOR","SIGNAL","Toroidal flux, Wb");
    n = mh.createNode(t,"SIGMAPAR","SIGNAL","Parallel conductivity,1/(Ohm*m)");
    n = mh.createNode(t,"AREAT","SIGNAL","Toroidal cross section,m2");
    n = mh.createNode(t,"VOLUME","SIGNAL","Volume inside magnetic surface,m3");
    n = mh.createNode(t,"FPOL","SIGNAL","Poloidal current function, m*T");

    t.setDefault(P)
    t.setDefault(mh.createNode(t,"ASTRA","STRUCTURE","Profiles from ASTRA"))  
    for i in range(int(len(PROFILES)/2)):
         n = mh.createNode(t,PROFILES[2*i],"SIGNAL",PROFILES[2*i+1]); 

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"P_BOUNDARY","STRUCTURE","R,Z for LCFS") )
    BND=t.getDefault()
    n = mh.createNode(t,"INDEX","NUMERIC","");    
    n = mh.createNode(t,"RBND","SIGNAL","R OF PLASMA_BOUNDARY");    
    n = mh.createNode(t,"ZBND","SIGNAL","Z OF PLASMA_BOUNDARY");  
  
    t.setDefault( mh.createNode(t,"XPOINTS","STRUCTURE","separatrix data") )    
    n = mh.createNode(t,"FXP1","SIGNAL","x-point 1 poloidal flux, Wb");    
    n = mh.createNode(t,"FXP2","SIGNAL","x-point 2 poloidal flux, Wb");    
    n = mh.createNode(t,"RXP1","SIGNAL","x-point 1 r-position,m");    
    n = mh.createNode(t,"ZXP1","SIGNAL","x-point 1 z-position,m");    
    n = mh.createNode(t,"RXP2","SIGNAL","x-point 2 r-position,m");    
    n = mh.createNode(t,"ZXP2","SIGNAL","x-point 2 z-position,m");    
    n = mh.createNode(t,"ACTIVE","SIGNAL","main x-point index (1 or 2) ");    

    t.setDefault(BND)
    t.setDefault( mh.createNode(t,"LIMITER","STRUCTURE","limiter data") )    
    LIM=t.getDefault()
    t.setDefault( mh.createNode(t,"VESSEL","STRUCTURE","hard limiter data") )    
    n = mh.createNode(t,"INDEX","NUMERIC","");    
    n = mh.createNode(t,"R","NUMERIC","r-position,m");    
    n = mh.createNode(t,"Z","NUMERIC","z-position,m");    

    t.setDefault(LIM)
    t.setDefault( mh.createNode(t,"PLASMA","STRUCTURE","plasma-limiter point") )    
    n = mh.createNode(t,"ACTIVE","SIGNAL","=1 if limiter");    
    n = mh.createNode(t,"FBND","SIGNAL","Limiter poloidal flux, Wb");    
    n = mh.createNode(t,"R","SIGNAL","r-position,m");    
    n = mh.createNode(t,"Z","SIGNAL","z-position,m");    

    t.setDefault(BND)
    t.setDefault( mh.createNode(t,"TARGETS","STRUCTURE","Target geometric parameters") )    
    n = mh.createNode(t,"RTORX","SIGNAL","Geometric axis r-position from ASTRA exp file,m");    
    n = mh.createNode(t,"ZX","SIGNAL","Geometric axis z-position from ASTRA exp file,m");    
    n = mh.createNode(t,"ELONGX","SIGNAL","Elongation from ASTRA exp file");    
    n = mh.createNode(t,"TRIANX","SIGNAL","Triangularity from ASTRA exp file");    
    n = mh.createNode(t,"ABCX","SIGNAL","Minor radius at midplane from ASTRA exp file,m");    

#DIVPSRB,DIVPSRT,HFSPSRB,HFSPSRT,MCB,MCT,GASBFLB,GASBFLT,BVLB,BVLT,DIVB,DIVT,INIVC000
    t.setDefault(node)
    t.setDefault( mh.createNode(t,"ROG","STRUCTURE","Rogowski loops") )
    t.setDefault( mh.createNode(t,"ALL","STRUCTURE","Rogowski loops") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    n = mh.createNode(t,"NAME","TEXT","Rogowski name array");    
    return ok


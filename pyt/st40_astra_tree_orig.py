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

## look at /home/ops/mds_trees/ for inspiration
def delete(pulseNo, node):
    t = Tree('ASTRA', pulseNo, 'edit')

    # get the username of who wrote this run
    try:
        n = t.getNode(r'\ASTRA::TOP.' + node + '.CODE_VERSION:USER')
        user_already_written = n.data()
    except:
        user_already_written = user

    # First warning if you are going to delete someone else' run
    if not(user_already_written==user):
        print('#####################################################')
        print('#  *** WARNING ***                                  #')
        print("#  You are about to delete a different user's run!  #")
        nspaces = 49 - len(user_already_written)
        spaces = ' '*nspaces
        print('#  ' + user_already_written + spaces + '#')
        print('#####################################################')

        print(' Proceed yes/no?')
        yes_typed = input(">>  ")
        if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
            return
        while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
            print(' Error try again')
            yes_typed = input(">>  ")

        print(' To confirm type in: "' + user_already_written + '"')
        user_typed = input(">>  ")
        while not(user_already_written==user_typed):
            print(' Error try again')
            user_typed = input(">>  ")
        print(' ')

    # Second warning to confirm delete
    print('#####################################################')
    print('#  *** WARNING ***                                  #')
    print('#  You are about to delete data                     #')
    nspaces = 49 - len(user_already_written)
    spaces = ' '*nspaces
    print('#  ' + node + spaces + '#')
    print('#####################################################')
    print(' Proceed yes/no?')
#    yes_typed='yes'
    yes_typed = input(">>  ")
    if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
        return
    while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
        print(' Error try again')
        yes_typed = input(">>  ")

    # Delete
    t.deleteNode(node)
    t.write()
    t.close
    print(' Data deleted')


def create(pulseNo, node, descr):
    
    ###############################################################
    ####################    Create the tree    ####################
    ##############################################################    
    try:
        t = Tree( 'ASTRA', pulseNo, 'edit' )

        # get the username of who wrote this run
        try:
            n = t.getNode(r'\ASTRA::TOP.' + node + '.CODE_VERSION:USER')
            user_already_written = n.data()
        except:
            user_already_written = user

        if not(user_already_written==user):
            print('########################################################')
            print('#  *** WARNING ***                                     #')
            print("#  You are about to overwrite a different user's run!  #")
            print('########################################################')

            print(' Proceed yes/no?')
            yes_typed = input(">>  ")
            if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
                return
            while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
                print('error try again')
                yes_typed = input(">>  ")

            print(' To confirm type in: "' + user_already_written + '"')
            user_typed = input(">>  ")
            while not(user_already_written==user_typed):
                print('error try again')
                user_typed = input(">>  ")
            print(' ')
    except:
        t = Tree( 'ASTRA', pulseNo, 'New' )

    # Second warning to confirm delete
    try:
        n = t.getNode(r'\ASTRA::TOP.' + node + '.CODE_VERSION:USER')
        user_already_written = n.data()
    except:
        user_already_written='noname'

    if (user_already_written==user):
        print('#####################################################')
        print('#  *** WARNING ***                                  #')
        print('#  You are about to overwrite data                  #')
        print('#  ' + node + '       #')
        print('#####################################################')
        print(' Proceed yes/no?')
        yes_typed = input(">>  ")
        if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
            return
            while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
                print(' Error try again')
                yes_typed = input(">>  ")

    branches = [node]
    descriptions = [descr]
    astra = t.getDefault()
    t.deleteNode(branches[0])

    t.setDefault(astra)

    # create 
#    t.setDefault( mh.createNode(t,"PSI2D","STRUCTURE",descriptions[0]) )    
#    n = mh.createNode(t,"RGRID","NUMERIC","Major radius coordinate m");    
#    n = mh.createNode(t,"ZGRID","NUMERIC","Vertical coordinate m");    
#    n = mh.createNode(t,"PSI","SIGNAL","Poloidal flux W");    
#    t.setDefault(astra)

    t.setDefault( mh.createNode(t,branches[0],"STRUCTURE",descriptions[0]) )
    t.addNode("CODE_VERSION", "STRUCTURE")
    n = t.addNode("CODE_VERSION:USER", "TEXT")
    n.putData(user)
    n= mh.createNode(t,"TIME","NUMERIC",  "time vector");
    n= mh.createNode(t,"DATE","TEXT",  "Date and time of calculation");
 
    t.setDefault( mh.createNode(t,"INPUT","STRUCTURE","Global parameters") )
    defaultNode = t.getDefault();
    n= mh.createNode(t,"CODE_FILES","NUMERIC",  "astra run zipped files");

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"GLOBAL","STRUCTURE","Global parameters") )  
    defaultNode = t.getDefault();
    n = mh.createNode(t,"IPL ","SIGNAL","Plasma current,        MA");
    n = mh.createNode(t,"BTVAC","SIGNAL","BT_vacuum at R=0.5m, T");
    n = mh.createNode(t,"DF  ","SIGNAL","simulated diamagnetic flux,  Wb");
    n = mh.createNode(t,"CR0 ","SIGNAL","MINOR RAD=(Rmax-Rmin)/2, m");
    n = mh.createNode(t,"RGEO","SIGNAL","MAJOR R = (Rmax+Rmin)/2, m");
    n = mh.createNode(t,"ZGEO","SIGNAL","Geom vertical position, m ");
    n = mh.createNode(t,"RC","SIGNAL","Current density center R_IP, m ");
    n = mh.createNode(t,"ZC","SIGNAL","Current density center Z_IP, m ");
    n = mh.createNode(t,"ELON","SIGNAL","ELONGATION BOUNDARY     ");
    n = mh.createNode(t,"TRIL","SIGNAL","LOWER TRIANGULARITY     ");
    n = mh.createNode(t,"TRIU","SIGNAL","UPPER TRIANGULARITY     ");
    n = mh.createNode(t,"QWL ","SIGNAL","Q(PSI) AT the LCFS      ");
    n = mh.createNode(t,"Q95 ","SIGNAL","Q(PSI) AT 95% of full poloidal flux inside LCFS");
    n = mh.createNode(t,"TE0 ","SIGNAL","Central electron temp, keV");
    n = mh.createNode(t,"TI0 ","SIGNAL","Central ion temp, keV");
    n = mh.createNode(t,"NE0 ","SIGNAL","Central electron density, 10E19m^-3 ");
    n = mh.createNode(t,"NEL ","SIGNAL","Line aver electron density 10E19m^-3 ");
    n = mh.createNode(t,"NEV ","SIGNAL","Volume aver electron density 10E19m^-3 ");
    n = mh.createNode(t,"TEV ","SIGNAL","Volume aver electron temp, keV");
    n = mh.createNode(t,"TIV ","SIGNAL","Volume aver ion temp, keV");
    n = mh.createNode(t,"TAUE","SIGNAL","Energy confinement time, s ");
    n = mh.createNode(t,"P_OH","SIGNAL","Total Ohmic power, W");
    n = mh.createNode(t,"IEXC","SIGNAL","Ion-electron exchange power, W");
    n = mh.createNode(t,"UPL ","SIGNAL","Loop Voltage,V          ");
    n = mh.createNode(t,"WTH ","SIGNAL","Total energy, J       ");
    n = mh.createNode(t,"Li3 ","SIGNAL","Internal inductance     ");
    n = mh.createNode(t,"BetP","SIGNAL","Poloidal beta           ");
    n = mh.createNode(t,"BetT","SIGNAL","Toroidal beta           ");
    n = mh.createNode(t,"BetN","SIGNAL","Beta normalized  ");
    n = mh.createNode(t,'Hoh',"SIGNAL","Neo-alcator H-factor");
    n = mh.createNode(t,'H98',"SIGNAL","ITER IPB(y,2) H-factor");
    n = mh.createNode(t,'HNSTX',"SIGNAL","NSTX scaling H-factor");
    n = mh.createNode(t,'HPB',"SIGNAL","Peter Buxton H-factor");
    n = mh.createNode(t,'HGLOB',"SIGNAL","Globus-M2 FEC2020 H-factor");
    n = mh.createNode(t,'HLMOD',"SIGNAL","L-mode scaling P.Yushmanov et al.NF(1990)1999 H-factor");
    n = mh.createNode(t,'ZEFF',"SIGNAL","Z effective at the plasma center");
    n = mh.createNode(t,'Res',"SIGNAL","Total plasma resistance Qj/Ipl^2, Ohm");
    n = mh.createNode(t,'Rmag',"SIGNAL","Magnetic axis hor position, m");
    n = mh.createNode(t,'Zmag',"SIGNAL","Magnetic axis vert position, m");
    n = mh.createNode(t,'Vol',"SIGNAL","Plasma volume, m^3");
    n = mh.createNode(t,'ROC',"SIGNAL","Effective plasma radius, m");
    n = mh.createNode(t,'P_NBI_E',"SIGNAL","Total power from NBI to electrons, W");
    n = mh.createNode(t,'P_NBI_I',"SIGNAL","Total power from NBI to ions, W");
    n = mh.createNode(t,"P_RF","SIGNAL","Total RF power to electrons,W")
    n = mh.createNode(t,"I_BS","SIGNAL","Total bootstrap current,MA")
    n = mh.createNode(t,"F_BS","SIGNAL","Bootstrap current fraction")
    n = mh.createNode(t,"I_NBI","SIGNAL","Total NB driven current,MA")
    n = mh.createNode(t,"NBI_NAMES","SIGNAL","NBI names, RFX,HNBI1=00,01,10,11")
    n = mh.createNode(t,"I_RF","SIGNAL","Total RF driven current,MA")
    n = mh.createNode(t,"I_OH","SIGNAL","Total Ohmic current,MA")
    n = mh.createNode(t,"F_NI","SIGNAL","Non-inductive current fraction")
    n = mh.createNode(t,"P_FUS_THERM","SIGNAL","Thermal fusion power,W")
    n = mh.createNode(t,"P_FUS_TOT","SIGNAL","Total fusion power: thermal+NBI,W")
    n = mh.createNode(t,"P_AUX","SIGNAL","Total external heating power,W")
    n = mh.createNode(t,"Q_FUS","SIGNAL","Fusion energy gain")
    n = mh.createNode(t,"P_TOT_E","SIGNAL","Total alpha power to electrons,W")
    n = mh.createNode(t,"P_TOT_I","SIGNAL","Total alpha power to ions,W")
    n = mh.createNode(t,"I_ICR","SIGNAL","Total ICR driven current,MA")
    n = mh.createNode(t,"FBND","SIGNAL","boundary poloidal flux,Wb")
    n = mh.createNode(t,"FAXS","SIGNAL","axis poloidal flux,Wb")
    n = mh.createNode(t,"QE","SIGNAL","electron power flux through LCFS, W");
    n = mh.createNode(t,"QI","SIGNAL","ion power flux through LCFS, W");
    n = mh.createNode(t,"QN","SIGNAL","electron flux through LCFS, 10^19/s");
    n = mh.createNode(t,"STOT","SIGNAL","Total electron source, 10^19/s");
    n = mh.createNode(t,"SPEL","SIGNAL","Pellet electron source, 10^19/s");
    n = mh.createNode(t,"SWALL","SIGNAL","Boundary electron source, 10^19/s");
    n = mh.createNode(t,"SBM","SIGNAL","Neutral beam electron source, 10^19/s");
    n = mh.createNode(t,"NNCL","SIGNAL","Wall cold neutral density, 10^19/m^3");
    n = mh.createNode(t,"TAUP","SIGNAL","Particle confinement time ,s");
    n = mh.createNode(t,"GAMMA","SIGNAL","KINX growth rate, 1/s")
    n = mh.createNode(t,"VTOR0","SIGNAL","Central toroidal velocity, m/s")
    n = mh.createNode(t,"TORQ","SIGNAL","Total torque from NB, N*m")
    n = mh.createNode(t,"TORQ_BE","SIGNAL","Collisional to electron torque from NB, N*m")
    n = mh.createNode(t,"TORQ_BI","SIGNAL","Collisional to ions torque from NB, N*m")
    n = mh.createNode(t,"TORQ_BTH","SIGNAL","Beam thermalisation torquefrom NB, N*m")
    n = mh.createNode(t,"TORQ_JXB","SIGNAL","JXB torque from NB, N*m")
    n = mh.createNode(t,"TORQ_BCX","SIGNAL","CX losses torque from NB, N*m")
    n = mh.createNode(t,"TAU_PHI","SIGNAL","Momentum confinement time, s")
    n = mh.createNode(t,"TOTNEUT","SIGNAL","total neutrons from as_nubeam_neutot_out, 1/s")
    n = mh.createNode(t,"BTNEUT","SIGNAL","beam-target neutrons from as_nubeam_neutot_out, 1/s")
    n = mh.createNode(t,"BBNEUT","SIGNAL","beam-beam neutrons from as_nubeam_neutot_out, 1/s")
    n = mh.createNode(t,"DDNEUT","SIGNAL","plasma-plasma DD neutron flux, 1/s")
    n = mh.createNode(t,"DTNEUT","SIGNAL"," neutron rate from D-T reaction in plasma, 1/s")
    n = mh.createNode(t,"INTNEUT","SIGNAL","time integrated neutron yield, -")
    n = mh.createNode(t,"Ftherm","SIGNAL","Thermal energy fraction, -")
    n = mh.createNode(t,"P_RAD","SIGNAL","Radiated power, W")
    n = mh.createNode(t,"Pabs","SIGNAL"," Absorbed power, W")
    n = mh.createNode(t,"Pnb","SIGNAL"," Injected beam power, W")
    n = mh.createNode(t,"Pth","SIGNAL"," Beam power thermalising into plasma, W")
    n = mh.createNode(t,"dPdt","SIGNAL"," dW_fast/dt, W")
    n = mh.createNode(t,"Pbo","SIGNAL"," Bad orbit loss power, W")
    n = mh.createNode(t,"Psh","SIGNAL"," Shine through power loss, W")
    n = mh.createNode(t,"Pcx","SIGNAL"," Charge exchange loss, W")
    n = mh.createNode(t,"ERFX","SIGNAL","RFX:beam energy, kV")
    n = mh.createNode(t,"FULLRFX","SIGNAL","RFX:fraction of beam current at full energy, -")
    n = mh.createNode(t,"HALFRFX","SIGNAL","RFX:fraction of beam current at half energy, -")
    n = mh.createNode(t,"EHNBI","SIGNAL","HNBI:beam energy, kV")
    n = mh.createNode(t,"FULLHNBI","SIGNAL","HNBI:fraction of beam current at full energy, -")
    n = mh.createNode(t,"HALFHNBI","SIGNAL","HNBI:fraction of beam current at half energy, -")
    n = mh.createNode(t,"Q0","SIGNAL","central q, -")
    n = mh.createNode(t,"NFASTV","SIGNAL","Volume averaged fast ion density from NUBEAM, 10^19/m^3")
    n = mh.createNode(t,"ZEFAV","SIGNAL","Volume averaged effective charge, -")
    n = mh.createNode(t,"NIZ1AV","SIGNAL","Volume averaged impurity 1 density, 10^19/m^3")
    n = mh.createNode(t,"NIZ2AV","SIGNAL","Volume averaged impurity 2 density, 10^19/m^3")
    n = mh.createNode(t,"NIZ3AV","SIGNAL","Volume averaged impurity 3 density, 10^19/m^3")
    n = mh.createNode(t,"HQ1","SIGNAL","HQ1 vertical position of q=1 surface relative to midplane, m")
    n = mh.createNode(t,"BgBFACTORe","SIGNAL","BgB model factor for electron heat conductivity,-")
    n = mh.createNode(t,"BgBFACTORi","SIGNAL","BgB model factor for ion heat conductivity,-")
    n = mh.createNode(t,"Wtherm","SIGNAL","Plasma thermal energy,J")
    n = mh.createNode(t,"Wfast","SIGNAL","Fast particle energy,J")
    n = mh.createNode(t,"P_ICR","SIGNAL"," ICR power to ions,W")
    n = mh.createNode(t,"BANGLE","SIGNAL","Angle of magnetic field line to toroidal direction (grad(phi)), Degree")
    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"BPPROBE","STRUCTURE","probe signals"))
    n = mh.createNode(t,"B","SIGNAL","Poloidal magnetic field, T");    
    n = mh.createNode(t,"R","NUMERIC","R position, M");    
    n = mh.createNode(t,"Z","NUMERIC","Z position, M");    
    n = mh.createNode(t,"ANGLE","NUMERIC","Angle, rad");    
    n = mh.createNode(t,"NAME","TEXT","Probe name");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"FLOOP","STRUCTURE","probe signals"))
    n = mh.createNode(t,"PSI","SIGNAL","Poloidal magnetic field, Wb");    
    n = mh.createNode(t,"V","SIGNAL","Loop voltage, V");    
    n = mh.createNode(t,"R","NUMERIC","R position, M");    
    n = mh.createNode(t,"Z","NUMERIC","Z position, M");    
    n = mh.createNode(t,"NAME","TEXT","Probe name");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"PASSIVES","STRUCTURE","PASSIVE FILAMENTS"))
    n = mh.createNode(t,"INDEX","NUMERIC","x vector(i) = i");       
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"RP","NUMERIC","R filament position, M");    
    n = mh.createNode(t,"ZP","NUMERIC","Z filament position, M");    
    n = mh.createNode(t,"RESP","NUMERIC","filament resistance, Ohm");    
    n = mh.createNode(t,"NAME","TEXT","filament name"); 
   
    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"CONSTRAINTS","STRUCTURE",descriptions[0]) )  
    t.setDefault( mh.createNode(t,"IP","STRUCTURE","Plasma current, A") )
    n = mh.createNode(t,"CVALUE","SIGNAL","simulated");    
    n = mh.createNode(t,"MVALUE","SIGNAL","experimental");    
    n = mh.createNode(t,"WEIGHT","SIGNAL","");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"PSI2D","STRUCTURE","2D psi") )    
    n = mh.createNode(t,"RGRID","NUMERIC","Major radius coordinate m");    
    n = mh.createNode(t,"ZGRID","NUMERIC","Vertical coordinate m");    
    n = mh.createNode(t,"PSI","SIGNAL","Poloidal flux W");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"PSU","STRUCTURE","Power supply units") )
    t.setDefault( mh.createNode(t,"CS","STRUCTURE","Central solenoid") )
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"V","SIGNAL","Voltage, V");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]+".PSU"))
    t.setDefault( mh.createNode(t,"MC","STRUCTURE","MC coil") )
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"V","SIGNAL","Voltage, V");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]+".PSU"))
    t.setDefault( mh.createNode(t,"DIV","STRUCTURE","DIV coil") )
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"V","SIGNAL","Voltage, V");    
 
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".PSU"))
    t.setDefault( mh.createNode(t,"PSH","STRUCTURE","Pusher coil") )
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"V","SIGNAL","Voltage, V");    
 
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".PSU"))
    t.setDefault( mh.createNode(t,"BVU","STRUCTURE","BVU coil") )
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"V","SIGNAL","Voltage, V");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]+".PSU"))
    t.setDefault( mh.createNode(t,"BVUT","STRUCTURE","Top BVU coil") )
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"V","SIGNAL","Voltage, V");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]+".PSU"))
    t.setDefault( mh.createNode(t,"BVUB","STRUCTURE","Bottom BVU coil") )
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"V","SIGNAL","Voltage, V");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]+".PSU"))
    t.setDefault( mh.createNode(t,"BVL","STRUCTURE","BVL coil") )
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"V","SIGNAL","Voltage, V");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"PROFILES","STRUCTURE","Profiles") )
    t.setDefault(t.getNode('\\TOP.'+branches[0]+'.PROFILES'))
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

    t.setDefault(t.getNode('\\TOP.'+branches[0]+'.PROFILES'))
    t.setDefault( mh.createNode(t,"ASTRA","STRUCTURE","Profiles from ASTRA") )    
    n = mh.createNode(t,"RHO","SIGNAL","rho - toroidal flux coordinate, m");    
    n = mh.createNode(t,"TE","SIGNAL","Electron temperature, keV");    
    n = mh.createNode(t,"NE","SIGNAL","Electron density, 10^19 m^-3");    
    n = mh.createNode(t,"NI","SIGNAL","Main ion density, 10^19 m^-3");    
    n = mh.createNode(t,"TI","SIGNAL","Ion temperature, keV");    
    n = mh.createNode(t,"ZEFF","SIGNAL","Effective ion charge");
    n = mh.createNode(t,"QNBE","SIGNAL","Beam power density to electrons, MW/m3");
    n = mh.createNode(t,"QNBI","SIGNAL","Beam power density to ions, MW/m3");
    n = mh.createNode(t,"Q_OH","SIGNAL","Ohmic heating power profile, MW/m3");
    n = mh.createNode(t,"Q_EI","SIGNAL","Electron-ion heat exchange due to Coulomb collisions, MW/m3");
    n = mh.createNode(t,"STOT","SIGNAL","Total electron source,10^19/s/m3");
    n = mh.createNode(t,"CHI_E","SIGNAL","Total electron heat conductivity, m^2/s");
    n = mh.createNode(t,"CHI_I","SIGNAL","Total ion heat conductivity, m^2/s");
    n = mh.createNode(t,"CHI_E_ANOM","SIGNAL","anomalous electron heat conductivity, m^2/s");
    n = mh.createNode(t,"CHI_I_ANOM","SIGNAL","anomalous ion heat conductivity, m^2/s");
    n = mh.createNode(t,"CHI_E_NEO","SIGNAL","neoclassical electron heat conductivity, m^2/s");
    n = mh.createNode(t,"CHI_I_NEO","SIGNAL","neoclassical ion heat conductivity, m^2/s");
    n = mh.createNode(t,"DIFF","SIGNAL","diffusion coefficient, m^2/s");
    n = mh.createNode(t,"DIFF_ANOM","SIGNAL","anomalous diffusion coefficient, m^2/s");
    n = mh.createNode(t,"QE","SIGNAL","electron power flux, MW");
    n = mh.createNode(t,"QI","SIGNAL","ion power flux, MW");
    n = mh.createNode(t,"QN","SIGNAL","total electron flux, 10^19/s");
    n = mh.createNode(t,"PEGN","SIGNAL","electron convective heat flux, MW");
    n = mh.createNode(t,"PIGN","SIGNAL","ion convective heat flux, MW");
    n = mh.createNode(t,"CC","SIGNAL","Parallel current conductivity, 1/(Ohm*m)");
    n = mh.createNode(t,"ELON","SIGNAL","Elongation profile");
    n = mh.createNode(t,"TRI","SIGNAL","Triangularity (up/down symmetrized) profile");
    n = mh.createNode(t,"RMID","SIGNAL","Centre of flux surfaces, m");
    n = mh.createNode(t,"RMINOR","SIGNAL","minor radius, m");
    n = mh.createNode(t,"N_D","SIGNAL","Deuterium density,10E19/m3")
    n = mh.createNode(t,"N_T","SIGNAL","Tritium density	,10E19/m3")
    n = mh.createNode(t,"T_D","SIGNAL","Deuterium temperature,keV")
    n = mh.createNode(t,"T_T","SIGNAL","Tritium temperature,keV")
    n = mh.createNode(t,"Q_RF","SIGNAL","RF power density to electron,MW/m3")
    n = mh.createNode(t,"Q_ALPHA_E","SIGNAL","Alpha power density to electrons,MW/m3")
    n = mh.createNode(t,"Q_ALPHA_I","SIGNAL","Alpha power density to ions,MW/m3")
    n = mh.createNode(t,"J_NBI","SIGNAL","NB driven current density,MA/m2")
    n = mh.createNode(t,"J_RF","SIGNAL"," EC driven current density,MA/m2")
    n = mh.createNode(t,"J_BS","SIGNAL","Bootstrap current density,MA/m2")
    n = mh.createNode(t,"J_OH","SIGNAL","Ohmic current density,MA/m2")
    n = mh.createNode(t,"J_TOT","SIGNAL","Total current density,MA/m2")
    n = mh.createNode(t,"Q_ICR","SIGNAL","ICRH power density to ions,MW/m3")
    n = mh.createNode(t,"J_ICR","SIGNAL","ICR current density,MA/m2") 
    n = mh.createNode(t,"PSIN","SIGNAL","Normalized poloidal flux -")
    n = mh.createNode(t,"SBM","SIGNAL","Particle source from beam, 10^19/m^3/s ")
    n = mh.createNode(t,"SPEL","SIGNAL","Particle source from pellets, 10^19/m^3/s")
    n = mh.createNode(t,"SWALL","SIGNAL","Particle source from wall neutrals, 10^19/m^3/s")
    n = mh.createNode(t,"OMEGA_TOR","SIGNAL","Toroidal rotation frequency, 1/s");
    n = mh.createNode(t,"TORQ_DEN","SIGNAL","Total torque density from NB, N*m/m3")
    n = mh.createNode(t,"TORQ_DEN_BE","SIGNAL","Collisional to electron torque density from NB, N*m/m3")
    n = mh.createNode(t,"TORQ_DEN_BI","SIGNAL","Collisional to ions torque density from NB, N*m/m3")
    n = mh.createNode(t,"TORQ_DEN_BTH","SIGNAL","Beam thermalisation torque density from NB, N*m/m3")
    n = mh.createNode(t,"TORQ_DEN_JXB","SIGNAL","JXB torque density from NB, N*m/m3")
    n = mh.createNode(t,"TORQ_DEN_BCX","SIGNAL","CX losses torque density from NB, N*m/m3")
    n = mh.createNode(t,"CHI_PHI","SIGNAL","Momentum transport coefficient, m2/s")
    n = mh.createNode(t,"QRAD","SIGNAL","Radiated power density, MW/m3")
    n = mh.createNode(t,"NF","SIGNAL","Fast ion density profile from NUBEAM, 10^19/m^3")
    n = mh.createNode(t,"NIZ1","SIGNAL","Impurity 1 density profile, 10^19/m^3")
    n = mh.createNode(t,"NIZ2","SIGNAL","Impurity 2 density profile, 10^19/m^3")
    n = mh.createNode(t,"NIZ3","SIGNAL","Impurity 3 density profile, 10^19/m^3")
    n = mh.createNode(t,"ZIM1","SIGNAL","Impurity 1 mean charge profile, ")
    n = mh.createNode(t,"ZIM2","SIGNAL","Impurity 2 mean charge profile, ")
    n = mh.createNode(t,"ZIM3","SIGNAL","Impurity 3 mean charge profile, ")
    n = mh.createNode(t,"DAN_IMP1","SIGNAL","Impurity 1 anomalous diffusion profile, m^2/s")
    n = mh.createNode(t,"DAN_IMP2","SIGNAL","Impurity 2 anomalous diffusion profile, m^2/s")
    n = mh.createNode(t,"DAN_IMP3","SIGNAL","Impurity 3 anomalous diffusion profile, m^2/s")
    n = mh.createNode(t,"VAN_IMP1","SIGNAL","Impurity 1 anomalous convection velocity profile, m/s")
    n = mh.createNode(t,"VAN_IMP2","SIGNAL","Impurity 2 anomalous convection velocity profile, m/s")
    n = mh.createNode(t,"VAN_IMP3","SIGNAL","Impurity 3 anomalous convection velocity profile, m/s")
    n = mh.createNode(t,"DNEO_IMP1","SIGNAL","Impurity 1 neoclassical diffusion profile, m^2/s")
    n = mh.createNode(t,"DNEO_IMP2","SIGNAL","Impurity 2 neoclassical diffusion profile, m^2/s")
    n = mh.createNode(t,"DNEO_IMP3","SIGNAL","Impurity 3 neoclassical diffusion profile, m^2/s")
    n = mh.createNode(t,"VNEO_IMP1","SIGNAL","Impurity 1 anomalous convection velocity profile, m/s")
    n = mh.createNode(t,"VNEO_IMP2","SIGNAL","Impurity 2 anomalous convection velocity profile, m/s")
    n = mh.createNode(t,"VNEO_IMP3","SIGNAL","Impurity 3 anomalous convection velocity profile, m/s")
#     Total pressure=0.5*(PBLON+PBPER) as used in EFIT
#     Energy=0.5*int(PBLON*dV)+int(PBPER*dV)
    n = mh.createNode(t,"PBLON","SIGNAL","Parallel pressure, Pa")
    n = mh.createNode(t,"PBPER","SIGNAL","Perpendicular pressure, Pa")
    n = mh.createNode(t,"WF","SIGNAL","Fast particle energy profile,MJ/m3")
    n = mh.createNode(t,"VAN","SIGNAL","Pinch velocity,m/s")
    n = mh.createNode(t,"DNEO","SIGNAL","Neoclassical diffusivity,m^2/s")
    n = mh.createNode(t,"VNEO","SIGNAL","Neoclassical pinch,m/s")
    n = mh.createNode(t,"VR","SIGNAL","dVolume/dRHO, m^2")
    n = mh.createNode(t,"PSI","SIGNAL","Poloidal flux on ASTRA mesh, Wb")
    n = mh.createNode(t,"NN","SIGNAL"," Neutral density, 10^19/m3")
    n = mh.createNode(t,"UPL","SIGNAL"," Loop voltage, V")
    n = mh.createNode(t,"SURF","SIGNAL","Flux surface area,m^2")
    n = mh.createNode(t,"VOL","SIGNAL","Flux surface  volume,m^3")

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"P_BOUNDARY","STRUCTURE","R,Z for LCFS") )
    n = mh.createNode(t,"INDEX","NUMERIC","");    
    n = mh.createNode(t,"RBND","SIGNAL","R OF PLASMA_BOUNDARY");    
    n = mh.createNode(t,"ZBND","SIGNAL","Z OF PLASMA_BOUNDARY");  
  
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".P_BOUNDARY"))
    t.setDefault( mh.createNode(t,"XPOINTS","STRUCTURE","separatrix data") )    
    n = mh.createNode(t,"FXP1","SIGNAL","x-point 1 poloidal flux, Wb");    
    n = mh.createNode(t,"FXP2","SIGNAL","x-point 2 poloidal flux, Wb");    
    n = mh.createNode(t,"RXP1","SIGNAL","x-point 1 r-position,m");    
    n = mh.createNode(t,"ZXP1","SIGNAL","x-point 1 z-position,m");    
    n = mh.createNode(t,"RXP2","SIGNAL","x-point 2 r-position,m");    
    n = mh.createNode(t,"ZXP2","SIGNAL","x-point 2 z-position,m");    
    n = mh.createNode(t,"ACTIVE","SIGNAL","main x-point index (1 or 2) ");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]+".P_BOUNDARY"))
    t.setDefault( mh.createNode(t,"LIMITER","STRUCTURE","limiter data") )    
    t.setDefault( mh.createNode(t,"VESSEL","STRUCTURE","hard limiter data") )    
    n = mh.createNode(t,"INDEX","NUMERIC","");    
    n = mh.createNode(t,"R","NUMERIC","r-position,m");    
    n = mh.createNode(t,"Z","NUMERIC","z-position,m");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]+".P_BOUNDARY.LIMITER"))
    t.setDefault( mh.createNode(t,"PLASMA","STRUCTURE","plasma-limiter point") )    
    n = mh.createNode(t,"ACTIVE","SIGNAL","=1 if limiter");    
    n = mh.createNode(t,"FBND","SIGNAL","Limiter poloidal flux, Wb");    
    n = mh.createNode(t,"R","SIGNAL","r-position,m");    
    n = mh.createNode(t,"Z","SIGNAL","z-position,m");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]+".P_BOUNDARY"))
    t.setDefault( mh.createNode(t,"TARGETS","STRUCTURE","Target geometric parameters") )    
    n = mh.createNode(t,"RTORX","SIGNAL","Geometric axis r-position from ASTRA exp file,m");    
    n = mh.createNode(t,"ZX","SIGNAL","Geometric axis z-position from ASTRA exp file,m");    
    n = mh.createNode(t,"ELONGX","SIGNAL","Elongation from ASTRA exp file");    
    n = mh.createNode(t,"TRIANX","SIGNAL","Triangularity from ASTRA exp file");    
    n = mh.createNode(t,"ABCX","SIGNAL","Minor radius at midplane from ASTRA exp file,m");    

#DIVPSRB,DIVPSRT,HFSPSRB,HFSPSRT,MCB,MCT,GASBFLB,GASBFLT,BVLB,BVLT,DIVB,DIVT,INIVC000
    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"ROG","STRUCTURE","Rogowski loops") )
    t.setDefault( mh.createNode(t,"DIVPSRB","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"DIVPSRT","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"HFSPSRB","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"HFSPSRT","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"MCB","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"MCT","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"GASBFLB","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"GASBFLT","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"BVLB","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"BVLT","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"DIVB","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"DIVT","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"INIVC000","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"MCWIRE","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"DIVBWIRE","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    t.setDefault(t.getNode('\\TOP.'+branches[0]+".ROG"))
    t.setDefault( mh.createNode(t,"BVLWIRE","STRUCTURE","") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
 
    t.write()
    t.close

def modifyhelp(pulseNo,node,descr):
    try:
        t = Tree( 'ASTRA', pulseNo, 'edit' )
    except:
        t = Tree( 'ASTRA', pulseNo, 'New' )
    astra = t.getDefault()
    t.setDefault(astra)
    descr0=t.getNode(node+":HELP").getData()
    print(descr0)
    t.getNode(node+":HELP").putData(descr)
    t.write()
    descr1=t.getNode(node+":HELP").getData()
    print(descr1)
    t.close

def addglobal(pulseNo,runnum,addnode,descr):
    try:
        t = Tree( 'ASTRA', pulseNo, 'edit' )
    except:
        t = Tree( 'ASTRA', pulseNo, 'New' )
    t.setDefault(t.getNode('\\TOP.'+runnum+".GLOBAL"))
    n = mh.createNode(t,addnode,"SIGNAL",descr);
    t.write()
    t.close

def copy_runs(pulseNo_from, run_from, pulseNo_to, run_to, tree):
    # Example usage:
    # move_runs(314, 'RUN1', 1000004, 'RUN1', 'ASTRA')
    
    path_from = '\\' + tree + '::TOP.' + run_from
    path_to = '\\' + tree + '::TOP.' + run_to
    print(path_from)

    # Read what we want to move:
    t_from = Tree(tree, pulseNo_from)
    command = "GETNCI('\\" + path_from + "***','FULLPATH')"
    fullpaths_from = t_from.tdiExecute(command).data().astype(str, copy=False).tolist()
    command = "GETNCI('\\" + path_from + "***','USAGE')"
    usages_from = t_from.tdiExecute(command).data()

    # Read where we want to 
    try:
        t_to = Tree(tree, pulseNo_to, 'EDIT')
        print('editing...')
    except:
        t_to = Tree(tree, pulseNo_to, 'NEW')
        print('new...')

    # Add the run if needed
    try:
        run_node_to = t_to.getNode(path_to)

        # Command line warning_message
        warning_message(pulseNo_to, path_to)

        # Delete node
        t_to.deleteNode(run_node_to)
    except:
        pass
    # Add a new fully empty node
    t_to.addNode(path_to)

    for i in range(0, len(fullpaths_from)):
        fullpath_from = fullpaths_from[i].strip()
        fullpath_to = fullpaths_from[i].replace(path_from, path_to).strip()
        usage = usages_from[i]
        if (usage==1):
            datatype = 'STRUCTURE'
        elif (usage==5):
            datatype = 'NUMERIC'
        elif (usage==6):
            datatype = 'SIGNAL'
        elif (usage==8):
            datatype = 'TEXT'
        elif (usage==11):
            datatype = 'SUBTREE'
        else:
            print('UNKNOWN DATA TYPE!!')
        # Make the node
        n = t_to.addNode(fullpath_to, datatype)

        # Move NUMBER, SIGNAL or TEXT
        if (usage==5)  or  (usage==6)  or  (usage==8):
            n_from = t_from.getNode(fullpath_from)
            n_to = t_to.getNode(fullpath_to)
            n_to.putData(n_from.getRecord())

    t_to.write()
    t_to.close()
    t_from.close()

    print('Data successfully moved')


def warning_message(pulseNo, node):
    pulseNo_str = str(pulseNo)
    print('#####################################################')
    print('#  *** WARNING ***                                  #')
    print('#  You are about to overwrite data                  #')
    spaces = ' '*(41 - len(pulseNo_str))
    print('#  pulseNo=' + pulseNo_str + spaces + '#')
    spaces = ' '*(49 - len(node))
    print('#  ' + node + spaces + '#')
    print('#####################################################')
    print(' Proceed yes/no?')
    yes_typed = input(">>  ")
    if (yes_typed.lower()=='no')  or  (yes_typed.lower()=='n'):
        return
    while not(not(yes_typed.lower()=='yes')  or  not(yes_typed.lower()=='y')):
        print(' Error try again')
        yes_typed = input(">>  ")


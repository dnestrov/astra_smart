# Script for creating the model tree for vacuum case (no plasma, just magnetics)
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
"IPL ","Plasma current, A",
"BTVAC","BT_vacuum at R=0.5m, T",
"DF  ","simulated diamagnetic flux,  Wb"]

def tree(t,run,descriptions,tree):
    if tree == 'ASTRA':
        t.deleteNode(run)
        t.setDefault( mh.createNode(t,run,"STRUCTURE",descriptions[0]) )
        node = t.getDefault()
        ok=True
    if tree == 'SOPHIA':
        t.setDefault(run)
        try:
            t.setDefault("VACUUM")
            ok=False
            return ok
        except:
            t.setDefault( mh.createNode(t,"VACUUM", "STRUCTURE",descriptions[0]))
            ok=True
        node = t.getDefault()

    t.addNode("CODE_VERSION", "STRUCTURE")
    n = t.addNode("CODE_VERSION:USER", "TEXT")
    n.putData(user)
    n= mh.createNode(t,"TIME","NUMERIC",  "time vector");
    n= mh.createNode(t,"DATE","TEXT",  "Date and time of calculation");
 
    t.setDefault( mh.createNode(t,"INPUT","STRUCTURE","Global parameters") )
    n= mh.createNode(t,"CODE_FILES","NUMERIC",  "astra run zipped files");
           
    t.setDefault(node)
    t.setDefault( mh.createNode(t,"GLOBAL","STRUCTURE","Global parameters") )
    for i in range(int(len(GLOBAL)/2)):
        n = mh.createNode(t,GLOBAL[2*i],"SIGNAL",GLOBAL[2*i+1]); 

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
    t.setDefault( mh.createNode(t,"BPPROBE","STRUCTURE","probe signals"))
    t.setDefault( mh.createNode(t,"ALL","STRUCTURE","all in one"))
    n = mh.createNode(t,"B","SIGNAL","Poloidal magnetic field, T");    
    n = mh.createNode(t,"R","NUMERIC","R position, M");    
    n = mh.createNode(t,"Z","NUMERIC","Z position, M");    
    n = mh.createNode(t,"ANGLE","NUMERIC","Angle, rad");    
    n = mh.createNode(t,"NAME","TEXT","Probe name");    
 
    t.setDefault(node)
    t.setDefault( mh.createNode(t,"FLOOP","STRUCTURE","probe signals"))
    t.setDefault( mh.createNode(t,"ALL","STRUCTURE","probe signals"))
    n = mh.createNode(t,"PSI","SIGNAL","Poloidal magnetic field, Wb");    
    n = mh.createNode(t,"V","SIGNAL","Loop voltage, V");    
    n = mh.createNode(t,"R","NUMERIC","R position, M");    
    n = mh.createNode(t,"Z","NUMERIC","Z position, M");    
    n = mh.createNode(t,"NAME","TEXT","Probe name");    

    t.setDefault(node)
    t.setDefault( mh.createNode(t,"PASSIVES","STRUCTURE","PASSIVE FILAMENTS"))
    n = mh.createNode(t,"I","SIGNAL","Current, MA");    
    n = mh.createNode(t,"RP","NUMERIC","R filament position, M");    
    n = mh.createNode(t,"ZP","NUMERIC","Z filament position, M");    
    n = mh.createNode(t,"DR","NUMERIC","DR for filament, M");    
    n = mh.createNode(t,"DZ","NUMERIC","DZ for filament, M");    
    n = mh.createNode(t,"RESP","NUMERIC","filament resistance, Ohm");    
    n = mh.createNode(t,"NAME","TEXT","filament name");  

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

#DIVPSRB,DIVPSRT,HFSPSRB,HFSPSRT,MCB,MCT,GASBFLB,GASBFLT,BVLB,BVLT,DIVB,DIVT,INIVC000
    t.setDefault(node)
    t.setDefault( mh.createNode(t,"ROG","STRUCTURE","Rogowski loops") )
    t.setDefault( mh.createNode(t,"ALL","STRUCTURE","All in one") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    n = mh.createNode(t,"NAME","TEXT","Rogowski name array");    
    return ok



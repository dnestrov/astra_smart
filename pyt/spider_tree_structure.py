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
PSUFPP=['SOL','PF1L','PF1U','PF2L','PF2U','PF3L','PF3U','PF4L','PF4U','PF5L','PF5U']
PFFPP=['SOL','PF1L','PF1U','PF2L','PF2U','PF3L','PF3U','PF4L','PF4U','PF5L','PF5U']
PSUFE23=['IPL','MC','PSH','DIV','BVL','BVUT','BVUB','CS']
PSUP23=['DIV','BVL','BVUT','BVUB','CS','MC','PSH']
PFFE23=['IPL','MCT','MCB','PSHT1','PSHB1','PSHT2','PSHB2','DIVT','DIVB','BVLT','BVLB','BVUT','BVUB','CS']

GLOBAL=[
"AMINOR","Minor radius (m)",
"ASPECT","Aspect ratio",
"BETAN","Normalised beta (%)",
"BETAP1","Poloidal beta, betaP(1)",
"BETAP2","Poloidal beta, betaP(2)",
"BETAP3","Poloidal beta, betaP(3)",
"BETAT","Toroidal beta (%)",
"BPOL_OMP","Poloidal magnetic field at (R_OMP,ZMAG) (T)",
"BTOT_OMP","Total magnetic field at (R_OMP,ZMAG) (T)",
"BTVAC_GEO","Btoroidal at the plasma geometric centre (T)",
"ELON","Elongation = 0.5*(ELON_UP+ELON_LOW)",
"ELON_LOW","Lower midplane elongation",
"ELON_UP","Upper midplane elongation",
"INV_ASPECT","Inverse aspect ratio",
"IP","Plasma current (A)",
"IROD","Total TF current (A)",
"LI","Internal inductance",
"LI1","Normalised internal inductance, li(1)",
"LI2","Normalised internal inductance, li(2)",
"LI3","Normalised internal inductance, li(3)",
"PSIA","Poloidal flux at the magnetic axis (Wb/rad)",
"PSIB","Poloidal flux at the plasma boundary (Wb/rad)",
"QWL","Q(PSI) AT the LCFS      ",
"Q95","q95",
"RCUR","Current centroid radius (m)",
"RGEO","Geometric axis radius (m)",
"RMAG","Magnetic axis radius (m)",
"R_OMP","R coordinate of OMP along Z=Zmagnetic (m)",
"SQRN","Squareness = 0.5*(SQRN_UP+SQRN_LOW)",
"SQRN_LOW","Lower midplane squareness",
"SQRN_UP","Upper midplane squareness",
"TRI","Triangularity = 0.5*(TRI_UP+TRI_LOW)",
"TRI_LOW","Lower midplane triangularity",
"TRI_UP","Upper midplane triangularity",
"VOL","Plasma volume (m^3)",
"WTH","Total thermal energy (J)",
"ZCUR","Current centroid height (m)",
"ZGEO","Geometric axis height (m)",
"ZMAG","Magnetic axis height (m)",
"DF","Full diamagnetic flux, Wb" ]

PROFILES=[
"AREA","Area profile",
"F","f=R*BT (m*T)",
"FFPRIME","f*d(f)/d(psi) (m^2*T^2/Wb/rad)",
"J_TOTAL","Total current",
"P","Pressure",
"PPRIME","d(Pressure)/d(psi) (Pa/Wb/rad)",
"Q","Safety factor, q",
"RHOTOR","Toroidal flux",
"VOL","Volume profile"]

PSI2D=[
"BR","2D Radial field (T)",
"BZ","2D Vertical field (T)",
"JTOR","2D Toroidal current density (A/m^2)",
"PSI","2D poloidal flux (Wb/rad)"]

P_BOUNDARY=[
"NBND","Number of points along the Last Closed Flux Surface",
"RBND","Radial position of Last Closed Flux Surface (m)",
"ZBND","Vertical position of Last Closed Flux Surface (m)"]
XPOINTS=[
"FXPM","",
"RXPM","",
"ZXPM",""]

def tree(t,branches,descriptions,astra):#,machin):
    #if machin == 'FPP': PSU=PSUFPP
    #if machin == 'FE23': PSU=PSUFE23
    #if machin == 'P2.3': PSU=PSUP23
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
    n = mh.createNode(t,"PSU2PF_TABLE","NUMERIC","Connection MATRIX: coil number x psu number");           

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"GLOBAL","STRUCTURE"," ") )
    for i in range(int(len(GLOBAL)/2)):
        #print(GLOBAL[2*i]+','+GLOBAL[2*i+1])
        n = mh.createNode(t,GLOBAL[2*i],"SIGNAL",GLOBAL[2*i+1]); 

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"PROFILES","STRUCTURE"," ") )
    t.setDefault( mh.createNode(t,"RHO","STRUCTURE"," ") )
    n = mh.createNode(t,"PSIN","NUMERIC","Normalised poloidal flux"); 
    for i in range(int(len(PROFILES)/2)):
        #print(PROFILES[2*i]+','+PROFILES[2*i+1])
        n = mh.createNode(t,PROFILES[2*i],"SIGNAL",PROFILES[2*i+1]); 

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"PSI2D","STRUCTURE"," ") )
    n = mh.createNode(t,"RGRID","NUMERIC","Major radius coordinate m");    
    n = mh.createNode(t,"ZGRID","NUMERIC","Vertical coordinate m");    
    for i in range(int(len(PSI2D)/2)):
        #print(PSI2D[2*i]+','+PSI2D[2*i+1])
        n = mh.createNode(t,PSI2D[2*i],"SIGNAL",PSI2D[2*i+1]); 

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"P_BOUNDARY","STRUCTURE"," ") )
    n = mh.createNode(t,"R_LIMITER","NUMERIC","Radial limiter points m");    
    n = mh.createNode(t,"Z_LIMITER","NUMERIC","Vertical limiter points m");    
    for i in range(int(len(P_BOUNDARY)/2)):
        n = mh.createNode(t,P_BOUNDARY[2*i],"SIGNAL",P_BOUNDARY[2*i+1]); 
    n = mh.createNode(t,"INDEX","NUMERIC","x vector(i) = i");       
    t.setDefault( mh.createNode(t,"XPOINTS","STRUCTURE"," ") )
    for i in range(int(len(XPOINTS)/2)):
        n = mh.createNode(t,XPOINTS[2*i],"SIGNAL",XPOINTS[2*i+1]); 
    n = mh.createNode(t,"INDEX","NUMERIC","x vector(i) = i");   
    
    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"BPPROBE","STRUCTURE","probe signals"))
    t.setDefault( mh.createNode(t,"ALL","STRUCTURE","all in one"))
    n = mh.createNode(t,"B","SIGNAL","Poloidal magnetic field, T");    
    n = mh.createNode(t,"R","NUMERIC","R position, M");    
    n = mh.createNode(t,"Z","NUMERIC","Z position, M");    
    n = mh.createNode(t,"ANGLE","NUMERIC","Angle, rad");    
    n = mh.createNode(t,"NAME","TEXT","Probe name");    

    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"FLOOP","STRUCTURE","probe signals"))
    t.setDefault( mh.createNode(t,"ALL","STRUCTURE","all in one"))
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
    n = mh.createNode(t,"DR","NUMERIC","DR for filament, M");    
    n = mh.createNode(t,"DZ","NUMERIC","DZ for filament, M");    
    n = mh.createNode(t,"RESP","NUMERIC","filament resistance, Ohm");    
    n = mh.createNode(t,"NAME","TEXT","filament name"); 

#DIVPSRB,DIVPSRT,HFSPSRB,HFSPSRT,MCB,MCT,GASBFLB,GASBFLT,BVLB,BVLT,DIVB,DIVT,INIVC000
    t.setDefault(t.getNode('\\TOP.'+branches[0]))
    t.setDefault( mh.createNode(t,"ROG","STRUCTURE","Rogowski loops") )
    t.setDefault( mh.createNode(t,"ALL","STRUCTURE","Rogowski loops") )
    n = mh.createNode(t,"I","SIGNAL","Current, A");    
    n = mh.createNode(t,"NAME","TEXT","Rogowski name array");    


"""
g=Tree('FREEGS',22999999).getNode("\\TOP.RUN1A.GLOBAL").getNodeWild('*').getPath().data()
num=g[0].decode().strip().find('BAL')
conn = Connection('192.168.1.7:8000')
conn.openTree('FREEGS',22999999)
for i in range(0,len(g)):
    name=g[i].decode().strip()[num+4:]
    node="\\TOP.RUN1A.GLOBAL."+name+":HELP"
    #print("\""+g[i].decode().strip()[num+4:]+"\",""\""+conn.get(node)+"\",")
    #print("\""+g[i].decode().strip()[num+4:]+"\",")
    print("      const("+str(i+2)+",i)=!conn.get(node))
g=Tree('FREEGS',22999999).getNode("\\TOP.RUN1A.PROFILES.RHO").getNodeWild('*').getPath().data()
num=g[0].decode().strip().find('RHO')
conn = Connection('192.168.1.7:8000')
conn.openTree('FREEGS',22999999)
for i in range(0,len(g)):
    name=g[i].decode().strip()[num+4:]
    node="\\TOP.RUN1A.PROFILES.RHO."+name+":HELP"
    print("\""+g[i].decode().strip()[num+4:]+"\",""\""+conn.get(node)+"\",")
    #print("\""+g[i].decode().strip()[num+4:]+"\",")

g=Tree('FREEGS',22999999).getNode("\\TOP.RUN1A.PSI2D").getNodeWild('*').getPath().data()
num=g[0].decode().strip().find('I2D')
conn = Connection('192.168.1.7:8000')
conn.openTree('FREEGS',22999999)
for i in range(0,len(g)):
    name=g[i].decode().strip()[num+4:]
    node="\\TOP.RUN1A.PSI2D."+name+":HELP"
    print("\""+g[i].decode().strip()[num+4:]+"\",""\""+conn.get(node)+"\",")
    #print("\""+g[i].decode().strip()[num+4:]+"\",")

g=Tree('FREEGS',22999999).getNode("\\TOP.RUN1A.P_BOUNDARY").getNodeWild('*').getPath().data()
num=g[0].decode().strip().find('ARY')
conn = Connection('192.168.1.7:8000')
conn.openTree('FREEGS',22999999)
for i in range(0,len(g)):
    name=g[i].decode().strip()[num+4:]
    node="\\TOP.RUN1A.P_BOUNDARY."+name+":HELP"
    print("\""+g[i].decode().strip()[num+4:]+"\",""\""+conn.get(node)+"\",")
    #print("\""+g[i].decode().strip()[num+4:]+"\",")

ipl,"Plasma current (A)",
btor,"Btoroidal at the plasma geometric centre (T)",
itf,"Total TF current (A)",
lint,,"Internal inductance",
li1,"Normalised internal inductance, li(1)"
li2,"Normalised internal inductance, li(2)"
li3,"Normalised internal inductance, li(3)"
btpm1,"Poloidal beta, betaP(1)",
btpm2,"Poloidal beta, betaP(2)",
btpm3,"Poloidal beta, betaP(3)",
bpol_omp,"Poloidal magnetic field at (R_OMP,ZMAG) (T)",
q95,"q95",
romp,"R coordinate of OMP along Z=Zmagnetic (m)",
sql,"Lower midplane squareness",
squ,"Upper midplane squareness",
elonl,"Lower midplane elongation",
elonu,"Upper midplane elongation",
zip,"Current centroid height (m)",
zgeo,"Geometric axis height (m)",
zmag,"Magnetic axis height (m)"
2D arrays:
"BPHI","2D Toroidal field (T)",
"BR","2D Radial field (T)",
"BZ","2D Vertical field (T)",
"JTOR","2D Toroidal current density (A/m^2)",


"""

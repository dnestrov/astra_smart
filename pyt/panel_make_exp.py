# python3 pyt/panel_make_expHDA.py
from MDSplus import *
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import make_exp as m
conn = Connection('192.168.1.7:8000')
combo_style={'size':(12,1)}
combobox1=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO2-')
runHDA=''
layout = [[sg.T("        "), sg.Button('make file',size=(20,4))],
          [sg.T("save to file  "), sg.Checkbox('', default=False, key="-tofile-")],
          [sg.T("SHOT number="), sg.Input('11089', size=(7,1),key="-SHOT-"),
           sg.T("time1="), sg.Input('0.01', size=(7,1), key="-time1-"),
           sg.T("time2="), sg.Input('0.15', size=(7,1), key="-time2-")],
          [sg.T("coil config    "), 
           sg.Radio('P2.3 (ASTRA)', "RADIO1", default=True, key="-P2.3-"),
           sg.Radio('FE23 (SOPHIA)', "RADIO1", default=False, key="-FE23-")],
          [sg.T("Vacuum shots:"),
           sg.Radio('P238(set currents)', "RADIO1", default=False, key="-P238-"),
           sg.Radio('V238 (set voltages)', "RADIO1", default=False, key="-V238-")],
          [sg.T("Test on MC:"),sg.Radio('MCT_', "RADIO1", default=False, key="-MCT_-")],
          [sg.T("EFIT boundary  "), sg.Checkbox('momentum', default=True, key="-efit-"),
           sg.T("EFIT conf="), sg.Input('BEST',size=(7,1), key="-efitrun-")],
          [sg.T("EFIT Boundary  "), sg.Checkbox('by points', default=False, key="-ifBND-"),
           sg.Input('64', size=(3,1), key="-ntheta-"),sg.T('mag surface points number')],
          [sg.T("PFIT Boundary  "), sg.Checkbox('momentum', default=False, key="-PFIT-")],
          [sg.T("Ti(0) and Te(0)"), sg.Checkbox('XRCS', default=True, key="-ifXRCS-")],
          [sg.T("Argon intensity"), sg.Checkbox('Ar', default=False, key="-ifAR-")],
          [sg.T("Coil currents  "), sg.Checkbox('PSU', default=False, key="-ifPSU-"),
           sg.Checkbox('Symmetry on BVUT & BVUB ', default=False, key="-ifSym-")],
          [sg.T("Density        "), sg.Checkbox('', default=False, key="-ifDEN-"),
           sg.Radio('NIR', "RADIO4", default=False, key="-ifNIR-"),
           sg.Radio('SMM', "RADIO4", default=True, key="-ifSMM-")],
          [sg.T("Ti from CX"),sg.Checkbox('', default=False, key="-ifCXTi-"),
           sg.Radio('PI', "RADIO0", default=False, key="-ifPITi-"),
           sg.Radio('TWS', "RADIO0", default=True, key="-ifTWSTi-")],
          [sg.T("Vtor from CX"),sg.Checkbox('', default=False, key="-ifCXVtor-"),
           sg.Radio('PI', "RADIO7", default=False, key="-ifPIVtor-"),
           sg.Radio('TWS', "RADIO7", default=True, key="-ifTWSVtor-")],
          [sg.Checkbox('read profiles', default=True, key="-ifprof-")],
          [sg.Radio('TS profiles ',"RADIO6", default=False, key="-ifTS-"),
           sg.T("Cut data from "),
           sg.Input('0.03',size=(5,1),key="-t1-"),sg.T("t1"),
           sg.Input('0.05',size=(5,1),key="-t2-"),sg.T("t2")],
          [sg.T("     "),sg.Radio('All', "RADIO2", default=False, key="-ifTSALL-"),
           sg.T("TS smoothing="), sg.Input('0.001',size=(7,1), key="-filter-"),
           sg.Radio(' from HFS', "RADIO2", default=True, key="-ifTSHFS-"),
           sg.Radio(' from LFS', "RADIO2", default=False, key="-ifTSLFS-")],
          [sg.Radio('HDA profiles', "RADIO6",default=False, key="-ifHDA-"),
           combobox1,sg.Button('reread runHDA from 25mln',size=(20,1))],
          [sg.Radio('BDA@BEST profiles', "RADIO6",default=True, key="-ifBDA-"),sg.T("BDA range"),sg.Input('0',size=(8,1), key="-bdarange-")],
          [sg.Radio('TRANSP NE,TE,TI profiles', "RADIO6",default=False, key="-ifTRANSP-"),sg.T("Shot"),
           sg.Input('40012513',size=(10,1), key="-shotT-"),sg.T("Run"),sg.Input('X05',size=(10,1), key="-runT-")],
          [sg.T("NBI power"),sg.Checkbox('', default=True, key="-ifNBI-"),
           sg.Radio('RUN1:PINJ', "RADIO5", default=False, key="-ifNBI1-"),
           sg.Radio('BEST:POWER', "RADIO5", default=True, key="-ifNBI2-"),
           sg.Radio('0 or 1', "RADIO5", default=False, key="-ifNBI3-")],
          [sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")]]
###Setting Window
window = sg.Window('ASTRA exp file options panel', layout, size=(600,750))

###Showing the Application, also GUI functions can be placed here.
while True:
    ifPSU=0;ifWIRE=0;ifNIR=0;ifSMM=0;ifNBI=-1;efit=0;pfit=0;ifAr=0;ifSym=0;ifBND=0;ifTS=0;ifTSHFS=0;ifTSLFS=0;ifHDA=0;ifBDA=0;ifTRANSP=0;ifTWSTi=0;ifTWSVtor=0;ifPITi=0;ifPIVtor=0;ifXRCS=0;filt=0.001;tofile=bool(False)
    event, values = window.read()
    shotHDA=int(values["-SHOT-"])+25000000
    shotBDA=int(values["-SHOT-"])
    shotT=int(values["-shotT-"])
    runT=str(values["-runT-"])
    runBDA='BDA.BEST'
    r=np.array([0])
    if event == "reread runHDA from 25mln":
        try:
            conn.openTree('HDA',shotHDA)
            r=Tree('HDA',shotHDA).getNode("\\TOP").getChildren().getPath().data()
        except:
            print('no HDA runs for '+str(shotHDA ))
            
            exit
        run=np.array([])
        runs=run.tolist()
        if r[0] != 0: 
            for i in range(0,len(r)):
                el=r[i][10:22].decode().strip()
                print(el) 
                text=conn.get(el+':HELP')
                print(text)
                run = np.append(run,el)
            runs=run.tolist()
        combobox1.Update(values=runs)
    if event == '-COMBO1-' :
        RUN= values['-COMBO1-']
#        print(RUN+':HELP')
        conn.openTree('HDA',shotHDA)
        text=conn.get(RUN+':HELP')
        print('Comment for '+RUN+':')
        print(text)
        runHDA=RUN
    shotnumber=int(values["-SHOT-"])
    time1=float(values["-time1-"])
    time2=float(values["-time2-"])
    t1=float(values["-t1-"])
    t2=float(values["-t2-"])
    ntheta=int(values["-ntheta-"])
    efitnumber=str(values["-efitrun-"])
    filt=float(values["-filter-"])
    bdarange=float(values["-bdarange-"])
    if values["-P2.3-"]== True : Program_configuration='P2.3'
    if values["-P238-"]== True : Program_configuration='P238'
    if values["-V238-"]== True : Program_configuration='V238'
    if values["-FE23-"]== True : Program_configuration='FE23'
    if values["-MCT_-"]== True : Program_configuration='MCT_'
    if values["-efit-"]== True :efit=1 
    if values["-ifBND-"]== True :ifBND=1 
    if values["-PFIT-"]== True :pfit=1 
    if values["-ifPSU-"]== True :ifPSU=1 # =1 Coil currents from PSU.PFNAME:I, =0 Coil currents from PSU2PF.I_PSU_BEST
    if values["-ifNIR-"]== True :ifNIR=1
    if values["-ifSMM-"]== True :ifSMM=1
    if values["-ifNBI1-"]== True :ifNBI=1
    if values["-ifNBI2-"]== True :ifNBI=2
    if values["-ifNBI3-"]== True :ifNBI=-1
    if values["-ifNBI-"]== False :ifNBI=0
    if values["-ifXRCS-"]== True :ifXRCS=1
    if values["-ifAR-"]== True :ifAr=1
    if values["-ifSym-"]== True :ifSym=1 # 0 BVUT&BVUB; 1 (BVUT+BVUB)/2 
    if values["-ifTSALL-"]== True :ifTS=1
    if values["-ifTSHFS-"]== True :ifTSHFS=1
    if values["-ifTSLFS-"]== True :ifTSLFS=1
    if values["-ifHDA-"]== True :ifHDA=1
    if values["-ifBDA-"]== True :ifBDA=1
    if values["-ifTRANSP-"]== True :ifTRANSP=1
    if values["-ifTWSTi-"]== True :ifTWSTi=1
    if values["-ifTWSVtor-"]== True :ifTWSVtor=1
    if values["-ifPITi-"]== True :ifPITi=1
    if values["-ifPIVtor-"]== True :ifPIVtor=1
    if values["-ifDEN-"]== False :ifSMM=0;ifNIR=0
    if values["-ifCXTi-"]== False :ifTWSTi=0;ifPITi=0
    if values["-ifCXVtor-"]== False :ifTWSVtor=0;ifPIVtor=0
    if values["-ifTS-"]== False :ifTS=0;ifTSHFS=0;ifTSLFS=0
    if values["-ifprof-"]== False :ifTS=0;ifTSHFS=0;ifTSLFS=0;ifHDA=0;ifBDA=0;ifTRANSP=0
    if values["-tofile-"]== True :tofile=bool(True)


    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make file":
        print('shotnumber,time1,time2,t1,t2,Program_configuration,efit,efitnumber,pfit,ifBND,ntheta,ifPSU,ifNIR,ifSMM,ifNBI,ifXRCS,ifAr,ifSym,ifTWSTi,ifTWSVtor,ifPITi,ifPIVtor,ifTS,ifTSHFS,ifTSLFS,filter,ifHDA,runHDA,ifBDA,bdarange,ifTRANSP,shotT,runT,tofile')
        print(shotnumber,time1,time2,t1,t2,Program_configuration,efit,efitnumber,pfit,ifBND,ntheta,ifPSU,ifNIR,ifSMM,ifNBI,ifXRCS,ifAr,ifSym,ifTWSTi,ifTWSVtor,ifPITi,ifPIVtor,ifTS,ifTSHFS,ifTSLFS,filt,ifHDA,runHDA,ifBDA,bdarange,ifTRANSP,shotT,runT,tofile)
        m.printout(shotnumber,time1,time2,t1,t2,Program_configuration,efit,efitnumber,pfit,ifBND,ntheta,ifPSU,ifNIR,ifSMM,ifNBI,ifXRCS,ifAr,ifSym,ifTWSTi,ifTWSVtor,ifPITi,ifPIVtor,ifTS,ifTSHFS,ifTSLFS,filt,ifHDA,runHDA,ifBDA,bdarange,ifTRANSP,shotT,runT,tofile)
    
window.close()


# python3 pyt/panel_pcs_sensors.py
import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import pcs_reading_functions as pcs
conn = Connection('192.168.1.7:8000')
r=Tree('astra',13011228).getNode("\\TOP").getChildren().getPath().data() 
g=Tree('astra',13011228).getNode("\\TOP.RUN613.GLOBAL").getNodeWild('*').getPath().data()
run=np.array([])
for i in range(0,len(r)):
    el=r[i][12:20].decode().strip()
    #print(el) 
    run = np.append(run,el)

runs=run.tolist()

combo_style={'size':(20,1)}
nprob=34
n1=30
count=0
prob=np.array([])
psiloop=np.array([])
vloop=np.array([])
for i in range(0,nprob):
          prob=np.append(prob,'B_BPPROBE_'+str(101+i))
probs=prob.tolist()
for i in range(0,n1):
          if i<9:
                    psiloop=np.append(psiloop,'PSI_FLOOP_00'+str(i+1))
          elif i != 27:
                    psiloop=np.append(psiloop,'PSI_FLOOP_0'+str(i+1))
psiloop=np.append(psiloop,'PSI_FLOOP_101')
psiloop=np.append(psiloop,'PSI_FLOOP_201')
psiloop=np.append(psiloop,'PSI_FLOOP_106')
psiloop=np.append(psiloop,'PSI_FLOOP_212')
for i in range(0,len(psiloop)):
    vloop=np.append(vloop,'V'+psiloop[i][3:])
psiloops=psiloop.tolist()
vloops=vloop.tolist()

#rogs=['I_ROG_INIVCHFSTOR'    ,'I_ROG_BVLT'    ,'I_ROG_TFWIRE'    ,'I_ROG_SOLWIRE'    ,'I_ROG_BVUTWIRE'    ,'I_ROG_PSHTWIRE'    ,'I_ROG_DIVTWIRE'    ,'I_ROG_BVLB'    ,'I_ROG_BVLWIRE'    ,'I_ROG_MCWIRE'    ,'I_ROG_BVUBWIRE'    ,'I_ROG_PSHBWIRE'    ,'I_ROG_DIVBWIRE'    ,'I_ROG_HFSPSRB'    ,'I_ROG_INIVC000'    ,'I_ROG_DIVPSRB'    ,'I_ROG_DIVPSRT'    ,'I_ROG_MCB'    ,'I_ROG_INIVC270_SPR'    ,'I_ROG_MCSUP003'    ,'I_ROG_MCT_SPR'    ,'I_ROG_HFSPSRT'    ,'I_ROG_MCT'    ,'I_ROG_GASBFLB'    ,'I_ROG_MCSUP001'    ,'I_ROG_INIVC270'    ,'I_ROG_MCSUP001_SPR'    ,'I_ROG_GASBFLT'    ,'I_ROG_GASBFLT_SPR']
rogs=["ROG_BVLB ","ROG_BVLT ","ROG_BVLWIRE ","ROG_BVUBWIRE ","ROG_BVUTWIRE ","ROG_DIVB ","ROG_DIVBWIRE ","ROG_DIVPSRB ","ROG_DIVPSRT ","ROG_DIVT ","ROG_DIVTWIRE ","ROG_GASBFLB ","ROG_GASBFLT ","ROG_GASBFLT_SPR ","ROG_HFSPSRB ","ROG_HFSPSRT ","ROG_INIVC000 ","ROG_INIVC270 ","ROG_INIVC270_SPR ","ROG_INIVCHFSTOR ","ROG_MCB ","ROG_MCSUP001 ","ROG_MCSUP001_SPR ","ROG_MCSUP003 ","ROG_MCT ","ROG_MCT_SPR ","ROG_MCWIRE ","ROG_PSHBWIRE ","ROG_PSHTWIRE ","ROG_SOLWIRE ","ROG_TFWIRE "]
rogs=[j.strip() for j in rogs]

combobox1=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=probs, **combo_style, enable_events=True, key='-COMBO2-')
combobox3=sg.InputCombo(values=psiloops, **combo_style, enable_events=True, key='-COMBO3-')
combobox31=sg.InputCombo(values=vloops, **combo_style, enable_events=True, key='-COMBO31-')
combobox4=sg.InputCombo(values=rogs, **combo_style, enable_events=True, key='-COMBO4-')
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4)),
           sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")],[sg.T("")],
          [sg.Checkbox('',default=True, key="-exp-"),
           sg.T("ST40 shot ="), sg.Input('11560', size=(6,1),key="-SHOT-")],
          [sg.Checkbox('',default=True, key="-astra-"),sg.T("ASTRA shot="), 
           sg.Input('13011560', size=(8,1),key="-shot-"),
           sg.Button('reread shot',size=(10,1))],
          [sg.T("RUN"),combobox1],
          [sg.T("PROBES"),combobox2],
          [sg.T("PSI_LOOPS"),combobox3],
          [sg.T("V_LOOPS"),combobox31],
          [sg.T("ROGS"),combobox4],
          [sg.T("")],[sg.T("")]]


window = sg.Window('tepcs vs sim_tepcs ', layout, size=(500, 500))
while True:
    event, values = window.read()
    shotst40=int(values["-SHOT-"])
    shotastra=int(values["-shot-"])
    if event == "reread shot":
        r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data()    
        run=np.array([])
        for i in range(0,len(r)):
            el=r[i][12:20].decode().strip()
            print(el) 
            if el[3]  !='0':run = np.append(run,el)
        runs=run.tolist()
        combobox1.Update(values=runs)
    if event == '-COMBO1-' :
        RUN= values['-COMBO1-']
#        print(RUN+':HELP')
        conn.openTree('astra',shotastra)
        text=conn.get(RUN+':HELP')
        print('Comment for '+RUN+':')
        print(text)
    if event == '-COMBO2-' :
        name= values['-COMBO2-']
    if event == '-COMBO3-' :
        name= values['-COMBO3-']
    if event == '-COMBO31-' :
        name= values['-COMBO31-']
    if event == '-COMBO4-' :
        name= values['-COMBO4-']
        name='I_'+name
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
        channel=0
        print(name)
        channel=pcs.sensors_map(name)
        print(channel)
        if channel == 999: print(name,'No such signal in tepcs tree')
        if values["-exp-"]== True and channel != 999: 
            treename='tepcs'
            TIME,VAR=pcs.pcs_readsensors32(shotst40,'',treename,channel,name,count)
            count=count+1
        if values["-astra-"]== True and channel != 999: 
            treename='sim_tepcs'
            TIME,VAR=pcs.pcs_readsensors32(shotastra,RUN,treename,channel,name,count)
            count=count+1
        legend=plt.legend(loc='upper right',fontsize='small')
        plt.show()


window.close()



# python3 pyt/panel_pcs_astra_sensors.py
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
import bpprobe_functions as b
import floop_functions as f
import rog_functions as rog

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
treename='sim_tepcs'
key='prob'
prob=np.array([])
loop=np.array([])
for i in range(0,nprob):
          prob=np.append(prob,'B_BPPROBE_'+str(101+i))
probs=prob.tolist()
for i in range(0,n1):
          if i<9:
                    loop=np.append(loop,'PSI_FLOOP_00'+str(i+1))
          elif i != 27:
                    loop=np.append(loop,'PSI_FLOOP_0'+str(i+1))
loops=loop.tolist()

rogs=['I_ROG_INIVCHFSTOR'    ,'I_ROG_BVLT'    ,'I_ROG_TFWIRE'    ,'I_ROG_SOLWIRE'    ,'I_ROG_BVUTWIRE'    ,'I_ROG_PSHTWIRE'    ,'I_ROG_DIVTWIRE'    ,'I_ROG_BVLB'    ,'I_ROG_BVLWIRE'    ,'I_ROG_MCWIRE'    ,'I_ROG_BVUBWIRE'    ,'I_ROG_PSHBWIRE'    ,'I_ROG_DIVBWIRE'    ,'I_ROG_HFSPSRB'    ,'I_ROG_INIVC000'    ,'I_ROG_DIVPSRB'    ,'I_ROG_DIVPSRT'    ,'I_ROG_MCB'    ,'I_ROG_INIVC270_SPR'    ,'I_ROG_MCSUP003'    ,'I_ROG_MCT_SPR'    ,'I_ROG_HFSPSRT'    ,'I_ROG_MCT'    ,'I_ROG_GASBFLB'    ,'I_ROG_MCSUP001'    ,'I_ROG_INIVC270'    ,'I_ROG_MCSUP001_SPR'    ,'I_ROG_GASBFLT'    ,'I_ROG_GASBFLT_SPR']

combobox1=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=probs, **combo_style, enable_events=True, key='-COMBO2-')
combobox3=sg.InputCombo(values=loops, **combo_style, enable_events=True, key='-COMBO3-')
combobox4=sg.InputCombo(values=rogs, **combo_style, enable_events=True, key='-COMBO4-')
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4)),sg.T("        "), 
           sg.Button('Exit',size=(4,2))],
          [sg.Checkbox('sim_tepcs tree',default=False, key="-sim_tepcs-")],
          [sg.Checkbox('ASTRA tree',default=False, key="-astratree-"),
           sg.Checkbox('Plasma',default=False, key="-plasma-"),
           sg.Checkbox('Vacuum',default=False, key="-vacuum-")],
          [sg.T("ASTRA shot="), sg.Input('13011560', size=(8,1),key="-shot-"),
           sg.Button('reread shot',size=(10,1))],
          [sg.T("RUN"),combobox1],
          [sg.T("PROBES"),combobox2],
          [sg.T("LOOPS"),combobox3],
          [sg.T("ROGS"),combobox4],
          [sg.T("")],[sg.T("")]]


window = sg.Window('Sensors from PCS vs ASTRA tree ', layout, size=(715, 500))
while True:
    event, values = window.read()
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
        runnumber=int(RUN[3:])
        RUNv='RUN0'+str(runnumber)
        RUNp='RUN'+str(runnumber)

    if event == '-COMBO2-' :
        name= values['-COMBO2-']
        key='prob'
    if event == '-COMBO3-' :
        name= values['-COMBO3-']
        key='loop'
    if event == '-COMBO4-' :
        name= values['-COMBO4-']
        key='rog'
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
        print(values["-sim_tepcs-"],values["-astratree-"])
        print(key,name)
        if values["-sim_tepcs-"] == True:
            channel=0
            channel=pcs.sensors_map(name)
            TIME,VAR=pcs.pcs_readsensors32(shotastra,RUN,treename,channel,name,count)
            count=count+1
        if values["-astratree-"] == True:
            if key=='prob':
                name0=name[2:]
                index=b.bpprobe_map(shotastra,RUNv,name0)
                if index ==999:exit()
                if values["-vacuum-"]== True : 
                    b.plot_bpprobe_astra_all0(shotastra,RUNv,name0,index,count)
                if values["-plasma-"]== True : 
                    b.plot_bpprobe_astra_all0(shotastra,RUNp,name0,index,count) 
            if key=='loop':
                name0=name[4:]
                index=f.floop_map(shotastra,RUNv,name0)
                if values["-vacuum-"]== True : 
                    f.plot_floop_astra_all0(shotastra,RUNv,name0,index,count)
                if values["-plasma-"]== True : 
                    f.plot_floop_astra_all0(shotastra,RUNp,name0,index,count) 
            if key=='rog':
                name0=name[2:]
                print(values["-vacuum-"],values["-plasma-"])
                if values["-vacuum-"]== True : 
                    rog.plot_rogname_astra_all(name0,shotastra,RUNv)
                if values["-plasma-"]== True : 
                    rog.plot_rogname_astra_all(name0,shotastra,RUNp)
            count=count+1
        legend=plt.legend(loc='upper left',fontsize='small')
        plt.show()


window.close()



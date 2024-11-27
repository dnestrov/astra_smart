# python3 pyt/panel_plot_prof.py
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
import plot_run_prof_fill as fill
import read_transp as transp
conn = Connection('192.168.1.7:8000')
r=Tree('astra',13011228).getNode("\\TOP").getChildren().getPath().data() 
g=Tree('astra',13011228).getNode("\\TOP.RUN613.PROFILES.ASTRA").getNodeWild('*').getPath().data()
run=np.array([])
for i in range(0,len(r)):
    el=r[i][12:20].decode().strip()
    #print(el) 
    run = np.append(run,el)

runs=run.tolist()
leng=12
var=np.array([])
num=g[0].decode().strip().find('S.ASTRA') 
for i in range(0,len(g)-1):
    el=g[i].decode().strip()[num+8:num+8+leng] 
    #print(el) 
    if(el != 'HELP'):var = np.append(var,el)

variables=var.tolist()
combo_style={'size':(12,1)}
combobox1=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO2-')
combobox3=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO3-')
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4))], [sg.T("")],
          [sg.T("ASTRA shot="), sg.Input('13011228', size=(8,1),key="-shot-"),
           sg.Button('reread shot',size=(10,1))],
          [sg.T("RUN"),combobox1,sg.Button('reread ASTRA names',size=(10,1)),
           sg.Button('HELPrun',size=(10,1))],
          [sg.T("ASTRA Profiles"),combobox2,sg.Button('HELP prof',size=(12,1))],
          [sg.T("TRANSP shot="), sg.Input('34011560', size=(8,1),key="-shotT-"),
           sg.T("TRANSP run"), sg.Input('T06', size=(5,1), key="-runT-"),
           sg.Button('reread TRANSP names',size=(10,1))],
          [sg.T("TRANSP Profiles"),combobox3],
          [sg.T("time1="), sg.Input('0.07', size=(7,1), key="-time1-"),
           sg.T("time2="), sg.Input('0.08', size=(7,1), key="-time2-")],
          [sg.T("")],[sg.T("")],
          [sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")]]

window = sg.Window('Plot profiles', layout, size=(715, 500))
while True:
    event, values = window.read()
    shotastra=int(values["-shot-"])
    shottransp=int(values["-shotT-"])
    runT=values["-runT-"]
    time1=float(values["-time1-"])
    time2=float(values["-time2-"])
    if event == "reread shot":
        r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data()    
        run=np.array([])
        for i in range(0,len(r)):
            el=r[i][12:20].decode().strip()
            print(el) 
            if el[3] !='0':run = np.append(run,el)
        runs=run.tolist()
        combobox1.Update(values=runs)
    if event == '-COMBO1-' :
        RUN= values['-COMBO1-']
        conn.openTree('astra',shotastra)
        text=conn.get(RUN+':HELP')
        print('Comment for '+RUN+':')
        print(text)
    if event == '-COMBO2-' :
        prof= values['-COMBO2-']
        conn.openTree('astra',shotastra)
        print(RUN+'.PROFILES.ASTRA.'+prof+':HELP')
        text=conn.get(RUN+'.PROFILES.ASTRA.'+prof+':HELP')
        print(prof+':')
        print(text)
    if event == "reread ASTRA names":
        var=np.array([])
        g=Tree('astra',shotastra).getNode("\\TOP."+RUN+".PROFILES.ASTRA").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('S.ASTRA') 
        for i in range(0,len(g)):
            el=g[i].decode().strip()[num+8:num+8+leng] 
            print(el)
            if(el != 'HELP'):var = np.append(var,el)
        variables=var.tolist()
        combobox2.Update(values=variables)
    if event == '-COMBO3-' :
        prof= values['-COMBO3-']
        conn.openTree('TRANSP_TEST',shottransp)
        print(RUN+'.PROFILES.ASTRA.'+prof+':HELP')
        text=conn.get(RUN+'.PROFILES.'+prof+':HELP')
        print(prof+':')
        print(text)
    if event == "reread TRANSP names":
        var=np.array([])
        g=Tree('TRANSP_TEST',shottransp).getNode("\\TOP."+RUN+".PROFILES.RHOTOR").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('S.RHOTOR') 
        for i in range(0,len(g)):
            el=g[i].decode().strip()[num+9:]#num+8+leng] 
            print(el)
            var = np.append(var,el)
        variables=var.tolist()
        combobox3.Update(values=variables)
    if event == "HELPrun":
        r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data()
        for i in range(0,len(r)):
            run=r[i][12:20].decode().strip()
            print(run+':HELP')
            if(run != 'HELP'):
                text=conn.get(run+':HELP')
                print(run+': ',text)
    if event == "HELP prof":
        g=Tree('astra',shotastra).getNode("\\TOP."+RUN+".PROFILES.ASTRA").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('S.ASTRA') 
        conn.openTree('astra',shotastra)
        for i in range(0,len(g)):
            prof=g[i].decode().strip()[num+8:num+8+leng] 
            print(RUN+'.PROFILES.ASTRA.'+prof+':HELP')
            if(prof != 'HELP'):
                text=conn.get(RUN+'.PROFILES.ASTRA.'+prof+':HELP')
                print(prof+': ',text)
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
      print(RUN,prof)
      fill.plot_fill(shotastra,prof,RUN,time1,time2)
      try:
          TIME.bit_length()
      except:
          plt.xlabel('rho_tor',fontsize=15)
          legend=plt.legend(loc='upper right',fontsize='small')
          plt.show()



window.close()



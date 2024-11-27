# python3 pyt/panel_ivc_astra.py&
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import passives_functions as a
col=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf']
nl=15
nr=10
shotelmag=206
count=0;count1=0
name='IVC_1T'
NAME=["IVC","IVC_OUT60","IVC_1T","IVC_1B","IVC_12_thickT","IVC_12_thickB","IVC_2T","IVC_2B","IVC_23_thickT","IVC_23_thickB","IVC_3T","IVC_3B","IVC_34_thickT","IVC_34_thickB","IVC_4T","IVC_4B","IVC_4_supportT","IVC_4_supportB","IVC_45_thickT","IVC_45_thickB","IVC_5T","IVC_5B","OVC","BVLTCASE","BVLBCASE","ERINGT","ERINGB","DIVTCASE","DIVBCASE","MCTCASE","MCBCASE","DIVPSRT","DIVPSRB","HFSPSRT","HFSPSRB","GASBFLB","GASBFLT"]
combo_style={'size':(12,1)}
combobox1=sg.InputCombo(values=NAME, **combo_style, enable_events=True, key='-COMBO1-')
layout = [[sg.Button('Exit',size=(4,2))],
          [sg.T("ASTRA shot="),sg.Input('13011717', size=(8,1),key="-shot-"),
           sg.T("ASTRA run"),sg.Input('3', size=(5,1), key="-run-"),
           sg.T("ASTRA device"),sg.Input('EFIT', size=(5,1), key="-machin-"),
           sg.T("time"),sg.Input('-0.1', size=(5,1), key="-time-")],
          [sg.T("filament structure"),combobox1,sg.T("resistivity factor"),sg.Input('1', size=(4,1),key="-factor-")],
          [sg.Button('start from fires0.dat',size=(20,4))],
          [sg.Button('modify fires.dat',size=(20,4))],
          [sg.Button('plot currents',size=(20,4))],
          [sg.Button("plot filaments",size=(20,2))],
          [sg.Button("New figure",size=(20,2))]]


###Setting Window
window = sg.Window('modify fires.dat', layout, size=(700,600))

while True:
          event, values = window.read()
          if event == sg.WIN_CLOSED or event=="Exit":
                    break          
          shot=int(values["-shot-"])
          run=str(values["-run-"])
          
          machin=str(values["-machin-"])
          time=float(values["-time-"])
          RUN='RUN'+str(run)
          if time < 0.009 :  RUN='RUN0'+str(run)
          factor=float(values["-factor-"])
          if event == '-COMBO1-' :
                    name=values['-COMBO1-']
                    
          if event == 'start from fires0.dat':
                    R,Z,dr,dz,resp,names=a.read_rz_file0(machin)
                    for i in range(0,len(names)):
                              if names[i]==name:
                                        resp[i]=factor*resp[i]
                    a.write_rz_file(machin,R,Z,dr,dz,resp,names)
                    print('cp fires0.dat fires.dat')
                    print('resistance for ',name, 'multiplied by ',factor)
          if event == 'modify fires.dat':
                    R,Z,dr,dz,resp,names=a.read_rz_file(machin)
                    for i in range(0,len(names)):
                              if names[i]==name:
                                        resp[i]=factor*resp[i]
                    a.write_rz_file(machin,R,Z,dr,dz,resp,names)
                    print('resistance for ',name, 'multiplied by ',factor)
  
          if event == 'plot currents':
                    TIME,VAR=a.read_passive_time(name,shot,RUN)
                    plt.plot(TIME,VAR,c=col[count],label='#'+str(shot)+'@'+RUN+',name='+name)
                    count+=1
                    if count > 30: count=0                    
                    plt.suptitle('Current in filament structure')
                    legend=plt.legend(loc='upper right',fontsize='small')
                    plt.show()

          if event== "plot filaments":
                    try:
                              R
                    except:
                              R,Z,dr,dz,resp,NAME1=a.read_rz_file(machin)
                    ind=np.array([])
                    print(NAME1)
                    nl=len(NAME1)
                    for i in range(0,nl):
                              if NAME1[i] == name: ind = np.append(ind,i)
                    index=ind.astype(int)
                    fig=plt.figure(100)
                    plt.plot(R[index],Z[index],linestyle='',c=col[count1],marker='+',label=machin+'@'+name)
                    count1+=1
                    if count1 > 30: count1=0                    
                    legend=plt.legend(loc='upper right',fontsize='small')
                    plt.show()
window.close()

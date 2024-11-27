# python3 pyt/panel_ivc.py&
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import passives_EFIT as e
col=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf']
nl=15
nr=10
shotelmag=206
NAME=["'_IVC_1'","'IVC_12_thick'","'IVC_2'","'IVC_23_thick'","'IVC_3'","'IVC_34_thick'","'IVC_4'","'IVC_4_support'","'IVC_45_thick'","'IVC_5'"]
layout = [[sg.Button('Exit',size=(4,2))],
          [sg.T("EFIT shot="),sg.Input('11560', size=(8,1),key="-shotE-"),
           sg.T("EFIT run"),sg.Input('BEST', size=(5,1), key="-runE-"),
           sg.T("EFIT time"),sg.Input('0.1', size=(5,1), key="-timeE-")],
          [sg.Checkbox('IVC',default=True, key="-IVC-")],
          [sg.Checkbox('1',default=False, key="-1-"),sg.Checkbox('2',default=False, key="-2-"),
           sg.Checkbox('3',default=False, key="-3-"),sg.Checkbox('4',default=False, key="-4-"),
           sg.Checkbox('5',default=False, key="-5-")],
          [sg.Checkbox('6',default=False, key="-6-"),sg.Checkbox('7',default=False, key="-7-"),
           sg.Checkbox('8',default=False, key="-8-"),sg.Checkbox('9',default=False, key="-9-"),
           sg.Checkbox('10',default=False, key="-10-")],
          [sg.Checkbox('11',default=False, key="-11-"),sg.Checkbox('12',default=False, key="-12-"),
           sg.Checkbox('13',default=False, key="-13-"),sg.Checkbox('14',default=False, key="-14-"),
           sg.Checkbox('15',default=False, key="-15-")],
          [sg.Button('make Basis plot',size=(20,4)),sg.Button('make Basis*DOF plot',size=(20,4)),
           sg.Button('make Basis*DOF/dr/dz plot',size=(20,4))],
          [sg.Checkbox(NAME[0],default=True, key="-r0-"),sg.Checkbox(NAME[1],default=True, key="-r1-")],
          [sg.Checkbox(NAME[2],default=True, key="-r2-"),sg.Checkbox(NAME[3],default=True, key="-r3-")],
          [sg.Checkbox(NAME[4],default=True, key="-r4-"),sg.Checkbox(NAME[5],default=True, key="-r5-")],
          [sg.Checkbox(NAME[6],default=True, key="-r6-"),sg.Checkbox(NAME[7],default=True, key="-r7-")],
          [sg.Checkbox(NAME[8],default=True, key="-r8-"),sg.Checkbox(NAME[9],default=True, key="-r9-")],
          [sg.Button('plot reordered',size=(20,4))],
          [sg.Button("plot EFIT filaments",size=(20,2))],
          [sg.Button("New figure",size=(20,2))]]

###Setting Window
window = sg.Window('Basis functions', layout, size=(700,600))

while True:
          event, values = window.read()
          if event == sg.WIN_CLOSED or event=="Exit":
                    break          
          shotefit=int(values["-shotE-"])
          runefit=str(values["-runE-"])
          timeefit=float(values["-timeE-"])
          ivc=False
          if values["-IVC-"] == True : ivc=True
          index=np.array([])
          for i in range(1,nl+1):
                    if values["-"+str(i)+"-"]== True : index=np.append(index,i)
          ind=index.astype(int)
          indexr=np.array([])
          for i in range(0,nr):
                    if values["-r"+str(i)+"-"]== True : indexr=np.append(indexr,i)
          indr=indexr.astype(int)
          if event== "make Basis plot":
                    try:
                              count
                              count+=1
                    except:
                              count=0
                    try:
                              Re
                    except:
                              Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
                    try:
                              ax
                    except:                              
                              fig=plt.figure(1)
                              ax = fig.add_subplot(111,projection='3d')
                    e.plot_basis(ax,Re,Ze,dre,dze,VAR,ivc,ind,shotefit,runefit,timeefit,count)                    
                    if ivc : plt.legend(loc='upper left',fontsize='small')
                    plt.show()
          if event== "make Basis*DOF plot":
                    try:
                              count
                              count+=1
                    except:
                              count=0
                    try:
                              Re
                    except:
                              Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
                    try:
                              ax
                    except:                              
                              fig=plt.figure(1)
                              ax = fig.add_subplot(111,projection='3d')
                    e.plot_ivc(ax,Re,Ze,dre,dze,VAR,ivc,ind,shotefit,runefit,timeefit,count)                    
                    if ivc : plt.legend(loc='upper left',fontsize='small')
                    plt.show()
          if event== "make Basis*DOF/dr/dz plot":
                    try:
                              count
                              count+=1
                    except:
                              count=0
                    try:
                              Re
                    except:
                              Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
                    try:
                              ax
                    except:                              
                              fig=plt.figure(1)
                              ax = fig.add_subplot(111,projection='3d')
                    e.plot_ivc_dens(ax,Re,Ze,dre,dze,VAR,ivc,ind,shotefit,runefit,timeefit,count)                    
                    if ivc : plt.legend(loc='upper left',fontsize='small')
                    plt.show()
          if event== "plot EFIT filaments":
                    try:
                              Re
                    except:
                              Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
                    try:
                              ax
                    except:
                              
                              fig=plt.figure(1)
                              ax = fig.add_subplot(111,projection='3d')
                    ax.scatter(Re,Ze,Re*0,c='black',marker='x')
                    plt.show()
          if event== "New figure":
                    try:
                              fig=plt.figure(1)
                              ax = fig.add_subplot(111,projection='3d')
                    except:
                              pass
          if event== 'plot reordered':
                    print(indr)
                    ind0,NAME9=e.read_IVC_names(indr)

                    try:
                              Re
                    except:
                              Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
                    try:
                              ncol
                              ncol+=1
                    except:
                              ncol=0
                    print(ind0,len(ind0))
                    e.read_ivc_current(Re,Ze,dre,dze,VAR,indr,shotefit,runefit,timeefit)
                    fig=plt.figure(2)
                    plt.plot(Re[ind0],Ze[ind0],linestyle='',color=col[ncol],marker='+',label=NAME9)
                    plt.legend(loc='upper left',fontsize='small')
                    plt.show()
window.close()

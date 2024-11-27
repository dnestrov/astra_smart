# python3 pyt/panel_voltages.py
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import voltages_functions as v
PSUASTRA=['DIV','BVL','BVUT','BVUB','CS','MC','PSH']
PSUST40=['DIV','BVL','BVUT','BVUB','SOL','MC','PSH']

layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4))], [sg.T("")],
          [sg.Checkbox('',default=True, key="-exp-"),
           sg.T("ST40 shot ="), sg.Input('11560', size=(6,1),key="-SHOT-")],
          [sg.Checkbox('Plasma',default=False, key="-plasma-"),
           sg.Checkbox('Vacuum',default=False, key="-vacuum-")],
          [sg.T("ASTRA shot="), sg.Input('13000025', size=(8,1),key="-shot-"),
           sg.T("ASTRA run"), sg.Input('105', size=(5,1), key="-run-")],
          [sg.Checkbox('DIV',default=True, key="-DIV-")],
          [sg.Checkbox('BVL',default=True, key="-BVL-")],
          [sg.Checkbox('BVUT',default=True, key="-BVUT-")],
          [sg.Checkbox('BVUB',default=True, key="-BVUB-")],
          [sg.Checkbox('SOL',default=True, key="-SOL-")],
          [sg.Checkbox('MC',default=False, key="-MC-")],
          [sg.Checkbox('PSH',default=False, key="-PSH-")],
          [sg.T("")],[sg.T("")],
          [sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")]]

    #[sg.Checkbox('',default=True, key="--")],
    


###Setting Window
window = sg.Window('coil voltages', layout, size=(600,600),keep_on_top=False)

###Showing the Application, also GUI functions can be placed here.
while True:
    event, values = window.read()
    shotst40=int(values["-SHOT-"])
    shotastra=int(values["-shot-"])
    runnumber=int(values["-run-"])
    RUNv='RUN0'+str(runnumber)
    RUNp='RUN'+str(runnumber)
    index=np.array([])
    if values["-DIV-"]== True : index=np.append(index,1)
    if values["-BVL-"]== True : index=np.append(index,2)
    if values["-BVUT-"]== True : index=np.append(index,3)
    if values["-BVUB-"]== True : index=np.append(index,4)
    if values["-SOL-"]== True : index=np.append(index,5)
    if values["-MC-"]== True : index=np.append(index,6)
    if values["-PSH-"]== True : index=np.append(index,7)

    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
        ind=index.astype(int)
        index=np.append(index,1)
        names=np.array([])
        for j in range(len(ind)):
            names=np.append(names,PSUASTRA[ind[j]-1])
        t1=0.5;t2=-1;t3=0.5;t4=-1
        if values["-exp-"]== True : 
            if values["-vacuum-"]== True : 
                t1,t2=v.astra_t1_t2(shotastra,RUNv)
            tmin=min(t1,t2)
            if values["-plasma-"]== True : 
                t1,t1=v.astra_t1_t2(shotastra,RUNp)
            tmax=max(t1,t2)
            print(tmin,tmax)
            v.plot_voltages_exp(shotst40,ind,tmin,tmax)
        if values["-vacuum-"]== True : 
            count=v.plot_voltages_astra(shotastra,RUNv,ind)
            if count == -1:
                count=v.plot_voltages_astra_all(shotastra,RUNv,names)
        if values["-plasma-"]== True : 
            count=v.plot_voltages_astra(shotastra,RUNp,ind)
            if count == -1:
                count=v.plot_voltages_astra_all(shotastra,RUNp,names)
        plt.legend(loc='upper left',fontsize='small')
        plt.show()


window.close()


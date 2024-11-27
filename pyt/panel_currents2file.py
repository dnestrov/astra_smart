# python3 pyt/panel_mds_tree.py
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import allcurrents_functions as a

layout = [[sg.T("")],
          [sg.T("        "), sg.Button('write file',size=(20,4))], [sg.T("")],
          [sg.T("coil config    "), 
           sg.Radio('P2.3', "RADIO1", default=True, key="-P2.3-"),
           sg.Radio('FE23', "RADIO1", default=False, key="-FE23-"),
           sg.Radio('EFSO', "RADIO1", default=False, key="-EFSO-")],
          [sg.T("Choose tree"),
           sg.Radio('ASTRA', "RADIO3", default=True, key="-astra-"),
           sg.Radio('SOPHIA', "RADIO3", default=False, key="-sophia-")],
          [sg.T("SHOT number="), sg.Input('11417', size=(6,1),key="-SHOT-"),
           sg.T("Range="), sg.Input('13000000', size=(8,1),key="-Range-"),
           sg.T("RUN"), sg.Input('1', size=(5,1), key="-RUN-"),
           sg.T("TIME"), sg.Input('0.009', size=(5,1), key="-time-")],
          [sg.Radio('Vacuum', "RADIO2", default=True, key="-ifVac-"),
           sg.Radio('Plasma', "RADIO2", default=False, key="-ifPla-")],
          [sg.Checkbox('Zero passivess',default=False, key="-zeros-")],
          [sg.T("")],[sg.T("")],
          [sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")]]
###Setting Window
window = sg.Window('write currents.dat to start ASTRA with all passives', layout, size=(600,600))

###Showing the Application, also GUI functions can be placed here.
while True:
    event, values = window.read()
    if values["-P2.3-"]== True : machin='exp/equ/P2.3'
    if values["-FE23-"]== True : machin='exp/equ/FE23'
    if values["-EFSO-"]== True : machin='exp/equ/EFSO'
    if values["-astra-"]== True : treename='ASTRA'
    if values["-sophia-"]== True : treename='SOPHIA'
    shotnumber=int(values["-SHOT-"])
    rang=int(values["-Range-"])
    runnumber=int(values["-RUN-"])
    time=float(values["-time-"])
    RUNv='RUN0'+str(runnumber)
    RUNp='RUN'+str(runnumber)
    zeros=values["-zeros-"]
    if treename == 'SOPHIA':RUNv=RUNp

    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "write file":
        if values["-ifVac-"]== True :          
            a.write_cur(treename,True,machin,rang+shotnumber,RUNv,time,zeros)
        if values["-ifPla-"]== True : 
            a.write_cur(treename,False,machin,rang+shotnumber,RUNp,time,zeros)
window.close()


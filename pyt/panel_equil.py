# python3 pyt/panel_equil.py
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import ll_astra as ll

layout = [[sg.Button('plot psi',size=(10,2)),
           sg.Checkbox('cur text', default=True, key="-curtext-"),
           sg.Button('Exit',size=(4,2))],
          [sg.T("Working dir   "), 
           sg.Radio('P2.3', "RADIO1", default=False, key="-P2.3-"),
           sg.Radio('FE23', "RADIO1", default=False, key="-FE23-"),
           sg.Radio('FPP1', "RADIO1", default=True, key="-FPP1-")],
          [sg.T("")]]
###Setting Window
window = sg.Window('Plot equilibrium', layout, size=(600,100))

###Showing the Application, also GUI functions can be placed here.
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    curtext=False
    if values["-curtext-"]== True : curtext=True
    if values["-P2.3-"]== True : WK='exp/equ/P2.3'
    if values["-FE23-"]== True : WK='exp/equ/FE23'
    if values["-FPP1-"]== True : WK='exp/equ/FPP1'
    if event== "plot psi":
        print(WK)
        ll.plot_psi(WK,curtext,True,'')
window.close()


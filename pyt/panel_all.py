# python3 pyt/panel_all.py&
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env

layout = [[sg.T("Preparation for ASTRA run"),
           sg.T("                                                   "), sg.Button('Exit',size=(4,2))],
          [sg.Button('make exp')],
          [sg.Button('mds tree'),sg.T("Make MDS+ tree for ASTRA result record")],
          [sg.Button('plot equil'),sg.Button('write currents.dat'),
           sg.T("write currents.dat to start ASTRA with all passives")],
          [sg.T("ST40 and ASTRA result analysis")],
          [sg.Button('ASTRA glob time'),sg.T("Plot global variables from ASTRA result record in MSD+")],
          [sg.Button('ASTRA prof time'),sg.T("Plot profiles from ASTRA result record in MSD+")],
          [sg.Button('EXP glob time'),
           sg.Button('EXP and ASTRA glob time')],
          [sg.Button('EXP and ASTRA XY 1'),
           sg.Button('EXP and ASTRA XY 2')],
          [sg.T("SOPHIA results analysis"),sg.Button("pcs vs mag")],
          [sg.T("ACT vs REF:"),sg.Button("calc"),sg.Button("exp"),sg.Button("calc vs exp")],
          [sg.T("EXP vs SOPHIA:")],
          [sg.T("MAG tree:"),sg.Button('bpprobes'),sg.Button('floops'),sg.Button('rogowskis'),
           sg.Button('exp-calc'),sg.Button('coilcurrents'),sg.Button('voltages')],
          [sg.T("TEPCS tree:"),sg.Button("pcs_sensors")],
          [sg.T("ASTRA vs EFIT:"),sg.Button("CHI^2"),
           sg.Button('passives'),sg.Button("modify fires.dat")]]


    #[sg.Checkbox('',default=True, key="--")],
    


###Setting Window
window = sg.Window('All panels', layout, size=(700,600),keep_on_top=False)

###Showing the Application, also GUI functions can be placed here.
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit": break
    if event== "bpprobes":os.system("python3 pyt/panel_bpprobes.py&")
    if event== "floops":os.system("python3 pyt/panel_floops.py&")
    if event== "mds tree":os.system("python3 pyt/panel_mds_tree.py&")
    if event== "plot equil":os.system("python3 pyt/panel_equil.py&")
    if event== "write currents.dat":os.system("python3 pyt/panel_currents2file.py&")
    if event== "rogowskis":os.system("python3 pyt/panel_rogowskis.py&")
    if event== "coilcurrents":os.system("python3 pyt/panel_coilcurrents.py&")
    if event== "make exp":os.system("python3 pyt/panel_make_exp.py&")
    if event== "ASTRA glob time":os.system("python3 pyt/panel_plot_glob.py&")
    if event== "ASTRA prof time":os.system("python3 pyt/panel_plot_prof_x.py&")
    if event== "voltages":os.system("python3 pyt/panel_voltages.py&")
    if event== "passives":os.system("python3 pyt/panel_passives.py&")
    if event== "EXP glob time":os.system("python3 pyt/panel_plot_glob_exp.py&")
    if event== "EXP and ASTRA glob time":os.system("python3 pyt/panel_plot_glob2.py&")
    if event== "EXP and ASTRA XY 1":os.system("python3 pyt/panel_plot_glob_exp_shotlist.py&")
    if event== "EXP and ASTRA XY 2":os.system("python3 pyt/panel_plot_global_shotlist.py&")
    if event== "pcs_sensors":os.system("python3 pyt/panel_pcs_sensors.py&")
    if event== "pcs vs mag":os.system("python3 pyt/panel_pcs_astra_sensors.py&")
    if event== "calc":os.system("python3 pyt/panel_calc_refvsact.py&")
    if event== "exp":os.system("python3 pyt/panel_exp_refvsact.py&")
    if event== "calc vs exp":os.system("python3 pyt/panel_calcexp_refvsact.py&")
    if event== "CHI^2":os.system("python3 pyt/panel_chi2.py&")
    if event== "modify fires.dat":os.system("python3 pyt/panel_ivc_astra.py&")
    if event== "exp-calc":os.system("python3 pyt/panel_chi.py&")
window.close()


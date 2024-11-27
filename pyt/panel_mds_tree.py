# python3 pyt/panel_mds_tree.py
import numpy as np
from MDSplus import *
import math
import sys
import vac_astra_tree as vacuu
import st40_astra_tree as astra
import spider_tree as spider
import sophia_tree as sophia
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env

conn = Connection('192.168.1.7:8000')
layout = [[sg.Button('make ASTRA tree',size=(20,4)),
           sg.T("                                "), sg.Button('Exit',size=(4,2))], 
          [sg.Button('make SPIDER tree',size=(20,4))],
          [sg.Button('make ASTRA nodes in SOPHIA tree',size=(30,4))],
          [sg.Radio('create', "RADIO1", default=True, key="-create-"),
           sg.Radio('modify help', "RADIO1", default=False, key="-modify-"),
           sg.Radio('delete', "RADIO1", default=False, key="-delete-")],
          [sg.T("SHOT number="), sg.Input('26', size=(6,1),key="-SHOT-"),
           sg.T("Range="), sg.Input('13000000', size=(8,1),key="-Range-"),
           sg.T("RUN"), sg.Input('1', size=(5,1), key="-RUN-")],
          [sg.Button('Read ASTRA RUNS',size=(10,2)),
           sg.Button('Read SPIDER RUNS',size=(10,2)),
           sg.Button('Read SOPHIA RUNS',size=(10,2))],
          [sg.T("help:"), sg.Input('run help', size=(100,1), key="-help-")],
          [sg.Checkbox('Vacuum', default=True, key="-ifVac-"),
           sg.Checkbox('Plasma', default=True, key="-ifPla-")],
          [sg.T("")]]
###Setting Window
window = sg.Window('MDS trees for ASTRA, SPIDER and SOPHIA', layout, size=(600,500))

###Showing the Application, also GUI functions can be placed here.
while True:
    ok=False
    event, values = window.read()
    shotnumber=int(values["-SHOT-"])
    rang=int(values["-Range-"])
    runnumber=int(values["-RUN-"])
    text=str(values["-help-"])
    RUNv='RUN0'+str(runnumber)
    RUNa='RUN'+str(runnumber)

    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make ASTRA tree":
        if values["-create-"]== True :         
            if values["-ifVac-"]== True : 
                ok=vacuu.create(rang+shotnumber,RUNv,text)
                if ok:print('Vacuum tree created',rang+shotnumber,RUNv,text)
                if not ok:print('done nothing')
            if values["-ifPla-"]== True : 
                ok=astra.create(rang+shotnumber,RUNa,text)
                if ok:print('ASTRA tree created',rang+shotnumber,RUNa,text)
                if not ok:print('done nothing')
        if values["-modify-"]== True :         
            if values["-ifVac-"]== True : vacuu.modifyhelp(rang+shotnumber,RUNv,text)
            if values["-ifPla-"]== True : astra.modifyhelp(rang+shotnumber,RUNa,text)
        if values["-delete-"]== True :         
            if values["-ifVac-"]== True : 
                vacuu.delete(rang+shotnumber,RUNv)
                print('Vacuum tree deleted',rang+shotnumber,RUNv)
            if values["-ifPla-"]== True : 
                astra.delete(rang+shotnumber,RUNa)
                print('ASTRA tree deleted',rang+shotnumber,RUNa)
    elif event== "make SPIDER tree":
        if values["-create-"]== True :         
            ok=spider.create(rang+shotnumber,RUNa,text)
            if ok:print('SPIDER tree created',rang+shotnumber,RUNa,text)
            if not ok:print('done nothing')
        if values["-modify-"]== True : spider.modifyhelp(rang+shotnumber,RUNa,text)
        if values["-delete-"]== True : 
            spider.delete(rang+shotnumber,RUNa)
            print('SPIDER tree deleted',rang+shotnumber,RUNa)
    elif event== "make ASTRA nodes in SOPHIA tree":
        if values["-create-"]== True :         
            ok=sophia.create(rang+shotnumber,RUNa)
            if ok : print('ASTRA nodes in SOPHIA tree are created for ',rang+shotnumber,RUNa)
            if not ok : print('ASTRA nodes in SOPHIA tree are NOT created for ',rang+shotnumber,RUNa)
        if values["-delete-"]== True : 
            ok=sophia.delete(rang+shotnumber,RUNa)
            if ok :print('SOPHIA tree deleted',rang+shotnumber,RUNa)
            if not ok :print('SOPHIA tree does NOT deleted',rang+shotnumber,RUNa)
    if event== "Read ASTRA RUNS":treename="astra"
    if event== "Read SPIDER RUNS":treename="spider"
    if event== "Read SOPHIA RUNS":treename="sophia"
    if event== "Read ASTRA RUNS" or event== "Read SPIDER RUNS" or event== "Read SOPHIA RUNS":    
        try:
            conn.openTree(treename,rang+shotnumber)
        except:
            print(treename,':  no runs for shot ',rang+shotnumber)
            continue
        
        r=Tree(treename,rang+shotnumber).getNode("\\TOP").getChildren().getPath().data()  
        run=np.array([])
        n1=13
        if treename == "astra": n1=12
        for i in range(0,len(r)):
            el=r[i][n1:20].decode().strip()
            run = np.append(run,el)
        runs=run.tolist()
        print(treename.upper(),rang+shotnumber)
        for i in range(0,len(run)):
            try:
                text=conn.get(run[i]+':HELP')
            except:
                text='no help text'
            print(runs[i])
            print(text)
         

window.close()


# python3 pyt/panel_passives.py
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import passives_functions as p
import passives_EFIT as e
NAME=["MCT","MCB","DIVT","DIVB","ERINGT","ERINGB","BVLT","BVLB","OVC","DIVPSRT","DIVPSRB","HFSPSRT","HFSPSRB"]
nl=len(NAME)
shotelmag=206
layout = [[sg.T("ASTRA shot="), sg.Input('13011560', size=(8,1),key="-shot-"),
           sg.T("ASTRA run"), sg.Input('206', size=(5,1), key="-run-"),
           sg.T("time"), sg.Input('0.1', size=(5,1), key="-time-"),
           sg.T("ASTRA device"),sg.Input('EFIT', size=(5,1), key="-machin-"),
           sg.Button('Exit',size=(4,2))],
          [sg.Button('make ASTRA plot',size=(20,4)),sg.Button("overplot another time",size=(20,4)),
           sg.Button("overplot another shot or run",size=(20,4))],
          [sg.T("EFIT shot="), sg.Input('11560', size=(8,1),key="-shotE-"),
           sg.T("EFIT run"), sg.Input('BEST', size=(8,1), key="-runE-"),
           sg.T("EFIT time"), sg.Input('0.1', size=(5,1), key="-timeE-")],
          [sg.Checkbox('IVC',default=True, key="-IVC-")],
          [sg.Checkbox(NAME[0],default=False, key="-0-"),sg.Checkbox(NAME[1],default=False, key="-1-")],
          [sg.Checkbox(NAME[2],default=False, key="-2-"),sg.Checkbox(NAME[3],default=False, key="-3-")],
          [sg.Checkbox(NAME[4],default=False, key="-4-"),sg.Checkbox(NAME[5],default=False, key="-5-")],
          [sg.Checkbox(NAME[6],default=False, key="-6-"),sg.Checkbox(NAME[7],default=False, key="-7-")],
          [sg.Checkbox(NAME[8],default=False, key="-8-")],
          [sg.Checkbox(NAME[9],default=False, key="-9-"),sg.Checkbox(NAME[10],default=False, key="-10-")],
          [sg.Checkbox(NAME[11],default=False, key="-11-"),sg.Checkbox(NAME[12],default=False, key="-12-")],
          [sg.Button('make EFIT plot',size=(20,4)),sg.Button('overplot EFIT',size=(20,4)),
           sg.Button('write currents.dat',size=(20,4))],
          [sg.Button("plot ASTRA filaments",size=(20,2)),sg.Button("plot EFIT filaments",size=(20,2))],
          [sg.Button("New figure",size=(20,2))]]
###Setting Window
window = sg.Window('Passive currents', layout, size=(700,600))

###Showing the Application, also GUI functions can be placed here.
while True:
          event, values = window.read()
          if event == sg.WIN_CLOSED or event=="Exit":
                    break
          shotastra=int(values["-shot-"])
          shotefit=int(values["-shotE-"])
          runnumber=int(values["-run-"])
          runefit=str(values["-runE-"])
          time=float(values["-time-"])
          timeefit=float(values["-timeE-"])
          machin=str(values["-machin-"])
          ivc=False
          if values["-IVC-"] == True : ivc=True
          index=np.array([])
          for i in range(0,nl):
                    if values["-"+str(i)+"-"]== True : index=np.append(index,i)
          ind=index.astype(int)
          if time<0.009:
                    RUN='RUN0'+str(runnumber)
          else:
                    RUN='RUN'+str(runnumber)
          if event== "make ASTRA plot":
                    try:
                              count
                              count+=1
                    except:
                              count=0
                    try:
                              Rp
                    except:
                              RP,ZP,dr,dz,resp,name=p.read_rz_file(machin)
                    try:
                              ax
                    except:                              
                              fig=plt.figure(1)
                              ax = fig.add_subplot(111,projection='3d')
                    TIME,CURRENT=p.plot_passives(ax,RP,ZP,dr,dz,name,shotastra,RUN,time,count)
                    plt.legend(loc='upper left',fontsize='small')                    
                    plt.show()
          if event== "overplot another time":
                    count+=1
                    p.plot_passives_newtime(ax,TIME,RP,ZP,dr,dz,CURRENT,time,count)
                    plt.legend(loc='upper left',fontsize='small')
                    plt.show()
          if event== "overplot another shot or run":
                    count+=1
                    try:
                              fig
                    except:                              
                              fig=plt.figure()
                              ax = fig.add_subplot(111,projection='3d')
                              count=0
                    TIME,CURRENT=p.plot_passives_newshot(ax,RP,ZP,dr,dz,shotastra,RUN,time,count)
                    plt.legend(loc='upper left',fontsize='small')
                    plt.show()

          if event== "make EFIT plot":
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
                              
                              fig=plt.figure()
                              ax = fig.add_subplot(111,projection='3d')
                    e.plot_passives(ax,Re,Ze,dre,dze,VAR,ivc,ind,shotefit,runefit,timeefit,count)                    
                    if ivc : plt.legend(loc='upper left',fontsize='small')
                    plt.show()
          if event== "overplot EFIT":                    
                    count+=1
                    try:
                              Re
                    except:
                              Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
                    e.plot_passives(ax,Re,Ze,dre,dze,VAR,ivc,ind,shotefit,runefit,timeefit,count)
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
                    ax.scatter(Re,Ze,Re*0,c='red',marker='x')
                    plt.show()
          if event== "plot ASTRA filaments":
                    try:
                              Rp
                    except:
                              print(shotastra,RUN)
                              RP,ZP,name=p.read_rz(shotastra,RUN)
                    try:
                              ax
                    except:
                              
                              fig=plt.figure(1)
                              ax = fig.add_subplot(111,projection='3d')
                    ax.scatter(RP,ZP,RP*0,c='black',marker='x')
                    plt.show()
          if event== "New figure":
                    try:
                              fig=plt.figure()
                              ax = fig.add_subplot(111,projection='3d')
                    except:
                              continue
          if event== 'write currents.dat':
                    try:
                              Re
                    except:
                              Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
                              #R,Z,dr,dz,VAR=e.read_EFIT_RZ()


                    PASS=e.read_passives(VAR,ivc,index,shotefit,runefit,timeefit)
                    CURR=e.read_active(shotefit,runefit,timeefit)

                    try:
                              filename='exp/equ/EFIT/currents.dat'
                              fw=open(filename,'w') 
                    except:
                              filename='EFIT/currents.dat'
                              fw=open(filename,'w')                               
                    fw.write(str(len(CURR))+'  '+str(len(PASS))+'\n')
                    for j in range(0,len(CURR)): 
                              fw.write(str(CURR[j])+'   ') 
                              if j>0 and j == int(j/3)*3:fw.write('\n')
                    fw.write('\n')
                    for j in range(0,len(PASS)): 
                              fw.write(str(PASS[j])+'   ') 
                              if j+1 == int((j+1)/3)*3:fw.write('\n')
                    fw.close()


window.close()
"""
#Creating fires.dat for EFIT filaments
Re,Ze,dre,dze,VAR=e.read_EFIT_RZ(shotelmag)
f = open("exp/equ/FE23/firesEFIT.dat", "w")
f.write(str(-len(Re))+'\n') 
NAME=["IVC","MC","DIV","ERING","BVL","OVC","DIVPSRT","DIVPSRB","HFSPSRT","HFSPSRB"]
index=[479,16,54,108,82,46,6,6,15,15,0]
ii=0
rest=0
for i in range(0,len(Re)):
          if ii < 5 and ii > 0:
                    if Ze[i] < 0 : 
                              name=NAME[ii]+'B'
                    else:
                              name=NAME[ii]+'T'
          else:
                    name=NAME[ii]
          f.write('1 '+str(Re[i])+' '+str(Ze[i])+' '+str(dre[i])+' '+str(dze[i])+' 690D-9 0 '+name+'\n')
          if i>=index[0]+rest: 
                    ii+=1
                    rest=rest+index[ii]
f.close()
"""




# python3 pyt/panel_floops.py
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import floop_functions as f
import pcs_reading_functions as pcs
nloop=41
n1=30
n2=6
n3=3
n4=3
name=np.array([])
#exp/equ/P2.3/fl_loop.dat
for i in range(0,n1):
          if i<9:
                    name=np.append(name,'FLOOP_00'+str(i+1))
          elif i != 27:
                    name=np.append(name,'FLOOP_0'+str(i+1))
for i in range(100,100+n2):name=np.append(name,'FLOOP_'+str(i+1))
for i in range(200,200+n3):name=np.append(name,'FLOOP_'+str(i+1))
for i in range(209,209+n4):name=np.append(name,'FLOOP_'+str(i+1))
for i in range(0,nloop):print(name[i])
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4)),
           sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")],
          [sg.Checkbox('',default=True, key="-exp-"),
           sg.T("ST40 shot ="), sg.Input('12050', size=(6,1),key="-SHOT-"),
           sg.T("                 "),sg.Button("PFIT inputs")],
          [sg.Checkbox('Plasma',default=False, key="-plasma-"),
           sg.Checkbox('Vacuum',default=False, key="-vacuum-"),
           sg.Checkbox('in ALL node',default=False, key="-all-")],
          [sg.T("ASTRA shot="), sg.Input('13012050', size=(8,1),key="-shot-"),
           sg.T("ASTRA run"), sg.Input('201', size=(5,1), key="-runA-")],
          [sg.Checkbox('',default=False, key="-EFIT-"),
           sg.T("EFIT shot="), sg.Input('12050', size=(8,1),key="-shotE-"),
           sg.Input('BEST', size=(10,1), key="-runE-")],          
          [sg.Checkbox(name[0],default=False, key="-"+name[0]+"-"),
           sg.Checkbox(name[10],default=False, key="-"+name[10]+"-"),
           sg.Checkbox(name[20],default=False, key="-"+name[20]+"-"),
           sg.Checkbox(name[30],default=False, key="-"+name[30]+"-"),
           sg.Checkbox(name[40],default=False, key="-"+name[40]+"-")],
          [sg.Checkbox(name[1],default=False,key="-"+name[1]+"-"),
           sg.Checkbox(name[11],default=False, key="-"+name[11]+"-"),
           sg.Checkbox(name[21],default=False, key="-"+name[21]+"-"),
           sg.Checkbox(name[31],default=False, key="-"+name[31]+"-")],
          [sg.Checkbox(name[2],default=False, key="-"+name[2]+"-"),
           sg.Checkbox(name[12],default=False, key="-"+name[12]+"-"),
           sg.Checkbox(name[22],default=False, key="-"+name[22]+"-"),
           sg.Checkbox(name[32],default=False, key="-"+name[32]+"-")],
          [sg.Checkbox(name[3],default=False, key="-"+name[3]+"-"),
           sg.Checkbox(name[13],default=False, key="-"+name[13]+"-"),
           sg.Checkbox(name[23],default=False, key="-"+name[23]+"-"),
           sg.Checkbox(name[33],default=False, key="-"+name[33]+"-")],
          [sg.Checkbox(name[4],default=False, key="-"+name[4]+"-"),
           sg.Checkbox(name[14],default=False, key="-"+name[14]+"-"),
           sg.Checkbox(name[24],default=False, key="-"+name[24]+"-"),
           sg.Checkbox(name[34],default=False, key="-"+name[34]+"-")],
          [sg.Checkbox(name[5],default=False, key="-"+name[5]+"-"),
           sg.Checkbox(name[15],default=False, key="-"+name[15]+"-"),
           sg.Checkbox(name[25],default=False, key="-"+name[25]+"-"),
           sg.Checkbox(name[35],default=False, key="-"+name[35]+"-")],
          [sg.Checkbox(name[6],default=False, key="-"+name[6]+"-"),
           sg.Checkbox(name[16],default=False, key="-"+name[16]+"-"),
           sg.Checkbox(name[26],default=False, key="-"+name[26]+"-"),
           sg.Checkbox(name[36],default=False, key="-"+name[36]+"-")],
          [sg.Checkbox(name[7],default=False, key="-"+name[7]+"-"),
           sg.Checkbox(name[17],default=False, key="-"+name[17]+"-"),
           sg.Checkbox(name[27],default=False, key="-"+name[27]+"-"),
           sg.Checkbox(name[37],default=False, key="-"+name[37]+"-")],
          [sg.Checkbox(name[8],default=False, key="-"+name[8]+"-"),
           sg.Checkbox(name[18],default=False, key="-"+name[18]+"-"),
           sg.Checkbox(name[28],default=False, key="-"+name[28]+"-"),
           sg.Checkbox(name[38],default=False, key="-"+name[38]+"-")],
          [sg.Checkbox(name[9],default=False, key="-"+name[9]+"-"),
           sg.Checkbox(name[19],default=False, key="-"+name[19]+"-"),
           sg.Checkbox(name[29],default=False, key="-"+name[29]+"-"),
           sg.Checkbox(name[39],default=False, key="-"+name[39]+"-")],
          [sg.Button("x1"),sg.Button("o1"),
           sg.Button("x2"),sg.Button("o2"),
           sg.Button("x3"),sg.Button("o3"),
           sg.Button("x4"),sg.Button("o4")],
          [sg.T("")]]

    #[sg.Checkbox('',default=True, key="--")],
    


###Setting Window
window = sg.Window('FLOOPS panel', layout, size=(600,600))

###Showing the Application, also GUI functions can be placed here.
while True:
          event, values = window.read()
          shotst40=int(values["-SHOT-"])
          shotastra=int(values["-shot-"])
          shotefit=int(values["-shotE-"])
          runastra=int(values["-runA-"])
          runefit=str(values["-runE-"])
          RUNv='RUN0'+str(runastra)
          RUNp='RUN'+str(runastra)
          ALL=False
          if values["-all-"]== True : ALL=True
          index=np.array([])
          t1=0.5;t2=-1;t3=0.5;t4=-1
          for i in range(0,nloop):
                    if values["-"+name[i]+"-"]== True : index=np.append(index,i)

          if event == sg.WIN_CLOSED or event=="Exit":
                    break
          elif event == "x1":
                    for i in range(0,10):
                              window["-"+name[i]+"-"].update(True)
          elif event == "o1":
                    print(event)
                    for i in range(0,10):
                              window["-"+name[i]+"-"].update(False)
          elif event == "x2":
                    for i in range(10,20):
                              window["-"+name[i]+"-"].update(True)
          elif event == "o2":
                    print(event)
                    for i in range(10,20):
                              window["-"+name[i]+"-"].update(False)
          elif event == "x3":
                    for i in range(20,30):
                              window["-"+name[i]+"-"].update(True)
          elif event == "o3":
                    print(event)
                    for i in range(20,30):
                              window["-"+name[i]+"-"].update(False)
          elif event == "x4":
                    for i in range(30,40):
                              window["-"+name[i]+"-"].update(True)
          elif event == "o4":
                    print(event)
                    for i in range(30,40):
                              window["-"+name[i]+"-"].update(False)
          elif event == "PFIT inputs":
                    for i in range(0,41):
                              window["-"+name[i]+"-"].update(False)
                    for i in range(0,41):
                              ok,index=pcs.pfit_inmap(name[i])
                              print(ok,i)
                              if ok == 'ok' : window["-"+name[i]+"-"].update(True)
          elif event== "make plot":
                    print(index)
                    ind=index.astype(int)
                    if values["-exp-"]== True : 
                              if values["-vacuum-"]== True : 
                                        t1,t2=f.astra_t1_t2(shotastra,RUNv)
                              tmin=min(t1,t2)
                              if values["-plasma-"]== True : 
                                        t1,t1=f.astra_t1_t2(shotastra,RUNp)
                              tmax=max(t1,t2)
                              print(tmin,tmax)
                              f.plot_floop_exp(shotst40,name,ind,tmin,tmax)
                    if values["-EFIT-"]== True : 
                              #f.plot_floop_efit_m(shotefit,runefit,ind)
                              f.plot_floop_efit_c(shotefit,runefit,ind)
                    if values["-vacuum-"]== True : 
                              if ALL:
                                        f.plot_floop_astra_all(shotastra,RUNv,name,ind)
                              else:
                                        f.plot_floop_astra(shotastra,RUNv,name,ind)
                    if values["-plasma-"]== True : 
                              if ALL:
                                        f.plot_floop_astra_all(shotastra,RUNp,name,ind) 
                              else:
                                        f.plot_floop_astra(shotastra,RUNp,name,ind) 
                    plt.legend(loc='upper left',fontsize='small')
                    plt.show()


window.close()


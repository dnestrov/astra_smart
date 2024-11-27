import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import sys
import read_efit_data as efit
shotnum=13311419
run='RUN2340' 
RUN=run
def read_virial(shotnum,name,run):
               print(shotnum,name,run)
               try:
                              TIME,VAR=efit.read_virial(shotnum,name,run)
               except:
                              print('No EFIT data for '+name)
                              return 0,0
               return TIME,VAR
def read_global(shotnum,name,run):
               print(shotnum,name,run)
               try:
                              TIME,VAR=efit.read_global(shotnum,name,run)
               except:
                              print('No EFIT data for '+name)
                              return 0,0
               return TIME,VAR

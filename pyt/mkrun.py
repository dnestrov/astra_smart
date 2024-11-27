#python3 mkrun.py ??000000 
from MDSplus import *
from numpy import *
import mdsHelpers as mh
from importlib import reload
reload(mh)
import st40_astra_tree as a
range=int(sys.argv[1])
a.create(range+11590,'RUN1','run in FENIX')

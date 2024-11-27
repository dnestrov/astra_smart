#python3 mkshot.py 9120 RUN500 test with strahl
from MDSplus import *
import numpy as np
import mdsHelpers as mh
from imp import reload
reload(mh)
import sys
import st40_astra_tree as astree
import vac_astra_tree as vactree
pulseNo = int(sys.argv[1])
run_number = 'RUN' + str(sys.argv[2])
vac_run_number = 'RUN0' + str(sys.argv[2])
text=''
for j in range(3, len(sys.argv)):
    text = text + ' ' + str(sys.argv[j])
astree.create(pulseNo, run_number, text)
vactree.create(pulseNo, vac_run_number, text)

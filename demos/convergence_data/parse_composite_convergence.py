#! bin/bash

import sys
import numpy as np

indx=1
col_lnL=9
for fname in sys.argv:
    dat = np.loadtxt(fname)
    print indx, np.mean(dat[:,col_lnL]), np.std(dat[:,col_lnL])
    indx+=1

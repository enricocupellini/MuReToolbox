# from xcorr import xcorr

import numpy as np

def ofacorr(of):
    MAXLAG = 8
    NDIVS = 4
    actmp = np.correlate(of, of, mode='full')
    # actmp = xcorr(of)
    ind1 = (len(actmp) + 1) // 2
    ind2 = min(len(actmp), ind1 + MAXLAG * NDIVS)
    ac = np.zeros(MAXLAG * NDIVS + 1)
    ac[:ind2 - ind1 + 1] = actmp[ind1:ind2 + 1]
    if ac[0] > 0:
        ac /= ac[0]
    return ac[2::2]

# original code

# function ac = ofacorr(of);
# % ac = ofacorr(of);
# %
# % Comment: Auxiliary function that resides in private directory

# MAXLAG = 8;
# NDIVS = 4;
# actmp = xcorr(of);
# ind1 = (length(actmp)+1)/2; ind2 = min(length(actmp),ind1+MAXLAG*NDIVS);
# ac=zeros(1,MAXLAG*NDIVS+1);
# ac(1:(ind2-ind1+1)) = actmp(ind1:ind2)';
# if ac(1)>0 ac = ac/ac(1); end
# ac = ac(3:2:end);
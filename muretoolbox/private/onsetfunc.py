import numpy as np

def onsetfunc(beatOnsets, accValues=None):
    """
    % Sum of delta functions at onset times weighted by values obtained from ACCVALUES

Input arguments:
>>> beatOnsets = sequence of note onsets measured in beat fractions
>>> accValues = values to weight the received onsets. If None each onset has the same weight
    accValues must be a function of beatOnset and must have the same number of elements of it
    >>> *** original library paramenter: ACCFUNC (optional) = accent function; ***

Output:
	OF = onset function

    Reference:
	Brown, J. (1992). Determination of meter of musical scores by
		autocorrelation. Journal of the acoustical society of America, 94 (4), 1953-1957.

    Comment: Auxiliary function that resides in private directory

    Change History :
    Date		Time	Prog	Note
    11.8.2002	18:36	PT	Created under MATLAB 5.3 (Macintosh)
    © Part of the MIDI Toolbox, Copyright © 2004, University of Jyvaskyla, Finland
    See License.txt
"""
    NDIVS = 4  
    MAXLAG = 8
    ob = [float(x) for x in beatOnsets]
    ob = np.asarray(ob)

    if accValues is not None:
        acc = np.asarray(accValues)
        acc = [float(x) for x in acc]
    else:
        acc = np.ones(len(ob))

    vlen = NDIVS * max([2 * MAXLAG, int(np.ceil(max(ob)))])
    of = np.zeros(vlen)
    ind = np.mod(np.round(ob * NDIVS), len(of)).astype(int)
    for k in range(len(ind)):
        of[ind[k]] = of[ind[k]] + acc[k]

    return of




# original code

# function of = onsetfunc(nmat, accfunc);

# NDIVS = 4; % four divisions per quater note
# MAXLAG=8;
# ob = onset(nmat);

# if nargin==2
# 	acc=feval(accfunc,nmat);
# else
# 	acc=ones(length(ob),1);
# end

# vlen = NDIVS*max([2*MAXLAG ceil(max(ob))+1]);
# of = zeros(vlen,1);
# ind = mod(round(ob*NDIVS),length(of))+1;
# for k=1:length(ind)
# 	of(ind(k)) = of(ind(k))+acc(k);
# end

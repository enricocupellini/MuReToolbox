from ismonophonic import ismonophonic

from private.onsetfunc import onsetfunc
from private.ofacorr import ofacorr
from melaccent import melaccent

import numpy as np

def meter(beatOnsets, beatDurations, pitches = None):
    """
    Autocorrelation-based estimate of meter

    Returns an autocorrelation-based estimate of meter of NMAT.
    Based on temporal structure and on Thomassen's melodic accent.
    Uses discriminant function derived from a collection of 12000 folk melodies.
    m = 2 for simple duple
    m = 3 for simple triple or compound

    Input argument:
>>> beatOnsets = sequence of note onsets represented as beat fractions
>>> beatDurations = sequence of durations from the same music source, represented as beat fractions
>>>	pitches (Optional) = array of midi pitches from the same music source. IF PRESENT uses a weighted combination
      of duration and melodic accents in the inference of meter (see Toiviainen & Eerola, 2004).

Output:
	M = estimate of meter (M=2 for simple duple; M=3 for simple triple or compound)

    References:
     Brown, J. (1993). Determination of the meter of musical scores by 
         autocorrelation. Journal of the Acoustical Society of America, 
         94(4), 1953-1957.
     Toiviainen, P., & Eerola, T. (2006). Autocorrelation in meter induction: the role of accent structure. Journal of the Acoustical Society of America, 119(2), 1164-1170.

    Change History :
    Date		Time	Prog	Note
    11.8.2002	18:36	PT	Created under MATLAB 5.3 (Macintosh)
    © Part of the MIDI Toolbox, Copyright © 2004, University of Jyvaskyla, Finland
    See License.txt
    """
    
    if len(beatOnsets) == 0 or len(beatDurations) == 0:
        return

    if pitches is None:
        ac = ofacorr(onsetfunc(beatOnsets, beatDurations))
        if ac[3] >= ac[5]:
            return 2
        else:
            return 3
    else:
        if not ismonophonic(beatOnsets, beatDurations):
            print(' Optimized version works only with monophonic input!')
            return None
        
        return weighted_meter(beatOnsets, beatDurations, pitches)

def weighted_meter(beatOnsets, beatDurations, pitches):
    ac1 = ofacorr(onsetfunc(beatOnsets, beatDurations))
    mel = melaccent(pitches, beatOnsets, beatDurations)
    ac2 = ofacorr(onsetfunc(beatOnsets, mel))

    df = -1.042 + 0.318 * ac1[2] + 5.240 * ac1[3] - 0.63 * ac1[5] + 0.745 * ac1[7] - 8.122 * ac1[11] + 4.160 * ac1[15]
    df -= 0.978 * ac2[2] + 1.018 * ac2[3] - 1.657 * ac2[5] + 1.419 * ac2[7] - 2.205 * ac2[11] + 1.568 * ac2[15]

    if df >= 0:
        return 2
    else:
        return 3
    
# original code

# function m = meter(nmat,option)

# if isempty(nmat), return; end

# if nargin<2

# 	ac = ofacorr(onsetfunc(nmat,'dur'));
# 	if ac(4) >= ac(6)
# 		m = 2;
# 	else
# 		m = 3;
# 	end

# else
# if ~ismonophonic(nmat), disp(' Optimized version works only with monophonic input!'); m=[]; return; end
# 	if strcmp(lower(option), 'optimal')~=1
# 			disp(['Unknown option:' option])
# 			disp('Accepted option is ''optimal''! ')
# 			return
# 	end
# 	m = weighted_meter(nmat);
# end

# %%%%%%%%%  Optimized (weighted) function
# function m = weighted_meter(nmat)
# % m = weighted_meter(nmat);

# ac1 = ofacorr(onsetfunc(nmat));
# ac2 = ofacorr(onsetfunc(nmat,'melaccent'));

# % discriminant function

# df = -1.042+0.318*ac1(3)+5.240*ac1(4)-0.63*ac1(6)+0.745*ac1(8)-8.122*ac1(12)+4.160*ac1(16);
# df=df-0.978*ac2(3)+1.018*ac2(4)-1.657*ac2(6)+1.419*ac2(8)-2.205*ac2(12)+1.568*ac2(16);

# if df>=0
# 	m = 2;
# else
# 	m = 3;
# end


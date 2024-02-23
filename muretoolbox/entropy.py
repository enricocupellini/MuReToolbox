import numpy as np

def entropy(d):
    """
% Entropy of a distribution
% function h = entropy(d);
% Returns the relative entropy of any distribution given as input argument
% 
% Input argument:
%	D = distribution
%
% Output:
%	H = relative entropy (0 =< H =< 1)
%
% Change History :
% Date		Time	Prog	Note
% 12.6.2002	15:20	TE	Created under MATLAB 5.3 (PC)
%� Part of the MIDI Toolbox, Copyright � 2004, University of Jyvaskyla, Finland
% See License.txt
"""

    d = np.asarray(d).flatten()
    d = d / np.sum(d + 1e-12)
    logd = np.log(d + 1e-12)
    h = -np.sum(d * logd) / np.log(len(d))
    
    return h

# original code

# d=d(:);
# d=d/sum(d+ 1e-12);
# logd = log(d + 1e-12); % this is slow for high dimensional matrices (TE)
# h = -sum(d.*logd)/log(length(d)); 
   
from ismonophonic import ismonophonic

import numpy as np

def durdist2(nmat):
    """
    % Duration dyad distribution
% dd = durdist2(nmat);
% Returns the distribution of pairs of note durations of successive
% notes as a 9 * 9 matrix
% For bin centers, see DURDIST1
%
% Input argument:
%	NMAT = notematrix
%
% Output:
%	DD = 9 * 9 distribution matrix of note duration pairs
%
% Change History :
% Date		Time	Prog	Note
% 10.6.2002	16:03	TE	Created under MATLAB 5.3 (PC)
% 8.8.2002	15:10	PT	Revised
%� Part of the MIDI Toolbox, Copyright � 2004, University of Jyvaskyla, Finland
% See License.txt"""

    if nmat.size == 0:
        return None
    if not ismonophonic(nmat):
        print(f"{mfilename} works only with monophonic input!")
        return None

    du = dur(nmat)
    du = du[du > 0]  # rimuovi le durate zero
    du = np.round(2 * np.log2(du))  # prendi i logaritmi e categorizza
    du = du[np.abs(du) <= 4]  # includi durate tra 1/16 e 1/1 note
    du = du + 5  # sposta gli indici delle categorie nell'intervallo 1 ... 9

    durd = np.zeros((9, 9))

    for k in range(1, len(du)):
        durd[du[k - 1], du[k]] += 1
        # pcolor(durd)  # diagnostica...

    dd = durd / np.sum(np.sum(durd + 1e-12))  # normalizza
    return dd

# original code

# function dd = durdist2(nmat)

# if isempty(nmat), return; end
# if ~ismonophonic(nmat), disp([mfilename, ' works only with monophonic input!']); dd=[]; return; end

# du = dur(nmat);
# du = du(du>0); % remove zero duations
# du = round(2*log2(du)); % take logarithms & categorize
# du = du(abs(du)<=4); % include duations between 1/16 and 1/1 notes
# du = du+5; % shift category indeces to range 1 ... 9

# durd = zeros(9,9);

# for k=2:length(du)
# 	durd(du(k-1),du(k)) = durd(du(k-1),du(k))+1;
# %pcolor(durd); % diagnostics...
# end

# dd = durd/sum(sum(durd+ 1e-12)); % normalize 


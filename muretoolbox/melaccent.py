import numpy as np
from ismonophonic import ismonophonic

def melaccent(pitches, onsets, dur):
    """
    Melodic accent salience according Thomassen's model

    Calculates melodic accent salience according Thomassen's model.
    Thomassen's model assigns melodic accents according to the possible
    melodic contours arising in 3-pitch windows.
    Accent values vary between 0 (no salience) and 1 (maximum salience)

Input arguments:
>>>	pitches = array of midi pitches from a given music source
>>>	ONSETS = sequence of onsets from the same music source
>>>	DUR =  sequence of durations from the same music source


Output:
	MA = accent values


    Example: 
    p = [60, 62, 64, 65, 67, 69, 71, 72];
    melaccent(p)

    Reference:
    Joseph Thomassen, "Melodic accent: Experiments and a tentative model,"
    Journal of the Acoustical Society of America, Vol. 71, No. 6 (1982) pp.1598-
    1605; see also, Erratum, Journal of the Acoustical Society of America,
    Vol. 73, No. 1 (1983) p.373.

Authors:
    Date		Time	Prog	Note
    14.6.2002	15:38	TE	Created under MATLAB 5.3 (PC)
    20.4.2003	13:23	PT	Revised
    © Part of the MIDI Toolbox Software Package, Copyright © 2004, University of Jyvaskyla, Finland
    See License.txt
"""
    if not pitches:
        return None
    
    if not ismonophonic(onsets, dur):
        print(f"{__name__} works only with monophonic input!")
        return None
    
    pc = pitches
    melodic_accent = np.zeros((len(pc),))
    mel2 = np.zeros((len(pc) - 2, 2))
    
    for i in range(len(pc) - 2):
        notewindow3 = pc[i:i + 3]

        motion1 = notewindow3[1] - notewindow3[0]
        motion2 = notewindow3[2] - notewindow3[1]
        
        if motion1 == 0 and motion2 == 0:
            melodic_accent[i + 1:i + 3] = [0.00001, 0.0]
        elif motion1 != 0 and motion2 == 0:
            melodic_accent[i + 1:i + 3] = [1, 0.0]
        elif motion1 == 0 and motion2 != 0:
            melodic_accent[i + 1:i + 3] = [0.00001, 1]
        elif motion1 > 0 and motion2 < 0:
            melodic_accent[i + 1:i + 3] = [0.83, 0.17]
        elif motion1 < 0 and motion2 > 0:
            melodic_accent[i + 1:i + 3] = [0.71, 0.29]
        elif motion1 > 0 and motion2 > 0:
            melodic_accent[i + 1:i + 3] = [0.33, 0.67]
        elif motion1 < 0 and motion2 < 0:
            melodic_accent[i + 1:i + 3] = [0.5, 0.5]

        mel2[i] = melodic_accent[i + 1:i + 3]
    
    p2 = np.zeros(len(pc))
    p2[0] = 1
    p2[1] = mel2[0, 0]
    
    for k in range(2, len(pc) - 1):
        tmp = [mel2[k - 2, 1], mel2[k - 1, 0]]
        p2[k] = np.prod([x for x in tmp if x != 0])
    
    p2[len(pc) - 1] = mel2[-1, 1]
    return p2


# original code

# function ma = melaccent(nmat)

# if isempty(nmat), return; end
# if ~ismonophonic(nmat), disp([mfilename, ' works only with monophonic input!']); ma=[]; return; end

# pc=pitch(nmat);

# % initialize empty vectors for melodic accent

# mel2=zeros(length(pc)-2,2); % PT

# for i=1:length(pc)-2
#     notewindow3=pc(i:i+2);

#     %---------------------> MELODIC ACCENT <-----------------------
#     motion1 = notewindow3(2) - notewindow3(1);
#     motion2 = notewindow3(3) - notewindow3(2);
#     if motion1==0 && motion2==0
#         melodic_accent(i+1:i+2) = [0.00001 0.0];
#     elseif motion1~=0 && motion2==0
#         melodic_accent(i+1:i+2) = [1 0.0]; % [1 0]
#     elseif motion1==0 && motion2~=0
#         melodic_accent(i+1:i+2) = [0.00001 1];
#     elseif motion1>0 && motion2<0
#         melodic_accent(i+1:i+2) = [0.83 0.17];
#     elseif motion1<0 && motion2>0
#         melodic_accent(i+1:i+2) = [0.71 0.29];
#     elseif motion1>0 && motion2>0
#         melodic_accent(i+1:i+2) = [0.33 0.67];
#     elseif motion1<0 && motion2<0
#         melodic_accent(i+1:i+2) = [0.5 0.5];
#     end

#     mel2(i,:)=melodic_accent(i+1:i+2); % PT
# end

# %---------------------> COMBINE & OUTPUT <-----------------------
# %PT
# p2=zeros(1,length(pc));
# p2(1)=1; p2(2)=mel2(1,1);
# for k=3:length(pc)-1
#     tmp=[mel2(k-2,2) mel2(k-1,1)];
#     p2(k)=prod(tmp(tmp~=0));
# end
# p2(length(pc))=mel2(end,2);
# ma=p2';
# % end PT
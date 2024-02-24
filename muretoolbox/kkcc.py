import numpy as np
from pcdist1 import pcdist1
from refstat import refstat

def kkcc(pitches, IOIs, profile='KRUMHANSL-KESSLER', opt=None):
    """
    Correlations of pitch-class distribution with Krumhansl-Kessler tonal hierarchies

	Returns the correlations of the pitch class distribution PCDIST1
	with each of the 24 Krumhansl-Kessler profiles.

Input arguments: 
>>>	pitches = array of midi pitches
>>>	IOIs = array of the input pitches' inter onset intervals in seconds. It must have the same length as pitches array minus one
>>>	PROFILE = 24 x 12 profile (Krumhansl-Kessler as default, or Temperley (1999) with
	'TEMPERLEY', and Albrecht and Schneider 2013 version with
	'ALBRECHT-SHANAHAN'
>>>	OPT = OPTIONS (optional), 'SALIENCE' return the correlations of the 
     pitch-class distribution according to the Huron & Parncutt (1993) 
     key-finding algorithm. 'TEMPERLEY'

Output: 
	C = 24-component vector containing the correlation coeffients
		between the pitch-class distribution of input pitches (and IOIs) and each 
 		of the 24 Krumhansl-Kessler (or alternative) profiles.

 Remarks: REFSTAT function is called to load the key profiles.

 Example: c = kkcc(pitches, IOIs, 'TEMPERLEY', 'salience')

 See also KEYMODE, KKMAX, and KKKEY in the MIDI Toolbox.

References:

 Albrecht, J., & Shanahan, D. (2013). The Use of Large Corpora to 
     Train a New Type of Key-Finding Algorithm. Music Perception: An 
     Interdisciplinary Journal, 31(1), 59-67.	

 Krumhansl, C. L. (1990). Cognitive Foundations of Musical Pitch.
	New York: Oxford University Press.

 Huron, D., & Parncutt, R. (1993). An improved model of tonality 
     perception incorporating pitch salience and echoic memory. 
     Psychomusicology, 12, 152-169. 

 Temperley, D. (1999). What's key for key? The Krumhansl-Schmuckler 
     key-finding algorithm reconsidered. Music Perception: An Interdisciplinary
     Journal, 17(1), 65-100.


 Authors:
  Date		Time	Prog	Note
 4.8.2002	11:39	TE	Created under MATLAB 5.3 (PC)
 Part of the MIDI Toolbox, Copyright 2004, University of Jyvaskyla, Finland
 See License.txt
"""

    if not pitches or not IOIs:
        return

    if opt is None:
        opt = []
    salienceflag = 0

    if opt == 'salience':
        salienceflag = True
    elif opt:
        print("Only 'SALIENCE' is a valid OPT! No options will be used in the analysis.")
    else:
        print("No options will be used in the analysis.")

    if salienceflag:
        sal = np.array([1, 0, 0.25, 0, 0, 0.5, 0, 0, 0.33, 0.17, 0.2, 0])
        sal2 = np.concatenate((sal, sal))
        salm = np.zeros((12, 12))  # pitch salience matrix
        for k in range(12):
            salm[k, :] = sal2[13 - k:25 - k]
        pcd = pcdist1(pitches, IOIs)
        pcds = pcd * salm
    else:
        pcds = pcdist1(pitches, IOIs)

    if profile == 'KRUMHANSL-KESSLER':
        kkprofs = refstat('kkprofs')
    elif profile == 'TEMPERLEY':
        kkprofs = refstat('kkprofs_t')
    elif profile == 'ALBRECHT-SHANAHAN':
        kkprofs = refstat('kkprofs_as')

    cm = np.corrcoef(np.vstack((pcds, kkprofs)))
    c = cm[0, 1:]

    return c

# original code

# function c = kkcc(nmat, profile, opt)

# if isempty(nmat), return; end

# if nargin<2, opt=[]; profile='KRUMHANSL-KESSLER'; end
# salienceflag = 0;

# if nargin==3
# 	if ischar(opt)==1
# 		salienceflag = strcmp(opt,'salience')
# 		if salienceflag==0
# 		disp('Only ''SALIENCE'' is a valid OPT!'); disp('No options will be used in the analysis.');
# 		end
# 	else
# 		disp('Only strings allowed in OPT. ''SALIENCE'' is a valid option!'); disp('No options will be used in the analysis.');

# 	end

# end



# if salienceflag==1
# 	sal = [1 0 0.25 0 0 0.5 0 0 0.33 0.17 0.2 0];
# 	sal2 = [sal sal];
# 	salm = zeros(12,12); % pitch salience matrix
# 		for k=1:12
# 			salm(k,:) = sal2(14-k:25-k);
# 		end
# 	pcd = pcdist1(nmat);
# 	pcds = pcd*salm;
# else
# 	pcds=pcdist1(nmat);
# end

# switch profile,
#     case 'KRUMHANSL-KESSLER'
#     kkprofs=refstat('kkprofs');
#     case 'TEMPERLEY'
#     kkprofs=refstat('kkprofs_t');
#     case 'ALBRECHT-SHANAHAN'
#     kkprofs=refstat('kkprofs_as');
# end
# cm = corrcoef([pcds; kkprofs]');
# c = cm(1,2:end);

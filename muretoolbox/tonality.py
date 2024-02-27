import numpy as np
from refstat import refstat
from keymode import keymode

def tonality(pitches, IOIs):
	"""
	Tonal stability of notes in melody

!** tonality function in the MIDI toolbox can be used to assign these values to note events 
	assuming the key is in C major or C minor  **!

	Function gives the tonal stability ratings for tones in the melody 
	after determining the key mode (minor/major) using the KEYMODE 
	function.

Input argument: 
>>>	pitches = array of midi pitches
>>>	IOIs = array of the input pitches' inter onset intervals in seconds. It must have the same length as pitches array minus one

Output: 
	P = tonality values for pitches 

	Remarks: This function calls the KEYMODE function. Alternatively,
	revised version of the Krumhansl & Kessler key profile ratings could be used.

Reference: 
	Krumhansl, C. L. (1990). Cognitive Foundations of Musical Pitch.
	New York: Oxford University Press.

	Example: p = tonality(createnmat)

	Authors:
	Date		Time	Prog	Note
	9.9.2002	09:02	TE	Created under MATLAB 5.3 (PC)
	© Part of the MIDI Toolbox, Copyright © 2004, University of Jyvaskyla, Finland
	See License.txt
"""
	if not pitches:
		return

	mode = keymode(pitches, IOIs)

	if mode == 1:
		kk, _ = refstat('kkmaj')
	elif mode == 2:
		kk, _ = refstat('kkmin')
	else:
		print('Key mode not specified (major=1, minor=2)')
		kk, _ = refstat('kkmaj')
        # return

	pc0 = np.mod(pitches, 12)
	p = [kk[i] for i in pc0]
	return p
# original code

# function p = tonality(nmat)

# if isempty(nmat), return; end

# mode=keymode(nmat);

# if mode ==1
# 	kk=refstat('kkmaj');
# elseif mode ==2
# 	kk=refstat('kkmin');
# else
# 	disp('Key mode not specified (major=1, minor=2)')
# 	kk=refstat('kkmaj');
# 	%return
# end

# pc0 = mod(nmat(:,4),12)+1;
# p=kk(pc0)';

import numpy as np
from ismonophonic import ismonophonic
from duraccent import duraccent

def pcdist2(pitches, IOIs, onsets = None, durations = None):

	"""
	2nd order pitch-class distribution

	Calculates the 2nd order pitch-class distribution of the input sequence
	weighted by note durational accents. The time interval 
	between consecutive notes, referred to as the Inter Onset Interval (IOI), is a component of the Parncutt's 
	durational accent model (1994).

	While the Matlab MidiToolbox uses 'note duration', this library utilizes IOIs,
	according to Parncutt's model. Therefore, the following limitations have to be consiered:
	- This function is intended to process only melodic (monophonic) sequences.
	- The durational accent of the last note in the sequence is assigned the mean value of all durational accents, as there is no Inter-Onset Interval (IOI) for that note.


Input argument:
>>>	pitches = array of midi pitches
>>>	IOIs = array of the input pitches' inter onset intervals in seconds. It must have the same length as pitches array minus one
>>>	ONSETS (optional)= sequence of onsets from a given music source
>>>	DUR (optional) = sequence of durations from the same music source
	if optional arguments are present you choose to work only with monophonic input (mirroring the behavior of the original library)

Output:
	PCD = 2nd order pitch-class distribution of the input sequence
	12 * 12 matrix
	e.g. PCD(1,2) = probability of transitions from C to C#

	Change History :
	Date		Time	Prog	Note
	17.6.2002	20:03	TE	Created under MATLAB 5.3 (PC)
	© Part of the MIDI Toolbox, Copyright © 2004, University of Jyvaskyla, Finland
	See License.txt
	"""
	IOIs = np.asarray(IOIs).flatten()
	if len(IOIs) == 0:
		print(f"{__name__} works only with IOIs array of length greater 0. The IOIs array must have a length one less than the pitches array.")
		return None
	if  len(IOIs) != len(pitches)-1:
		print(f"{__name__} works only with IOIs array of length greater 0. The IOIs array must have a length one less than the pitches array.")
		return None

	if onsets and durations:
		if not ismonophonic(onsets, durations):
			print(f"monophonic control activated by optional arguments has detected that the input is not monophonic!")
			return None

	pc = np.mod(pitches, 12)  # C = 0 etc.
	du = duraccent(IOIs)  # IOIs are weighted by Parncutt's durational accent
	pcd = np.zeros((12, 12))

	for k in range(1, len(du)):
		pcd[pc[k-1], pc[k]] += du[k-1] * du[k]

	pcd[pc[-2], pc[-1]] += du[-1] * np.mean(du)

	pcd /= np.sum(pcd + 1e-12)  # normalize
		
	return pcd

# original code

# function pcd = pcdist2(nmat)

# if isempty(nmat), return; end
# if ~ismonophonic(nmat), disp([mfilename, ' works only with monophonic input!']); pcd=[]; return; end

# pc = mod(pitch(nmat),12)+1; % C = 1 etc.
# du = duraccent(dur(nmat,'sec')); % durations are weighted by Parncutt's durational accent
# pcd = zeros(12,12);
# for k=2:length(pc)

# 	pcd(pc(k-1),pc(k)) = pcd(pc(k-1),pc(k))+du(k-1)*du(k);

# end
# pcd = pcd/sum(sum(pcd + 1e-12)); % normalize 


import numpy as np
from duraccent import duraccent

def pcdist1(pitches, IOIs: np.ndarray):
	"""
	Pitch-class distribution weighted by note durations

	Calculates the pitch-class distribution weighted by note durational accents. The time interval 
	between consecutive notes, referred to as the Inter Onset Interval (IOI), is a component of the Parncutt's 
	durational accent model (1994).

	While the Matlab MidiToolbox uses 'note duration', this library utilizes IOIs,
	according to Parncutt's model. Therefore, the following limitations have to be consiered:
	- This function is intended to process only melodic sequences.
	- The durational accent of the last note in the sequence is assigned a value of 1, as there is no Inter-Onset Interval (IOI) for that note.


Input argument: 
>>>	pitches = array of midi pitches
>>>	IOIs = array of inter onset intervals in seconds. It must have the same length of pitches


Output: 
	PCD = 12-component vector listing the probabilities of
	pitch-classes (C, C#, D, D#, E, F, F#, G, G#, A, A#, B).

	See also: IVDIST1, DURDIST1, PCDIST2, IVDIST2, DURDIST2


	Author		Date
	T. Eerola	2.2.2003
	© Part of the MIDI Toolbox, Copyright © 2004, University of Jyvaskyla, Finland
	See License.txt
	"""
	if len(pitches) == 0:
		return "pitches = 0" #None
	if  len(IOIs) != len(pitches)-1:
		return "mismatch number of elements" #None

	pc = np.mod(pitches, 12) + 1  # C = 1 etc.
	du = duraccent(IOIs)  # durations are weighted by Parncutt's durational accent

	pcd = np.zeros(12)
	for k in range(len(du)):
		pcd[pc[k] - 1] += du[k]

	pcd[pc[-1]] += 1 # The durational accent of the last note in the sequence is assigned a value of 1, as there is no Inter-Onset Interval (IOI) for that note.

	pcd = pcd / np.sum(pcd + 1e-12)  # normalize
	return pcd


#original code

# function pcd = pcdist1(nmat)

# if isempty(nmat), return; end
# pc = mod(nmat(:,4),12)+1; % C = 1 etc.
# %dur = nmat(:,2);
# du = duraccent(dur(nmat,'sec')); % durations are weighted by Parncutt's durational accent
# pcd = zeros(1,12);
# for k=1:length(pc)
# 	pcd(pc(k)) = pcd(pc(k))+du(k);
# end
# pcd = pcd/sum(pcd + 1e-12); % normalize 



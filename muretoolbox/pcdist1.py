import numpy as np
from duraccent import duraccent

def pcdist1(pitches, IOIs):
	"""
	Pitch-class distribution weighted by note durations

	Calculates the pitch-class distribution weighted by note durational accents. The time interval 
	between consecutive notes, referred to as the Inter Onset Interval (IOI), is a component of the Parncutt's 
	durational accent model (1994).

	While the Matlab MidiToolbox uses 'note duration', this library utilizes IOIs,
	according to Parncutt's model. Therefore, the following limitations have to be consiered:
	- This function is intended to process only melodic (monophonic) sequences.
	- The durational accent of the last note in the sequence is assigned the mean value of all durational accents, as there is no Inter-Onset Interval (IOI) for that note.


Input argument: 
>>>	pitches = array of midi pitches
>>>	IOIs = array of the input pitches' inter onset intervals in seconds. It must have the same length as pitches array minus one


Output: 
	PCD = 12-component vector listing the probabilities of
	pitch-classes (C, C#, D, D#, E, F, F#, G, G#, A, A#, B).

	See also: IVDIST1, DURDIST1, PCDIST2, IVDIST2, DURDIST2


	Author		Date
	T. Eerola	2.2.2003
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

	pc = np.mod(pitches, 12)  # C = 0 etc.
	du = duraccent(IOIs)  # IOIs are weighted by Parncutt's durational accent

	pcd = np.zeros(12)
	for k in range(len(du)):
		pcd[pc[k]] += du[k]

	pcd[pc[-1]] += np.mean(du) # The durational accent of the last note in the sequence is assigned the mean value of durational accents, as there is no Inter-Onset Interval (IOI) for that note.

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



def ismonophonic(onsets, dur, overlap=0.1):
	"""
	Returns 1 if monophonic sequence (logical function)

	Returns 1 if the sequence has NO overlapping notes. Function can be 
	used for finding errors in monophonic melodies and checking whether analysis is
	suitable for the selected sequence. For example, ivdist1 cannot be meaningfully
	performed for a polyphonic input.

Input argument: 
>>>	ONSETS = sequence of onsets from a given music source
>>>	DUR =  sequence of durations from the same music source
>>>	OVERLAP (Optional) = Criteria for allowing short overlap between events. The default value is 0.1 seconds


Output: 
	L = 1 (is monophonic) or 0 (polyphonic)

	Authors:
	Date		Time	Prog	Note
	2.11.2001	20:24	TE	Created under MATLAB 5.3 (PC)
	© Part of the MIDI Toolbox, Copyright © 2004, University of Jyvaskyla, Finland
	See License.txt
	"""

	if  len(onsets) != len(dur):
		return "mismatch number of elements" #None
	
	l = 1
	c = []
	for i in range(1, len(onsets)):
		c.append(onsets[i] - (onsets[i-1] + dur[i-1]))
		if c[i-1] < -overlap:
			l = 0

	return l

#original code

# function l = ismonophonic(nmat,overlap,timetype)

# if isempty(nmat), return; end
# if nargin<3, timetype='sec'; end
# if nargin<2, overlap=0.1; end

# l=1;
# c=[];
# a=onset(nmat,timetype);
# b=dur(nmat,timetype);
# 	for i=2:size(nmat,1)
# 	c(i)=a(i)-(a(i-1)+b(i-1));
# 		if c(i) < -overlap % overlap criteria (for example, 0.05-3.0)
# 		l=0;
# 		end
# 	end

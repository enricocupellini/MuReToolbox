from kkcc import kkcc

def keymode(pitches, IOIs):
    """
    Mode (major vs. minor) estimation

	Functions estimates the key mode (1=major, 2=minor) based on 
	Krumhansl-Kessler key finding algorithm and pitch distribution.
	This function is used to assign TONALITY values to the input sequence.

Input argument: 
>>>	pitches = array of midi pitches
>>>	IOIs = array of the input pitches' inter onset intervals in seconds. It must have the same length as pitches array minus one

Output: 
	K = estimated mode of input sequence (1=major, 2=minor)

	Remarks: 

	Example: k = keymode(nmat)

	See also KKCC, KKMAX, and KKKEY in the MIDI Toolkit.

	Authors:
	Date		Time	Prog	Note
	10.11.2002	11:21	TE	Created under MATLAB 5.3 (PC)
	© Part of the MIDI Toolbox, Copyright © 2004, University of Jyvaskyla, Finland
	See License.txt
    """
    
    if not pitches or not IOIs:
        return

    u = kkcc(pitches, IOIs)
    major = u[0]
    minor = u[12]

    if major > minor:
        return 1
    elif major < minor:
        return 2
    else:
        print('major/minor equally strong!')
        return 0


# original code

# function k = keymode(nmat)

# if isempty(nmat), return; end

# u = kkcc(nmat);
# major =u(1);
# minor =u(13);
# 	if major>minor
# 		k=1;
# 	elseif major<minor
# 		k=2;
# 	else
# 		k=0;
# 		disp('major/minor equally strong!')
# 	end

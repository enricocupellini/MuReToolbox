import numpy as np

def duraccent(ioi,tau = 0.5, accent_index = 2):

    """
    Duration accent by Parncutt (1994)
    
    Function returns duration accent of the events (Parncutt, 1994), p. 430-431
    where tau represents saturation duration (proportional to the duration of the echoic 
    store) and accent index that covers the minimum discriminable duration. 

    While the Matlab MidiToolbox uses 'note duration', this library uses IOIs,
    according to Parncutt's model.

Input arguments: 
>>>	IOI = inter onset interval in seconds
>>>	TAU (optional) = saturation duration (default 0.5)
>>>	ACCENT_INDEX (optional) = minimum discriminable duration (default 2)

Output: 
D = new duration vector corresponding to the size of input vector

    References: Parncutt, R. (1994). A perceptual model of pulse salience and metrical
        accent in musical rhythms. Music Perception. 11(4), 409-464.

    Authors:
      Date		Time	Prog	Note
    12.2.2003	15:50	TE	Created under MATLAB 5.3 (PC)
    © Part of the MIDI Toolbox, Copyright © 2004, University of Jyvaskyla, Finland
    See License.txt
    """

    D = (1-np.exp(-ioi/tau))**accent_index; # % duration weigth
    return D

# original code

# if nargin < 3; tau=0.5; end
# if nargin < 2; accent_index=2; end

# D = (1-exp(-dur/tau)).^accent_index; % duration weigth
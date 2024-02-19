import numpy as np

def duraccent(ioi,tau = 0.5, accent_index = 2):

    """
Duration accent by Parncutt (1994)
    
Function returns duration accent of the events (Parncutt, 1994), p. 430-431
where tau represents saturation duration (proportional to the duration of the echoic 
store) and accent index that covers the minimum discriminable duration. 

While the Matlab MidiToolbox implementation uses 'note duration', this implementatin
according to Parncutt's model uses IOI.

Input arguments: 
>>> IOI = inter onset interval in seconds
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
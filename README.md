#MIDI toolbox 1.1 (2016)

ECMidiToolbox is a partial porting of the MIDI Toolbox 1.1. library from MATLAB to Python. Where indicated, the original functions have been modified. Please refer to the original version below for further information.

    Toiviainen, P., & Eerola, T. (2016). MIDI Toolbox 1.1. URL: https://github.com/miditoolbox/1.1

The main difference from the original library lies in the use of "nmat," a table that in the original library results from importing the MIDI file, while the function parameters here take individual features of interest like pitches, durations, velocities.


##Not included from original library due to logic changes:

- dur.m

# MuReToolbox 0.9 (February 2024)

MuReToolbox, an acronym for Music Research Toolbox, is a partial porting of the MIDI Toolbox 1.1. library from MATLAB to Python. Where indicated, the original functions have been modified. Please refer to the original version below for further information.

    Toiviainen, P., & Eerola, T. (2016). MIDI Toolbox 1.1. URL: https://github.com/miditoolbox/1.1

## Main differences from the original library:

- The present library does not provide Midi import 

- "nmat" (note matrix), table resulting from the MIDI file import it is not used here. Functions here accept single music features like pitches, durations, velocities as input parameters.

- Utilities to process nmat are no needed, therefore a number of function like "dur()", "onset()", "pitch()" are not provided by the present library

- Durational accents according to Parncutt's model, are computed using Inter Onset Intervals (IOIs) while the Matlab MidiToolbox uses 'note duration'.


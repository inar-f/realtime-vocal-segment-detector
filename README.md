# realtime-vocal-segment-detector
# Vocal Segment Detector

A small project exploring real-time vocal segment detection for use in a future vocal rider.

The goal is to identify different parts of a vocal, such as:

* Silence
* Breath
* Sibilance
* Plosives
* Voiced sounds
* Transitions

The current approach looks at simple audio features such as level, frequency balance, harmonicity, and changes between frames.

## Current Status

Very early prototype.

So far, the project includes:

* Initial ideas and classification rules
* A Python prototype for overlapping audio frames
* Early DSP / metric experimentation
* A JUCE project for future real-time implementation

## Goal

Eventually, I want to use the detected vocal segment type to help a vocal rider make more informed and predictable gain decisions.

The project is still experimental and the final approach may change as I test different ideas.

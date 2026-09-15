/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"

//==============================================================================
/**
*/
class VocalSegmentDetectorAudioProcessorEditor
    : public juce::AudioProcessorEditor,
    private juce::Timer
{
public:
    VocalSegmentDetectorAudioProcessorEditor (VocalSegmentDetectorAudioProcessor&);
    ~VocalSegmentDetectorAudioProcessorEditor() override;

    //==============================================================================
    void paint (juce::Graphics&) override;
    void resized() override;

private:
    // This reference is provided as a quick way for your editor to
    // access the processor object that created it.
    VocalSegmentDetectorAudioProcessor& audioProcessor;

    // MY CODE HERE HERE HERE
    void timerCallback() override;

    juce::Label levelLabel;
    juce::Label signalLabel;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (VocalSegmentDetectorAudioProcessorEditor)
};

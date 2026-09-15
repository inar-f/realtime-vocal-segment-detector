/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin processor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>

// add any extra includes here
// for example, things needed by your own member variables
#include <../Builds/VisualStudio2026/SignalDetector.h>

//==============================================================================
/**
*/
class VocalSegmentDetectorAudioProcessor : public juce::AudioProcessor
{
public:
    //==============================================================================
    VocalSegmentDetectorAudioProcessor();
    ~VocalSegmentDetectorAudioProcessor() override;

    //==============================================================================
    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

#ifndef JucePlugin_PreferredChannelConfigurations
    bool isBusesLayoutSupported(const BusesLayout& layouts) const override;
#endif

    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    //==============================================================================
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    //==============================================================================
    const juce::String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    //==============================================================================
    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram(int index) override;
    const juce::String getProgramName(int index) override;
    void changeProgramName(int index, const juce::String& newName) override;

    //==============================================================================
    void getStateInformation(juce::MemoryBlock& destData) override;
    void setStateInformation(const void* data, int sizeInBytes) override;

    // put public getter functions here
    // these let the editor or other classes read analysis results
    // example purpose: get current level, get current category
    SignalDetector signalDetector;
    float getCurrentLevelDb() const noexcept;
    bool isSignalPresent() const noexcept;

private:
    // put internal variables here
    // these store analysis state and current results
    // example purpose: current level, signal detected, current category

    // later, reusable detector objects can also go here
    // example purpose: VocalSegmentDetector detector;

    //==============================================================================
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(VocalSegmentDetectorAudioProcessor)
};
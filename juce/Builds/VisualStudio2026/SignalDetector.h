#pragma once

#include <juce_audio_basics/juce_audio_basics.h>

// simple start- just detect if there is a signal or nah
class SignalDetector
{
public:
    void process(const juce::AudioBuffer<float>& buffer) noexcept;
    bool isSignalPresent() const noexcept;
    float getCurrentLevelDb() const noexcept;

private:
    bool signalPresent = false;
    float currentLevelDb = -100.0f;
};
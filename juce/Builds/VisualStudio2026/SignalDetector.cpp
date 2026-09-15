#include "SignalDetector.h"

bool SignalDetector::isSignalPresent() const noexcept
{
	return signalPresent;
}

float SignalDetector::getCurrentLevelDb() const noexcept
{
	return currentLevelDb;
}

void SignalDetector::process(const juce::AudioBuffer<float>& buffer) noexcept
{
    float highestRms = 0.0f;

    for (int channel = 0; channel < buffer.getNumChannels(); ++channel)
    {
        const float channelRms =
            buffer.getRMSLevel(channel, 0, buffer.getNumSamples());

        highestRms = juce::jmax(highestRms, channelRms);
    }

    currentLevelDb =
        juce::Decibels::gainToDecibels(highestRms, -100.0f);

    constexpr float signalThresholdDb = -50.0f;
    signalPresent = currentLevelDb > signalThresholdDb;
}
/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
VocalSegmentDetectorAudioProcessorEditor::VocalSegmentDetectorAudioProcessorEditor (VocalSegmentDetectorAudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p)
{
    // Make sure that before the constructor has finished, you've set the
    // editor's size to whatever you need it to be.
    setSize (400, 300);

    //MY CODE HERE!!
    addAndMakeVisible(levelLabel);
    addAndMakeVisible(signalLabel);

    startTimerHz(30);
}

VocalSegmentDetectorAudioProcessorEditor::~VocalSegmentDetectorAudioProcessorEditor()
{
}

//==============================================================================
void VocalSegmentDetectorAudioProcessorEditor::paint (juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll (getLookAndFeel().findColour (juce::ResizableWindow::backgroundColourId));

    g.setColour (juce::Colours::white);
    g.setFont (juce::FontOptions (15.0f));
    g.drawFittedText ("Hello World!", getLocalBounds(), juce::Justification::centred, 1);
}

void VocalSegmentDetectorAudioProcessorEditor::resized()
{
    // This is generally where you'll want to lay out the positions of any
    // subcomponents in your editor..

    levelLabel.setBounds(20, 20, 200, 30);
    signalLabel.setBounds(20, 60, 200, 30);
}

// MY CODE
//==============================================================================
void VocalSegmentDetectorAudioProcessorEditor::timerCallback()
{
    const float level = audioProcessor.getCurrentLevelDb();
    const bool signal = audioProcessor.isSignalPresent();

    levelLabel.setText(
        "Level: " + juce::String(level, 1) + " dB",
        juce::dontSendNotification
    );

    signalLabel.setText(
        signal ? "Signal: YES" : "Signal: NO",
        juce::dontSendNotification
    );
}

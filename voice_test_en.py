#!/usr/bin/env python3
# Voice wakeup test - English version

import pyttsx3

print("=== Voice Wakeup Test ===")

# Initialize engine
engine = pyttsx3.init()
print("Voice engine initialized")

# Set properties
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)

# Wake words
wake_words = ["lobster", "openclaw", "jarvis"]
print(f"Wake words: {wake_words}")

# Test voice output
print("\n1. Testing basic voice output...")
engine.say("Voice wakeup test starting")
engine.runAndWait()

print("\n2. Testing wake word responses...")

# Test lobster wake
print("Testing wake word: lobster")
engine.say("Lobster robot activated, Jarvis mode starting")
engine.runAndWait()

# Test openclaw wake
print("Testing wake word: openclaw")
engine.say("OpenClaw voice wakeup enabled, ready to serve")
engine.runAndWait()

# Test jarvis wake
print("Testing wake word: jarvis")
engine.say("Jarvis online, master please command")
engine.runAndWait()

print("\n3. Completion message...")
engine.say("Voice wakeup test completed, Lobster robot permanently on standby")
engine.runAndWait()

print("\nVoice wakeup test SUCCESS!")
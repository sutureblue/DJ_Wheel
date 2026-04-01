# DJ_Wheel

DJ Wheel is a hardware–software system that turns a rotary encoder into a digital record player.  
A physical wheel controls audio playback in real time—forward, backward, and at discrete speeds—using a continuous playhead model inspired by vinyl.

---

## How It Works

- An **Arduino Uno** reads a rotary encoder and calculates:
  - Rotation speed (RPM)
  - Direction

- It sends serial data to a **Raspberry Pi**

- A Python audio engine interprets that data to control playback:
  - Continuous playhead (like a record)
  - Reverse playback support
  - Discrete speed levels (no pitch-bending artifacts)
  - Smooth fades on direction changes
  - Auto-reset after inactivity

---

## Why It Exists

- Most digital audio interfaces treat input as **commands**
- This system treats input as **motion**

It’s designed to feel physical, responsive, and continuous—closer to interacting with a record than pressing buttons in software.

---

## Features

- Real-time scrubbing with direction awareness
- Reverse-first motion support
- Quantized playback speeds for stability
- Click/pop suppression via fade logic
- Robust USB audio output (installation-safe)
- Boot autostart via systemd

---

## Hardware

- Arduino Uno
- Rotary encoder
- Raspberry Pi
- USB speakers *(recommended for transient protection)*

---

## Software

- Python
  - sounddevice
  - soundfile
  - numpy
  - pyserial
- Serial communication between Arduino and Pi
- systemd user service for autostart

---

## Status

- Working, installation-ready system
- Designed for reliability over perfection

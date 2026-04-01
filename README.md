# DJ_Wheel

DJ Wheel is a hardware–software system that turns a rotary encoder into a digital record player.  
A physical wheel controls audio playback in real time—forward, backward, and at discrete speeds—using a continuous playhead model inspired by vinyl.

This system was developed as part of a combined **praxinoscope–zoetrope sculpture**, where intuitive, physical interaction was essential. The interface is designed to feel immediate and legible—something you understand by touch, not instruction.

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

It was designed specifically for use within a **praxinoscope–zoetrope sculpture**, where interaction needed to be:
- Immediate
- Physical
- Self-explanatory

The goal was to create something that feels closer to handling a record than operating software.

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

# DJ Wheel

DJ Wheel is a hardware–software system that turns a rotary encoder into a digital record player.  
A physical wheel controls audio playback in real time,
forward, backward, and at discrete speeds,
using a continuous playhead model inspired by vinyl.

It's really a simple setup if you have all the pieces.

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

This system was developed for a sculptural work combining a **praxinoscope** and **zoetrope** animation devices that require continuous rotation to function.

Because the animation is driven by physical rotation, the sound system had to operate the same way.  
The result, as a necessity, is a DJ style wheel.

The rotating pillar beneath and attached to animation sculptures is what the rotary wheel is engaged by and controls the speed.
This model was inspired by a [Scott Garner](https://scottmadethis.net/) piece titled, _Musical Chair_, though this system replaces his MIDI-based stepping with direct audio playback from a continuous file.

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
- Rotary encoder and wheel, [I used this](https://www.amazon.com/Polyurethane-Position-Measuring-Mounting-600PPR300mm/dp/B07H28H5FY/ref=sr_1_2_sspa?crid=381OCL5VTV7XB&dib=eyJ2IjoiMSJ9.JBezVbtQtsuvDk49jNP2apwkAZIRe-ceCRLaNt1KGC4TW55rmV7KS5MRlePsroqwA6RtzypKCt72QNMhl48bPbwCs8tqOAmN36Je9dyva92ahaKkJg0bnIeAx9sOaydKrYsZeRnkgv9A7-xrJfhkNLq5WmvEz1L1Mc_n-4gPsbfZcugQdnRUeId27Ur8cGrhOYuZtbsyaUcdXPcpuaC3UkaOehWNj3pThcOGSMigvFs.RjDjfHJmA0kl3KqNKgsuPxwYNhUSvxJs-41G_pyWWuo&dib_tag=se&keywords=rotary%2Bwheel%2Bencoder&qid=1775069639&sprefix=rotary%2Bwheel%2Bencode%2Caps%2C132&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)
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

- Working, installation-ready
- Designed for reliability and feel
- It is a lot of fun.

## License## License
This project is licensed under [CC BY-NC-SA 4.0](LICENSE).  
See the [full license details](https://creativecommons.org/licenses/by-nc-sa/4.0/).

Some portions of the code were developed with AI assistance.

# ============================
# DJ Wheel — Raspberry Pi Script
# ============================
# Replace paths and device names below with your own setup.

import soundfile as sf
import sounddevice as sd
import numpy as np
import threading
import time
import serial
import re

# ----------------------------
# CONFIG — EDIT THESE
# ----------------------------

# INSERT YOUR AUDIO FILE PATH
path = "/home/your_username/path/to/your_audio.wav"

# INSERT YOUR SERIAL PORT
# (check with: ls /dev/ttyUSB*)
PORT = "/dev/ttyUSB0"

# Arduino baud rate (must match Arduino code)
BAUD = 115200

# ----------------------------
# AUDIO SETTINGS
# ----------------------------
BLOCKSIZE = 2048
LATENCY = "high"  # "low" if you want tighter response (less stable)
FADE_MS = 30

# ----------------------------
# RPM / PLAYBACK SETTINGS
# ----------------------------
RPM_AT_1X = 80.0
RPM_MIN_REGISTER = 1.0
RPM_DEADBAND = 1.0
EFF_DEADBAND = max(RPM_MIN_REGISTER, RPM_DEADBAND)

# Discrete playback speeds (like DJ pitch steps)
LEVEL_RATES = [0.0, 0.125, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]

RPM_SMOOTH_ALPHA = 0.06
LEVEL_BAND_RPM = 6.0
LEVEL_HOLD_S = 0.18

RESET_AFTER_S = 30.0
SNAP_ON_MOTION_START = True

# ----------------------------
# LOAD AUDIO
# ----------------------------
audio, sr = sf.read(path, dtype="float32", always_2d=True)
frames, channels = audio.shape

# ----------------------------
# SHARED STATE
# ----------------------------
lock = threading.Lock()
running = True

playhead = 0.0
rate = 0.0
target_rate = 0.0

latest_rpm = 0.0
rpm_filt = 0.0

fade_samples = int((FADE_MS / 1000.0) * sr)
fade_remaining = 0

rpm_re = re.compile(r"RPM:([\-0-9.]+)")
last_motion_time = time.monotonic()

# ----------------------------
# HELPERS
# ----------------------------
def level_to_rpm(level_idx):
    return abs(LEVEL_RATES[level_idx]) * RPM_AT_1X

def choose_level_locked(abs_rpm, prev_level):
    if abs_rpm < EFF_DEADBAND:
        return 0

    if prev_level == 0:
        rpms = np.array([level_to_rpm(i) for i in range(1, len(LEVEL_RATES))])
        return int(np.argmin(np.abs(rpms - abs_rpm))) + 1

    prev_rpm = level_to_rpm(prev_level)
    down = max(1, prev_level - 1)
    up = min(len(LEVEL_RATES) - 1, prev_level + 1)

    if abs_rpm < (0.5 * (prev_rpm + level_to_rpm(down)) - LEVEL_BAND_RPM):
        return down
    if abs_rpm > (0.5 * (prev_rpm + level_to_rpm(up)) + LEVEL_BAND_RPM):
        return up

    return prev_level

# ----------------------------
# AUDIO CALLBACK
# ----------------------------
def callback(outdata, frame_count, time_info, status):
    global playhead, rate, fade_remaining

    with lock:
        tr = target_rate
        ph = playhead
        fr = fade_remaining

    # Smooth rate changes
    rate += 0.25 * (tr - rate)
    r = rate

    if abs(r) < 1e-6:
        out = np.zeros((frame_count, channels), dtype=np.float32)
        new_ph = ph
    else:
        pos = (ph + r * np.arange(frame_count)) % frames
        i0 = pos.astype(np.int64)
        i1 = (i0 + 1) % frames
        frac = pos - i0
        out = (1 - frac)[:, None] * audio[i0] + frac[:, None] * audio[i1]
        new_ph = (pos[-1] + r) % frames

    # Fade on direction change
    if fr > 0:
        n = min(fr, frame_count)
        out[:n] *= np.linspace(0, 1, n)[:, None]
        fr -= n

    outdata[:] = out

    with lock:
        playhead = new_ph
        fade_remaining = fr

# ----------------------------
# SERIAL THREAD
# ----------------------------
def serial_thread():
    global target_rate, fade_remaining, latest_rpm, rpm_filt, last_motion_time

    last_sign = 0
    direction = 1.0
    current_level = 0
    last_level_change = 0.0
    rpm_initialized = False
    was_moving = False

    # Connect to Arduino
    s = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2.0)  # allow Arduino to reset

    while running:
        now = time.monotonic()

        # Reset after inactivity
        if abs(target_rate) < 1e-6 and now - last_motion_time > RESET_AFTER_S:
            with lock:
                playhead = 0.0
                target_rate = 0.0
                fade_remaining = 0
            rpm_initialized = False
            was_moving = False

        raw = s.readline()
        m = rpm_re.search(raw.decode(errors="replace"))
        if not m:
            continue

        rpm_raw = float(m.group(1))
        if abs(rpm_raw) < RPM_MIN_REGISTER:
            rpm_raw = 0.0

        moving = abs(rpm_raw) >= RPM_MIN_REGISTER
        if moving:
            last_motion_time = now

        # Smooth RPM input
        if SNAP_ON_MOTION_START and moving and not was_moving:
            rpm_filt = rpm_raw
            rpm_initialized = True
        elif not rpm_initialized:
            rpm_filt = rpm_raw
            rpm_initialized = True
        else:
            rpm_filt = (1 - RPM_SMOOTH_ALPHA) * rpm_filt + RPM_SMOOTH_ALPHA * rpm_raw

        was_moving = moving
        rpm_use = rpm_filt if abs(rpm_filt) >= RPM_MIN_REGISTER else 0.0
        latest_rpm = rpm_use
        abs_rpm = abs(rpm_use)

        # Determine direction
        if rpm_use > EFF_DEADBAND:
            new_dir = 1.0
        elif rpm_use < -EFF_DEADBAND:
            new_dir = -1.0
        else:
            new_dir = direction

        sign = 0 if abs_rpm <= EFF_DEADBAND else (1 if new_dir > 0 else -1)
        if sign and last_sign and sign != last_sign:
            fade_remaining = fade_samples
        if sign:
            last_sign = sign
        direction = new_dir

        # Quantize speed levels
        desired = choose_level_locked(abs_rpm, current_level)
        if moving and desired == 0:
            desired = 1

        if desired != current_level and now - last_level_change >= LEVEL_HOLD_S:
            current_level = desired
            last_level_change = now

        with lock:
            target_rate = direction * LEVEL_RATES[current_level]

# ----------------------------
# START
# ----------------------------
threading.Thread(target=serial_thread, daemon=True).start()

with sd.OutputStream(
    samplerate=sr,
    channels=channels,
    blocksize=BLOCKSIZE,
    latency=LATENCY,
    callback=callback,
):
    while running:
        time.sleep(0.05)

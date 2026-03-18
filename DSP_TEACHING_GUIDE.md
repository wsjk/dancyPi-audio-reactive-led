# DSP.py Teaching Guide - Audio Signal Processing for LED Visualization

## Table of Contents

1. [Introduction](#introduction)
2. [What This File Does](#what-this-file-does)
3. [Core Concepts You'll Learn](#core-concepts-youll-learn)
4. [The ExpFilter Class - Smoothing Data](#the-expfilter-class---smoothing-data)
5. [FFT Functions - Converting Sound to Frequency](#fft-functions---converting-sound-to-frequency)
6. [The Mel Filterbank - Mimicking Human Hearing](#the-mel-filterbank---mimicking-human-hearing)
7. [Complete Data Flow](#complete-data-flow)
8. [Customizing LED Behavior](#customizing-led-behavior)
9. [Exercises for Learning](#exercises-for-learning)
10. [Troubleshooting Guide](#troubleshooting-guide)

---

## Introduction

Welcome! This guide will teach you how the `dsp.py` file works. **DSP** stands for **Digital Signal Processing** - the science of analyzing and manipulating digital signals (like audio).

### What You'll Build Understanding Of:

- How sound waves become numbers
- How to detect different frequencies (bass, mids, treble)
- How to smooth noisy data for better visuals
- How to modify the code to change LED behavior

### Prerequisites:

- Basic Python knowledge (variables, functions, classes)
- High school math (no calculus needed!)
- Curiosity about how audio visualizers work

---

## What This File Does

Think of `dsp.py` as a **translator**:

```
🎵 Sound Waves → 🔢 Numbers → 📊 Frequencies → 💡 LED Controls
```

**Real-world analogy**: If audio is a recipe, this file is the kitchen that processes ingredients (sound) into a meal (visual data for LEDs).

### The Three Main Jobs:

1. **Smoothing** (ExpFilter class) - Makes jerky data smooth
2. **Frequency Analysis** (rfft function) - Breaks sound into bass/mid/treble
3. **Perceptual Scaling** (Mel filterbank) - Groups frequencies like human ears hear them

---

## Core Concepts You'll Learn

### 1. What is Frequency?

**Frequency** = How many times per second a sound wave vibrates

- Measured in **Hertz (Hz)**
- **Low frequency (20-200 Hz)**: Bass drum, sub-bass
- **Mid frequency (200-2000 Hz)**: Vocals, guitars
- **High frequency (2000-20000 Hz)**: Cymbals, hi-hats

**Example**: When you hear a bass drop, that's low-frequency sound (40-80 Hz) making your chest rumble.

### 2. What is FFT?

**FFT** = Fast Fourier Transform

A mathematical algorithm that answers: "What frequencies are in this sound?"

**Analogy**: 
- You hear a chord on a guitar (mix of notes)
- FFT tells you: "That's E (82 Hz) + A (110 Hz) + C# (138 Hz)"

**Before FFT**: Audio is a wave over time (amplitude vs. time)
```
Time Domain:
  ^
  |    /\      /\
  |   /  \    /  \
  |  /    \  /    \
  | /      \/      \
  +------------------→ time
```

**After FFT**: Audio is broken into frequencies (amplitude vs. frequency)
```
Frequency Domain:
  ^
  |     |      |
  | |   |   |  |
  | |   |   |  |    |
  +-|-|-|-|-|-|-|---→ frequency
    ^   ^   ^   ^
   bass mid treble
```

### 3. What is Smoothing?

Raw audio data jumps around rapidly. Without smoothing, LEDs would flicker chaotically.

**Smoothing** = Averaging new values with old values for gradual transitions

**Example**:
```
Raw data:     [5, 98, 12, 89, 8, 95]  ← Chaotic!
Smoothed:     [5, 45, 35, 55, 40, 60] ← Gradual changes
```

---

## The ExpFilter Class - Smoothing Data

### Purpose

Creates smooth, pleasant LED transitions instead of strobing effects.

### The Code

```python
class ExpFilter:
    """Simple exponential smoothing filter"""
    def __init__(self, val=0.0, alpha_decay=0.5, alpha_rise=0.5):
        """Small rise / decay factors = more smoothing"""
        assert 0.0 < alpha_decay < 1.0, 'Invalid decay smoothing factor'
        assert 0.0 < alpha_rise < 1.0, 'Invalid rise smoothing factor'
        self.alpha_decay = alpha_decay
        self.alpha_rise = alpha_rise
        self.value = val
```

### Breaking It Down

#### Line 1: Class Definition

```python
class ExpFilter:
```

**What's a class?** A blueprint for creating objects. Like a cookie cutter that makes cookies.

#### Lines 3-5: The Constructor (`__init__`)

```python
def __init__(self, val=0.0, alpha_decay=0.5, alpha_rise=0.5):
```

**What does `__init__` do?** Runs automatically when you create a new ExpFilter object.

**Parameters explained**:
- `val`: Starting value (like starting LED brightness at 0)
- `alpha_decay`: Speed of fading OUT (0.0 = very slow, 1.0 = instant)
- `alpha_rise`: Speed of lighting UP (0.0 = very slow, 1.0 = instant)

**Example usage**:
```python
# Create a filter that lights up fast but fades slow
my_filter = ExpFilter(val=0.0, alpha_decay=0.1, alpha_rise=0.9)
```

#### Lines 6-7: Safety Checks

```python
assert 0.0 < alpha_decay < 1.0, 'Invalid decay smoothing factor'
assert 0.0 < alpha_rise < 1.0, 'Invalid rise smoothing factor'
```

**What is `assert`?** A safety check. If the condition is False, the program stops with an error message.

**Why?** Alpha values outside 0-1 don't make mathematical sense for exponential smoothing.

#### Lines 8-10: Store the Values

```python
self.alpha_decay = alpha_decay
self.alpha_rise = alpha_rise
self.value = val
```

**What is `self`?** Refers to "this specific object". Like saying "my phone" vs "a phone".

### The Update Method - Where the Magic Happens

```python
def update(self, value):
    if isinstance(self.value, (list, np.ndarray, tuple)):
        alpha = value - self.value
        alpha[alpha > 0.0] = self.alpha_rise
        alpha[alpha <= 0.0] = self.alpha_decay
    else:
        alpha = self.alpha_rise if value > self.value else self.alpha_decay
    self.value = alpha * value + (1.0 - alpha) * self.value
    return self.value
```

#### Step-by-Step Breakdown

**Line 2-5: Handle Multiple Values at Once**

```python
if isinstance(self.value, (list, np.ndarray, tuple)):
```

Checks: "Am I smoothing one number or many numbers?"
- **One number**: Single LED brightness
- **Multiple numbers**: All 24 frequency bins at once

**Lines 3-5: Choose Alpha for Each Value**

```python
alpha = value - self.value                    # Calculate difference
alpha[alpha > 0.0] = self.alpha_rise         # If going up, use rise speed
alpha[alpha <= 0.0] = self.alpha_decay       # If going down, use decay speed
```

**Visual example**:
```
Current values: [10, 50, 30]
New values:     [40, 20, 30]
Differences:    [+30, -30, 0]
                 ↓    ↓    ↓
Alphas used:    [rise, decay, decay]
```

**Line 7: Simple Case (One Value)**

```python
alpha = self.alpha_rise if value > self.value else self.alpha_decay
```

If-else in one line! Reads as: "Use rise alpha if increasing, else use decay alpha"

**Line 8: The Smoothing Formula**

```python
self.value = alpha * value + (1.0 - alpha) * self.value
```

This is **exponential weighted average**:
- `alpha`: Weight given to NEW value (0-1)
- `(1.0 - alpha)`: Weight given to OLD value

**Math example**:
```
Current LED brightness: 20
New audio peak: 100
Alpha: 0.3

Calculation: (0.3 × 100) + (0.7 × 20)
           = 30 + 14
           = 44

Result: LED brightness becomes 44 (not 100)
Next frame: (0.3 × 100) + (0.7 × 44) = 30 + 30.8 = 60.8
Gradually approaches 100!
```

### Why Two Different Alphas?

**Creative effect**: LEDs can **light up instantly** but **fade slowly** (trailing effect)

```python
# Fast attack, slow release (like a drum hit with reverb)
filter = ExpFilter(val=0.0, alpha_decay=0.05, alpha_rise=0.95)

# Slow attack, fast release (smooth, responsive)
filter = ExpFilter(val=0.0, alpha_decay=0.8, alpha_rise=0.2)
```

---

## FFT Functions - Converting Sound to Frequency

### rfft() - Real FFT (Used in This Project)

```python
def rfft(data, window=None):
    window = 1.0 if window is None else window(len(data))
    ys = np.abs(np.fft.rfft(data * window))
    xs = np.fft.rfftfreq(len(data), 1.0 / config.MIC_RATE)
    return xs, ys
```

#### Breaking It Down

**Line 1: Function Definition**

```python
def rfft(data, window=None):
```

**Parameters**:
- `data`: Array of audio samples (numbers representing sound wave)
- `window`: Optional function to reduce edge effects (explained below)

**Line 2: Handle Window Function**

```python
window = 1.0 if window is None else window(len(data))
```

**What's a window function?** 

Raw audio chunks have sharp edges that cause "frequency leakage" in FFT. Windows smooth these edges.

**Visual**:
```
Without window (sharp edges):
|█████████|  ← Creates false frequencies

With window (tapered edges):
 /███████\   ← Cleaner frequency data
```

Common windows: Hamming, Hanning, Blackman (not used in this simple version)

**Line 3: Perform FFT**

```python
ys = np.abs(np.fft.rfft(data * window))
```

**Step by step**:
1. `data * window`: Apply window function to audio
2. `np.fft.rfft(...)`: Real FFT (optimized for real-valued audio)
3. `np.abs(...)`: Get magnitude only (ignore phase)

**Why `rfft` instead of `fft`?** 
- Audio is real-valued (not complex)
- `rfft` is 2x faster and uses half the memory
- Returns only positive frequencies (negative are mirror images)

**Line 4: Get Frequency Labels**

```python
xs = np.fft.rfftfreq(len(data), 1.0 / config.MIC_RATE)
```

**What does this do?** Creates an array of frequency values for each FFT bin.

**Example**:
```python
# If config.MIC_RATE = 48000 Hz and len(data) = 1024

xs = [0, 46.875, 93.75, 140.625, ..., 24000]
     ↑       ↑       ↑        ↑           ↑
    DC    1st bin  2nd bin  3rd bin  Nyquist
```

**Line 5: Return Results**

```python
return xs, ys
```

Returns two arrays:
- `xs`: Frequencies (Hz)
- `ys`: Amplitudes (how loud each frequency is)

### Example Usage

```python
# Simulate audio data
import numpy as np
audio_samples = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 48000))  # 440 Hz (A note)

# Run FFT
frequencies, amplitudes = rfft(audio_samples)

# Find strongest frequency
strongest_freq_index = np.argmax(amplitudes)
detected_frequency = frequencies[strongest_freq_index]
print(f"Detected: {detected_frequency} Hz")  # Should be ~440 Hz
```

### fft() - Complex FFT (Not Used in This Project)

```python
def fft(data, window=None):
    window = 1.0 if window is None else window(len(data))
    ys = np.fft.fft(data * window)
    xs = np.fft.fftfreq(len(data), 1.0 / config.MIC_RATE)
    return xs, ys
```

**Difference**: Returns complex numbers (includes phase information)

**When to use**: 
- Need both positive and negative frequencies
- Analyzing phase relationships
- Not needed for LED visualization!

---

## The Mel Filterbank - Mimicking Human Hearing

### What is a Mel Scale?

The **mel scale** is a perceptual frequency scale based on how humans hear.

**Key insight**: We don't hear frequencies linearly!

**Examples**:
- 100 Hz → 200 Hz: Sounds like a BIG difference (octave jump)
- 10,000 Hz → 10,100 Hz: Barely noticeable difference

**The mel scale spaces frequency bins to match this perception**:
```
Linear Scale (bad for audio):
|-----|-----|-----|-----|-----|  ← Equal spacing
0    2k    4k    6k    8k   10k Hz

Mel Scale (good for audio):
|--|---|-----|--------|---------| ← Wider at high frequencies
0  200  500  1k   2k   5k   10k Hz
```

### create_mel_bank() Function

```python
def create_mel_bank():
    global samples, mel_y, mel_x
    samples = int(config.MIC_RATE * config.N_ROLLING_HISTORY / (2.0 * config.FPS))
    mel_y, (_, mel_x) = melbank.compute_melmat(num_mel_bands=config.N_FFT_BINS,
                                               freq_min=config.MIN_FREQUENCY,
                                               freq_max=config.MAX_FREQUENCY,
                                               num_fft_bands=samples,
                                               sample_rate=config.MIC_RATE)
```

#### Line-by-Line Breakdown

**Line 2: Global Variables**

```python
global samples, mel_y, mel_x
```

**What is `global`?** Makes these variables accessible everywhere in the file (not just in this function).

**Why?** Other parts of the code need these pre-calculated values.

**Line 3: Calculate Sample Size**

```python
samples = int(config.MIC_RATE * config.N_ROLLING_HISTORY / (2.0 * config.FPS))
```

**This calculates**: How many audio samples to analyze in each FFT calculation

**Formula explained**:
```
samples = (samples per second × time window) / (2.0 × updates per second)
```

**Real example** (typical values):
```
config.MIC_RATE = 48,000 Hz           (48,000 audio samples per second)
config.N_ROLLING_HISTORY = 2 seconds  (look at last 2 seconds of audio)
config.FPS = 60                       (update LEDs 60 times per second)

samples = (48,000 × 2) / (2.0 × 60)
        = 96,000 / 120
        = 800 samples per FFT
```

**Why divide by 2.0?** Related to Nyquist theorem - we need at least 2 samples per wave cycle.

**Lines 4-8: Create Mel Filterbank Matrix**

```python
mel_y, (_, mel_x) = melbank.compute_melmat(
    num_mel_bands=config.N_FFT_BINS,      # Output: 24 mel bins
    freq_min=config.MIN_FREQUENCY,         # Analyze from 200 Hz
    freq_max=config.MAX_FREQUENCY,         # Up to 12,000 Hz
    num_fft_bands=samples,                 # Input: 800 FFT bins
    sample_rate=config.MIC_RATE)           # 48,000 Hz sample rate
```

**What does this do?**

Creates a **transformation matrix** that converts:
- **800 FFT frequency bins** (raw, evenly-spaced)
- **24 mel bins** (perceptually-spaced)

**Visual representation**:

```
FFT Output (800 bins - Linear spacing):
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||...
0Hz        1kHz       2kHz       3kHz       4kHz      5kHz...

                        ↓ mel_y matrix transforms ↓

Mel Bins (24 bins - Perceptual spacing):
[==][===][====][=====][======][========][==========][==============]...
 0   200  400   700   1100   1600     2500      4000      7000  12kHz
 ↑                                                               ↑
Bass frequencies (narrow bins)        Treble frequencies (wide bins)
```

**Return values explained**:

```python
mel_y, (_, mel_x) = melbank.compute_melmat(...)
```

- `mel_y`: Matrix for transformation (shape: 24 × 800)
- `mel_x`: Center frequency of each mel bin (array of 24 values)
- `_`: Ignored value (bin edge frequencies we don't need)

**How the matrix works**:

```python
# Later in the code (simplified):
fft_bins = [0.1, 0.5, 2.3, 0.8, ...]  # 800 values from FFT
mel_bins = mel_y @ fft_bins             # Matrix multiplication
# mel_bins = [1.2, 3.5, 0.8, ...]       # 24 values for LEDs
```

The `@` operator does **matrix multiplication**, which groups and weights FFT bins into mel bins.

### Global Variable Initialization

```python
samples = None
mel_y = None
mel_x = None
create_mel_bank()
```

**Why initialize as `None` first?**

1. **Good practice**: Declare variables before using them
2. **Prevents errors**: If `create_mel_bank()` fails, variables still exist
3. **Code clarity**: Shows what variables will be available

**Last line**: Immediately calls `create_mel_bank()` to populate these with actual values.

---

## Complete Data Flow

### The Full Pipeline (From Microphone to LEDs)

```
┌──────────────┐
│  Microphone  │ Records sound waves
└──────┬───────┘
       │ [0.1, 0.5, 0.3, -0.2, 0.4, ...] ← 800 audio samples
       ↓
┌──────────────┐
│  rfft()      │ Converts time → frequency
└──────┬───────┘
       │ xs = [0, 48, 96, 144, ...] Hz       ← Frequency labels
       │ ys = [0.1, 0.5, 2.3, 0.8, ...] ← Amplitudes
       ↓
┌──────────────┐
│  mel_y @     │ Groups 800 bins → 24 mel bins
│  matrix      │ (Matrix multiplication)
└──────┬───────┘
       │ [1.2, 3.5, 0.8, 2.1, ...] ← 24 perceptual frequency bands
       ↓
┌──────────────┐
│  ExpFilter   │ Smooths the values
└──────┬───────┘
       │ [1.1, 3.2, 0.9, 2.0, ...] ← 24 smoothed values
       ↓
┌──────────────┐
│visualization │ Splits into bass/mid/treble
│    .py       │ Maps to RGB colors
└──────┬───────┘
       │ Red:   [1.1, 3.2, 0.9, ...]  ← Bins 0-7 (bass)
       │ Green: [2.0, 1.5, 0.7, ...]  ← Bins 8-15 (mids)
       │ Blue:  [0.8, 1.2, 2.5, ...]  ← Bins 16-23 (treble)
       ↓
┌──────────────┐
│  LED Strip   │ 💡💡💡💡💡💡💡💡
└──────────────┘
```

### Real-World Example: Bass Drop Detection

Let's trace what happens when a bass drop hits:

**1. Microphone captures the sound**
```python
audio_samples = [0.9, 0.8, -0.9, -0.8, 0.9, ...]  # Low frequency, high amplitude
```

**2. FFT analyzes frequencies**
```python
frequencies, amplitudes = rfft(audio_samples)
# amplitudes[0:10] = [0.0, 8.5, 9.2, 8.8, ...]  ← High amplitude at low frequencies!
# amplitudes[100:110] = [0.1, 0.2, 0.1, ...]    ← Low amplitude at high frequencies
```

**3. Mel filterbank groups them**
```python
mel_bins = mel_y @ amplitudes
# mel_bins[0:8] = [8.9, 8.7, 8.5, ...]    ← Bass bins (HIGH values)
# mel_bins[8:16] = [0.5, 0.3, 0.2, ...]   ← Mid bins (low values)
# mel_bins[16:24] = [0.1, 0.1, 0.2, ...]  ← Treble bins (low values)
```

**4. ExpFilter smooths**
```python
smoothed = filter.update(mel_bins)
# If previous value was 2.0 and new value is 8.9:
# smoothed[0] = 0.9 × 8.9 + 0.1 × 2.0 = 8.01 + 0.2 = 8.21
```

**5. Visualization maps to LEDs**
```python
# In visualization.py (scroll mode)
r = int(np.max(smoothed[0:8]))    # r = 8 → Red LEDs very bright (bass!)
g = int(np.max(smoothed[8:16]))   # g = 0 → Green LEDs off
b = int(np.max(smoothed[16:24]))  # b = 0 → Blue LEDs off

# Result: Bright red flash = bass drop detected! 🔴💥
```

---

## Customizing LED Behavior

### Goal: Make More LEDs Light Up Per Frequency (Without Buying New Hardware)

You have **144 LEDs** but want **more dramatic, wider light patterns**. Here are proven methods:

### Method 1: Reduce Frequency Bins (Most Dramatic) ⭐ RECOMMENDED

**What it does**: Fewer bins = each bin covers wider frequency range = bigger LED reactions

**Edit `config.py`**:

```python
# Find this line:
N_FFT_BINS = 24  # Default

# Change to:
N_FFT_BINS = 8   # Each bin covers 3x wider frequency range!
```

**After changing, run**:
```bash
cd /path/to/python/folder
python3 -c "import dsp; dsp.create_mel_bank()"
```

**Why this works**:

With 24 bins:
```
Bass bins: [0-7]   = 8 bins × (144 LEDs / 24 bins) = 48 LEDs for bass
```

With 8 bins:
```
Bass bins: [0-2]   = 3 bins × (144 LEDs / 8 bins) = 54 LEDs for bass
Plus wider frequency coverage = more likely to trigger!
```

**Recommended values**:

| N_FFT_BINS | Effect | Best For |
|------------|--------|----------|
| **6** | Extremely dramatic, chunky | Heavy bass music (EDM, dubstep) |
| **8** | Very dramatic, bold | Parties, energetic music |
| **12** | Moderate drama | Balanced, most genres |
| **16** | Subtle widening | Rock, vocals |
| **24** | Default (detailed) | Studio monitoring |

### Method 2: Adjust Smoothing for Longer Trails

**What it does**: LEDs stay lit longer, creating trailing/comet effects

**Edit `visualization.py`**:

Find where ExpFilter is created (look for lines like this):

```python
# Original (example from line ~110):
gain = ExpFilter(np.tile(0.01, config.N_FFT_BINS), 
                 alpha_decay=0.001, 
                 alpha_rise=0.99)

# Change to longer trails:
gain = ExpFilter(np.tile(0.01, config.N_FFT_BINS), 
                 alpha_decay=0.0001,  # Slower fade (was 0.001)
                 alpha_rise=0.99)
```

**Parameters to tweak**:

```python
alpha_decay:  # Controls fade-out speed
  1.0   = Instant off (no trail)
  0.5   = Medium trail
  0.1   = Long trail
  0.01  = Very long trail
  0.001 = Extremely long trail

alpha_rise:   # Controls light-up speed
  1.0   = Instant on (snappy)
  0.9   = Fast response (good for music)
  0.5   = Slow response (smooth, dreamy)
  0.1   = Very slow (underwater effect)
```

**Creative combinations**:

```python
# Fast attack, long release (comet/shooting star effect)
ExpFilter(alpha_decay=0.001, alpha_rise=0.95)

# Slow attack, fast release (breathing effect)
ExpFilter(alpha_decay=0.8, alpha_rise=0.2)

# Both slow (underwater, dreamy)
ExpFilter(alpha_decay=0.3, alpha_rise=0.3)
```

### Method 3: Amplify Frequency Response

**What it does**: Makes quieter sounds trigger more LEDs

**Edit `visualization.py`**:

In the `visualize_scroll()` function (around line 118):

```python
# Original:
y = y**2.0        # Square the values (emphasizes peaks)
gain.update(y)
y /= gain.value
y *= 255.0

# More sensitive (lights up easier):
y = y**1.5        # Lower exponent = more sensitivity
gain.update(y)
y /= gain.value
y *= 350.0        # Higher multiplier = brighter (was 255.0)
```

**Exponent effects**:

```python
y = y**3.0   # Very sharp response (only strong beats)
y = y**2.0   # Default (balanced)
y = y**1.5   # More sensitive
y = y**1.0   # Very sensitive (lights up for everything)
```

### Method 4: Change Frequency Ranges

**What it does**: Focus on specific frequency ranges (more bass, less treble)

**Edit `config.py`**:

```python
# Original (balanced):
MIN_FREQUENCY = 200    # Start at 200 Hz
MAX_FREQUENCY = 12000  # End at 12,000 Hz

# Bass-heavy (clubs, EDM):
MIN_FREQUENCY = 60     # Include sub-bass
MAX_FREQUENCY = 8000   # Cut high treble

# Treble-focused (vocals, acoustic):
MIN_FREQUENCY = 500    # Cut low bass
MAX_FREQUENCY = 16000  # Include more highs
```

**After changing, regenerate mel bank**:
```bash
python3 -c "import dsp; dsp.create_mel_bank()"
```

### Method 5: Visualization Mode Selection

Different modes show more/fewer LEDs:

**Edit which mode runs in your main file**:

```python
# In visualization.py or your main script:

# ENERGY mode - Shows most LEDs (fills up based on volume)
visualize_energy(...)

# SCROLL mode - Medium LEDs (center LED that scrolls out)
visualize_scroll(...)

# SPECTRUM mode - Least LEDs (one LED per frequency)
visualize_spectrum(...)
```

**Energy mode breakdown** (from lines 147-166):

```python
# This mode lights up MORE LEDs because it fills from the start
third = len(y) // 3
r = int(np.mean(y[:third]**scale))   # Number of red LEDs to light
g = int(np.mean(y[third: 2*third]**scale))
b = int(np.mean(y[2*third:]**scale))

p[0, :r] = 255.0    # Lights up FIRST 'r' LEDs (could be many!)
p[1, :g] = 255.0    # Lights up FIRST 'g' LEDs
p[2, :b] = 255.0    # Lights up FIRST 'b' LEDs
```

**To make energy mode even more dramatic**:

```python
# Around line 153:
scale = 2.0   # Original
scale = 3.0   # More dramatic (was 2.0)

# This means:
# r = int(np.mean(y[:third]**3.0))  # Cubed values = much bigger numbers!
```

### Quick Reference: "More LEDs" Settings

**Copy these into `config.py` for maximum drama**:

```python
# Maximum drama settings:
N_FFT_BINS = 6           # Was 24 (fewer bins = wider coverage)
MIN_FREQUENCY = 60       # Was 200 (include more bass)
MAX_FREQUENCY = 8000     # Was 12000 (focus on bass/mids)
N_PIXELS = 144           # Your LED count
```

**Then in `visualization.py`, find the gain filter and change**:

```python
gain = ExpFilter(np.tile(0.01, config.N_FFT_BINS), 
                 alpha_decay=0.0005,   # Very long trails
                 alpha_rise=0.99)       # Fast response
```

**And amplify the response**:

```python
# In visualize_scroll (around line 118):
y = y**1.5    # Was 2.0 (more sensitive)
# ... (other code)
y *= 350.0    # Was 255.0 (brighter)
```

---

## Exercises for Learning

### Beginner Level

**Exercise 1: Create Your First Filter**

```python
# Create a new file: test_filter.py
import numpy as np
from dsp import ExpFilter

# Create a filter
my_filter = ExpFilter(val=0.0, alpha_decay=0.2, alpha_rise=0.8)

# Simulate audio peaks
audio_peaks = [0, 10, 50, 100, 80, 60, 40, 20, 0]

print("Frame | Audio Peak | Filtered Value")
print("------|------------|---------------")
for i, peak in enumerate(audio_peaks):
    smoothed = my_filter.update(peak)
    print(f"  {i}   |     {peak:3d}    |     {smoothed:6.2f}")
```

**Expected output**: You'll see smoothed values that gradually rise and fall.

**Exercise 2: Experiment with Different Alphas**

Try changing `alpha_rise` and `alpha_decay` to see how smoothing changes:

```python
# Fast rise, slow fall (exciting!)
filter1 = ExpFilter(alpha_decay=0.1, alpha_rise=0.9)

# Slow rise, fast fall (smooth)
filter2 = ExpFilter(alpha_decay=0.9, alpha_rise=0.1)

# Very smooth (underwater)
filter3 = ExpFilter(alpha_decay=0.3, alpha_rise=0.3)
```

### Intermediate Level

**Exercise 3: Visualize FFT Output**

```python
# test_fft.py
import numpy as np
import matplotlib.pyplot as plt
from dsp import rfft

# Generate a 440 Hz sine wave (musical note A)
duration = 1.0  # seconds
sample_rate = 48000
t = np.linspace(0, duration, int(sample_rate * duration))
audio = np.sin(2 * np.pi * 440 * t)

# Run FFT
frequencies, amplitudes = rfft(audio)

# Plot
plt.figure(figsize=(12, 4))
plt.plot(frequencies[:500], amplitudes[:500])  # Plot first 500 bins
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('FFT of 440 Hz Sine Wave')
plt.grid(True)
plt.show()
```

**Challenge**: Add more sine waves (chords) and see multiple peaks!

**Exercise 4: Compare Mel Bins vs Linear Bins**

```python
# Understand mel spacing
import config
from dsp import create_mel_bank, mel_x

create_mel_bank()

print("Mel Bin | Center Frequency (Hz)")
print("--------|---------------------")
for i, freq in enumerate(mel_x):
    print(f"   {i:2d}   |      {freq:7.1f}")

print(f"\nNotice: Bins get wider at higher frequencies!")
print(f"Bin 0-1 spacing: {mel_x[1] - mel_x[0]:.1f} Hz")
print(f"Bin 22-23 spacing: {mel_x[23] - mel_x[22]:.1f} Hz")
```

### Advanced Level

**Exercise 5: Create a Custom Visualization Mode**

Add this function to `visualization.py`:

```python
def visualize_bass_pulse(y):
    """Custom mode: Only react to bass, pulse all LEDs same color"""
    global p
    
    # Get bass energy (first third of frequency bins)
    third = len(y) // 3
    bass_energy = np.mean(y[:third]**2.0) * 255.0
    bass_energy = int(np.clip(bass_energy, 0, 255))
    
    # Pulse all LEDs red based on bass
    p[0, :] = bass_energy  # Red channel
    p[1, :] = 0            # Green off
    p[2, :] = 0            # Blue off
    
    return p
```

**Exercise 6: Frequency Range Finder**

Create a tool to find the best frequency ranges for your music:

```python
# frequency_analyzer.py
import numpy as np
from dsp import rfft, create_mel_bank, mel_y, mel_x
import sounddevice as sd

create_mel_bank()

def analyze_audio_live(duration=5):
    """Record audio and show which frequencies are strongest"""
    print(f"Recording {duration} seconds...")
    audio = sd.rec(int(duration * 48000), samplerate=48000, channels=1)
    sd.wait()
    
    # Analyze
    frequencies, amplitudes = rfft(audio.flatten())
    mel_bins = mel_y @ amplitudes
    
    # Show results
    print("\nFrequency Band Analysis:")
    print("Mel Bin | Frequency | Energy | Bar")
    print("--------|-----------|--------|" + "-"*30)
    
    for i, (freq, energy) in enumerate(zip(mel_x, mel_bins)):
        bar = "█" * int(energy / np.max(mel_bins) * 30)
        print(f"   {i:2d}   | {freq:7.1f} Hz | {energy:6.2f} | {bar}")
    
    print(f"\nDominant frequencies: {mel_x[np.argsort(mel_bins)[-3:]]} Hz")

analyze_audio_live()
```

---

## Troubleshooting Guide

### Problem: LEDs flickering like crazy

**Cause**: Not enough smoothing

**Solution**:
```python
# In visualization.py, find ExpFilter and decrease alpha_decay:
alpha_decay=0.001  # Was probably higher
```

### Problem: LEDs barely responding to music

**Cause**: Too much smoothing or not enough sensitivity

**Solutions**:

1. **Increase alpha values**:
```python
alpha_rise=0.95  # Was probably lower
```

2. **Lower the exponent**:
```python
y = y**1.5  # Was 2.0 or higher
```

3. **Check MIN_FREQUENCY**:
```python
MIN_FREQUENCY = 60  # Make sure it's low enough for bass
```

### Problem: Only treble/high frequencies working

**Cause**: MIN_FREQUENCY too high

**Solution**:
```python
# In config.py:
MIN_FREQUENCY = 60  # Was probably 200+
```

Then regenerate:
```bash
python3 -c "import dsp; dsp.create_mel_bank()"
```

### Problem: Code crashes with "samples is None"

**Cause**: `create_mel_bank()` wasn't called

**Solution**:
Make sure `config.py` has all required values:
```python
MIC_RATE = 48000
N_ROLLING_HISTORY = 2
FPS = 60
N_FFT_BINS = 24
MIN_FREQUENCY = 200
MAX_FREQUENCY = 12000
```

### Problem: "Assert" error when creating ExpFilter

**Cause**: Alpha values outside 0-1 range

**Solution**:
```python
# Make sure:
0.0 < alpha_decay < 1.0
0.0 < alpha_rise < 1.0

# WRONG:
ExpFilter(alpha_decay=1.5)  # Too high!
ExpFilter(alpha_rise=0.0)   # Can't be exactly 0

# RIGHT:
ExpFilter(alpha_decay=0.5)
ExpFilter(alpha_rise=0.99)
```

### Problem: Not enough bass response

**Solutions**:

1. **Focus on bass frequencies**:
```python
MIN_FREQUENCY = 40    # Lower
MAX_FREQUENCY = 4000  # Cut treble
```

2. **Use energy mode instead of scroll**:
```python
# Energy mode lights up more LEDs for bass
visualize_energy(...)  # Instead of visualize_scroll(...)
```

3. **Increase bass bin weighting**:
```python
# In visualization.py, in visualize_scroll():
third = len(y) // 3
r = int(np.max(y[:third]) * 1.5)  # Multiply bass by 1.5x
```

---

## Summary

### What You Learned

✅ **ExpFilter**: Smooths data by averaging new and old values  
✅ **FFT**: Converts time-domain audio to frequency-domain data  
✅ **Mel Scale**: Groups frequencies like human ears perceive them  
✅ **Pipeline**: Microphone → FFT → Mel Bins → Smooth → LEDs  
✅ **Customization**: How to make more LEDs light up without new hardware  

### Key Takeaways

1. **Fewer bins = more dramatic**: `N_FFT_BINS = 8` for parties
2. **Lower exponents = more sensitive**: `y = y**1.5` instead of `y**2.0`
3. **Slower decay = longer trails**: `alpha_decay=0.001` for comet effects
4. **Focus on bass**: `MIN_FREQUENCY = 60`, `MAX_FREQUENCY = 8000`

### Quick Settings for More LEDs

```python
# config.py
N_FFT_BINS = 8           # Fewer bins (was 24)
MIN_FREQUENCY = 60       # More bass (was 200)
MAX_FREQUENCY = 8000     # Less treble (was 12000)

# visualization.py (in ExpFilter):
alpha_decay=0.0005       # Longer trails (was 0.001)

# visualization.py (in processing):
y = y**1.5               # More sensitive (was 2.0)
y *= 350.0               # Brighter (was 255.0)
```

### Next Steps

1. **Try the exercises** to cement your understanding
2. **Experiment with different alpha values** for your music style
3. **Adjust N_FFT_BINS** to find your sweet spot
4. **Create custom visualization modes** (Exercise 5)
5. **Share your settings** with the community!

### Further Resources

- **FFT Tutorial**: https://www.dspguide.com/ch8/1.htm
- **Mel Scale Explained**: https://en.wikipedia.org/wiki/Mel_scale
- **NumPy Documentation**: https://numpy.org/doc/stable/
- **Python Classes**: https://docs.python.org/3/tutorial/classes.html

---

## Appendix: Configuration Reference

### config.py Settings That Affect dsp.py

```python
# Audio capture
MIC_RATE = 48000              # Sample rate (Hz) - standard is 44100 or 48000
N_ROLLING_HISTORY = 2         # Time window (seconds) for FFT

# Frequency analysis
N_FFT_BINS = 24               # Number of mel frequency bands
MIN_FREQUENCY = 200           # Lowest frequency to analyze (Hz)
MAX_FREQUENCY = 12000         # Highest frequency to analyze (Hz)

# Display
FPS = 60                      # LED update rate (frames per second)
N_PIXELS = 144                # Number of LEDs on your strip
```

### Typical Value Ranges

| Setting | Min | Typical | Max | Notes |
|---------|-----|---------|-----|-------|
| MIC_RATE | 8000 | 48000 | 96000 | Higher = better quality |
| N_FFT_BINS | 4 | 24 | 128 | Lower = more dramatic |
| MIN_FREQUENCY | 20 | 200 | 500 | Lower = more bass |
| MAX_FREQUENCY | 4000 | 12000 | 20000 | Higher = more treble |
| FPS | 30 | 60 | 120 | Higher = smoother |
| alpha_decay | 0.0001 | 0.001-0.5 | 0.99 | Lower = longer trails |
| alpha_rise | 0.1 | 0.5-0.99 | 0.99 | Higher = snappier |

---

**Happy coding! 🎵💡🎉**

*Made with ❤️ for beginners learning audio DSP*


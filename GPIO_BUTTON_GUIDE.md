# GPIO Button Controls Guide - Raspberry Pi 3B

## Overview

This guide shows you how to add physical buttons to your Raspberry Pi 3B to control LED visualization parameters **while the script is running**. No need to stop and restart!

---

## What You Can Control

Press buttons to adjust these parameters in real-time:

| Parameter | What It Does | Effect |
|-----------|-------------|---------|
| **N_FFT_BINS** | Number of frequency bands | More bins = detailed, fewer = dramatic |
| **Sensitivity** | How reactive to sound | Higher = louder sounds needed |
| **Visualization Mode** | Effect type | Scroll / Energy / Spectrum |

---

## Hardware Setup

### Required Components

- **Raspberry Pi 3B** (already have this!)
- **5 momentary push buttons** (normally open)
- **Jumper wires** (female-to-female recommended)
- **Breadboard** (optional, makes wiring easier)

### No Resistors Needed!

The code uses **internal pull-up resistors** built into the Raspberry Pi, so you don't need any external components!

### Button Wiring Diagram

Connect each button between a GPIO pin and GND (ground):

```
Raspberry Pi 3B Pinout (GPIO pins only):

     3.3V [ 1] [ 2] 5V
  GPIO  2 [ 3] [ 4] 5V
  GPIO  3 [ 5] [ 6] GND  ← Use this for button ground
  GPIO  4 [ 7] [ 8] GPIO 14
      GND [ 9] [10] GPIO 15
 GPIO 17 [11] [12] GPIO 18  ← LED strip (don't use for buttons)
 GPIO 27 [13] [14] GND  ← Can use for button ground
 GPIO 22 [15] [16] GPIO 23  ← Button 1: Decrease FFT bins
     3.3V [17] [18] GPIO 24  ← Button 2: Increase FFT bins
 GPIO 10 [19] [20] GND  ← Can use for button ground
  GPIO 9 [21] [22] GPIO 25  ← Button 3: Cycle visualization
 GPIO 11 [23] [24] GPIO 8
      GND [25] [26] GPIO 7
  GPIO 0 [27] [28] GPIO 1
  GPIO 5 [29] [30] GND  ← Can use for button ground
  GPIO 6 [31] [32] GPIO 12
 GPIO 13 [33] [34] GND  ← Can use for button ground
 GPIO 19 [35] [36] GPIO 16  ← Button 4: Decrease sensitivity
 GPIO 26 [37] [38] GPIO 20
      GND [39] [40] GPIO 21
```

### Wiring Table

| Button Function | GPIO Pin | Physical Pin | Wire To |
|----------------|----------|--------------|---------|
| Decrease FFT Bins | GPIO 23 | Pin 16 | One button terminal |
| Increase FFT Bins | GPIO 24 | Pin 18 | One button terminal |
| Cycle Visualization | GPIO 25 | Pin 22 | One button terminal |
| Decrease Sensitivity | GPIO 16 | Pin 36 | One button terminal |
| Increase Sensitivity | GPIO 17 | Pin 11 | One button terminal |
| Ground (all buttons) | GND | Pins 6, 9, 14, 20, 25, 30, 34, 39 | Other button terminal |

### Simple Breadboard Layout

```
Raspberry Pi                    Breadboard
  GPIO 23 ──────────────────► Button 1 ─┐
  GPIO 24 ──────────────────► Button 2 ─┤
  GPIO 25 ──────────────────► Button 3 ─┼──► GND Rail ◄── Pi GND
  GPIO 16 ──────────────────► Button 4 ─┤
  GPIO 17 ──────────────────► Button 5 ─┘
```

### Photo Guide (Example)

```
[Button pressed = LED lights up]

Button wiring (side view):
    ┌─────┐
    │  •  │ ← Terminal 1 (connect to GPIO pin)
    │     │
    │  •  │ ← Terminal 2 (connect to GND)
    └─────┘
```

---

## Software Setup

### Files Already Created

The installation created these files:
- `gpio_controls.py` - Main GPIO control module
- Updated `visualization.py` - Integrated with GPIO

### Installation Steps

**Step 1: Install RPi.GPIO (if not already installed)**

```bash
cd ~/Desktop/work/rpi/dancyPi-audio-reactive-led/python
sudo apt-get update
sudo apt-get install python3-rpi.gpio
```

Or using pip:
```bash
pip3 install RPi.GPIO
```

**Step 2: Test GPIO Setup (Before Connecting Buttons)**

```bash
cd ~/Desktop/work/rpi/dancyPi-audio-reactive-led/python
python3 gpio_controls.py
```

You should see:
```
GPIO Button Controls Initialized!
====================================
Button Mappings:
  GPIO 23: Decrease frequency bins (more dramatic)
  GPIO 24: Increase frequency bins (more detail)
  ...
```

**Step 3: Connect Your Buttons**

Now physically wire the buttons according to the wiring table above.

**Step 4: Test Button Presses**

With the test script still running (`python3 gpio_controls.py`), press each button. You should see messages like:

```
🎵 FFT Bins decreased to: 16 (more dramatic!)
   Each frequency bin covers wider range
   → Bigger, bolder LED reactions
```

**Step 5: Run the Full Visualization**

```bash
cd ~/Desktop/work/rpi/dancyPi-audio-reactive-led/python
sudo python3 visualization.py scroll
```

Or with energy mode:
```bash
sudo python3 visualization.py energy
```

> **Note**: Use `sudo` because LED control requires root privileges.

---

## Button Functions Explained

### Button 1: Decrease FFT Bins (GPIO 23)

**Press to make effects MORE DRAMATIC**

- **What it does**: Reduces the number of frequency bands
- **Effect**: Each band covers wider frequency range → bigger LED reactions
- **Options**: Cycles through [6, 8, 12, 16, 24, 32, 48]
- **Best for**: Parties, bass-heavy music (EDM, dubstep)

**Example:**
```
Current: 24 bins (detailed)
Press button →
New: 16 bins (more dramatic)
Press again →
New: 12 bins (very dramatic)
```

### Button 2: Increase FFT Bins (GPIO 24)

**Press to make effects MORE DETAILED**

- **What it does**: Increases the number of frequency bands
- **Effect**: Narrower frequency ranges → more precise visualization
- **Options**: Cycles through [6, 8, 12, 16, 24, 32, 48]
- **Best for**: Studio monitoring, acoustic music

### Button 3: Cycle Visualization Mode (GPIO 25)

**Press to change the visual effect**

- **Modes**: Scroll → Energy → Spectrum → Scroll (loops)
- **Scroll**: Colors originate from center, scroll outward (cool trails)
- **Energy**: LEDs fill up based on bass/mid/treble energy (volume meter)
- **Spectrum**: Direct frequency-to-position mapping (equalizer style)

### Button 4: Decrease Sensitivity (GPIO 16)

**Press to make LEDs LESS REACTIVE**

- **What it does**: Increases the exponent (y = y^exponent)
- **Effect**: Requires louder sounds to trigger LEDs
- **Options**: [1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0]
- **Best for**: Noisy environments, loud concerts
- **Math**: Higher exponent = only peaks show up

### Button 5: Increase Sensitivity (GPIO 17)

**Press to make LEDs MORE REACTIVE**

- **What it does**: Decreases the exponent
- **Effect**: Responds to quieter sounds
- **Options**: [1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0]
- **Best for**: Quiet music, ambient sounds
- **Math**: Lower exponent = everything shows up

---

## Usage Examples

### Scenario 1: Party Mode (Maximum Drama!)

1. Start visualization: `sudo python3 visualization.py energy`
2. Press **Button 1** (Decrease Bins) several times → Get to 6 or 8 bins
3. Press **Button 5** (Increase Sensitivity) once or twice → More reactive
4. Press **Button 3** to try Energy mode if not already

**Result**: Big, bold flashes that react strongly to bass drops! 🎉

### Scenario 2: Chill Ambient Mode

1. Start visualization: `sudo python3 visualization.py scroll`
2. Press **Button 2** (Increase Bins) to 32 or 48 bins
3. Press **Button 4** (Decrease Sensitivity) to 2.5 or 3.0
4. Keep Scroll mode for smooth trails

**Result**: Smooth, detailed, relaxing visualization 🌊

### Scenario 3: Find Your Sweet Spot

Playing music you like:
1. Start with default settings
2. Press **Button 3** to try each visualization mode
3. Adjust bins (Buttons 1 & 2) until you like the effect
4. Fine-tune sensitivity (Buttons 4 & 5) based on volume level

---

## Customization

### Change GPIO Pin Numbers

Edit `gpio_controls.py`, line ~50:

```python
# GPIO Pin Configuration
BUTTON_PINS = {
    'decrease_bins': 23,      # Change to your preferred pin
    'increase_bins': 24,      # Change to your preferred pin
    'cycle_visualization': 25,
    'decrease_sensitivity': 16,
    'increase_sensitivity': 17,
}
```

### Add More FFT Bin Options

Edit `gpio_controls.py`, line ~59:

```python
N_FFT_BINS_OPTIONS = [6, 8, 12, 16, 24, 32, 48, 64]  # Add 64
```

### Add More Sensitivity Options

Edit `gpio_controls.py`, line ~60:

```python
SENSITIVITY_OPTIONS = [1.0, 1.2, 1.5, 1.8, 2.0, 2.2, 2.5, 3.0]  # Add 2.2
```

### Change Debounce Time

If buttons are too sensitive or not responsive enough:

Edit `gpio_controls.py`, line ~67:

```python
DEBOUNCE_TIME = 0.3  # Increase (slower) or decrease (faster)
```

---

## Troubleshooting

### Problem: "RPi.GPIO not available"

**Solution**: Install the GPIO library:
```bash
sudo apt-get install python3-rpi.gpio
```

### Problem: Buttons don't respond

**Checklist:**
1. ✓ Are buttons wired correctly? (GPIO pin → Button → GND)
2. ✓ Are you using the correct GPIO pin numbers (BCM mode)?
3. ✓ Did you run with `sudo`? (Required for GPIO access)
4. ✓ Test individual button: `python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP); print(GPIO.input(23))"`

Should print `1` when not pressed, `0` when pressed.

### Problem: Buttons trigger multiple times per press

**Solution**: Increase debounce time in `gpio_controls.py`:
```python
DEBOUNCE_TIME = 0.5  # Was 0.3
```

### Problem: "Permission denied" error

**Solution**: Run with sudo:
```bash
sudo python3 visualization.py scroll
```

### Problem: Script crashes when pressing button

**Check**: Make sure you're running the script from the correct directory:
```bash
cd ~/Desktop/work/rpi/dancyPi-audio-reactive-led/python
sudo python3 visualization.py scroll
```

### Problem: Changes don't take effect

**For FFT bins**: The mel filterbank needs to be recreated (this happens automatically)

**For sensitivity**: Changes apply immediately to scroll mode

**For visualization mode**: Should switch immediately - press Button 3 to confirm

---

## Advanced: Add Your Own Button Functions

### Example: Add a "Brightness" Button

**Step 1**: Add GPIO pin to `gpio_controls.py`:

```python
BUTTON_PINS = {
    'decrease_bins': 23,
    'increase_bins': 24,
    'cycle_visualization': 25,
    'decrease_sensitivity': 16,
    'increase_sensitivity': 17,
    'toggle_brightness': 12,  # NEW
}
```

**Step 2**: Add button handler:

```python
def button_callback(button_name):
    # ...existing code...
    elif button_name == 'toggle_brightness':
        toggle_brightness()

def toggle_brightness():
    """Toggle between bright and dim modes"""
    if config.BRIGHTNESS == 255:
        config.BRIGHTNESS = 128
        print("\n💡 Brightness: DIM (50%)\n")
    else:
        config.BRIGHTNESS = 255
        print("\n💡 Brightness: BRIGHT (100%)\n")
```

---

## Safety Notes

⚠️ **Important**:
- Never connect buttons to 5V or 3.3V pins - only GPIO and GND
- Don't connect/disconnect buttons while script is running
- Always run `gpio_controls.cleanup()` or press Ctrl+C cleanly to release GPIO resources

✅ **Safe Shutdown**:
```bash
# In the terminal running visualization.py:
Ctrl + C  # Press once, wait for cleanup message
```

---

## Quick Reference Card

Print this and keep near your Pi!

```
┌─────────────────────────────────────────────┐
│   Raspberry Pi LED Visualizer Controls      │
├─────────────────────────────────────────────┤
│  [GPIO 23] Decrease FFT Bins (more drama)   │
│  [GPIO 24] Increase FFT Bins (more detail)  │
│  [GPIO 25] Cycle Viz Mode (scroll/energy/sp)│
│  [GPIO 16] Decrease Sensitivity (less react)│
│  [GPIO 17] Increase Sensitivity (more react)│
├─────────────────────────────────────────────┤
│  FFT Bin Options: 6→8→12→16→24→32→48       │
│  Sensitivity: 1.0→1.2→1.5→1.8→2.0→2.5→3.0  │
│  Viz Modes: Scroll → Energy → Spectrum      │
└─────────────────────────────────────────────┘
```

---

## Summary

✅ **What You Accomplished**:
- Added 5 physical buttons to control parameters in real-time
- No need to stop/restart the script to change settings
- Easy hardware setup (no external resistors needed)
- Debounced, reliable button handling

🎵 **Now you can**:
- Adjust FFT bins on the fly (6-48 bins)
- Change sensitivity for different music volumes
- Cycle through visualization modes
- Find the perfect settings for any music!

🚀 **Next Steps**:
- Experiment with different button combinations
- Add custom button functions (brightness, color schemes)
- Share your setup with the community!

---

**Happy visualizing! 🎉💡🎵**

*Made with ❤️ for Raspberry Pi LED projects*


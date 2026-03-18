# Quick Start: GPIO Button Controls for Raspberry Pi LED Visualizer

## 🎯 What This Does

Add 5 physical buttons to your Raspberry Pi 3B to control LED parameters **while the visualization is running**!

- ⬇️ **Button 1 (GPIO 23)**: Fewer frequency bins → More dramatic effects
- ⬆️ **Button 2 (GPIO 24)**: More frequency bins → More detailed effects  
- 🔄 **Button 3 (GPIO 25)**: Cycle through visualization modes (scroll/energy/spectrum)
- 🔉 **Button 4 (GPIO 16)**: Less sensitive → Needs louder sounds
- 🔊 **Button 5 (GPIO 17)**: More sensitive → Responds to quiet sounds

---

## 🔧 Hardware Setup (5 Minutes)

### What You Need
- 5 momentary push buttons
- Jumper wires
- Breadboard (optional)

### Wiring (Simple!)
Connect each button between GPIO pin and GND:

```
Button 1: GPIO 23 ─── [Button] ─── GND (any ground pin)
Button 2: GPIO 24 ─── [Button] ─── GND
Button 3: GPIO 25 ─── [Button] ─── GND
Button 4: GPIO 16 ─── [Button] ─── GND
Button 5: GPIO 17 ─── [Button] ─── GND
```

**No resistors needed!** (Internal pull-ups are used)

### Ground Pins You Can Use
- Pin 6, 9, 14, 20, 25, 30, 34, or 39

---

## 💻 Software Setup (2 Minutes)

### Step 1: Install GPIO Library (if needed)

```bash
sudo apt-get update
sudo apt-get install python3-rpi.gpio
```

### Step 2: Test Your Button Wiring

```bash
cd ~/Desktop/work/rpi/dancyPi-audio-reactive-led/python
python3 test_buttons.py
```

Press each button - you should see confirmation messages.

### Step 3: View Pinout Reference (optional)

```bash
python3 test_buttons.py pinout
```

---

## 🚀 Running the Visualizer

### Start with Button Controls

```bash
cd ~/Desktop/work/rpi/dancyPi-audio-reactive-led/python
sudo python3 visualization.py scroll
```

You should see:
```
====================================
GPIO Button Controls Initialized!
====================================
Button Mappings:
  GPIO 23: Decrease frequency bins (more dramatic)
  GPIO 24: Increase frequency bins (more detail)
  GPIO 25: Cycle visualization mode
  GPIO 16: Decrease sensitivity
  GPIO 17: Increase sensitivity
====================================
Initial settings:
  N_FFT_BINS: 24
  Sensitivity: 2.0 (exponent)
====================================
```

### Try Different Modes

```bash
# Scroll mode (default - colors scroll outward)
sudo python3 visualization.py scroll

# Energy mode (fills up like a volume meter)
sudo python3 visualization.py energy

# Spectrum mode (equalizer style)
sudo python3 visualization.py spectrum
```

---

## 🎮 How to Use Buttons

### Press & Test

While visualization is running, press any button:

**Button 1 (GPIO 23)** - Make effects MORE DRAMATIC:
```
🎵 FFT Bins decreased to: 16 (more dramatic!)
   Each frequency bin covers wider range
   → Bigger, bolder LED reactions
```

**Button 2 (GPIO 24)** - Make effects MORE DETAILED:
```
🎵 FFT Bins increased to: 32 (more detail!)
   Each frequency bin covers narrower range
   → More precise frequency resolution
```

**Button 3 (GPIO 25)** - Change Visualization:
```
✨ Visualization mode: ENERGY
   → LEDs fill up based on frequency energy
```

**Button 4 (GPIO 16)** - Less Sensitive:
```
🔉 Sensitivity decreased: y = y**2.5
   → Less reactive, requires louder sounds
   → Better for noisy environments
```

**Button 5 (GPIO 17)** - More Sensitive:
```
🔊 Sensitivity increased: y = y**1.5
   → More reactive, responds to quieter sounds
   → Better for quiet music
```

---

## 🎉 Usage Scenarios

### Party Mode (Maximum Impact!)
1. Start: `sudo python3 visualization.py energy`
2. Press **Button 1** 3-4 times → Get to 6 or 8 bins
3. Press **Button 5** once → Increase sensitivity
4. 🎉 Enjoy massive bass reactions!

### Chill Mode (Smooth & Relaxing)
1. Start: `sudo python3 visualization.py scroll`
2. Press **Button 2** 2-3 times → Get to 32 or 48 bins
3. Press **Button 4** once → Decrease sensitivity
4. 🌊 Enjoy smooth, flowing colors

### Find Your Perfect Settings
1. Start with any mode
2. Press **Button 3** to try different visualizations
3. Adjust **Buttons 1 & 2** for dramatic vs. detailed
4. Fine-tune **Buttons 4 & 5** based on music volume

---

## 🛠️ Troubleshooting

### Buttons Don't Work

**Test wiring:**
```bash
python3 test_buttons.py
```

**Common issues:**
- ❌ Forgot to run with `sudo`
- ❌ Wrong GPIO pin numbers (must use BCM mode)
- ❌ Button wired to 3.3V instead of GND
- ❌ No ground connection

### "RPi.GPIO not available"

```bash
sudo apt-get install python3-rpi.gpio
```

### Buttons Trigger Multiple Times

Edit `gpio_controls.py` line 67:
```python
DEBOUNCE_TIME = 0.5  # Increase from 0.3
```

### Script Crashes

Make sure you're in the correct directory:
```bash
cd ~/Desktop/work/rpi/dancyPi-audio-reactive-led/python
sudo python3 visualization.py scroll
```

---

## 📝 Default Settings

| Parameter | Default | Options |
|-----------|---------|---------|
| N_FFT_BINS | 24 | 6, 8, 12, 16, 24, 32, 48 |
| Sensitivity | 2.0 | 1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0 |
| Visualization | scroll | scroll, energy, spectrum |

---

## 🎓 Learn More

- **Full GPIO Guide**: See `GPIO_BUTTON_GUIDE.md` for detailed explanations
- **DSP Guide**: See `DSP_TEACHING_GUIDE.md` to understand how the code works
- **Customize**: Edit `gpio_controls.py` to add your own button functions!

---

## 🔄 Clean Shutdown

Always exit cleanly to release GPIO resources:

```bash
Ctrl + C  # Press once in the terminal
```

You should see: `GPIO cleaned up successfully`

---

## ✅ Summary

**Files Created:**
- ✅ `gpio_controls.py` - Main button control module
- ✅ `test_buttons.py` - Wiring test utility  
- ✅ `GPIO_BUTTON_GUIDE.md` - Comprehensive guide
- ✅ Updated `visualization.py` - Integrated GPIO controls

**What You Can Do:**
- ✅ Adjust FFT bins (6-48) in real-time
- ✅ Change sensitivity on the fly
- ✅ Cycle through visualization modes
- ✅ No need to restart the script!

**Next Steps:**
- Wire up your buttons
- Test with `test_buttons.py`
- Run `sudo python3 visualization.py scroll`
- Press buttons and have fun! 🎉

---

**Enjoy your new interactive LED visualizer! 🎵💡✨**


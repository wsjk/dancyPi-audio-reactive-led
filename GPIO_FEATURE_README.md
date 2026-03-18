# 🎮 GPIO Button Controls - NEW FEATURE!

## Control Parameters in Real-Time with Physical Buttons

Now you can adjust LED visualization parameters **while the script is running** using physical buttons connected to your Raspberry Pi's GPIO pins!

### 🎯 What You Can Control

- **FFT Bins** (6-48): Adjust frequency resolution for dramatic or detailed effects
- **Sensitivity** (1.0-3.0): Change reactivity based on music volume
- **Visualization Mode**: Cycle between Scroll, Energy, and Spectrum modes

### 🚀 Quick Setup

**1. Wire 5 buttons to your Raspberry Pi:**

```
GPIO 23 → Button → GND  (Decrease FFT bins)
GPIO 24 → Button → GND  (Increase FFT bins)
GPIO 25 → Button → GND  (Cycle visualization mode)
GPIO 16 → Button → GND  (Decrease sensitivity)
GPIO 17 → Button → GND  (Increase sensitivity)
```

**No external resistors needed!** Internal pull-ups are enabled.

**2. Install GPIO library (if not already installed):**

```bash
sudo apt-get install python3-rpi.gpio
```

**3. Test your button connections:**

```bash
cd python
python3 test_buttons.py
```

Press each button to verify wiring. You should see confirmation messages.

**4. Run the visualizer with button support:**

```bash
sudo python3 visualization.py scroll
```

Buttons now work automatically! Press them while the visualization is running.

### 📚 Detailed Guides

- **[QUICK_START_GPIO.md](QUICK_START_GPIO.md)** - Fast setup guide (5 minutes)
- **[GPIO_BUTTON_GUIDE.md](GPIO_BUTTON_GUIDE.md)** - Complete wiring & usage guide
- **[DSP_TEACHING_GUIDE.md](DSP_TEACHING_GUIDE.md)** - Learn how the audio processing works

### 🎮 Button Functions

| Button | GPIO | Function | Effect |
|--------|------|----------|--------|
| 1 | 23 | Decrease FFT Bins | More dramatic (6→8→12→16→24→32→48) |
| 2 | 24 | Increase FFT Bins | More detailed (same range) |
| 3 | 25 | Cycle Visualization | Scroll → Energy → Spectrum |
| 4 | 16 | Decrease Sensitivity | Less reactive (louder sounds needed) |
| 5 | 17 | Increase Sensitivity | More reactive (quiet sounds trigger) |

### 💡 Usage Examples

**Party Mode (Maximum Drama):**
```bash
sudo python3 visualization.py energy
# Then press Button 1 several times → fewer bins = bigger reactions!
# Press Button 5 once → more sensitive to bass
```

**Chill Mode (Smooth Detail):**
```bash
sudo python3 visualization.py scroll
# Then press Button 2 several times → more bins = smoother
# Press Button 4 once → less reactive = calm
```

### 🔧 Customization

Want to customize button pins or add new functions? Edit `python/gpio_controls.py`:

```python
BUTTON_PINS = {
    'decrease_bins': 23,      # Change to your preferred GPIO pin
    'increase_bins': 24,
    # ... add more buttons!
}
```

See [GPIO_BUTTON_GUIDE.md](GPIO_BUTTON_GUIDE.md) for advanced customization examples.

---


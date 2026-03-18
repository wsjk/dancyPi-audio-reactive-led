"""GPIO Button Controls for Raspberry Pi Audio Reactive LED Strip

This module provides GPIO button functionality to change parameters while
the visualization is running. Buttons are connected to GPIO pins with
internal pull-up resistors (buttons connect GPIO pin to ground when pressed).

Hardware Setup:
---------------
Connect buttons between GPIO pins and GND (ground). The internal pull-up
resistor is enabled, so when not pressed, the pin reads HIGH, and when
pressed it reads LOW.

Example wiring:
  Button 1: GPIO 23 ---- [Button] ---- GND
  Button 2: GPIO 24 ---- [Button] ---- GND
  Button 3: GPIO 25 ---- [Button] ---- GND
  Button 4: GPIO 16 ---- [Button] ---- GND
  Button 5: GPIO 17 ---- [Button] ---- GND

No external resistors needed!

Usage:
------
Import and initialize in your visualization script:
    import gpio_controls
    gpio_controls.init_gpio_controls()

The buttons will work automatically in the background using threading.
"""

from __future__ import print_function
from __future__ import division
import time
import config
import dsp

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    print("WARNING: RPi.GPIO not available. GPIO controls disabled.")
    GPIO_AVAILABLE = False

# GPIO Pin Configuration
# Change these pin numbers to match your button wiring
BUTTON_PINS = {
    'decrease_bins': 23,      # Decrease N_FFT_BINS
    'increase_bins': 24,      # Increase N_FFT_BINS
    'cycle_visualization': 25, # Cycle through visualization modes
    'decrease_sensitivity': 16, # Decrease sensitivity (higher exponent)
    'increase_sensitivity': 17, # Increase sensitivity (lower exponent)
}

# Parameter ranges and step sizes
N_FFT_BINS_OPTIONS = [6, 8, 12, 16, 24, 32, 48]
SENSITIVITY_OPTIONS = [1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0]
VISUALIZATION_MODES = ['scroll', 'energy', 'spectrum']

# Current state tracking
current_bins_index = 4  # Default to 24 bins
current_sensitivity_index = 4  # Default to 2.0
current_viz_index = 0  # Default to scroll

# Debounce parameters
DEBOUNCE_TIME = 0.3  # seconds
last_press_time = {}

# Store reference to visualization module (set by init function)
visualization_module = None


def init_gpio_controls(viz_module=None):
    """Initialize GPIO controls for parameter adjustment

    Parameters
    ----------
    viz_module : module, optional
        Reference to the visualization module to enable mode switching
    """
    global visualization_module
    visualization_module = viz_module

    if not GPIO_AVAILABLE:
        print("GPIO controls not available - continuing without button support")
        return False

    try:
        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Initialize all button pins with pull-up resistors
        for button_name, pin in BUTTON_PINS.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            last_press_time[button_name] = 0

            # Add event detection for falling edge (button press)
            GPIO.add_event_detect(
                pin,
                GPIO.FALLING,
                callback=lambda channel, name=button_name: button_callback(name),
                bouncetime=300  # Built-in hardware debounce (ms)
            )

        print("\n" + "="*60)
        print("GPIO Button Controls Initialized!")
        print("="*60)
        print("Button Mappings:")
        print(f"  GPIO {BUTTON_PINS['decrease_bins']}: Decrease frequency bins (more dramatic)")
        print(f"  GPIO {BUTTON_PINS['increase_bins']}: Increase frequency bins (more detail)")
        print(f"  GPIO {BUTTON_PINS['cycle_visualization']}: Cycle visualization mode")
        print(f"  GPIO {BUTTON_PINS['decrease_sensitivity']}: Decrease sensitivity")
        print(f"  GPIO {BUTTON_PINS['increase_sensitivity']}: Increase sensitivity")
        print("="*60)
        print(f"Initial settings:")
        print(f"  N_FFT_BINS: {config.N_FFT_BINS}")
        print(f"  Sensitivity: 2.0 (exponent)")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"Error initializing GPIO: {e}")
        return False


def button_callback(button_name):
    """Handle button press events with debouncing

    Parameters
    ----------
    button_name : str
        Name of the button that was pressed
    """
    global current_bins_index, current_sensitivity_index, current_viz_index

    # Software debounce check
    current_time = time.time()
    if current_time - last_press_time[button_name] < DEBOUNCE_TIME:
        return
    last_press_time[button_name] = current_time

    # Handle button actions
    if button_name == 'decrease_bins':
        decrease_fft_bins()
    elif button_name == 'increase_bins':
        increase_fft_bins()
    elif button_name == 'cycle_visualization':
        cycle_visualization_mode()
    elif button_name == 'decrease_sensitivity':
        decrease_sensitivity()
    elif button_name == 'increase_sensitivity':
        increase_sensitivity()


def decrease_fft_bins():
    """Decrease the number of FFT bins (more dramatic effect)"""
    global current_bins_index

    if current_bins_index > 0:
        current_bins_index -= 1
        new_bins = N_FFT_BINS_OPTIONS[current_bins_index]
        config.N_FFT_BINS = new_bins

        # Recreate mel filterbank with new bins
        dsp.create_mel_bank()

        # Recreate gain filter with new size
        import visualization
        visualization.gain = dsp.ExpFilter(
            np.tile(0.01, config.N_FFT_BINS),
            alpha_decay=0.001,
            alpha_rise=0.99
        )

        print(f"\n🎵 FFT Bins decreased to: {new_bins} (more dramatic!)")
        print(f"   Each frequency bin covers wider range")
        print(f"   → Bigger, bolder LED reactions\n")
    else:
        print(f"\n⚠️  Already at minimum bins: {N_FFT_BINS_OPTIONS[0]}\n")


def increase_fft_bins():
    """Increase the number of FFT bins (more detailed effect)"""
    global current_bins_index

    if current_bins_index < len(N_FFT_BINS_OPTIONS) - 1:
        current_bins_index += 1
        new_bins = N_FFT_BINS_OPTIONS[current_bins_index]
        config.N_FFT_BINS = new_bins

        # Recreate mel filterbank with new bins
        dsp.create_mel_bank()

        # Recreate gain filter with new size
        import visualization
        visualization.gain = dsp.ExpFilter(
            np.tile(0.01, config.N_FFT_BINS),
            alpha_decay=0.001,
            alpha_rise=0.99
        )

        print(f"\n🎵 FFT Bins increased to: {new_bins} (more detail!)")
        print(f"   Each frequency bin covers narrower range")
        print(f"   → More precise frequency resolution\n")
    else:
        print(f"\n⚠️  Already at maximum bins: {N_FFT_BINS_OPTIONS[-1]}\n")


def cycle_visualization_mode():
    """Cycle through available visualization modes"""
    global current_viz_index

    if visualization_module is None:
        print("\n⚠️  Visualization module not available for mode switching\n")
        return

    current_viz_index = (current_viz_index + 1) % len(VISUALIZATION_MODES)
    mode_name = VISUALIZATION_MODES[current_viz_index]

    # Update the visualization effect
    if mode_name == 'scroll':
        visualization_module.visualization_effect = visualization_module.visualize_scroll
    elif mode_name == 'energy':
        visualization_module.visualization_effect = visualization_module.visualize_energy
    elif mode_name == 'spectrum':
        visualization_module.visualization_effect = visualization_module.visualize_spectrum

    print(f"\n✨ Visualization mode: {mode_name.upper()}")
    if mode_name == 'scroll':
        print("   → Colors originate from center and scroll outward")
    elif mode_name == 'energy':
        print("   → LEDs fill up based on frequency energy")
    elif mode_name == 'spectrum':
        print("   → Direct frequency-to-LED mapping")
    print()


def decrease_sensitivity():
    """Decrease sensitivity (increase exponent - less reactive)"""
    global current_sensitivity_index

    if current_sensitivity_index < len(SENSITIVITY_OPTIONS) - 1:
        current_sensitivity_index += 1
        new_sensitivity = SENSITIVITY_OPTIONS[current_sensitivity_index]

        print(f"\n🔉 Sensitivity decreased: y = y**{new_sensitivity}")
        print(f"   → Less reactive, requires louder sounds")
        print(f"   → Better for noisy environments\n")
    else:
        print(f"\n⚠️  Already at minimum sensitivity: {SENSITIVITY_OPTIONS[-1]}\n")


def increase_sensitivity():
    """Increase sensitivity (decrease exponent - more reactive)"""
    global current_sensitivity_index

    if current_sensitivity_index > 0:
        current_sensitivity_index -= 1
        new_sensitivity = SENSITIVITY_OPTIONS[current_sensitivity_index]

        print(f"\n🔊 Sensitivity increased: y = y**{new_sensitivity}")
        print(f"   → More reactive, responds to quieter sounds")
        print(f"   → Better for quiet music\n")
    else:
        print(f"\n⚠️  Already at maximum sensitivity: {SENSITIVITY_OPTIONS[0]}\n")


def get_current_sensitivity():
    """Get the current sensitivity exponent value

    Returns
    -------
    float
        Current sensitivity exponent value
    """
    return SENSITIVITY_OPTIONS[current_sensitivity_index]


def cleanup():
    """Clean up GPIO resources on shutdown"""
    if GPIO_AVAILABLE:
        try:
            GPIO.cleanup()
            print("\nGPIO cleaned up successfully")
        except Exception as e:
            print(f"\nError cleaning up GPIO: {e}")


# Import numpy here (after config is available)
import numpy as np


if __name__ == '__main__':
    # Test GPIO setup
    print("Testing GPIO Controls...")
    print("This will initialize GPIO pins and wait for button presses.")
    print("Press Ctrl+C to exit.\n")

    init_gpio_controls()

    try:
        print("Waiting for button presses...")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        cleanup()


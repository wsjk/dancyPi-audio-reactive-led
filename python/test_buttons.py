#!/usr/bin/env python3
"""
Button Wiring Test Script for Raspberry Pi 3B

This script helps you verify your button connections are correct.
It will show the status of each GPIO pin in real-time.

Usage:
    python3 test_buttons.py

Press Ctrl+C to exit.
"""

import time
import sys

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("ERROR: RPi.GPIO not installed!")
    print("Install with: sudo apt-get install python3-rpi.gpio")
    sys.exit(1)

# Button pin configuration (must match gpio_controls.py)
BUTTONS = {
    23: "Decrease FFT Bins (More Dramatic)",
    24: "Increase FFT Bins (More Detail)",
    25: "Cycle Visualization Mode",
    16: "Decrease Sensitivity",
    17: "Increase Sensitivity",
}

def test_buttons():
    """Test all button connections"""

    print("\n" + "="*70)
    print("Button Connection Test")
    print("="*70)
    print("\nInitializing GPIO pins...")

    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Initialize all pins with pull-up resistors
    for pin in BUTTONS.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("✓ GPIO initialized successfully!\n")
    print("="*70)
    print("Button Status (press each button to test)")
    print("="*70)
    print("\nPin states:")
    print("  HIGH (1) = Not pressed (pulled up by internal resistor)")
    print("  LOW  (0) = Pressed (connected to ground)")
    print("\n" + "-"*70 + "\n")

    previous_states = {pin: 1 for pin in BUTTONS.keys()}

    try:
        while True:
            # Check each button
            for pin, description in BUTTONS.items():
                current_state = GPIO.input(pin)

                # Print when state changes
                if current_state != previous_states[pin]:
                    if current_state == 0:  # Button pressed
                        print(f"✓ GPIO {pin:2d}: PRESSED  - {description}")
                    else:  # Button released
                        print(f"  GPIO {pin:2d}: Released - {description}")
                    previous_states[pin] = current_state

            time.sleep(0.05)  # Check 20 times per second

    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("Test Summary")
        print("="*70)

        # Final status check
        all_working = True
        for pin, description in BUTTONS.items():
            state = GPIO.input(pin)
            status = "✓ OK (reads HIGH when not pressed)" if state == 1 else "✗ ISSUE (stuck LOW)"
            print(f"GPIO {pin:2d}: {status}")
            if state == 0:
                all_working = False

        print("\n" + "="*70)
        if all_working:
            print("✓ All buttons working correctly!")
            print("\nYou can now run: sudo python3 visualization.py scroll")
        else:
            print("✗ Some pins are stuck LOW - check your wiring!")
            print("\nTroubleshooting:")
            print("  1. Make sure buttons connect GPIO → Button → GND")
            print("  2. Check that no wires are crossed")
            print("  3. Verify GND connection is solid")
        print("="*70 + "\n")

        GPIO.cleanup()


def show_pinout():
    """Display Raspberry Pi pinout reference"""
    print("\n" + "="*70)
    print("Raspberry Pi 3B GPIO Pinout (looking at board from above)")
    print("="*70)
    print("""
    3.3V [ 1] [ 2] 5V        ← Do not use for buttons
   GPIO2 [ 3] [ 4] 5V        ← Do not use for buttons  
   GPIO3 [ 5] [ 6] GND       ← Can use this GND
   GPIO4 [ 7] [ 8] GPIO14
     GND [ 9] [10] GPIO15
  GPIO17 [11] [12] GPIO18    ← LED strip (don't use) / Button 5
  GPIO27 [13] [14] GND       ← Can use this GND
  GPIO22 [15] [16] GPIO23    ← Button 1: Decrease FFT bins
    3.3V [17] [18] GPIO24    ← Button 2: Increase FFT bins
  GPIO10 [19] [20] GND       ← Can use this GND
   GPIO9 [21] [22] GPIO25    ← Button 3: Cycle visualization
  GPIO11 [23] [24] GPIO8
     GND [25] [26] GPIO7
   GPIO0 [27] [28] GPIO1
   GPIO5 [29] [30] GND       ← Can use this GND
   GPIO6 [31] [32] GPIO12
  GPIO13 [33] [34] GND       ← Can use this GND
  GPIO19 [35] [36] GPIO16    ← Button 4: Decrease sensitivity
  GPIO26 [37] [38] GPIO20
     GND [39] [40] GPIO21
    
Wiring Instructions:
  • Each button connects: GPIO pin → Button → Any GND pin
  • No resistors needed (internal pull-ups enabled)
  • All buttons can share the same GND rail
    """)
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("Raspberry Pi Button Test Utility")
    print("="*70)

    if len(sys.argv) > 1 and sys.argv[1] == "pinout":
        show_pinout()
    else:
        print("\nOptions:")
        print("  python3 test_buttons.py          - Test button connections")
        print("  python3 test_buttons.py pinout   - Show GPIO pinout reference")
        print("\nStarting button test in 2 seconds...")
        print("Press Ctrl+C to exit at any time\n")
        time.sleep(2)

        test_buttons()


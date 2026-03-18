# Raspberry Pi 3B Button Wiring Diagram

## Simple Visual Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                    Raspberry Pi 3B                               │
│                                                                  │
│  Physical Pin Layout (40 pins):                                 │
│                                                                  │
│       3.3V [ 1] [ 2] 5V                                         │
│      GPIO2 [ 3] [ 4] 5V                                         │
│      GPIO3 [ 5] [ 6] GND ───────────────────┐                  │
│      GPIO4 [ 7] [ 8] GPIO14                 │                  │
│        GND [ 9] [10] GPIO15                 │                  │
│  ┌─ GPIO17 [11] [12] GPIO18 (LED Strip)     │  Ground Rail     │
│  │  GPIO27 [13] [14] GND ───────────────────┤                  │
│  │  GPIO22 [15] [16] GPIO23 ─┐              │  All buttons     │
│  │     3.3V [17] [18] GPIO24 ─┤              │  connect here    │
│  │  GPIO10 [19] [20] GND ─────┤──────────────┤                  │
│  │   GPIO9 [21] [22] GPIO25 ──┤──────────────┘                  │
│  │  GPIO11 [23] [24] GPIO8    │                                 │
│  │      GND [25] [26] GPIO7   │                                 │
│  │   GPIO0 [27] [28] GPIO1    │                                 │
│  │   GPIO5 [29] [30] GND      │                                 │
│  │   GPIO6 [31] [32] GPIO12   │                                 │
│  │  GPIO13 [33] [34] GND      │                                 │
│  │  GPIO19 [35] [36] GPIO16 ──┘                                 │
│  │  GPIO26 [37] [38] GPIO20                                     │
│  │      GND [39] [40] GPIO21                                    │
│  │                                                               │
│  └──────────────────────────────────────────────────────────────┘
│                            │
│                            │
│                       ┌────▼─────────┐
│                       │   Button 5   │
│                       │  (Increase   │
│                       │ Sensitivity) │
│                       └──────────────┘

```

## Breadboard Layout

```
                    Raspberry Pi GPIO Pins
                            ┃
                ┌───────────┼───────────┐
                │           │           │
         GPIO 23│    GPIO 24│    GPIO 25│    GPIO 16│    GPIO 17│
                │           │           │           │           │
                ▼           ▼           ▼           ▼           ▼
              ┌───┐       ┌───┐       ┌───┐       ┌───┐       ┌───┐
              │   │       │   │       │   │       │   │       │   │
              │ ● │       │ ● │       │ ● │       │ ● │       │ ● │
              │   │       │   │       │   │       │   │       │   │
              │ ● │       │ ● │       │ ● │       │ ● │       │ ● │
              │   │       │   │       │   │       │   │       │   │
              └─┬─┘       └─┬─┘       └─┬─┘       └─┬─┘       └─┬─┘
                │           │           │           │           │
                └───────────┴───────────┴───────────┴───────────┘
                                        │
                                        │
                                    GND Pin (6, 9, 14, 20, 25, 30, 34, or 39)

         Button 1       Button 2     Button 3     Button 4     Button 5
     Decrease Bins  Increase Bins  Cycle Mode   Less Sense   More Sense
```

## Detailed Wiring Table

| Button # | Function | GPIO # | Physical Pin | To Button Terminal 1 | To Button Terminal 2 |
|----------|----------|--------|--------------|---------------------|---------------------|
| 1 | Decrease FFT Bins | 23 | 16 | Connect | - |
| 2 | Increase FFT Bins | 24 | 18 | Connect | - |
| 3 | Cycle Visualization | 25 | 22 | Connect | - |
| 4 | Decrease Sensitivity | 16 | 36 | Connect | - |
| 5 | Increase Sensitivity | 17 | 11 | Connect | - |
| - | Ground (all buttons) | GND | 6/9/14/20/25/30/34/39 | - | Connect |

## Button Internal Wiring

```
Each Momentary Push Button:
(Normally Open - NO)

    Terminal 1 ─────┐  ┌───── Terminal 3
                    │  │
                 ┌──┴──┴──┐
                 │        │
    Not Pressed: │   ·    │  (Open circuit)
                 │        │
                 └────────┘

                 ┌────────┐
                 │        │
    Pressed:     │   —    │  (Closed circuit)
                 │        │
                 └──┬──┬──┘
                    │  │
    Terminal 2 ─────┘  └───── Terminal 4

Note: Most buttons have 4 terminals but internally:
  - Terminals 1 & 3 are connected
  - Terminals 2 & 4 are connected
  
Use: Terminal 1 (or 3) to GPIO pin
     Terminal 2 (or 4) to GND
```

## Color-Coded Wiring (Suggested)

If using colored wires for easy identification:

```
🔴 Red wires:    DON'T USE (5V - dangerous for GPIO!)
🟠 Orange:       GPIO 23 → Button 1
🟡 Yellow:       GPIO 24 → Button 2
🟢 Green:        GPIO 25 → Button 3
🔵 Blue:         GPIO 16 → Button 4
🟣 Purple:       GPIO 17 → Button 5
⚫ Black wires:  All buttons to GND (ground rail)
```

## Physical Layout Example

```
                     ┌──────────────────┐
                     │  Raspberry Pi 3B │
                     └──────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    │    (GPIO Pins)    │
                    │                   │
                    │                   │
                    ▼                   ▼
    ┌────────────────────────────────────────┐
    │          Breadboard                    │
    │  ═══════════════════════════════════  │← Power rails
    │                                        │
    │   [Btn1] [Btn2] [Btn3] [Btn4] [Btn5] │
    │     ○      ○      ○      ○      ○    │
    │     │      │      │      │      │    │
    │  ─────────────────────────────────── │← Ground rail
    │                                        │
    │  ═══════════════════════════════════  │
    └────────────────────────────────────────┘
```

## Step-by-Step Wiring Instructions

### Step 1: Identify Your Buttons
- Get 5 momentary push buttons (normally open)
- Test with multimeter: Should be OPEN when not pressed, CLOSED when pressed

### Step 2: Connect Buttons to Breadboard (Optional)
If using a breadboard:
1. Insert all 5 buttons in a row
2. Leave space between each button
3. Orient buttons so terminals align with breadboard rows

### Step 3: Connect GPIO Pins to Buttons
Use female-to-male jumper wires:

```
Raspberry Pi → Button
─────────────────────────
Pin 16 (GPIO 23) → Button 1, Terminal 1
Pin 18 (GPIO 24) → Button 2, Terminal 1
Pin 22 (GPIO 25) → Button 3, Terminal 1
Pin 36 (GPIO 16) → Button 4, Terminal 1
Pin 11 (GPIO 17) → Button 5, Terminal 1
```

### Step 4: Connect Ground to All Buttons
Use male-to-male jumpers on breadboard, or direct wires:

```
Raspberry Pi GND → All buttons (Terminal 2)

You can use ANY GND pin:
- Pin 6 (near top, convenient)
- Pin 9
- Pin 14
- Pin 20
- Pin 25
- Pin 30
- Pin 34
- Pin 39

Connect ONE GND pin to a breadboard ground rail,
then connect all button Terminal 2's to that rail.
```

### Step 5: Verify Wiring
**Without power:**
1. Check each GPIO wire goes to correct pin
2. Verify all buttons connected to same GND
3. Make sure no wires touch each other
4. Double-check pin numbers (easy to miscount!)

**With power (Pi on):**
```bash
python3 test_buttons.py
```
Press each button, should see confirmation messages.

## Troubleshooting Wiring Issues

### Problem: Button doesn't register

**Check:**
- [ ] Wire connected to correct GPIO pin?
- [ ] Wire connected to correct physical pin number?
- [ ] Button terminal connections solid?
- [ ] Ground connection present?
- [ ] Button is normally-open (NO) type?

**Test with multimeter:**
1. Set to continuity mode (beep)
2. Touch probes to button terminals
3. No beep when not pressed = good
4. Beep when pressed = good
5. Always beeps = button stuck or wrong type

### Problem: All buttons trigger at once

**Likely causes:**
- Wires crossed or touching
- Short circuit somewhere
- Using normally-closed (NC) buttons instead of NO

### Problem: Inconsistent triggering

**Likely causes:**
- Loose connection
- Bad jumper wire
- Dirty button contacts
- Need better debounce settings in code

## Safe Practices

✅ **DO:**
- Connect buttons between GPIO and GND
- Use female-to-male jumpers for Pi to breadboard
- Double-check pin numbers before powering on
- Test with multimeter when unsure
- Keep wires organized and labeled

❌ **DON'T:**
- Never connect GPIO directly to 5V or 3.3V power
- Don't swap wires while Pi is running
- Don't use excessive force on GPIO pins
- Don't short circuit GPIO pins together
- Don't power on if wiring looks wrong

## Visual Pin Reference Card

```
Print this and keep near your Pi!

┌──────────────────────────────────────┐
│    Raspberry Pi 3B GPIO Reference    │
├──────────────────────────────────────┤
│                                      │
│  Button 1: Pin 16 = GPIO 23         │
│  Button 2: Pin 18 = GPIO 24         │
│  Button 3: Pin 22 = GPIO 25         │
│  Button 4: Pin 36 = GPIO 16         │
│  Button 5: Pin 11 = GPIO 17         │
│                                      │
│  Ground pins: 6, 9, 14, 20, 25,     │
│               30, 34, 39             │
│                                      │
│  ⚠️  LED strip: Pin 12 (GPIO 18)     │
│     Don't use this for buttons!     │
│                                      │
└──────────────────────────────────────┘
```

## Complete Component Checklist

- [ ] Raspberry Pi 3B (with Raspberry Pi OS)
- [ ] 5 × Momentary push buttons (normally open)
- [ ] 6 × Female-to-male jumper wires (Pi to breadboard)
- [ ] 5 × Male-to-male jumper wires (breadboard ground rail)
- [ ] 1 × Breadboard (optional but recommended)
- [ ] Multimeter (optional, for testing)

## Ready to Test!

Once wired, run:

```bash
cd ~/Desktop/work/rpi/dancyPi-audio-reactive-led/python
python3 test_buttons.py
```

Then start the visualizer:

```bash
sudo python3 visualization.py scroll
```

**Press buttons and watch the magic! 🎉💡🎵**


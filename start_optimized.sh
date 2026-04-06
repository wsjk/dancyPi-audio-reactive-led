#!/bin/bash
# Optimized startup script for dancyPi-audio-reactive-led on Raspberry Pi 3B
# Run with: sudo ./start_optimized.sh [spectrum|energy|scroll]

# Default to spectrum if no argument provided
EFFECT=${1:-spectrum}

# Valid effects
if [[ ! "$EFFECT" =~ ^(spectrum|energy|scroll)$ ]]; then
    echo "Invalid effect: $EFFECT"
    echo "Usage: sudo ./start_optimized.sh [spectrum|energy|scroll]"
    exit 1
fi

echo "Starting audio-reactive LED with '$EFFECT' effect..."
echo "Optimized for Raspberry Pi 3B"
echo ""

# Change to python directory
cd "$(dirname "$0")/python"

# Set CPU governor to performance for consistent frame rates
echo "Setting CPU governor to performance mode..."
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null

# Increase process priority for better real-time performance
echo "Starting visualization with high priority..."
nice -n -10 python3 visualization.py "$EFFECT"

# Restore CPU governor on exit
echo ""
echo "Restoring CPU governor to ondemand mode..."
echo ondemand | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null


#!/usr/bin/env python3
"""
Performance profile switcher for dancyPi-audio-reactive-led
Allows easy switching between performance presets optimized for different scenarios
"""

import os
import sys

PROFILES = {
    'max_performance': {
        'name': 'Maximum Performance',
        'description': 'Lowest resource usage, minimal features',
        'settings': {
            'USE_GUI': False,
            'DISPLAY_FPS': False,
            'FPS': 30,
            'N_FFT_BINS': 16,
            'MIC_RATE': 44100,
        }
    },
    'balanced': {
        'name': 'Balanced (Default)',
        'description': 'Good balance of quality and performance for RPi3B',
        'settings': {
            'USE_GUI': False,
            'DISPLAY_FPS': False,
            'FPS': 40,
            'N_FFT_BINS': 24,
            'MIC_RATE': 48000,
        }
    },
    'quality': {
        'name': 'Maximum Quality',
        'description': 'Best visual quality, higher resource usage',
        'settings': {
            'USE_GUI': False,
            'DISPLAY_FPS': False,
            'FPS': 50,
            'N_FFT_BINS': 32,
            'MIC_RATE': 48000,
        }
    },
    'debug': {
        'name': 'Debug Mode',
        'description': 'GUI enabled for tuning and debugging',
        'settings': {
            'USE_GUI': True,
            'DISPLAY_FPS': True,
            'FPS': 30,
            'N_FFT_BINS': 24,
            'MIC_RATE': 48000,
        }
    },
}


def read_config(config_path):
    """Read the current config.py file"""
    with open(config_path, 'r') as f:
        return f.read()


def update_setting(config_content, setting, value):
    """Update a specific setting in the config content"""
    import re

    # Handle boolean values
    if isinstance(value, bool):
        value_str = str(value)
    else:
        value_str = str(value)

    # Find and replace the setting
    pattern = rf'^{setting}\s*=\s*.*$'
    replacement = f'{setting} = {value_str}'

    config_content = re.sub(pattern, replacement, config_content, flags=re.MULTILINE)
    return config_content


def apply_profile(profile_name):
    """Apply a performance profile"""
    if profile_name not in PROFILES:
        print(f"Error: Profile '{profile_name}' not found")
        print(f"Available profiles: {', '.join(PROFILES.keys())}")
        return False

    profile = PROFILES[profile_name]
    config_path = os.path.join(os.path.dirname(__file__), 'python', 'config.py')

    if not os.path.exists(config_path):
        print(f"Error: config.py not found at {config_path}")
        return False

    # Backup current config
    backup_path = config_path + '.backup'
    with open(config_path, 'r') as f:
        original_content = f.read()
    with open(backup_path, 'w') as f:
        f.write(original_content)

    print(f"\n=== Applying Profile: {profile['name']} ===")
    print(f"Description: {profile['description']}\n")

    # Apply settings
    config_content = original_content
    for setting, value in profile['settings'].items():
        config_content = update_setting(config_content, setting, value)
        print(f"  {setting} = {value}")

    # Write updated config
    with open(config_path, 'w') as f:
        f.write(config_content)

    print(f"\n✓ Profile applied successfully!")
    print(f"  Backup saved to: {backup_path}")
    return True


def show_profiles():
    """Display all available profiles"""
    print("\n=== Available Performance Profiles ===\n")
    for key, profile in PROFILES.items():
        print(f"{key}:")
        print(f"  Name: {profile['name']}")
        print(f"  Description: {profile['description']}")
        print(f"  Settings:")
        for setting, value in profile['settings'].items():
            print(f"    - {setting}: {value}")
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 set_performance_profile.py <profile_name>")
        print("       python3 set_performance_profile.py list")
        print("\nExamples:")
        print("  python3 set_performance_profile.py balanced")
        print("  python3 set_performance_profile.py max_performance")
        print("  python3 set_performance_profile.py list")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'list':
        show_profiles()
    elif command in PROFILES:
        if apply_profile(command):
            print("\nYou can now run the visualization with:")
            print("  sudo ./start_optimized.sh spectrum")
    else:
        print(f"Error: Unknown profile or command '{command}'")
        print("\nUse 'list' to see available profiles:")
        print("  python3 set_performance_profile.py list")
        sys.exit(1)


if __name__ == '__main__':
    main()


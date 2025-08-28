#!/usr/bin/env python3
"""
Install Pillow (PIL) for image processing
"""

import subprocess
import sys

def install_pillow():
    """Install Pillow package for image processing"""
    try:
        print("📦 Installing Pillow for image processing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("✅ Pillow installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Pillow: {e}")
        return False

if __name__ == "__main__":
    install_pillow()
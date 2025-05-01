#!/bin/bash
echo "Installing required packages for Arducam IMX219 Autofocus..."
sudo apt update
sudo apt install -y python3-opencv i2c-tools v4l-utils
echo "Installation complete. You can now run: python3 Autofocus_2025.py -i 9"
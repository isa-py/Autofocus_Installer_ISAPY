AUTOFOCUS INSTALLER (ISAPY): IMX219 (Arducam B0181) + Jetson Orin Nano

FILES INCLUDED:
- Autofocus_2025.py      → Main autofocus script using OpenCV + GStreamer
- Focuser.py             → Motorized focus controller over I2C
- install_full.sh        → Installer for dependencies
- README.txt             → Setup instructions

SETUP STEPS:
1. Connect IMX219 to CAM1.
2. Run the installer script:
   chmod +x install_full.sh && ./install_full.sh
3. Launch autofocus:
   python3 Autofocus_2025.py -i 9

REQUIREMENTS:
- JetPack 6 or later
- Python 3
- OpenCV with GStreamer
- Access to I2C (i2c-tools)

Controls:
- ESC exits
- ENTER re-runs autofocus

#!/bin/bash
#
# Setup script for ELEC 392 PiCar-X Autonomous Taxi
# This script helps set up the environment on a Raspberry Pi
#

set -e

echo "======================================================"
echo "ELEC 392 PiCar-X Autonomous Taxi Setup"
echo "======================================================"
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "WARNING: This doesn't appear to be a Raspberry Pi."
    echo "Some hardware features may not work."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "Step 1: Updating system packages..."
sudo apt-get update
echo "✓ System packages updated"
echo ""

# Install system dependencies
echo "Step 2: Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-opencv \
    libatlas-base-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libharfbuzz0b \
    libwebp6 \
    libjasper1 \
    libilmbase23 \
    libopenexr23 \
    libgstreamer1.0-0 \
    libavcodec58 \
    libavformat58 \
    libswscale5
echo "✓ System dependencies installed"
echo ""

# Install Python dependencies
echo "Step 3: Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✓ Python dependencies installed"
echo ""

# Enable I2C and Camera
echo "Step 4: Configuring Raspberry Pi..."
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_camera 0
echo "✓ I2C and Camera enabled"
echo ""

# Download models
echo "Step 5: Downloading object detection models..."
python3 utils/download_models.py
echo "✓ Models downloaded"
echo ""

# Set up Coral USB Accelerator
echo "Step 6: Setting up Coral USB Accelerator..."
echo "Installing Edge TPU runtime..."
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y libedgetpu1-std
echo "✓ Coral USB Accelerator configured"
echo ""

echo "======================================================"
echo "Setup Complete!"
echo "======================================================"
echo ""
echo "Next steps:"
echo "1. Reboot your Raspberry Pi: sudo reboot"
echo "2. Connect your PiCar-X hardware"
echo "3. Plug in the Coral USB Accelerator"
echo "4. Run examples:"
echo "   - Basic control: python3 examples/basic_control.py"
echo "   - Lane following: python3 examples/lane_following_demo.py"
echo "   - Object detection: python3 examples/object_detection_demo.py"
echo "   - Full autonomous: python3 examples/autonomous_taxi_demo.py"
echo ""
echo "Happy coding!"
echo "======================================================"

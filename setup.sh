#!/usr/bin/env bash

sudo apt-get update
sudo apt-get upgrade
cd ~/

# Install pigpio
rm pigpio.zip
sudo rm -rf PIGPIO
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make -j4
sudo make install

# Append pigpiod to second to last line in rc.local to startup pigpio daemon on boot
sudo sed '$ipigpiod' /etc/rc.local

# Install pygame
sudo apt-get install pygame

sudo reboot
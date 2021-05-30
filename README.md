
**Requirements:**
```
sudo apt update
sudo apt upgrade
sudo apt install git
git clone https://github.com/tamasfonak/hepp
```
Autohotspot from [here](https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/183-raspberry-pi-automatic-hotspot-and-static-hotspot-installer)

Log2Ram from [here](https://github.com/azlux/log2ram)
```
cd ./hepp/Autohotspot
chmod 0775 ./autohotspot-setup.sh
sudo ./autohotspot-setup.sh
```
**Run:**
```
sudo apt install omxplayer python3-pip
sudo pip3 install omxplayer-wrapper
sudo pip3 install Flask
cd ./hepp
chmod 0775 ./*
python3 ./hepp.py
```

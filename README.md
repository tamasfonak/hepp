Log2Ram from [here](https://github.com/azlux/log2ram)
```
echo "deb http://packages.azlux.fr/debian/ buster main" | sudo tee /etc/apt/sources.list.d/azlux.list
wget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -
sudo apt install log2ram
```
**Run:**
```
sudo apt update
sudo apt upgrade
sudo apt install omxplayer python3-pip git
sudo pip3 install omxplayer-wrapper
git clone https://github.com/tamasfonak/hepp
cd ./hepp
python3 hepp.py
```
Autohotspot from [here](https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/183-raspberry-pi-automatic-hotspot-and-static-hotspot-installer)
```
cd ./hepp/Autohotspot
chmod 0775 ./autohotspot-setup.sh
sudo ./autohotspot-setup.sh
```
AutoStart
```
sudo nano /etc/rc.local

sudo /usr/bin/python3 /home/pi/hepp/hepp.py &
exit 0
```

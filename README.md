
Megvizsgálni [here](https://pymotw.com/2/socket/tcp.html)



**Requirements:**
```
sudo apt update
sudo apt upgrade
sudo apt install git
git clone https://github.com/tamasfonak/hepp
```
Autohotspot from [here](https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/183-raspberry-pi-automatic-hotspot-and-static-hotspot-installer)
```
cd ./hepp/Autohotspot
chmod 0775 ./autohotspot-setup.sh
sudo ./autohotspot-setup.sh
```
Log2Ram from [here](https://github.com/azlux/log2ram)
```
echo "deb http://packages.azlux.fr/debian/ buster main" | sudo tee /etc/apt/sources.list.d/azlux.list
wget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -
sudo apt install log2ram
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

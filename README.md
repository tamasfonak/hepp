
**Requirements:**
```
sudo apt update
sudo apt upgrade
sudo apt install -y hostapd dnsmasq libdbus-1{,-dev}
sudo systemctl unmask hostapd
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq
```
This site was built using [Here](https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/158-raspberry-pi-auto-wifi-hotspot-switch-direct-connection)
```
sudo nano /etc/hostapd/hostapd.conf
sudo nano /etc/default/hostapd
sudo nano /etc/dnsmasq.conf
sudo nano /etc/network/interfaces
sudo cp /etc/network/interfaces /etc/network/interfaces-backup
sudo nano /etc/sysctl.conf
sudo nano /etc/dhcpcd.conf
sudo nano /etc/systemd/system/autohotspot.service
sudo systemctl enable autohotspot.service
sudo nano /usr/bin/autohotspotN
sudo chmod +x /usr/bin/autohotspotN
```
pip3 install omxplayer-wrapper

**Run:**
```
python3 hepp.py
```

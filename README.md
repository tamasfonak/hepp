
Requirements:

sudo apt update
sudo apt upgrade
sudo apt install -y hostapd dnsmasq libdbus-1{,-dev}
sudo systemctl unmask hostapd
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq

sudo nano /etc/hostapd/hostapd.conf

#2.4GHz setup wifi 80211 b,g,n
interface=wlan0
driver=nl80211
ssid=HEPP
hw_mode=g
channel=8
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=12345678
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP TKIP
rsn_pairwise=CCMP
#80211n - Change GB to your WiFi country code
country_code=HU
ieee80211n=1
ieee80211d=1

sudo nano /etc/default/hostapd

DAEMON_CONF="/etc/hostapd/hostapd.conf"

sudo nano /etc/dnsmasq.conf

#AutoHotspot config
interface=wlan0
bind-dynamic 
server=8.8.8.8
domain-needed
bogus-priv
dhcp-range=192.168.50.150,192.168.50.200,12h

sudo nano /etc/network/interfaces

# interfaces(5) file used by ifup(8) and ifdown(8)
# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'
# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

sudo cp /etc/network/interfaces /etc/network/interfaces-backup

sudo nano /etc/sysctl.conf

net.ipv4.ip_forward=1

sudo nano /etc/dhcpcd.conf

nohook wpa_supplicant

sudo nano /etc/systemd/system/autohotspot.service

[Unit]
Description=Automatically generates an internet Hotspot when a valid ssid is not in range
After=multi-user.target
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/autohotspotN
[Install]
WantedBy=multi-user.target

sudo systemctl enable autohotspot.service

sudo nano /usr/bin/autohotspotN

sudo chmod +x /usr/bin/autohotspotN



pip3 install omxplayer-wrapper


Run:

$ python3 hepp.py

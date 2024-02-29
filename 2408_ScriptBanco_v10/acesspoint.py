import json
import network

ssid = 'DCPO-CFG'
password = 'dcpopass'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
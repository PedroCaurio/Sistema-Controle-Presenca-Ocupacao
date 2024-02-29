from machine import Pin, SPI
from libMFRC522 import MFRC522
from umqtt.simple import MQTTClient
from network import WLAN,STA_IF
from time import sleep_ms

spi =SPI(1,baudrate=100000,polarity=0,phase=0,sck=Pin(18),mosi=Pin(23),miso=Pin(19))
sda = Pin(5, Pin.OUT)

led = Pin(4, Pin.OUT)

rede = "RedmiNote11S"
senha = "pedro1234"
broker = "broker.hivemq.com"
Clientid = "iagoCarniere"

def ativaWifi(ssid, pas):
  wifi = WLAN(STA_IF)
  wifi.active(True)
  if not wifi.isconnected():
    wifi.connect(ssid, pas)
    tentativas = 0
    while not wifi.isconnected() and tentativas <10:
      sleep_ms(1000)
      tentativas += 1
      print(tentativas)
    print('Wifi conectado')  
  return wifi if wifi.isconnected() else None

dispR = b'autoifrs/tcc/reg/env'
dispE = b'autoifrs/tcc/reg/rec'

def receber(top, payload):
    msg = payload.decode()
    if top == dispR:
        print("Chegou")
        if msg == '0':
            led(1)
            sleep_ms(1000)
            led(0)
            sleep_ms(1000)
            led(1)
            sleep_ms(1000)
            led(0)
        else:
            led(1)
            sleep_ms(300)
            led(0)
            sleep_ms(300)
            led(1)
            sleep_ms(300)
            led(0)
    
#--------------------------------#
rede = ativaWifi(rede, senha)
print("Wifi conectado!")
cliente = MQTTClient(Clientid, broker)
cliente.set_callback(receber)
cliente.connect()
cliente.subscribe(dispR)
print("Conectado ao broker!")
#--------------------------------#

rdr = MFRC522(spi, sda)
uid = ""

while True:
    cliente.check_msg()
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            a = str(uid)
            print(a)
            cliente.publish(dispE, a)               
            sleep_ms(1000)
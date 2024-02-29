from machine import Pin, SPI, SoftI2C
from libMFRC522 import MFRC522
from umqtt.simple import MQTTClient
from network import WLAN,STA_IF
from time import sleep_ms
import ssd1306

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

spi =SPI(1,baudrate=100000,polarity=0,phase=0,sck=Pin(18),mosi=Pin(23),miso=Pin(19))
sda = Pin(5, Pin.OUT)

display.rect(1, 2, 127, 18, 1)
display.text('AUTOMACAO', 27, 8, 1)
display.fill_rect(1, 18, 127, 43, 1)#apagar conteudo
display.text('BEM-VINDO', 31, 24, 0 )
display.text('Autores:', 1, 40, 0 )
display.text('Iago C. Pedro C.', 1, 50, 0 )
display.show()
sleep_ms(2000)

sala = '902'
capacidade = 0
ocupacao = 0

fecho = Pin(4, Pin.OUT)

rede = "RedmiNote11S"
senha = "pedro1234"
broker = "broker.hivemq.com"
Clientid = "pedroCaurio"

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

dispR = b'autoifrs/tcc/disp/env'
dispE = b'autoifrs/tcc/disp/rec'
inic  = b'autoifrs/tcc/disp/ini'
ativ  = b'autoifrs/tcc/disp/ati'

def receber(top, payload):
    global ocupacao
    global capacidade
    print("Tchau")
    if top == ativ:
        print('Ativação')
        msg = payload.decode()
        m = msg.split(';')
        ocupacao = m[1]
        capacidade = m[0]
        print(m)
    elif top == dispR:
        msg = payload.decode()
        m = msg.split(';')
        if m[0] == "0":
            #print(m)
            if m[1] == "0":                                    
                cliente.publish(inic, "{}".format(sala))
                print("Liberado")
                if m[2] == '0':
                    display.fill_rect(1, 18, 127, 43, 1)
                    display.text('BEM VINDO', 30, 24, 0 )
                    display.text('ALUNO!', 45, 36, 0 )
                    display.show()
                    sleep_ms(4000)
                elif m[2] == '1':
                    display.fill_rect(1, 18, 127, 43, 1)
                    display.text('BEM VINDO', 30, 24, 0 )
                    display.text('PROFESSOR!', 28, 36, 0 )
                    fecho(1)
                    display.show()
                    sleep_ms(4000)   
            elif m[1] == "1":
                cliente.publish(inic, "{}".format(sala))
                if m[2] == '0':
                    display.fill_rect(1, 18, 127, 43, 1)
                    display.text('ADEUS', 45, 24, 0 )
                    display.text('ALUNO!', 45, 36, 0 )
                    display.show()
                    sleep_ms(4000)
                if m[2] == '1':
                    display.fill_rect(1, 18, 127, 43, 1)
                    display.text('ADEUS', 45, 24, 0 )
                    display.text('PROFESSOR!', 25, 36, 0 )
                    display.show()
                    fecho(0)
                  #  if m[3] == '1':
                  #      print("Não trancar")
                  #  else:
                  #      print("Trancar")
                    sleep_ms(4000)
        if m[0] == "1":
            display.fill_rect(1, 18, 127, 43, 1)
            display.text('CARTAO', 43, 24, 0 )
            display.text('DESABILITADO', 17, 36, 0)
            display.show()
            sleep_ms(2000)
        if m[0] == "2":
            display.fill_rect(1, 18, 127, 43, 1)
            display.text('CARTAO', 43, 24, 0 )
            display.text('DESAPARECIDO', 17, 36, 0)
            sleep_ms(2000)
        if m[0] == "3":
            print ("Registro incompleto!")
        if m[0] == "4":
            display.fill_rect(1, 18, 127, 43, 1)
            display.text('CARTAO SEM', 24, 24, 0 )
            display.text('REGISTRO!', 30, 36, 0 )
            display.show()
            sleep_ms(2000)
            
        if m[0] == "5":
            display.fill_rect(1, 18, 127, 43, 1)
            display.text('SALA', 40, 24, 0 )
            display.text('TRANCADA', 30, 36, 0 )
            display.show()
            sleep_ms(2000)
            
        if m[0] == "6":
            display.fill_rect(1, 18, 127, 43, 1)
            display.text('SALA', 40, 24, 0 )
            display.text('CHEIA', 38, 36, 0 )
            display.show()
            sleep_ms(2000)   
    else:
        display.fill_rect(1, 18, 127, 43, 1)
        display.text('ERRO!', 40, 24, 0 )
        display.show()
        sleep_ms(2000)

#--------------------------------#
display.fill_rect(1, 18, 127, 43, 1)
display.text('CONECTANDO', 30, 28, 0 )
display.text('AO WIFI', 40, 38, 0 )
display.show()
sleep_ms(2000)
rede = ativaWifi(rede, senha)
print("Wifi conectado!")
display.fill_rect(1, 18, 127, 43, 1)
display.text('CONECTANDO', 30, 28, 0 )
display.text('AO BROKER', 33, 38, 0 )
display.show()
sleep_ms(2000)
cliente = MQTTClient(Clientid, broker)
cliente.set_callback(receber)
cliente.connect()
cliente.subscribe(dispR)
cliente.subscribe(ativ)
print("Conectado ao broker!")

display.fill_rect(1, 18, 127, 43, 1)
display.text('COLETANDO', 33, 28, 0 )
display.text('DADOS', 47, 38, 0 )
display.show()
cliente.publish(inic, "{}".format(sala))
sleep_ms(2500)
#cliente.check_msg()
sleep_ms(2500)

#--------------------------------#



rdr = MFRC522(spi, sda)
uid = ""

while True:
    cliente.check_msg()
    print('Aguardando')
    display.fill_rect(1, 18, 127, 43, 1)
    display.text('OCUPACAO ATUAL', 8, 24, 0 )
    display.text('{}'.format(ocupacao), 40, 40, 0 )
    display.text('/', 55, 40, 0 )
    display.text('{}'.format(capacidade), 70, 40, 0 )
    display.show()
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            a = str(uid)+";{}".format(sala)
            print(a)
            display.fill_rect(1, 18, 127, 43, 1)
            display.text('CARTAO LIDO', 25, 27, 0 )
            display.text('AGUARDE', 40, 38, 0 )
            display.show()
            cliente.publish(dispE, a)
            sleep_ms(1000)
                
#            sleep_ms(1000)
                


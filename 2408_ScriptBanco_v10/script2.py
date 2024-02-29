import sqlite3
import paho.mqtt.client as mqtt
#from network import STA_IF, WLAN

clienteID = "pedrocaurio"
broker = "broker.hivemq.com"



ssid = 'Note8Rocha'
senha = 'exagerado'

topicor = b'automacao/tcciagopedro/requisicoes'
topicoe = b'automacao/tcciagopedro/respostas'
'''
def ativaWifi(rede, senha):

  wifi = WLAN(STA_IF)
  wifi.active(True)
  if not wifi.isconnected():
    wifi.connect(rede, senha)
    tentativas = 0
    while not wifi.isconnected() and tentativas <10:
      sleep_ms(1000)
      tentativas += 1
    print('Wifi conectado')  
  return wifi if wifi.isconnected() else None
'''
def receber(top, payload):
    if top == topicor:
        msg = payload.decode()
        print(msg)
        pesq = cur.execute("SELECT etiqueta, estado FROM tag WHERE etiqueta={}".format(msg))
        painel = pesq.fetchall()

        if painel[0][1] == 'ativo':
            cliente.publish(topicor, 'Deu Bom')
        else:
            cliente.publish(topicor, 'QUEM É TU MAGRÃO?')
    else:
        print('erro')


#rede = ativaWifi(net, pas)
cliente = mqtt.Client()
cliente.connect(broker, 1883, 60)
cliente.subscribe(topicor)

con = sqlite3.connect("Database")
cur = con.cursor()

while True:
    cliente.check_msg()
    

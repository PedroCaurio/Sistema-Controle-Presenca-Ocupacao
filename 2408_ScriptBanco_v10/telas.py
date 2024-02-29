from machine import Pin, SPI, SoftI2C
from libMFRC522 import MFRC522
from umqtt.simple import MQTTClient
from network import WLAN,STA_IF
from time import sleep_ms
import ssd1306

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.fill(0)
#display.text('Bem vindo', 20, 24, 1 )
#display.text('aluno!', 23, 34, 1 )
display.rect(1, 2, 127, 18, 1)
display.text('AUTOMACAO', 27, 8, 1)
display.fill_rect(1, 18, 127, 43, 1)#apagar conteudo

#display.text('CONECTANDO', 30, 28, 0 )
#display.text('AO WIFI', 40, 38, 0 )

#display.text('BEM-VINDO', 31, 24, 0 )
#display.text('Autores:', 1, 40, 0 )
#display.text('Iago C. Pedro C.', 1, 50, 0 )

#display.text('OCUPACAO ATUAL', 8, 24, 0 )
#display.text('10', 57, 40, 0 )

#display.text('CARTAO LIDO', 25, 27, 0 )
#display.text('AGUARDE', 40, 38, 0 )

#display.text('BEM VINDO', 30, 24, 0 )
#display.text('PROFESSOR!', 28, 36, 0 )

#display.text('ADEUS', 45, 24, 0 )
#display.text('PROFESSOR!', 25, 36, 0 )

#display.text('CARTAO SEM', 24, 24, 0 )
#display.text('REGISTRO!', 30, 36, 0 )

display.text('CARTAO', 43, 24, 0 )
display.text('DESAPARECIDO', 17, 36, 0)

display.show()
sleep_ms(2000)

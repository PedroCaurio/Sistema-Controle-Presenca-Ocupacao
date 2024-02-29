import ssd1306
from machine import Pin, SPI, SoftI2C
from time import sleep_ms

#spi = SoftSPI(baudrate=500000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

#dc = Pin(4)   # data/command
#rst = Pin(5)  # reset
#cs = Pin(15)  # chip select, some modules do not have a pin for this

#display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, cs)

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

a = 0

while True:
    a = a + 1
    sleep_ms(3000)
    if a == 2:
        display.fill(0)
        display.text('Oie', 20, 24, 1 )
        display.show()
    elif a == 3:
        display.fill(0)
        display.text('Opa', 20, 24, 1 )
        display.show()
    else:
        display.text('Acabou', 20, 24, 1 )
        display.show()
        
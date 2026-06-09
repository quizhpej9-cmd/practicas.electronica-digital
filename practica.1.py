from machine import I2C, Pin
import time
from lcd_api import LcdApi
from lcd_i2c import I2cLcd

# Configuración del I2C (ajusta pines según tu placa)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Dirección del LCD (0x27 como en tu código)
I2C_ADDR = 0x27
TOTAL_ROWS = 2
TOTAL_COLUMNS = 16

lcd = I2cLcd(0x27 , 2, 16)

while True:
    lcd.move_to(0, 0)
    lcd.putstr("Hola, buestan")
    time.sleep(1)

    lcd.clear()

    lcd.move_to(0, 1)
    lcd.putstr("hola, quizhpe")
    time.sleep(1)

    lcd.clear()

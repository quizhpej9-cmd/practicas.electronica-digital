from machine import Pin, I2C
from time import sleep
from lcd_i2c import I2cLcd

# Dirección del LCD (prueba 0x27 o 0x3F)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(0x27, 2, 16)


# Limpiar pantalla
lcd.clear()

# Texto con espacios para efecto de entrada/salida
texto = "    hola, bienvenido joel y abraham    "

while True:
    for i in range(len(texto) - 15):
        lcd.move_to(0, 0)  # Fila 1
        lcd.putstr(texto[i:i+16])
        sleep(0.3)

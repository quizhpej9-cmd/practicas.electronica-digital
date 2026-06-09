from time import sleep
from lcd_i2c import I2cLcd

# Inicializar LCD
lcd = I2cLcd(0x27, 2, 16)

# ❤️ Crear corazón
def crear_corazon():
    corazon =   [
        0b00000,
        0b01010,
        0b11111,
        0b11111,
        0b11111,
        0b01110,
        0b00100,
        0b00000
    ]
    lcd.custom_char(0, corazon)

# ▶️ Ejecutar
lcd.clear()
crear_corazon()

# Mostrar solo el corazón en el centro
lcd.move_to(7, 0)   # posición centrada en fila 1
lcd.putchar(chr(0))

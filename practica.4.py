from time import sleep
from lcd_i2c import I2cLcd

lcd = I2cLcd(0x27, 2, 16)

# 🔷 Crear figura personalizada (la que enviaste)
def crear_figura():
    figura = [
        0b00100,
        0b01100,
        0b11100,
        0b00100,
        0b11111,
        0b11111,
        0b01110,
        0b00000
    ]
    lcd.custom_char(0, figura)

# 🔁 Movimiento de izquierda a derecha
def mover_figura(delay=0.2):
    while True:
        for col in range(16):
            lcd.clear()
            lcd.move_to(col, 0)   # mover en fila 1
            lcd.putchar(chr(0))
            sleep(delay)

# ▶️ Ejecutar
lcd.clear()
crear_figura()
mover_figura()

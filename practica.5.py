from time import sleep
from lcd_i2c import I2cLcd

lcd = I2cLcd(0x27, 2, 16)

# 🔷 Figura personalizada
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

# 🔁 Movimiento de la figura
def mover_figura():
    for col in range(16):
        lcd.clear()
        lcd.move_to(col, 0)
        lcd.putchar(chr(0))
        sleep(0.2)

# 📜 Texto en movimiento
def texto_scroll(texto, delay=0.25):
    texto = " " * 16 + texto + " " * 16
    for i in range(len(texto) - 15):
        lcd.move_to(0, 1)  # fila 2
        lcd.putstr(texto[i:i+16])
        sleep(delay)

# ▶️ Ejecutar
lcd.clear()
crear_figura()

# Primera pasada
mover_figura()

# Segunda pasada
mover_figura()

# Mostrar mensaje en movimiento
texto_scroll("A llegado a la meta")

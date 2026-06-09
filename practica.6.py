from machine import Pin, I2C
import time
from lcd_api import LcdApi
from lcd_i2c import I2cLcd

# ---------------------------
# CONFIG LCD
# ---------------------------
I2C_ADDR = 0x27
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd( 0x27, 2, 16)

# ---------------------------
# TECLADO CORREGIDO
# ---------------------------
class Keypad4x4:
    def __init__(self, row_pins, col_pins):
        self.rows = [Pin(pin, Pin.OUT) for pin in row_pins]
        self.cols = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in col_pins]

        self.keys = [
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D']
        ]

        for row in self.rows:
            row.value(1)

    def getKey(self):
        for i, row in enumerate(self.rows):
            row.value(0)

            for j, col in enumerate(self.cols):
                if col.value() == 0:
                    time.sleep_ms(80)  # mejor anti-rebote
                    if col.value() == 0:
                        while col.value() == 0:
                            pass
                        row.value(1)
                        return self.keys[i][j]

            row.value(1)

        return None

# 🔥 Pines YA CORREGIDOS según tu caso
rows = [17, 5, 18, 19]
cols = [16, 4, 2, 15]

keypad = Keypad4x4(rows, cols)

# ---------------------------
# PROGRAMA PRINCIPAL
# ---------------------------
lcd.clear()
lcd.putstr("Ingresa:")

texto = ""

while True:
    key = keypad.getKey()

    if key:
        print("Tecla:", key)

        # 🔹 Borrar
        if key == "*":
            texto = ""
            lcd.clear()
            lcd.putstr("Borrado")
            time.sleep(1)
            lcd.clear()
            lcd.putstr("Ingresa:")

        # 🔹 Confirmar
        elif key == "#":
            lcd.clear()
            lcd.putstr("Guardado:")
            lcd.move_to(0,1)
            lcd.putstr(texto)
            time.sleep(2)

            texto = ""
            lcd.clear()
            lcd.putstr("Ingresa:")

        # 🔹 Escribir
        else:
            texto += key
            lcd.clear()
            lcd.putstr("Ingresa:")
            lcd.move_to(0,1)
            lcd.putstr(texto)

    time.sleep(0.1)

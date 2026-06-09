from machine import Pin, I2C
import time
from lcd_api import LcdApi
from lcd_i2c import I2cLcd

# ================= LCD =================

I2C_ADDR = 0x27

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

lcd = I2cLcd(0x27, 2, 16)

# ================= TECLADO =================

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

                    time.sleep_ms(80)

                    if col.value() == 0:

                        while col.value() == 0:
                            pass

                        row.value(1)

                        return self.keys[i][j]

            row.value(1)

        return None

# ================= PINES =================

rows = [17, 5, 18, 19]
cols = [16, 4, 2, 15]

keypad = Keypad4x4(rows, cols)

# ================= CONTRASEÑA =================

PASSWORD = "2009"

# ================= INICIO =================

lcd.clear()
lcd.putstr("Sistema listo")
time.sleep(2)

# ================= LOOP PRINCIPAL =================

while True:

    ingreso = ""

    lcd.clear()
    lcd.putstr("Clave:")
    lcd.move_to(0,1)

    while True:

        key = keypad.getKey()

        if key:

            print("Tecla:", key)

            # 🔴 BORRAR
            if key == "*":

                ingreso = ""

                lcd.clear()
                lcd.putstr("Borrado")
                time.sleep(1)

                lcd.clear()
                lcd.putstr("Clave:")
                lcd.move_to(0,1)

            # 🟢 CONFIRMAR CON #
            elif key == "#":

                break

            # 🔹 ESCRIBIR
            else:

                if len(ingreso) < 16:

                    ingreso += key

                    lcd.putstr("*")

    # ================= VALIDAR =================

    lcd.clear()

    if ingreso == PASSWORD:

        lcd.putstr("Acceso")
        lcd.move_to(0,1)
        lcd.putstr("ACEPTADO")

    else:

        lcd.putstr("Acceso")
        lcd.move_to(0,1)
        lcd.putstr("DENEGADO")

    time.sleep(3)

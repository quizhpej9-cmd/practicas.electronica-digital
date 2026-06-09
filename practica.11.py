import utime
from lcd_i2c import I2cLcd

# LCD
I2C_ADDR = 0x27
lcd = I2cLcd(I2C_ADDR, 2, 16)

# Personaje
objeto = bytearray([
    0b00100,
    0b01110,
    0b11111,
    0b01110,
    0b01110,
    0b00000,
    0b00000,
    0b00000
])

lcd.custom_char(0, objeto)

# Posición inicial
x = 0
y = 0

# Dirección
dx = 1
dy = 1

while True:

    lcd.clear()

    lcd.move_to(x, y)
    lcd.putchar(chr(0))

    utime.sleep_ms(150)

    x += dx
    y += dy

    # Rebote horizontal
    if x >= 15:
        x = 15
        dx = -1

    elif x <= 0:
        x = 0
        dx = 1

    # Rebote vertical
    if y >= 1:
        y = 1
        dy = -1

    elif y <= 0:
        y = 0
        dy = 1

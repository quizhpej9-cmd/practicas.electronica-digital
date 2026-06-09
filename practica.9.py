import utime
from machine import Pin
from lcd_i2c import I2cLcd

# ==========================
# LCD I2C
# ==========================
I2C_ADDR = 0x27
lcd = I2cLcd(I2C_ADDR, 2, 16)

# ==========================
# TECLADO 4x4
# R1=17 R2=5 R3=18 R4=19
# C1=16 C2=4 C3=2 C4=15
# ==========================
filas_pines = [17, 5, 18, 19]
columnas_pines = [16, 4, 2, 15]

filas = [Pin(p, Pin.OUT) for p in filas_pines]
columnas = [Pin(p, Pin.IN, Pin.PULL_DOWN) for p in columnas_pines]

teclas = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# ==========================
# PERSONAJE
# ==========================
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

# ==========================
# POSICIÓN INICIAL
# ==========================
pos_x = 0
pos_y = 1

# ==========================
# ACTUALIZAR LCD
# ==========================
def actualizar_pantalla():
    lcd.clear()
    lcd.move_to(pos_x, pos_y)
    lcd.putchar(chr(0))

# ==========================
# LEER TECLADO
# ==========================
def leer_tecla():

    for fila in filas:
        fila.value(0)

    for i, fila in enumerate(filas):

        fila.value(1)

        for j, columna in enumerate(columnas):

            if columna.value() == 1:

                tecla = teclas[i][j]

                while columna.value() == 1:
                    utime.sleep_ms(20)

                fila.value(0)
                return tecla

        fila.value(0)

    return None

# ==========================
# INICIO
# ==========================
lcd.clear()
actualizar_pantalla()

print("Sistema listo")
print("2=Arriba")
print("4=Izquierda")
print("6=Derecha")
print("8=Abajo")

# ==========================
# BUCLE PRINCIPAL
# ==========================
while True:

    tecla = leer_tecla()

    if tecla:

        if tecla == '4':
            if pos_x > 0:
                pos_x -= 1

        elif tecla == '6':
            if pos_x < 15:
                pos_x += 1

        elif tecla == '2':
            if pos_y > 0:
                pos_y -= 1

        elif tecla == '8':
            if pos_y < 1:
                pos_y += 1

        actualizar_pantalla()

        print("Tecla:", tecla,
              "| Coordenadas:",
              "(", pos_x, ",", pos_y, ")")

    utime.sleep_ms(10)

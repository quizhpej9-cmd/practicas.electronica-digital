from machine import Pin, I2C
from lcd_api import LcdApi
from lcd_i2c import I2cLcd
import network
import ntptime
import time

# ================= WIFI =================

SSID = "mencho"
PASSWORD = "987654321"

wifi = network.WLAN(network.STA_IF)

# Reinicia el WiFi
wifi.active(False)
time.sleep(1)

wifi.active(True)
time.sleep(2)

# Conectar
wifi.connect(SSID, PASSWORD)

print("Conectando WiFi...")
# ================= LCD =================

I2C_ADDR = 0x27

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

lcd = I2cLcd(0x27, 2, 16)

# ================= CONECTANDO =================

lcd.clear()
lcd.putstr("Conectando WiFi")

timeout = 15

while not wifi.isconnected() and timeout > 0:
    print("Conectando...")
    time.sleep(1)
    timeout -= 1

lcd.clear()
lcd.putstr("WiFi conectado")
time.sleep(2)

# ================= OBTENER HORA =================

lcd.clear()
lcd.putstr("Obteniendo hora")

try:
    ntptime.settime()
    lcd.clear()
    lcd.putstr("Hora sincronizada")
except:
    lcd.clear()
    lcd.putstr("Error de hora")

time.sleep(2)

# ================= LOOP =================

while True:

    # Hora UTC
    t = time.localtime()

    # 🔥 Ajuste Ecuador UTC-5
    hora = (t[3] - 0) % 24
    minuto = t[4]
    segundo = t[5]

    # Mostrar en LCD
    lcd.clear()

    lcd.putstr("Hora actual:")

    lcd.move_to(0,1)

    texto = "{:02}:{:02}:{:02}".format(
        hora,
        minuto,
        segundo
    )

    lcd.putstr(texto)

    time.sleep(1)

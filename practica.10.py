import machine
import time
from lcd_i2c import I2cLcd  # Importa tu librería lcd_i2c.py

# ── Configuración del Relé ──────────────────────────────────
PIN_RELE = 18
rele = machine.Pin(PIN_RELE, machine.Pin.OUT)
rele.value(0) # Inicia apagado

# También dejamos el LED azul de la placa (GPIO 2) como testigo visual adicional
led_interno = machine.Pin(2, machine.Pin.OUT)
led_interno.value(0)

# ── Configuración del LCD I2C ──────────────────────────────
DIR_LCD = 0x27 
lcd = I2cLcd(DIR_LCD, 2, 16)

# ── Configuración del Teclado 4x4 ──────────────────────────
FILAS = 4
COLS = 4

teclas = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

pines_filas = [13, 12, 14, 27]
pines_cols = [26, 25, 33, 32]

row_pins = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in pines_filas]
col_pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pines_cols]

def leer_teclado():
    for j, col_pin in enumerate(col_pins):
        col_pin.value(0)
        for i, row_pin in enumerate(row_pins):
            if row_pin.value() == 0:
                while row_pin.value() == 0:
                    time.sleep_ms(10)
                col_pin.value(1)
                return teclas[i][j]
        col_pin.value(1)
    return None

# ── Caracteres Personalizados (Flecha) ─────────────────────
flecha_der = [0x00, 0x04, 0x06, 0x1F, 0x1F, 0x06, 0x04, 0x00]
lcd.custom_char(0, flecha_der)

# ── Variables del Programa ──────────────────────────────────
entrada_usuario = ""
tiempo_activacion = 0 

# ── Funciones de Interfaz ───────────────────────────────────
def actualizar_display():
    lcd.move_to(8, 0)
    lcd.putstr("        ")
    lcd.move_to(8, 0)
    if len(entrada_usuario) > 0:
        lcd.putstr(entrada_usuario)
    else:
        lcd.putstr("_")

def mostrar_pantalla_principal():
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putchar(chr(0))
    lcd.putstr(" Segs: ")
    lcd.move_to(0, 1)
    lcd.putstr("#=OK *=Borrar B=5s")
    actualizar_display()

def mostrar_error(msg):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("ERROR:")
    lcd.move_to(0, 1)
    lcd.putstr(msg)
    time.sleep(2)

def activar_motor(segundos):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("MOTOR ENCENDIDO")
    lcd.move_to(0, 1)
    lcd.putstr(f"Por {segundos} segundos")
    
    print(f"Activando relé por {segundos} segundos...")
    rele.value(1)        # ¡Manda energía al relé! (Enciende el motor)
    led_interno.value(1) # Prende el led de la placa como apoyo
    
    time.sleep(segundos) # Mantiene el motor encendido
        
    rele.value(0)        # ¡Apaga el relé! (Detiene el motor)
    led_interno.value(0)
    print("Relé desactivado.")
    
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Terminado.")
    time.sleep(1)

# ── Configuración Inicial ───────────────────────────────────
lcd.move_to(0, 0)
lcd.putstr("Control de Rele")
lcd.move_to(0, 1)
lcd.putstr("ESP32 Listo")
time.sleep(2)

mostrar_pantalla_principal()

# ── Bucle Principal ─────────────────────────────────────────
while True:
    tecla = leer_teclado()
    
    if tecla:
        print(f"Tecla: {tecla}")
        
        if '0' <= tecla <= '9':
            if len(entrada_usuario) < 4:
                entrada_usuario += tecla
                actualizar_display()
                
        elif tecla == '#':
            if len(entrada_usuario) > 0:
                tiempo_activacion = int(entrada_usuario)
                if tiempo_activacion > 0:
                    activar_motor(tiempo_activacion)
                else:
                    mostrar_error("Tiempo invalido")
                entrada_usuario = ""
                mostrar_pantalla_principal()
                
        elif tecla == '*':
            entrada_usuario = ""
            mostrar_pantalla_principal()
            
        elif tecla == 'B':
            activar_motor(5)
            mostrar_pantalla_principal()
            
        elif tecla == 'C':
            activar_motor(10)
            mostrar_pantalla_principal()
            
        elif tecla == 'D':
            rele.value(0)
            led_interno.value(0)
            entrada_usuario = ""
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Apagado Forzado")
            time.sleep(1)
            mostrar_pantalla_principal()

    time.sleep_ms(20)

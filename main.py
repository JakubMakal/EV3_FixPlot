#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Initialize the EV3 display
ev3 = EV3Brick()

#!/usr/bin/env pybricks-micropython

left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
color_sensor = ColorSensor(Port.S4)
touch_sensor_cycle = TouchSensor(Port.S3)    
touch_sensor_confirm = TouchSensor(Port.S2)  
gyro = GyroSensor(Port.S1)


robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=80)


def turn_degrees(target_angle, speed):
    """Otočí vozítko o zadaný počet stupňů.
       Měří se změna úhlu pomocí gyro senzoru."""
    initial_angle = gyro.angle()
    if target_angle > 0:
        left_motor.run(speed)
        right_motor.run(-speed)
        while (gyro.angle() - initial_angle) < target_angle:
            wait(10)
    elif target_angle < 0:
        left_motor.run(-speed)
        right_motor.run(speed)
        while (initial_angle - gyro.angle()) < abs(target_angle):
            wait(10)
    left_motor.stop()
    right_motor.stop()

# ---------------------------------------------------
# Funkce pro vykreslení jednotlivých obrazců


def draw_circle():
    # Pro "kruh" se robot otočí o 360° (ne úplně přesný kruh, ale ilustrativní).
    for _ in range(36):  # 10° otoček 36x simuluje kruh
        robot.straight(30)
        robot.turn(10)

def draw_triangle():
    for i in range(3):
        robot.straight(100)
        robot.turn(240)
        

def draw_square():
    for i in range(4):
        robot.straight(100)
        robot.turn(90)

def draw_rectangle():
    robot.straight(150)
    robot.turn(90)
    robot.straight(100)
    robot.turn(90)
    robot.straight(150)
    robot.turn(90)
    robot.straight(100)
    robot.turn(90)

def draw_star():
    for i in range(5):
        robot.straight(100)
        robot.turn(144)

def draw_pentagon():
    for i in range(5):
        robot.straight(100)
        robot.turn(1200)

# ---------------------------------------------------
# Detekce barvy víčka fixu pomocí barevného senzoru

ev3.screen.clear()
ev3.screen.draw_text(10, 50, "Umísti fix s barevnym vickem")
wait(2000)

# Program čeká, dokud senzor nezachytí platnou barvu
detected_color = color_sensor.color()
while detected_color is None:
    detected_color = color_sensor.color()
    wait(10)

# Nastavení voleb obrazců podle detekované barvy fixu
if detected_color == Color.RED:
    options = ["circle", "triangle"]
elif detected_color == Color.GREEN:
    options = ["square", "rectangle"]
elif detected_color == Color.BLUE:
    options = ["star", "pentagon"]
else:
    ev3.screen.draw_text(50, 50, "ERROR 404 COLOR NOT FOUND")
    wait(100)
    exit(1)

# ---------------------------------------------------
# Výběr obrazce pomocí touch senzorů

selected_index = 0
ev3.screen.clear()
ev3.screen.draw_text(50, 50, options[selected_index])
ev3.screen.draw_text(10, 80, "Stiskni pro zmenu, potvrdit pro volbu")

while True:
    if touch_sensor_cycle.pressed():
        # Po stisknutí změníme volbu a počkáme na uvolnění tlačítka (debounce)
        while touch_sensor_cycle.pressed():
            wait(10)
        selected_index = (selected_index + 1) % len(options)
        ev3.screen.clear()
        ev3.screen.draw_text(50, 50, options[selected_index])
        wait(300)
    if touch_sensor_confirm.pressed():
        while touch_sensor_confirm.pressed():
            wait(10)
        break

selected_shape = options[selected_index]
ev3.screen.clear()
ev3.screen.draw_text(10, 50, "Zvoleno: " + selected_shape)
wait(1000)

# ---------------------------------------------------
# Vykreslení vybraného obrazce

if selected_shape == "circle":
    draw_circle()
elif selected_shape == "triangle":
    draw_triangle()
elif selected_shape == "square":
    draw_square()
elif selected_shape == "rectangle":
    draw_rectangle()
elif selected_shape == "star":
    draw_star()
elif selected_shape == "pentagon":
    draw_pentagon()

ev3.screen.clear()
ev3.screen.draw_text(10, 50, "Hotovo!")


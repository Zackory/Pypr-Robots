import time
import pigpio
import numpy as np

port1 = 12
port2 = 13
gpio = pigpio.pi()
gpio.set_PWM_frequency(port1, 1000)

for i in np.arange(-1.0, 1.0, 0.05):
    gpio.set_servo_pulsewidth(port1, 1500 + 1000*i)
    time.sleep(0.2)

gpio.stop()

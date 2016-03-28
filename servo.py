class Servo:
    gpio = None

    def __init__(self, port, positionRange=500):
        if Servo.gpio is None:
            print 'Creating Servo GPIO'
            Servo.gpio = pigpio.pi()
        self.port = port
        self.positionRange = positionRange
        self.speed = 0
        self.position = 1500
        # Set frequency and pulse width
        Servo.gpio.set_PWM_frequency(port, 100)
        Servo.gpio.set_servo_pulsewidth(port, 0)

    # Speed between -1.0 and 1.0
    def setSpeed(self, speed):
        if self.speed != speed and abs(speed) <= 1.0:
            # Set servo pulse width to adjust speed of continuous servo
            self.speed = speed
            # Safe range (1000-2000), <1500 backwards, >1500 forwards, 1500 stopped (max range of 500-2500)
            Servo.gpio.set_servo_pulsewidth(self.port, 0 if speed == 0 else 1500 + speed*500)

    # Position between -1.0 and 1.0
    def setPosition(self, position):
        if self.position != position and abs(position) <= 1.0:
            # Set servo pulse width to adjust position of fixed rotation servo
            self.position = position
            # 1500 center point (max range 500-2500, safe range 1000-2000)
            Servo.gpio.set_servo_pulsewidth(self.port, 1500 + position*self.positionRange)

    # Position between -1.0 and 1.0
    def alterPosition(self, positionIncrement):
        newPos = self.position + positionIncrement
        if newPos > 1.0: newPos = 1.0
        elif newPos < -1.0: newPos = -1.0
        if self.position != newPos:
            # Set servo pulse width to adjust position of fixed rotation servo
            self.position = newPos
            # 1500 center point (max range 500-2500, safe range 1000-2000)
            Servo.gpio.set_servo_pulsewidth(self.port, 1500 + newPos * self.positionRange)

    def stop(self):
        Servo.gpio.set_servo_pulsewidth(self.port, 0)

    @staticmethod
    def stopGpio():
        Servo.gpio.stop()

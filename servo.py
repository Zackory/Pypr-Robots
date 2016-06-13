import pigpio

class Servo:
    gpio = None

    def __init__(self, port, positionRange=500, invert=False):
        if Servo.gpio is None:
            print 'Creating Servo GPIO'
            Servo.gpio = pigpio.pi()
        self.port = port
        self.positionRange = positionRange
        self.speed = 0
        self.position = 1500
        self.inv = -1 if invert else 1
        # Set frequency and pulse width
        Servo.gpio.set_PWM_frequency(port, 100)
        Servo.gpio.set_servo_pulsewidth(port, 0)

    # Speed between -1.0 and 1.0 (used for continuous rotation servos)
    def setSpeed(self, speed):
        speed *= self.inv # Invert the speed if necessary
        if self.speed != speed and abs(speed) <= 1.0:
            # Set servo pulse width to adjust speed of continuous servo
            self.speed = speed
            # Safe range (1000-2000), <1500 backwards, >1500 forwards, 1500 stopped (max range of 500-2500)
            Servo.gpio.set_servo_pulsewidth(self.port, 0 if speed == 0 else 1500 + speed*self.positionRange)

    # Position between -1.0 and 1.0 (used for fixed 180 degree rotation servos)
    def setPosition(self, position):
        position *= self.inv # Invert the position if necessary
        if self.position != position and abs(position) <= 1.0:
            # Set servo pulse width to adjust position of fixed rotation servo
            self.position = position
            # 1500 center point (max range 500-2500, safe range 1000-2000)
            Servo.gpio.set_servo_pulsewidth(self.port, 1500 + position*self.positionRange)

    # Add to current position between -1.0 and 1.0 (used for fixed 180 degree rotation servos)
    def alterPosition(self, positionIncrement):
        positionIncrement *= self.inv # Invert the position increment if necessary
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

import time
import servo
import joystick

joy = joystick.Joystick(0)
magnitude = 1 / 10.0

leftEye = servo.Servo(17, 1000)
rightEye = servo.Servo(18, 1000)

done = False
while not done:
    # Process all joystick events
    joy.processEvents()
    done = joy.get(joy.RBumper)

    # Update servo positions based on joystick
    LThumbX = joy.get(joy.LThumbX)
    if abs(LThumbX) >= 0.1:
        leftEye.alterPosition(LThumbX * magnitude)

    RThumbX = joy.get(joy.RThumbX)
    if abs(RThumbX) >= 0.1:
        rightEye.alterPosition(RThumbX * magnitude)

    time.sleep(0.05)

try:
    joy.quitJoystick()
except:
    pass

leftEye.stop()
rightEye.stop()
leftEye.stopGpio()

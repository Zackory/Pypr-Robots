import time
import servo
import joystick

joy = joystick.Joystick(0)
magnitude = 1 / 10.0

leftEye = servo.Servo(17, 900)
rightEye = servo.Servo(18, 900)

if False:
    # Test that both eyes are moving!
    for i in xrange(-10, 11):
        leftEye.setPosition(i / 10.0)
        rightEye.setPosition(i / 10.0)
        time.sleep(0.5)
    exit()

# Start eyes at an initial position
leftEye.setPosition(1.0)
rightEye.setPosition(-1.0)

done = False
connected = True
while not done:
    # Process all joystick events
    joy.processEvents()
    done = joy.get(joy.RBumper)
    if joy.getToggle(joy.LBumper):
        connected = not connected
        leftEye.setPosition(1.0)
        rightEye.setPosition(-1.0)

    # Update servo positions based on joystick
    LThumbX = joy.get(joy.LThumbX)
    if abs(LThumbX) >= 0.1:
        leftEye.alterPosition(LThumbX * magnitude)
        if connected:
            rightEye.alterPosition(-LThumbX * magnitude)

    if not connected:
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

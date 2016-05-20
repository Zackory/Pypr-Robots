import time
import servo
import joystick

joy = joystick.Joystick(0)
magnitude = 1 / 10.0

leftEye = servo.Servo(17, 900)
rightEye = servo.Servo(18, 900)
leftEar = servo.Servo(22, 900)
rightEar = servo.Servo(23, 900)

if False:
    # Test that both eyes and ears are moving!
    for i in xrange(-10, 11):
        leftEye.setPosition(i / 10.0)
        rightEye.setPosition(-i / 10.0)
        leftEar.setPosition(i / 10.0)
        rightEar.setPosition(-i / 10.0)
        time.sleep(0.5)
    exit()

# Start eyes at an initial position
leftEye.setPosition(1.0)
rightEye.setPosition(-1.0)
leftEar.setPosition(-1.0)
rightEar.setPosition(1.0)

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

    # Update servos for eye positions based on joystick
    LThumbX = joy.get(joy.LThumbX)
    if abs(LThumbX) >= 0.1:
        leftEye.alterPosition(LThumbX * magnitude)
        if connected:
            rightEye.alterPosition(-LThumbX * magnitude)

    if not connected:
        RThumbX = joy.get(joy.RThumbX)
        if abs(RThumbX) >= 0.1:
            rightEye.alterPosition(RThumbX * magnitude)

    # Update servos for ear positions based on joystick
    LHat = joy.get(joy.LHat)
    RHat = joy.get(joy.RHat)
    if LHat:
        leftEar.alterPosition(1 * magnitude)
        if connected:
            rightEar.alterPosition(-1 * magnitude)
    elif RHat:
        leftEar.alterPosition(-1 * magnitude)
        if connected:
            rightEar.alterPosition(1 * magnitude)

    if not connected:
        B = joy.get(joy.B)
        Y = joy.get(joy.Y)
        if B:
            rightEar.alterPosition(1 * magnitude)
        elif Y:
            rightEar.alterPosition(-1 * magnitude)

    time.sleep(0.05)

try:
    joy.quitJoystick()
except:
    pass

leftEye.stop()
rightEye.stop()
leftEar.stop()
rightEar.stop()
leftEye.stopGpio()

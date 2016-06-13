import time
import servo
import joystick

joy = joystick.Joystick(0)
magnitude = 1 / 10.0

base = servo.Servo(17, 900)
gripper = servo.Servo(18, 900)
arm = servo.Servo(22, 900)
forearm = servo.Servo(23, 900)

# Start servos at an initial position
base.setPosition(0.0)
gripper.setPosition(0.0)
arm.setPosition(0.0)
forearm.setPosition(0.0)

if False:
    # Test that all joints are moving!
    for i in xrange(-10, 11):
        base.setPosition(i / 10.0)
        gripper.setPosition((i+9) / 19.0)
        arm.setPosition(i / 10.0)
        forearm.setPosition(-i / 10.0)
        time.sleep(0.5)
    exit()

done = False
while not done:
    # Process all joystick events
    joy.processEvents()
    done = joy.get(joy.RBumper)

    # Update servos for eye positions based on joystick
    LThumbX = joy.get(joy.LThumbX)
    if abs(LThumbX) >= 0.1:
        base.alterPosition(-LThumbX * magnitude)

    LThumbY = joy.get(joy.LThumbY)
    if abs(LThumbY) >= 0.1:
        arm.alterPosition(LThumbY * magnitude)

    RThumbY = joy.get(joy.RThumbY)
    if abs(RThumbY) >= 0.1:
        forearm.alterPosition(-RThumbY * magnitude)

    RThumbX = joy.get(joy.RThumbX)
    if abs(RThumbX) >= 0.1:
        gripper.alterPosition(RThumbX * magnitude)

    time.sleep(0.05)

try:
    joy.quitJoystick()
except:
    pass

base.stop()
gripper.stop()
arm.stop()
forearm.stop()
base.stopGpio()

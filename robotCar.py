import time
import servo
import joystick

joy = joystick.Joystick(0)

backLeft = servo.Servo(17, 1000)
backRight = servo.Servo(18, 1000)
frontLeft = servo.Servo(22, 1000)
frontRight = servo.Servo(23, 1000)

done = False
isTank = False
while not done:
    # Process all joystick events
    joy.processEvents()
    done = joy.get(joy.RBumper)
    if joy.getToggle(joy.LBumper):
        # Swap between arcade and tank driving
        isTank = not isTank

    # Update servo positions based on joystick
    if isTank:
        # Tank driving based on the left and right joysticks
        # Move right wheels
        RThumbY = joy.get(joy.RThumbY)
        if abs(RThumbY) >= 0.1:
            frontRight.setSpeed(RThumbY)
            backRight.setSpeed(RThumbY)
        else:
            frontRight.stop()
            backRight.stop()

        # Move left wheels
        LThumbY = joy.get(joy.LThumbY)
        if abs(LThumbY) >= 0.1:
            frontLeft.setSpeed(-LThumbY)
            backLeft.setSpeed(-LThumbY)
        else:
            frontLeft.stop()
            backLeft.stop()
    else:
        # Arcade driving based solely on the right joystick
        # Using the joystick to tank drive formulas provided at:
        # http://home.kendra.com/mauser/Joystick.html
        RThumbY = joy.get(joy.RThumbY)
        RThumbX = joy.get(joy.RThumbX)
        v = (1-abs(RThumbX))*RThumbY + RThumbY
        w = (1-abs(RThumbY))*RThumbX + RThumbX
        right = (v + w) / 2.0
        left = (v - w) / 2.0
        if abs(right) >= 0.1 or abs(left) >= 0.1:
            frontRight.setSpeed(right)
            backRight.setSpeed(right)
            frontLeft.setSpeed(left)
            backLeft.setSpeed(left)
        else:
            frontRight.stop()
            backRight.stop()
            frontLeft.stop()
            backLeft.stop()

    time.sleep(0.05)

try:
    joy.quitJoystick()
except:
    pass

backLeft.stop()
backRight.stop()
frontLeft.stop()
frontRight.stop()
backLeft.stopGpio()

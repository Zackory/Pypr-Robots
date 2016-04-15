import pygame

class Joystick:
    # Static variables for joystick events (type, index) | (types: 0 = button, 1 = trigger/axis, 2 = hat)
    A = (0, 0) # Triangle
    B = (0, 1) # O
    X = (0, 2) # X
    Y = (0, 3) # Square
    LBumper = (0, 4)
    RBumper = (0, 5)

    LThumbX = (1, 0)
    LThumbY = (1, 1)
    LTrigger = (1, 2)
    RThumbX = (1, 3)
    RThumbY = (1, 4)
    RTrigger = (1, 5)

    def __init__(self, index=None):
        # Initialize joystick
        pygame.init()
        pygame.joystick.init()

        self.joystick = None
        if index is not None:
            self.setJoystick(index)
        self.buttonToggles = [False]*6

    def setJoystick(self, index):
        if index >= pygame.joystick.get_count():
            print 'No joystick available with index', index
            return
        self.joystick = pygame.joystick.Joystick(index)
        self.joystick.init()
        print 'Joystick %i initalized, press Right Bumper (R1) to exit' % index

        # Fix error of triggers not appearing as axes
        if self.joystick.get_numaxes() < 6:
            self.LTrigger = (0, 6)
            self.RTrigger = (0, 7)
            self.RThumbX = (1, 2)
            self.RThumbY = (1, 3)

    @staticmethod
    def processEvents():
        # Process all events from pygame
        for _ in pygame.event.get():
            pass

    def get(self, event):
        t, i = event # (type, index)
        return self.button(i) if t == 0 else self.axis(i) if t == 1 else self.hat(i)

    def getToggle(self, event):
        # Returns true only once when a button has been pressed and released
        t, i = event
        if t != 0: return False
        if self.button(i):
            self.buttonToggles[i] = True
        elif self.buttonToggles[i]:
            self.buttonToggles[i] = False
            return True
        return False

    # Helper functions
    def button(self, i):
        if i > self.joystick.get_numbuttons():
            print 'Unable to find button %d, there are only %d buttons' % (i, self.joystick.get_numbuttons())
            return False
        return self.joystick.get_button(i) == 1
    def axis(self, i):
        if i > self.joystick.get_numaxes():
            print 'Unable to find axis %d, there are only %d axes' % (i, self.joystick.get_numaxes())
            return 0
        return self.joystick.get_axis(i)
    def hat(self, i):
        if i > self.joystick.get_numhats():
            print 'Unable to find hat %d, there are only %d hats' % (i, self.joystick.get_numhats())
            return 0
        return self.joystick.get_hat(i)
    def displayJoystickEvents(self):
        print 'Buttons:', [self.button(i) for i in xrange(self.joystick.get_numbuttons())], \
            '| Axes:', [self.axis(i) for i in xrange(self.joystick.get_numaxes())], \
            '| Hats', [self.hat(i) for i in xrange(self.joystick.get_numhats())]

    def quitJoystick(self):
        # Quit joystick control
        self.joystick.quit()
        pygame.joystick.quit()
        pygame.quit()


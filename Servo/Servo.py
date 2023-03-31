from machine import PWM,Pin
class Servo:
    def __init__(self,p,frq=50):
        self.pin=PWM(Pin(p),freq=frq)
    def write(self,deg):
        self.pin.duty(int(deg*103/180+24))

from machine import Pin
from time import sleep
class Lcd:

    def __init__(self, D7, D6,D5,D4,e1,rs,D3=0,D2=0,D1=0,D0=0,e2=0,Type="2*16",Mode="4-b"):
        self.Col1=0
        self.Row1=1
        self.Col2=0
        self.Row2=1
        self.size=int(Type.split('*')[1])
        self.lines=int(Type.split('*')[0])
        self.Mode=Mode
        self.D7 = Pin(D7,Pin.OUT)
        self.D6 = Pin(D6,Pin.OUT)
        self.D5 = Pin(D5,Pin.OUT)
        self.D4 = Pin(D4,Pin.OUT)
        if self.Mode=="4-b":
            self.D3 = Pin(D7,Pin.OUT)
            self.D2 = Pin(D6,Pin.OUT)
            self.D1 = Pin(D5,Pin.OUT)
            self.D0 = Pin(D4,Pin.OUT)
        elif self.Mode=="8-b":
            self.D3 = Pin(D3,Pin.OUT)
            self.D2 = Pin(D2,Pin.OUT)
            self.D1 = Pin(D1,Pin.OUT)
            self.D0 = Pin(D0,Pin.OUT)
        self.E1 = Pin(e1,Pin.OUT)
        if self.lines==2:
            self.E2=self.E1
        else:
            self.E2=Pin(e2,Pin.OUT)
        self.Rs = Pin(rs,Pin.OUT)  
    def set_display_mode(self):
        if self.Mode=="4-b":
            self.cmd(0x20)
            sleep(0.05)
            self.cmd(0x28) 
        else:
            self.cmd(0x30)
            sleep(0.05)
            self.cmd(0x38)
    def moveto(self,row,coloun):
        if row == 1 :
            self.Col1=coloun
            self.Row1=1
            self.cmd(0x80+coloun,1)
        elif row == 2 :
            self.Col1=coloun
            self.Row1=2
            self.cmd(0xc0+coloun,1)
        elif row == 3 :
            self.Col2=coloun
            self.Row2=1
            self.cmd(0x80+coloun,2)
        elif row == 4 :
            self.Col2=coloun
            self.Row2=1
            self.cmd(0xc0+coloun,2)
    def set_display_mode1(self):
        if self.Mode=="4-b": 
           self.Rs.value(0)   
           self.D7.value(0)
           self.D6.value(0)
           self.D5.value(1)
           self.D4.value(0)
           self.E1.value(1)
           self.E2.value(1)
           sleep(0.001)
           self.E1.value(0)
           self.E2.value(0)
        else:
           self.Rs.value(0)
           self.D7_3.value(0)
           self.D6_2.value(0)
           self.D5_1.value(1)
           self.D4_0.value(1)
           self.E1.value(1)
           self.E2.value(1)
           sleep(0.001)
           self.E1.value(0)
           self.E2.value(0) 
         
    def return_home(self):
        self.Col1=0
        self.Row1=1
        self.Col2=0
        self.Row2=1
        self.cmd(0x02)    
    def clear(self):
        self.Col1=0
        self.Row1=1
        self.Col2=0
        self.Row2=1
        self.cmd(0x01)
    def cursor_display_On(self):
        self.cmd(0x0F)
    def shif_cursor_right(self):
        self.cmd(0x14)
    def start(self):
        self.set_display_mode1()
        self.set_display_mode()
        self.clear()
        self.cursor_display_On()
        self.return_home()
    def write(self,text,s=1): 
        for i in text: 
            if self.Col1==self.size and self.Row1==1:
                self.Col1=0 
                self.Row1=2 
            elif self.Col1==self.size and self.Row1==2:
                self.Col1=0
                self.Row1=1
            elif self.Col2==self.size and self.Row2==1:
                self.Col2=0 
                self.Row2=2 
            elif self.Col2==self.size and self.Row2==2:
                self.Col2=0
                self.Row2=1
            if s==1:
                self.moveto(self.Row1,self.Col1)
                self.cmd(ord(i),1,True)
                self.Col1=self.Col1+1
            elif s==2:
                self.moveto(self.Row2,self.Col2)
                self.cmd(ord(i),2,True)
                self.Col2=self.Col2+1
    def cmd(self,cm,w=0,write=False):
        if write==True:
            self.Rs.value(1)
            
        else:
            self.Rs.value(0)
       
        c="{0:b}".format(cm)
        while len(c)<8:
            c="0"+c
        self.D7.value(int(c[0]))
        self.D6.value(int(c[1]))
        self.D5.value(int(c[2]))
        self.D4.value(int(c[3]))
        if self.Mode=="4-b":
            if w==0:
                self.E1.value(1)
                self.E2.value(1)
                sleep(0.001)
                self.E1.value(0)
                self.E2.value(0)
            elif w==1:
                self.E1.value(1)
                sleep(0.001)
                self.E1.value(0)
            elif w==2:
                self.E2.value(1)
                sleep(0.001)
                self.E2.value(0)
        self.D3.value(int(c[4]))
        self.D2.value(int(c[5]))
        self.D1.value(int(c[6]))
        self.D0.value(int(c[7]))
        if w==0:
            self.E1.value(1)
            self.E2.value(1)
            sleep(0.001)
            self.E1.value(0)
            self.E2.value(0)
        elif w==1:
            self.E1.value(1)
            sleep(0.001)
            self.E1.value(0)
        elif w==2:
            self.E2.value(1)
            sleep(0.001)
            self.E2.value(0)

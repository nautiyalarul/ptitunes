from serial import Serial
import sys
sys.path.append("..")
from FingerPackets import *
import time

#TODO: random number of packet per event
#TODO: quick packets/noise

class BoardSerialSimulator:
    def __init__(self,portToSendTo):
        #create a new Serial object onto variable self.s
        self.setPort(portToSendTo)
        self.fp = FingerPacket()

    def setPort(self, portToSendTo):
        if not type(portToSendTo) in (str,int):
            raise TypeError, ("use str like /dev/something or integer (ie 7 for COM8 on windows)", )
        #if some port was already open, close it
        if hasattr(self, 's') and isinstance(s, Serial):
            self.s.close()
        #remove previous port and create a new one to the new port address
        self.s = Serial(portToSendTo) 
        
    def start(self):
        if not hasattr(self, 's'):
            raise Exception,("port unset, use setPort() first",)
        while self.s.isOpen():
            self.fp.fromFullRandom()
            newChar = self.fp.toChar()
            #self.s.write(newChar * 200)
            #self.fp.fromFieldValues(EVENTPRESSED, 1)
            #newChar = self.fp.toChar()
            print "sending===>", self.fp
            self.s.write(newChar*32)
            time.sleep(1)

a = BoardSerialSimulator(7)
print "starting"
a.start()
print "done"

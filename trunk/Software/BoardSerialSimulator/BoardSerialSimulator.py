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
        print "hop"
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
        print "BoardSerialSimulator: could connect object"
        
    def start(self):
        cpt = 0
        if not hasattr(self, 's'):
            raise Exception,("port unset, use setPort() first",)
        self.fp.fromFullRandom()
        while self.s.isOpen():
            cpt+=1
            if cpt > 10 and cpt < 15:
                print "BoardSimulator : drag mode"
                self.fp.fromFieldValues(EVENTPRESSED, randint(0, 7))
                newChar = self.fp.toChar()
                print "sending===>", self.fp
                self.s.write(newChar*32)
            elif cpt > 20:
                cpt=0
            else:
                self.fp.fromFullRandom()
                newChar = self.fp.toChar()
                print "sending===>", self.fp
                self.s.write(newChar*32)
            time.sleep(1)

if __name__ == "__main__":
    a = BoardSerialSimulator(7)
    print "starting"
    a.start()
    print "done"

import sys
sys.path.append("..")
from FingerPackets import *
import serial
import time

#tells the most present character in a string
def whatsMostFrequent(buf):
    found = {}
    maxi = 0
    wheremaxi = None
    for a in buf:
        if not found.has_key(a):
            found[a] = 1
        else:
            found[a] += 1
        if found[a] > maxi:
            maxi = found[a]
            wheremaxi = a
    return wheremaxi

#returns the elements common and not None in the s1 and s2 sets
#returns None if no such elements
def commonElements(s1, s2):
    i = s1.intersection(s2)
    #any(i) : if i is not full of None/False elements
    return i if len(i) > 0 and any(i) else None

""">>> a = set([3,4])
>>> b = set([4,5])
>>> a - b
set([3])
>>> b -a
set([5])"""
#returns the elements not in common and not None in the s1 and s2 sets in this order:
#[first element of s1 found not present in s2, first element of s2 found not present in s1]
#returns None if no such elements
def differentElements(s1, s2):
    try:
        differentInS1 = list(s1-s2)[0]
        differentInS2 = list(s2-s1)[0]
        #any(i) : if i is not full of None/False elements
        return [differentInS1, differentInS2] if len(i) > 0 and any(i) else None
    except:
        return None



class PacketsListener:
    def __init__(self, setupAndListenDirectly=True):
        self.s = None
        self.fp = FingerPacket()
        self.lastMostFrequent = '0'
        self.pressStarted = False
        self.pressedButtons = set([])
        self.dragStartBtns = None
        self.dragEndBtns = None
        self.dragPathBtns = []
        self.defaultActuatorClass = iTunesActuator
        self.currentActuatorObject = None
        self.setDefaultActuator()
        if setupAndListenDirectly:
            self.openConnection()
            
    def __del__(self):
        self.closeConnection()
        if self.currentActuatorObject:
            del self.currentActuatorObject #will call the object' destructor which is supposed to do disconnections
    
    #act is class
    def setActuator(self, act):
        self.currentActuator = act()
    
    def setDefaultActuator(self):
        self.currentActuatorObject = self.defaultActuatorClass()
    
    def openConnection(self):
        try:
            #open COM 7
            print "opening serial port COM7"
            self.s = serial.Serial(6) 
            print "success opening port"
        except:
            print "couldn't open serial port COM7"
            return False
        return True
    
    def closeConnection(self):
        if self.s != None:
            self.s.close()
        return True
    
    #returns True if path is clockwise False otherwise
    def pathIsClockwise(self, dragPath):
        #dragPath is not a set and is unsorted...
        last = dragPath[0]
        nbInc = 0
        for now in dragPath[1:]:
            nbInc += 1 if now > last else -1 if now < last else 0
        return nbInc >= 0 #say True if clockwise (more increases than decreases)

    #call this function with a timer or in between sleeps
    def listenOnce(self):
        #read by blocks of 32 bytes
        try:
            buf = self.s.read(32)
        except:
            return False
        mostFrequent = whatsMostFrequent(buf)
        #ON PACKET EXACT DATA CHANGE
        if mostFrequent != self.lastMostFrequent:
            self.fp.fromChar(mostFrequent)
            et = self.fp.easyRead["eventType"]
            #ON PRESS
            if et == EVENTPRESSED:
                    self.pressedButtons.clear()
                    for a in ("1", "2"): self.pressedButtons.add(self.fp.easyRead["fingerID"+a])
                    #START RECORDING PRESSES POSITIONS IF NOT STARTED
                    if not self.pressStarted:
                        self.pressStarted = True
                        self.dragStartBtns = self.pressedButtons
                        self.emitHighLevelEvent("press_start",self.pressedButtons)
                    #add the pressed button to the dragPath
                    self.dragPathBtns.append(self.pressedButtons)
            #on NOTHING/UNDEFINED (no more PRESS)
            else:
                print "OTHER EVENT"
                #if we had started noting press & there's no press anymore
                #STOP RECORDING AND ANALYZE STUFF TO LOOK FOR 1. DRAGGING 2. RELEASE
                if self.pressStarted:
                    self.pressStarted = False
                    self.dragEndBtns = self.dragPathBtns[len(self.dragPathBtns)-1]
                    #if we did not end our dragging where we started <=> if this is a real dragging
                    #(assuming that the user does not move fingers  back&forth nor  does full revolutions)
                    de = differentElements(self.dragStartBtns, self.dragEndBtns)
                    #if drag and start buttons are the same
                    if not de:
                            self.emitHighLevelEvent("release", self.dragEndBtns)
                    #IF DRAG HAS DIFFERENT START AND END BUTTONS=> DRAG EVENT
                    else :
                        #if less than 2 buttons recorded while dragging => error/skip
                        if len(self.dragPathBtns) < 2:
                            print "There must be a problem... this is a real drag and there's less than 2 buttons recorded in path."
                        else:
                            CW = self.pathIsClockwise(self.dragPathBtns)
                            self.emitHighLevelEvent("drag", (CW, self.dragPathBtns))
                            #reset dragging
                    self.dragPathBtns = []
                    self.dragEndBtns.clear()
                    self.dragStartBtns.clear()
                    self.pressedButtons.clear()
        return True

    #highLevelEventStringID may be : "press_start" "drag" or "release"
    #"press_start" : data is a set([]) of at most button IDs
    #"release" : same kind as for "press_start"
    #"drag" : [startButtonId,None or MiddleButtonId, endButtonId]
    def emitHighLevelEvent(self, evtStr,data):
        print "highlevelevent:", evtStr, "data:", data
        if evtStr == "press_start":
            print "press_start", data
            for a in data:
                setButtonState(a, True)
        elif evtStr == "drag":
            for pos, a in enumerate(data[1]):
                setButtonState(a, True, 1+pos*0.1)
        if self.currentActuatorObject:
            #pass message to select actuator
            print "ACTION", self.currentActuatorObject.act(evtStr, data)
        else:
            print "self.currentActuatorObject is None !"

class Actuator:
    def __init__(self):
        #init something here... like start iTunes
        pass
    
    def __del__(self):
        #close something here before being deleted
        pass
    
    def connect(self):
        #import comm module etc etc...
        pass

    #returns ("Event Type", "Details (ie buttons pressed)", "Action name done") with each field depending on the event
    def act(self, evtStr, data):
        pass

class iTunesActuator(Actuator):
    def __init__(self):
        #init something here... like start iTunes
        self.connect() #will set up self.iTunes
        self.lastWasPlay = False
        self.lastVolume = None
    
    def __del__(self):
        #close something here
        del self.iTunes #probably inefficient anyway...
        pass
    
    def connect(self):
        import win32com.client
        try:
            self.iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
            print "connected to iTunes"
            #TODO emit signal iTunes active
            return True
        except:
            #TODO emit signal iTunes not active
            self.iTunes = None
            print "not connected to iTunes"
            return False
        
    #returns ("Event Type", "Details (ie buttons pressed)", "Action name done")
    def act(self, evtStr, data):
        if self.iTunes == None:
            print "SerialParser, iTunesActuator: iTunes was not plugged yet last time, I'll call connect() for your first"
            #if did not manage to connect to iTunes
            if not self.connect():
                return ("Warning", "iTunes is unreachable",  "None")
            #else we continue the program now
        if evtStr == "release":
            #if double press of buttons 0 and 3 (LEFT & RIGHT) => MUTE/UNMUTE
            if set([0, 3]) == data:
                if self.iTunes.SoundVolume == 0:
                    if self.lastVolume == None:
                        self.iTunes.SoundVolume = 100
                    else:
                        self.iTunes.SoundVolume = self.lastVolume
                else:
                    self.iTunes.SoundVolume = 0
                #store last volume for next time
                self.lastVolume = self.iTunes.SoundVolume
                return ("DoubleRelease", "Button 0 & 3","iTunes mute" if self.lastVolume == 0 else "iTunes unmute" )
                    
            #if press of CENTER button : PLAY/PAUSE
            elif 7 in data:
                if self.lastWasPlay:
                    self.iTunes.Play()
                else:
                    self.iTunes.Pause()
                self.lastWasPlay = not(self.lastWasPlay)
                return ("Release", "Button 7", "iTunes Play" if self.lastWasPlay else "iTunes Pause")
            #if LEFT button => PREV TRACK
            elif 0 in data:
                self.iTunes.PreviousTrack()
                return ("Release", "Button 0", "iTunes Previous track")
            #if LEFT button => PREV TRACK
            elif 3 in data:
                self.iTunes.NextTrack()
                return ("Release", "Button 0", "iTunes Next track")
        #if DRAG => VOLUME UP/DOWN of a certain amount depending on drag path length & clockwise-ness
        elif evtStr == "drag":
            volumeStep = int(len(data[1])/2.0*25)
            self.iTunes.SoundVolume += volumeStep if data[0] else -volumeStep #data[0] is clockwise bool
            return ("Drag", "Button %d => %d" % (data[1][0], data[1][len(data[1])-1]), "iTunes Volume "+ "up" if volumeStep >0 else "down" )
            

def setButtonState(buttonId, enable, forNsecondsOnly=0):
    #TODO in QT buttons[buttonId].setPressed(enable)
    if forNsecondsOnly:
        #put a timer once
        pass



if __name__ == "__main__":
    pl = PacketsListener()
    while 1:
        pl.listenOnce()

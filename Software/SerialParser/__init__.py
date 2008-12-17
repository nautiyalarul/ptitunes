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
    differentInS1 = (s1-s2)[0]
    differentInS2 = (s2-s1)[0]
    #any(i) : if i is not full of None/False elements
    return [differentInS1, differentInS2] if len(i) > 0 and any(i) else None



class PacketsListener:
    def __init__(self, setupAndListenDirectly=True):
        self.s = None
        self.fp = FingerPacket()
        self.lastMostFrequent = '0'
        self.pressStarted = False
        self.pressedButtons = set([])
        self.dragStartBtns = None
        self.dragEndBtns = None
        self.dragPath = []
        self.defaultActuator = iTunesActuator
        self.currentActuator = self.defaultActuator
        if setupAndListenDirectly:
            self.openConnection()
            
    def __del__(self):
        self.closeConnection()
    
    def setActuator(self, act):
        self.currentActuator = act
    
    def setDefaultActuator(self, act):
        self.currentActuator = defaultActuator
    
    def openConnection(self):
        try:
            #open COM 7
            self.s = serial.Serial(6) 
        except:
            return False
        return True
    
    def closeConnection(self):
        if self.s != None:
            self.s.close()
        return True

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
                        emitHighLevelEvent("press_start",self.pressedButtons)
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
                            emitHighLevelEvent("release", self.dragEndBtns)
                    #IF DRAG HAS DIFFERENT START AND END BUTTONS=> DRAG EVENT
                    else :
                        l = len(self.dragPathBtns)
                        #if less than 2 buttons recorded while dragging => error/skip
                        if l < 2:
                            print "There must be a problem... this is a real drag and there's less than 2 buttons recorded in path."
                        #if 2 btns recording while dragging, startButton + 1 middleButton+endButton
                        if l == 2:
                            cpy = [de[0],  None,  de[1]]
                            emitHighLevelEvent("drag", cpy)
                            del cpy
                        #if there are 3 or more buttons in path, find the closest button (closestElem) which is not
                        #start or middle button and is closest to middle
                        elif l >= 3: 
                            
                            dragPathElementsNotInStartAndEnd = set(self.dragPathBtns) - de
                            minDist = 500
                            middleIndex = len(self.dragPathBtns)/2
                            closestElem = None
                            for pos, el in enumerate(self.dragPathBtns):
                                if el in dragPathElementsNotInStartAndEnd:
                                    d= abs(pos-middleIndex)
                                    if d<minDist:
                                        minDist = d
                                        closestElem = el
                            if closestElem == None:
                                print "man learn to code... putting None for middle drag button anyway..."
                                closestElem = None
                            cpy = [de[0], closestElem, de[1]]
                            #3 btn for a path is enough info to send for high level analysis (CCW ? CW...)
                            emitHighLevelEvent("drag", cpy)
                            del cpy
                                    
                    #whether drag start != drag end or not...
                    #we have finished dragging and whether we noted useful or not
                    #we clear the data for a next dragging
                        #clear dragging things for next dragging happening
                        self.dragStartBtns.clear()
                        self.dragEndBtns.clear()
                    #clear dragging & button press/release things for next dragging happening
                    self.pressedButtons.clear()
                    self.pressStarted = False
                    self.dragPathBtns = []
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
        elif evStr == "drag":
            for a in data:
                setButtonState(a, True, 1)
        
        #pass message to select actuator


class Actuator:
    def __init__(self):
        #init something here... like start iTunes
        pass
    
    def __del__(self):
        #close something here
        pass
        
    #returns ("Event Type", "Details (ie buttons pressed)", "Action name done")
    def act(self, evStr, data):
        if evStr == "release":
            

def setButtonState(buttonId, enable, forNsecondsOnly=0):
    buttons[buttonId].setPressed(enable)
    if forNseconds:
        #put a timer once
        pass



if __name__ == "__main__":
    pl = PacketsListener()
    pl.

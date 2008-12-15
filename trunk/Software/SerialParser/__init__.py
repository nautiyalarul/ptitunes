import sys
sys.path.append("..")
from FingerPackets import *
import serial
import time

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

def listen():
    #open COM 7
    s = serial.Serial(6) 
    fp = FingerPacket()
    lastMostFrequent = '0'
    pressStarted = False
    dragStartBtnID = -1
    dragEndBtnID = -1
    dragPath = []
    while 1:
        #read by blocks of 32 bytes
        buf = s.read(32)
        mostFrequent = whatsMostFrequent(buf)
        #if event change from last read to current read
        if mostFrequent != lastMostFrequent:
            fp.fromChar(mostFrequent)
            et = fp.easyRead["eventType"]
            if et == EVENTPRESSED:
                    pressedBtnID = fp.easyRead["fingerID1"]
                    if not pressStarted:
                        pressStarted = True
                        dragStartBtnID = pressedBtnID
                    #if 1 button is pressed, ok we take it
                    #& let's assume that if 2 buttons are pressed, they are very close to gether
                    #note the dragging path along in a list
                    else:
                        dragPath.append(pressedBtnID)
            else:
                #if we had started noting press & there's no press anymore
                if pressStarted:
                    pressStarted = False
                    dragEndBtnID = fp.easyRead["fingerID2"]
                    #if we did not end our dragging where we started <=> if this is a real dragging
                    #(assuming that the user does not move fingers  back&forth nor  does full revolutions)
                    if dragEndBtnID != dragStartBtnID:
                        l = len(dragPath)
                        if l < 2:
                            print "There must be a problem... this is a real drag and there's less than 2 buttons recorded in path."
                        #if startButton + 1 middleButton+endButton
                        else if l == 3: 
                            
                            #we make a copy of the dragPath because we know list simple copy is just reference copy
                            cpy = [i for i in dragPath]
                            #3 btn for a path is enough info to send for high level analysis (CCW ? CW...)
                            emitHighLevelEvent("drag", cpy)
                            del cpy
                        #if we have more than 3 events
                        else:
                            #we look for a button closest to the middle that is not the start or end buttons
                            middleID = len(dragPath)/2 #integer division == lower
                            m = dragPath[middleID]
                            #if the middle button in the drag list is different from start and end
                            #we take it and search futher
                            if m != dragStartBtnID and m!= dragEndBtnID:
                                cpy = [dragStartBtnID, m, dragEndBtnID]
                                emitHighLevelEvent("drag", cpy)
                                del cpy
                            #if the middle button is not different from end and start
                            #we browse the whole list
                            else:
                                foundMiddle = None
                                posMiddle = dragStartBtnID
                                lastClosestDistance = 30
                                for m in dragPath:
                                    if m != dragStartBtnID and m != dragEndBtnID:
                                        foundMiddle = m
                                        if abs(posMiddle-middleID) < 30:
                                            #TODO
                            #right search
                            for a in dragPath[middleID:]:
                                if 
                            
                            
                    dragStartBtnID = -1
                    dragEndBtnID = -1
                    pressStarted = False
                    dragPath = []
            mapActionToEvent(fp)
            print fp
        time.sleep(1)

def emitHighLevelEvent():

def mapActionToEvent(finishedEventChar):
    et = finishedEventChar.easyRead["eventType"]
    bt1 = et.easyRead["buttonID1"]
    bt2 = et.easyRead["buttonID2"]
    #if pressed
    if et == EVENTPRESSED:
        #if single release (two same buttons <=> single button pressed)
        if bt1 == bt2:
            onRelease(bt1)
        #if double release (or more.. but only the board tells only about the first two buttons)
        else:
            onDouble(bt1, bt2)
        
listen()

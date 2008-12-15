import sys
sys.path.append("..")
from binaryOperations import value2binstr
from random import randint

# ---- POSSIBLE EVENT TYPES for makeFingerEventPacket's eventType parameter----
EVENTNOP = 0
EVENTPRESSED = 1
#2 is used here, but makeFingerEventPacket generates a random number between 2 and 3 for that.
EVENTUNDEFINED = 2

#for info, EVENT*** constants are used to be passed as parameters to this file's python functions, but they have the same values in packets as well (except for EVENTUNDEFINED which may be either of 2 or 3), though in binary form on 2 bits only.

"""create an instance of this class passing it a character, or an eventType in EVENTNOP,EVENTPRESSED, a fingerID2 and/or 1. It stores an internal representation of a read character.
- if EVENTNOP, fingerID2 and fingerID1 can be omitted
- if EVENTPRESSED, at least one out of fingerID1, fingerID2 has to have a value in [1,8]
if only 1 fingerID in the two is given, the final packet will have twice the same IDs (that follows our specification).
if 2 fingerIDs are given, unless keyword parameters are used, the parameter order is still interpreted as in the function definition: fingerID2, fingerID1"""
class FingerPacket(object):
    def __init__(self, eventType=None, fingerID2=-1, fingerID1=-1, fromString=""):
        self._eventType = self._fingerID2 = self.fingerID1 = None
        self.easyRead = {"eventType":0, "fingerID2":0, "fingerID1":0}
        if fromString != "":
            if len(fromString) > 1:
                self.fromBinaryString(fromString)
            else:
                self.fromChar(fromString)
        else:
            if eventType== None:
                self.fromFieldValues(0, 0, 0)
                print "warning: nothing passed, putting all 3 fields to 0"
            else:
                self.fromFieldValues(eventType, fingerID2, fingerID1)
    
    def _updateEasyRead(self):
        self.easyRead["eventType"] = self._eventTypeBinaryStringToConstant(self._eventType)
        self.easyRead["fingerID2"] = int(self._fingerID2,2)
        self.easyRead["fingerID1"] = int(self._fingerID1,2)
    
    def fromChar(self, someChar):
        if len(someChar) != 1:
            raise ValueError,("this function needs a 1 character long string to work. Given: "+someChar, )
        
        #print "before: %s (string) %c (char) %d (ord)" % (someChar, someChar, ord(someChar))
        binstr = value2binstr(ord(someChar), 8)
        after = int(binstr, 2)
        #print "after: %s (binstring) %d (binstring to int) %c (chr of int)" % (binstr, after, chr(after))
        self.fromBinaryString(binstr)
    
    def fromBinaryString(self, aBinaryStringRepresentation):
        exitWithError = False
        #if parameter is not an 8-characters string made of 1s and 0s, exit with error
        if not type(aBinaryStringRepresentation) == str or len(aBinaryStringRepresentation) != 8:
            exitWithError = True
        else:
            try:
                i = int(aBinaryStringRepresentation, 2)
            except:
                #if not a string
                exitWithError = True
            #if not a string or not 8 characters long
        if exitWithError:    
            raise ValueError, ("given parameter is empty or not an 8 bits (with only 1s and 0s) string: "+ str(aBinaryStringRepresentation)+".",)
        
        self._eventType,  self._fingerID2,  self._fingerID1 = aBinaryStringRepresentation[0:2],  aBinaryStringRepresentation[2:5], aBinaryStringRepresentation[5:8]
        self._updateEasyRead()
        
        """print "FROM STRING________________below______"
        print "binaryRepealsentation : ", aBinaryStringRepresentation
        print "self._eventType", self._eventType, type(self._eventType)
        print "self._fingerID2", self._fingerID2, type(self._fingerID2)
        print "self._fingerID1", self._fingerID1, type(self._fingerID1)"""
    
    def fromUndefinedRandom(self):
        self._eventType= value2binstr(randint(2, 3), 2)
        self._fingerID1 = value2binstr(randint(0, 7), 3)
        self._fingerID2 = value2binstr(randint(0, 7), 3)
        self._updateEasyRead()
    
    def fromFullRandom(self):
        self._eventType= value2binstr(randint(0, 3), 2) #this line changes from fromUndefinedRandom
        self._fingerID1 = value2binstr(randint(0, 7), 3)
        self._fingerID2 = value2binstr(randint(0, 7), 3)
        self._updateEasyRead()
        
    def fromFieldValues(self,eventType, fingerID2=-1, fingerID1=-1):
        #---- PARAMETER CHECKING AND ADAPTATION ----
        #if uncorrect eventType value, exit with error
        if not eventType in (EVENTNOP, EVENTPRESSED, EVENTUNDEFINED, 3):
            raise ValueError, ("eventType should be one of EVENTNOP,EVENTPRESSED,EVENTUNDEFINED, given: "+str(eventType), )
            
        if eventType in (EVENTUNDEFINED, 3):
            header = value2binstr(eventType, 2)
            fingerID1 = 0 if not self._rightEventTypeRange(fingerID1) else fingerID1
            fingerID2 = 0 if not self._rightEventTypeRange(fingerID2) else fingerID2
        
        elif eventType == EVENTNOP:
            header = "00"
            fingerID1 = fingerID2 = 0
    
        #if required to generate a button pressed packet
        elif eventType == EVENTPRESSED:
            header = "01"
            given1 = False if fingerID1 == -1 else True
            given2 = False if fingerID2 == -1 else True
            #if no event types given, exit with error
            if not given1 and not given2:
                raise SyntaxError, ("for EVENTPRESSED events, function takes at least one parameter between 1 and 8; 0 given or value is -1.", )
            
            rightRange1 = True if self._rightEventTypeRange(fingerID1) else False
            rightRange2 = True if self._rightEventTypeRange(fingerID2) else False
            #if at least one of the provided finger IDs has a correct value, exit with error
            if (not rightRange1 and given1) or (not rightRange2 and given2):
                raise ValueError, ("for EVENTPRESSED events, provided fingerID values must be between 1 and 8. Values given: fingerID2: "+str(fingerID2)+", fingerID1: "+str(fingerID1)+".", )
            
            #if only one correct fingerID is given, copy its value into the other fingerID variable
            if rightRange2 and not rightRange1:
                fingerID1 = fingerID2
            elif rightRange1 and not rightRange2:
                fingerID2 = fingerID1
            #else if both values are correct, we keep them as is
                
        #--- FINAL CHARACTER'S FIELDS PACKING ---
        #header is ok (set at the beginning of each of the above if statements)
        self._fingerID1 = value2binstr(fingerID1, 3)
        #print "before assignement:", fingerID1, "after:", self._fingerID1
        self._fingerID2 = value2binstr(fingerID2, 3)
        #print "before assignement:", fingerID2, "after:", self._fingerID2
        self._eventType = value2binstr(eventType, 2) if eventType != EVENTUNDEFINED else value2binstr(randint(2, 3), 2)
        #print "before assignement:", eventType, "after:", self._eventType
        self._updateEasyRead()
    
    def _eventTypeConstantToString(self, eventTypeAsConstant):
        return "EVENTNOP" if (eventTypeAsConstant == EVENTNOP or eventTypeAsConstant == 3) else "EVENTPRESSED" if eventTypeAsConstant == EVENTPRESSED else "EVENTUNDEFINED"
    
    def _eventTypeBinaryStringToConstant(self, eventTypeAsBinaryString):
        a = int(eventTypeAsBinaryString, 2)
        if a == 3: a=2 #move EVENTUNDEFINED 's 3 to the usual 2
        return a
    
    def __repr__(self):
        b = self.toBinaryString()
        c = self.toChar()
        et = int(self._eventType, 2)
        eventString = _eventTypeToString(et)
        return "FingerPacket: binary:%s character:'%s', eventType=%s, fingerID2=%d, fingerID1=%d" % (b,c, eventString, int(self._fingerID2, 2), int(self._fingerID1, 2))
        #2 param after % : c if eventString != "EVENTNOP" else '0'

    def toBinaryString(self):
        return self._eventType+self._fingerID2+self._fingerID1

    def toChar(self):
        """"if self._eventType == EVENTNOP:
            return '0'
        else:"""
        """print "toChar() will send:", self._eventType+self._fingerID2+self._fingerID1
        print "self._eventType", self._eventType, type(self._eventType)
        print "self._fingerID2", self._fingerID2, type(self._fingerID2)
        print "self._fingerID1", self._fingerID1, type(self._fingerID1)"""
        return chr(int(self._eventType+self._fingerID2+self._fingerID1, 2))
    
    def toInt(self):
        return int(self._eventType+self._fingerID2+self._fingerID1, 2)

    def _rightEventTypeRange(self, val):
        return val >= 0 and val <= 7

""""fp = FingerPacket(EVENTNOP)
print fp
fp.fromFieldValues(EVENTNOP, 3)
print fp
fp.fromFieldValues(EVENTPRESSED, 1, 4)
print fp
fp.fromFieldValues(EVENTPRESSED, 3,  7)
print fp"""

fp = FingerPacket()
fp.fromChar('a')
print "fp's toChar gives", fp.toChar()
print fp.easyRead
ap = FingerPacket(EVENTPRESSED, 4, 5)
ap.fromChar(fp.toChar())
print ap.easyRead

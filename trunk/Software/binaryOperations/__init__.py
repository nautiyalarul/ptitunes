import sys
sys.path.append("..")

#this is python2.6+ only, because we're lazy using the builtin bin() function
"converts 'someInteger' into string representing its binary writing with no 'b' unlike python2.6+'s builtin bin(), and at a length of 'length' by adding/removind heading zeros if necessary. If the request 'length' would change the actual number value (ie it would remove heading ones), exits with (raises) a ValueError."
def value2binstr(someInteger, length=0):
    r= bin(someInteger).replace('b', '').zfill(length)
    #if some length is given, and its smaller than the writing length, try removing heading zeros
    #and exit with error if failed because there were too few heading zeros to do that
    if length and length < len(r):
        r2 = r
        nbToRemove = len(r2)-length
        nbRemoved = 0
        while r2[0] == '0':
            r2 = r2[1:]
            nbRemoved += 1
        if nbRemoved < nbToRemove:
            raise ValueError, ("can't put %d which binary is %s at a length of %d because there are only %d heading zeros" % (someInteger, length, nbToRemove), )
        else:
            r = r2
    #if asked to have a bigger length than the default binary representation, add the right number of heading zeros
    elif length > len(r):
        r = '0'*(length-len(r))+r
    return r

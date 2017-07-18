#!/usr/bin/env python
# -*- coding: utf8-*-
'''
Created on 07/07/2017

@author: Antoine de Chassey
'''

from models.sigfox import Sigfox
import win32event, win32api, winerror
import time

# Disallowing Multiple Instance
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print "Multiple instances not allowed"
    exit(0)


# Get idle time
def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


if __name__ == "__main__":
    while(1):
        idleTime = getIdleTime()
        
        sigfox = Sigfox()
        sigfox.connect()
            
        # Check if idle time is smaller than 10 minutes
        if(idleTime <= 60 * 10):
            
        #     sigfox.testDevice()
        #     sigfox.getDeviceID()
        #     sigfox.getDevicePAC()
        #     sigfox.setPower("EU")
        #     sigfox.setTxFreq("868130000")
        #     sigfox.openLibrary("EU")
         
            # Someone is here, sending a message with the idle time in minutes
#             win32api.MessageBox(0, "Get back to WORK!", "Oh no...")

            if(idleTime >= 60 * 8):
                sigfox.sendPayload("25")
            elif(idleTime >= 60 * 4):
                sigfox.sendPayload("50")
            else:
                sigfox.sendPayload("100")
        
        else:
            sigfox.sendPayload("0")
        
        sigfox.disconnect()
        # Loop every 10 minutes
        time.sleep(60 * 10)

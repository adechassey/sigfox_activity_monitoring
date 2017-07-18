#!/usr/bin/env python
# -*- coding: utf8-*-
'''
Created on 29/06/2017

@author: Antoine de Chassey
'''

import serial, binascii, sys

'''
Sigfox
'''
class Sigfox():
    
    def __init__(self):
        pass
       
    
    def connect(self):
        # port='/dev/ttyS0'
        try:
            self.ser = serial.Serial(port='COM18', baudrate=9600, timeout=None, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
            if self.ser.isOpen():
                print(self.ser.name + ' is open...')
            self._connected = True
            print("--------------------------------")
            print(self.ser.readline().rstrip('\r\n'))
        except:
            print("/!\ Please make sure the port is correct for Uplynx RCZ1 /!\ ")
            sys.exit()
        
    def disconnect(self):
        self.ser.close()
        self._connected = False
        
    
    '''
    MODULE AT COMMANDS
    '''
    def testDevice(self):        
        cmd = "AT$V?\r"
        self.ser.write(cmd.encode())
        print("--------------------------------")
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        
        cmd = "AT$OOB?\r\n"
        self.ser.write(cmd.encode())
        print("--------------------------------")
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        
        
    def getDeviceID(self):
        cmd = "\rAT$ID?\r\n"
        self.ser.write(cmd.encode())
        print("--------------------------------")
        print(self.ser.readline())
        self._deviceID = str(self.ser.readline().decode("ASCII")[0:8])
        print("Device ID: " + self._deviceID)
        print(self.ser.readline().rstrip('\r\n'))
        
        
    def getDevicePAC(self):
        cmd = "\rAT$PAC?\r\n"
        self.ser.write(cmd.encode())
        print("--------------------------------")
        print(self.ser.readline().rstrip('\r\n'))
        self._devicePAC = str(self.ser.readline().decode("ASCII")[0:16])
        print("Device PAC: " + self._devicePAC)
        print(self.ser.readline().rstrip('\r\n'))
    
    
    def setTxFreq(self, freq):
        cmd = "\rAT$IF=" + freq + "\r\n"
        self.ser.write(cmd.encode())
        print("--------------------------------")
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))

        
    def getTxFreq(self):
        cmd = "\rAT$IF?\r\n"
        self.ser.write(cmd.encode())
        print("--------------------------------")
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        
        
    def setPower(self, region):
        if(region == "EU"):
            cmd = "\rAT$302=14\r\n"
            self.ser.write(cmd.encode())
            print("--------------------------------")
            print(self.ser.readline().rstrip('\r\n'))
            print(self.ser.readline().rstrip('\r\n'))
            print(self.ser.readline().rstrip('\r\n'))
        elif(region == "US"):
            cmd = "\rAT$302=22\r\n"
            self.ser.write(cmd.encode())
            print("--------------------------------")
            print(self.ser.readline().rstrip('\r\n'))
            print(self.ser.readline().rstrip('\r\n'))
            print(self.ser.readline().rstrip('\r\n'))
        else:
            print("Invalid region (must be EU or US)")
    
    
    def getStandard(self):
        cmd = "\rAT$STD?\r\n"
        self.ser.write(cmd.encode())
        print("--------------------------------")
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
            
            
    def openLibrary(self, region):
        if(region == "EU"):
            cmd = "\rAT$O=0,1\r\n"
            self.ser.write(cmd.encode().rstrip('\r\n'))
            print("--------------------------------")
            print(self.ser.readline().rstrip('\r\n'))
            print(self.ser.readline().rstrip('\r\n'))
            print(self.ser.readline().rstrip('\r\n'))
        elif(region == "US"):
            cmd = "\rAT$O=1,1\r\n"
            self.ser.write(cmd.encode())
            print("--------------------------------")
            print(self.ser.readline().rstrip('\r\n'))
            print(self.ser.readline().rstrip('\r\n'))
            print(self.ser.readline().rstrip('\r\n'))
        else:
            print("Invalid region (must be EU or US)")
            
    
    def sendPayload(self, frame):
        bytesFrame = str.encode(frame)
        hexFrame = str(binascii.hexlify(bytesFrame)).encode('ASCII')
        
        cmd = "\rAT$SF=" + hexFrame + "\r\n"
        self.ser.write(cmd.encode())
        print("--------------------------------")
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
        print(self.ser.readline().rstrip('\r\n'))
                        
    
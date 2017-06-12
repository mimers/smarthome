import os
import re
import sys
import time
import binascii
from bluepy import btle

class ScanDelegate(btle.DefaultDelegate):
    def __init__(self, opts):
        btle.DefaultDelegate.__init__(self)
        self.opts = opts

    def handleNotification(self, handle, data):
        print data
    
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if not isNewDev:
            return
        name = ""
        for (sdid, desc, val) in dev.getScanData():
            if sdid == 9:
                name = val
            elif sdid  == 8 and name == "":
                name = val
        if name == "" or re.match("LED-LIGHT-.+", name) == None:
            print("Not valid name for dev: ", dev.addr)
            return
        print ("connecting to dev: ", name)
        con = btle.Peripheral(dev).withDelegate(self)
        try:
            chars = con.getCharacteristics()
            lastReadableChar = None
            for char in chars:
                if char.supportsRead():
                    lastReadableChar = char
            if lastReadableChar != None:
                while True:
                    con.waitForNotifications(12)
        finally:
            con.disconnect()


def main() :
    scanner = btle.Scanner(0).withDelegate(ScanDelegate({}))
    devices = scanner.scan(3)

        

if __name__ == "__main__":
    main()

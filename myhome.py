#!/usr/bin/python

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
from pymongo import MongoClient
from bluepy import btle
import json


LIGHT_PIN = 21
SHORT_DATA_TAG = 8
COMPLETE_DATA_TAG = 9

print "setup gpio..."
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.output(LIGHT_PIN, 1)

print "prepare mongodb..."
db = MongoClient("localhost:3550")["smart-home"]
deviceStatus = {}

class DeviceConnection():
  """Helper to communicate with ble devices"""
  def __init__(self, addr):
    self.addr = addr
    self.con = btle.Peripheral(addr).withDelegate(self)
    self.characterristic = self.con.getCharacteristics()[-1]
    self.writeValue('Q')

  def handleNotification(self, handle, data):
      print "Got notify @ ", self.addr, " data = (", data, ")"
      self.data = data
      self.online = True

  def getValue(self):
    return self.characterristic.read()

  def writeValue(self, val):
    ret = self.characterristic.write(val)
    self.con.waitForNotifications(3)
    return ret

def connectDevice(addr):
  try:
    deviceStatus[addr] = DeviceConnection(addr)
    print "connect to ", addr, " succeed."
    return True
  except Exception as e:
    print "connect to ", addr, " failed."
    return False

def getValidName(scanEntry):
  if scanEntry is None:
    return ""
  name = ""
  for (sdid, desc, val) in dev.getScanData():
      if sdid == COMPLETE_DATA_TAG:
          name = val
      elif sdid  == SHORT_DATA_TAG and name == "":
          name = val
  return name


print "prepare btle..."
for d in db.devices.find():
  connectDevice(d['addr'])

app = Flask(__name__, static_url_path='')

@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/lights')
def get_all_lights():
  return json.dumps(deviceStatus)

@app.route('/connect/<addr>')
def connect_to(addr):
  return connectDevice(addr)

@app.route('/add/<addr>/<name>')
def addDevice(addr, name):
  db.devices.insert({'addr': addr, 'name': name})
  if connectDevice(addr):
    return json.dumps(deviceStatus[addr])
  else
    return json.dumps({'msg': 'failed to connect ' + addr, 'code': -1})


@app.route('/scan')
def scan_blte():
  scanner = btle.Scanner()
  devices = scanner.scan(5)
  newDevices = []
  devAddrList = deviceStatus.keys()
  for entry in devices:
    if not entry.addr in devAddrList:
      # new device detected!
      newDevices.append({'addr': entry.addr, 'name': getValidName(entry)})
  return json.dumps(newDevices)

@app.route('/light/state/<op>/<val>')
def light_state(op=None, val="0"):
  if op == 'get':
    return str(1 if 0 is GPIO.input(LIGHT_PIN) else 0)
  elif op == 'set':
    GPIO.output(LIGHT_PIN, 1 if 0 is int(val) else 0)
    return ''
  else:
    print 'unkown operation.'
    return ''

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=3568)

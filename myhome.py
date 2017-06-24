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

class DeviceConnection(dict):
  """Helper to communicate with ble devices"""
  def __init__(self, addr, name):
    dict.__init__(self, addr=addr, name=name)
    self.addr = addr
    self.con = btle.Peripheral(addr).withDelegate(self)
    self.characteristic = self.con.getCharacteristics()[-1]
    print "connected ", name, " using handle ", self.characteristic.getHandle()
    self.getValue()

  def handleNotification(self, handle, data):
      print "Got notify @ ", self.addr, " data = (", data, ")"
      self.data = data
      self.online = True
      self['value'] = data
      self['online'] = self.online

  def getValue(self):
    self.writeValue('Q$')
    return self.data

  def writeValue(self, val):
    ret = self.characteristic.write(val)
    self.con.waitForNotifications(3)
    return ret

def connectDevice(addr, name=""):
  try:
    deviceStatus[addr] = DeviceConnection(addr, name)
    print "connect to ", addr, " succeed."
    return True
  except Exception as e:
    print "connect to ", addr, " failed. ", e
    return False

def getValidName(scanEntry):
  if scanEntry is None:
    return ""
  name = ""
  for (sdid, desc, val) in scanEntry.getScanData():
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
  return json.dumps(deviceStatus.values())

@app.route('/connect/<addr>')
def connect_to(addr):
  return json.dumps(connectDevice(addr))

@app.route('/add/<addr>/<name>')
def addDevice(addr, name):
  db.devices.insert({'addr': addr, 'name': name})
  if connectDevice(addr):
    return json.dumps(deviceStatus[addr])
  else:
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

@app.route('/light/<op>/<addr>')
def ble_op(op, addr):
  try:
      con = deviceStatus[addr]
      print op, " @ ", addr
      if op == 'set':
        val = request.args.get('val', None)
        if val is None:
            return "false"
        con.writeValue(val)
        return json.dumps(con.getValue())
      elif op == 'get':
        return json.dumps(con.getValue())
      else:
        return 'invalid params'
  except Exception as e:
      print e
      return 'failed'



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
  print "start server..."
  app.run(debug=True, use_reloader=False, host='0.0.0.0', port=3568)

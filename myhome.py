#!/usr/bin/python

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
from pymongo import MongoClient


LIGHT_PIN = 21
print "setup gpio..."
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.output(LIGHT_PIN, 1)

print "prepare mongodb..."
db = MongoClient("localhost:3550")["smart-home"]


app = Flask(__name__, static_url_path='')

@app.route('/')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('index.html', name=name)

@app.route('/lights')
def get_all_lights():
    return


@app.route('/light/state/<op>')
def light_state(op=None):
  if op == 'get':
    return str(1 if 0 is GPIO.input(LIGHT_PIN) else 0)
  elif op == 'set':
    GPIO.output(LIGHT_PIN, 1 if 0 is int(request.args.get('on', 0)) else 0)
    return ''
  else:
    print 'unkown operation.'
    return ''


    

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=3568)




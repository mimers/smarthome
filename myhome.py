#!/usr/bin/python

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO

LIGHT_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_PIN, GPIO.OUT)

app = Flask(__name__, static_url_path='')

@app.route('/')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('index.html', name=name)

@app.route('/light/state/<op>')
def light_state(op=None):
  if op == 'get':
    if GPIO.input(LIGHT_PIN) == 0:
      return 'false'
    else
      return 'true'
  elif op == 'set':
    GPIO.output(LIGHT_PIN, int(request.args.get('on', 0)))
    return ''
  else:
    print 'unkown operation.'
    return ''


    

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=3568)




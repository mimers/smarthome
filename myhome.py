from flask import Flask
from flask import render_template
import RPi.GPIO as GPIO

app = Flask(__name__, static_url_path='')

@app.route('/')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('index.html', name=name)

@app.route('/light/state/<name>')
def light_state(op=None)
  if op == 'get':
    return GPIO.input(21)

    

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=3568)



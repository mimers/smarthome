from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
  return 'hi, i am smart home from the future'

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(filename='favicon.ico')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3568)



from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path='')

@app.route('/')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('index.html', name=name)

@app.route('/static/favicon.ico')
def send_favicon():
  return app.send_static_file('static/favicon.ico')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=3568)



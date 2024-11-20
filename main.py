from flask import Flask, render_template # type: ignore
from data import items

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', items = items)

@app.route('/404')
def error():
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask, render_template
from data import items

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', items = items)

if __name__ == "__main__":
    app.run(debug=True)



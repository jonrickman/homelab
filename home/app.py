from flask import Flask

app = Flask(__name__)


if __name__ == "__main__":

    from src.urls import *

    app.run(debug=True, host='0.0.0.0')

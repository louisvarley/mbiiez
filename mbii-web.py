from flask import Flask
from mbiiez import settings


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=settings.web_service.port)

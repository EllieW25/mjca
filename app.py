#Starts flask
from flask import Flask
from config import Config

app = Flask(__name__)

app.config.from_object(Config)


@app.route('/')
def home():
    return """
    <h1>MJCA</h1>
    <p> If you see this flask is working! :D </p>
    """

if __name__ == '__main__':
    app.run(debug=True)
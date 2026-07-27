#Starts flask
from flask import Flask
from config import Config
from database import create_database

app = Flask(__name__)

app.config.from_object(Config)
create_database()

@app.route('/')
def home():
    return "The school messenger is running."
if __name__ == '__main__':
    app.run(debug=True)
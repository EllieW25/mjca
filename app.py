#Starts flask
from flask import Flask, render_template
from config import Config
from models import db, Recipient

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    teachers = Recipient.query.filter_by(
        recipient_type='Teacher',
    ).all()
    substitutes = Recipient.query.filter_by(
        recipient_type='Substitute',
    ).all()


    return render_template(
        'index.html',
         teachers=teachers,
         substitutes=substitutes
    )

if __name__ == '__main__':
    app.run(debug=True)
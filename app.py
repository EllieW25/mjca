#Starts flask
from flask import Flask, render_template, request, redirect
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
@app.route('/add', methods=['GET', 'POST'])
def add_recipient():
    if request.method == 'POST':
        recipient = Recipient(
            name=request.form['name'],
            phone=request.form['phone'],
            recipient_type=request.form['recipient_type'],
            department=request.form['department']
        )
        db.session.add(recipient)
        db.session.commit()

        return redirect('/')
    return render_template("add_recipient.html")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipient(id):

    recipient = Recipient.query.get_or_404(id)

    if request.method == 'POST':

        recipient.name = request.form['name']
        recipient.phone = request.form['phone']
        recipient.recipient_type = request.form['recipient_type']
        recipient.department = request.form['department']

        if "active" in request.form:
            recipient.active = True
        else:
            recipient.active = False

        db.session.commit()

        return redirect('/')

    return render_template(
        "edit_recipient.html",
        recipient=recipient
    )

if __name__ == '__main__':
    app.run(debug=True)
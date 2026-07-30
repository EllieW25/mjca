#Starts flask
from flask import Flask, render_template, request, redirect
from config import Config
from models import *
from sms import send_sms

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():

    teachers = Recipient.query.filter_by(
        recipient_type='Teacher',
        active=True
    ).all()
    substitutes = Recipient.query.filter_by(
        recipient_type='Substitute',
        active = True
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

@app.route("/send", methods=["POST"])
def send():

    recipient_ids = request.form.getlist('recipient_ids')
    message = request.form['message']

    print(recipient_ids)
    print(message)

    if not recipient_ids:
        print("No recipients selected.")
        return redirect('/')

    if not message.strip():
        print("No message entered.")
        return redirect('/')

    new_message = Message(
        body=message
    )
    db.session.add(new_message)
    db.session.commit()

    recipients = Recipient.query.filter(
        Recipient.id.in_(recipient_ids)
    ).all()

    for recipient in recipients:
       send_sms(
           recipient.phone,
           message
       )
       message_recipient = MessageRecipient(
            message_id=new_message.id,
            recipient_id=recipient.id
        )
       db.session.add(message_recipient)

    db.session.commit()

    return redirect('/')

@app.route("/history")
def history():
    messages = Message.query.order_by(
        Message.created_at.desc()
    ).all()
    return render_template(
        'history.html',
        messages=messages
    )
@app.route("/manage")
def manage():
    active_recipients = Recipient.query.filter_by(
        active=True
    ).all()
    inactive_recipients = Recipient.query.filter_by(
        active=False
    ).all()
    return render_template(
        "manage.html",
        active_recipients=active_recipients
        ,inactive_recipients=inactive_recipients
    )
@app.route("/sms-reply", methods=["POST"])
def sms_reply():

    print("==== Reply Recieved ====")

    phone = request.form['From']
    body = request.form['Body']

    print("Phone:",phone)
    print("all recipients:")
    for r in Recipient.query.all():
        print(f"{r.name} -> {r.phone}")
    print("body:",body)

    recipient = Recipient.query.filter_by(
        Recipient._phone == phone).first()
    print("recipient:",recipient)

    print(repr(phone))
    for r in Recipient.query.all():
        print(repr(r.phone))

    if not recipient:
        print("Recipient not found.")
        return "Unknown sender", 200
    message_recipient = MessageRecipient.query.filter_by(
        recipient_id=recipient.id
    ).order_by(
        MessageRecipient.id.desc()
    ).first()
    reply = Reply(
        message_id=message_recipient.message_id,
        recipient_id=recipient.id,
        body=body
    )
    db.session.add(reply)
    db.session.commit()
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
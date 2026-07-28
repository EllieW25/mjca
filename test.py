from app import app
from models import db, Recipient

with app.app_context():

    recipients = Recipient.query.all()

    for person in recipients:
        print(
            person.name,
            person.recipient_type,
            person.phone,
            person.active
        )
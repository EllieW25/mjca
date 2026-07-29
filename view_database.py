from app import app
from models import db, Recipient, Message, MessageRecipient

with app.app_context():

    print("\nRecipients")
    print("-" * 40)
    for recipient in Recipient.query.all():
        print(recipient.id, recipient.name, recipient.phone)

    print("\nMessages")
    print("-" * 40)
    for message in Message.query.all():
        print(message.id, message.body)

    print("\nMessage Recipients")
    print("-" * 40)
    for mr in MessageRecipient.query.all():
        print(
            "ID:", mr.id,
            "Message:", mr.message_id,
            "Recipient:", mr.recipient_id
        )
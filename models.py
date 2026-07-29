#Defines database tables
from flask_sqlalchemy import SQLAlchemy #creating a sqlalchemy object
from datetime import datetime
from zoneinfo import ZoneInfo
from services.phone import normalize_phone, validate_phone

db = SQLAlchemy()

class Recipient(db.Model):  #class is stored in the database
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False    #makes sure the field cannot be empty
    )
    _phone = db.Column(
        "phone",
        db.String(20),
        nullable=False,
        unique=True
    )

    @property
    def phone(self):
        return self._phone
    @phone.setter
    def phone(self, value):
        cleaned = normalize_phone(value)

        if not validate_phone(cleaned):
            raise ValueError("Invalid phone number")
        self._phone = cleaned

    recipient_type = db.Column(   #do not name it 'type' since that's an existing python function
        db.String(20),
        nullable=False
    )
    department = db.Column(
        db.String(50)
    )
    active = db.Column(
        db.Boolean,
        default=True
    )
    messages = db.relationship(   #this will connect a recipient to a message
        "MessageRecipient",
        back_populates="recipient",
    )
    def __repr__(self):   #allows us to print the actual name instead of the address
        return f"<Recipient {self.name}>"

class Message(db.Model):  # stores all created messages
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    body = db.Column(
        db.Text,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(ZoneInfo("America/Chicago")),
    )
    archived = db.Column(
        db.Boolean,
        default=False
    )
    recipients = db.relationship(
        "MessageRecipient",
        back_populates="message",
    )
    replies = db.relationship(
        "Reply",
        back_populates="message",
        cascade = "all, delete-orphan",
    )
    def __repr__(self):
        return f"<Message {self.id}>"

class MessageRecipient(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    message_id = db.Column(
        db.Integer,
        db.ForeignKey('message.id'),
        nullable=False
    )
    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('recipient.id'),
        nullable=False
    )
    sent = db.Column(
        db.Boolean,
        default=False
    )
    sent_at = db.Column(
        db.DateTime,
    )
    message = db.relationship(
        "Message",
        back_populates="recipients",
    )
    recipient = db.relationship(
        "Recipient",
        back_populates="messages",
    )
class Reply(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    message_id = db.Column(
        db.Integer,
        db.ForeignKey('message.id'),
        nullable=False
    )
    message_recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('message_recipient.id'),
        nullable=False
    )
    body = db.Column(
        db.Text,
        nullable=False
    )
    received_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(ZoneInfo("America/Chicago"))
    )
    message = db.relationship(
        "Message",
        back_populates="replies",
    )
    recipient = db.relationship(
        "Recipient",
    )
    archived = db.Column(
        db.Boolean,
        default=False
    )
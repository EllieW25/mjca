#Defines database tables
from flask_sqlalchemy import SQLAlchemy #creating an sqlalchemy object

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
    phone = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )
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
    def __repr__(self):   #allows us to print the actual name instead of the address
        return f"<Recipient {self.name}>"
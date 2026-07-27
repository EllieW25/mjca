from app import app
from models import db, Recipient

with app.app_context():
    teacher = Recipient(
        name="Mrs. Smith",
        phone="+91123456789",
        recipient_type = "Teacher",
        department = "Engineering",
    )
    db.session.add(teacher)
    db.session.commit()

    print("Teacher added")
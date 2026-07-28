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

    substitute = Recipient(
        name= "Joe kingston",
        phone="356 898 3240",
        recipient_type = "Substitute",
        department = "Engineering",
        active = False,
    )
    db.session.add(substitute)
    db.session.commit()

    print("Teacher added")
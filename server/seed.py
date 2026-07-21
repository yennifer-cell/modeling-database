from app import app
from models import db, Driver

with app.app_context():
    sam = Driver(name="Sam")
    peter = Driver(name="Peter")
    Trisha= Driver(name="Trisha")

    db.session.add_all([sam, peter, Trisha])
    db.session.commit()

    
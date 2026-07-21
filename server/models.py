from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    truck = db.relationship('Truck', back_populates='driver', uselist=False)

class Truck(db.Model):
    __tablename__ = 'trucks'
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String)
    driver_id=db.Column(db.Integer, db.ForeignKey('drivers.id'))
    expenses = db.relationship('Expense', back_populates='truck', uselist=True)
    driver = db.relationship('Driver', back_populates='truck', uselist=False)
    trips = db.relationship('Trip', back_populates='truck')


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String)
    expense_date = db.Column(db.String)
    truck_id= db.Column(db.Integer, db.ForeignKey('trucks.id'))
    truck = db.relationship('Truck', back_populates='expenses', uselist=False)

class Trip(db.Model):
    __tablename__= 'trips'

    id = db.Column(db.Integer, primary_key = True)
    trip_date = db.Column(db.String)
    origin = db.Column(db.String)
    distance = db.Column(db.String)
    destination = db.Column(db.String)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id')) 
    truck_id = db.Column(db.Integer, db.ForeignKey('trucks.id'))
    truck = db.relationship('Truck', back_populates='trips')
    revenue = db.relationship('Revenue', back_populates='trips')

class Revenue(db.Model):
    __tablename__='revenues'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id')) 

    trips = db.relationship('Trip', back_populates='revenue')
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate #Used to keep track of the version of our db

from models import db, Truck, Driver, Expense, Trip, Revenue

app = Flask(__name__)


#configure a connection to our local database
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///tomashi_logistics.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICTAIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# new_truck = Truck(plate_numer="KDH308S")
# db.session.add(new_truck)
# db.session.commit()

# new_driver = Driver(name="David")
# db.session.add(new_truck)
# db.session.commit()

#CRUD: Create, Retrieve, Update, Delete

@app.route("/drivers", methods=['GET'])
def get_drivers():
    drivers = Driver.query.all()
    return jsonify([{"id": driver.id, "name": driver.name} for driver in drivers])

@app.route("/drivers", methods=['POST'])
def add_driver():
    data = request.get_json()
    
    new_driver = Driver(name=data["name"])
    db.session.add(new_driver)
    db.session.commit()

    return jsonify(
        {
            "id": new_driver.id,
            "name": new_driver.name
        }
    ), 201

@app.route("/drivers/<int:id>", methods=["PATCH", "PUT"])
def update_driver(id):
    data = request.get_json()
    driver = Driver.query.filter_by(id=id).first()
    if not driver:
        return jsonify({"error":"Driver not found"})
    
    for key, value in data.items():
        if hasattr(driver, key):
            setattr(driver, key, value)

    db.session.commit()

    return jsonify({
        "id": driver.id,
        "name": driver.name
    }), 201

@app.route("/drivers/<int:id>", methods=["DELETE"])
def delete_driver(id):
    driver = Driver.query.filter_by(id=id).first()
    if not driver:
        return jsonify({"error":"Driver not found"})
    db.session.delete(driver)
    db.session.commit()
    return jsonify({
        "id": driver.id,
        "name": driver.name
    }), 201
# ==========================================
# TRIP CRUD OPERATIONS
# ==========================================

@app.route("/trips", methods=['GET'])
def get_trips():
    trips = Trip.query.all()
    return jsonify([{
        "id": trip.id, 
        "trip_date": trip.trip_date,
        "origin": trip.origin,
        "distance": trip.distance,
        "destination": trip.destination,
        "driver_id": trip.driver_id,
        "truck_id": trip.truck_id
    } for trip in trips])

@app.route("/trips", methods=['POST'])
def add_trip():
    data = request.get_json()
    
    new_trip = Trip(
        trip_date=data["trip_date"],
        origin=data["origin"],
        distance=data["distance"],
        destination=data["destination"],
        driver_id=data["driver_id"],
        truck_id=data["truck_id"]
    )
    db.session.add(new_trip)
    db.session.commit()

    return jsonify(
        {
            "id": new_trip.id,
            "trip_date": new_trip.trip_date,
            "origin": new_trip.origin,
            "distance": new_trip.distance,
            "destination": new_trip.destination,
            "driver_id": new_trip.driver_id,
            "truck_id": new_trip.truck_id
        }
    ), 201

@app.route("/trips/<int:id>", methods=["PATCH", "PUT"])
def update_trip(id):
    data = request.get_json()
    trip = Trip.query.filter_by(id=id).first()
    
    if not trip:
        return jsonify({"error":"Trip not found"})
    
    for key, value in data.items():
        if hasattr(trip, key):
            setattr(trip, key, value)

    db.session.commit()

    return jsonify({
        "id": trip.id,
        "trip_date": trip.trip_date,
        "origin": trip.origin,
        "distance": trip.distance,
        "destination": trip.destination,
        "driver_id": trip.driver_id,
        "truck_id": trip.truck_id
    }), 201

@app.route("/trips/<int:id>", methods=["DELETE"])
def delete_trip(id):
    trip = Trip.query.filter_by(id=id).first()
    
    if not trip:
        return jsonify({"error":"Trip not found"})
        
    db.session.delete(trip)
    db.session.commit()
    
    return jsonify({
        "id": trip.id,
        "trip_date": trip.trip_date,
        "origin": trip.origin,
        "distance": trip.distance,
        "destination": trip.destination,
        "driver_id": trip.driver_id,
        "truck_id": trip.truck_id
    }), 201
if __name__ == '__main__':
    app.run(port=5555, debug=True)
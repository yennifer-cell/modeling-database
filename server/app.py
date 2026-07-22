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

#Drivers
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
@app.route("/trucks", methods=["GET"])
def get_trucks():
    trucks = Truck.query.all()
    return jsonify([{"id": truck.id, "plate_number": truck.plate_number} for truck in trucks])

@app.route("/trucks", methods=['POST'])
def add_truck():
    data = request.get_json()
    
    driver_id = data.get("driver_id", None)
    driver = Driver.query.filter_by(id=driver_id).first()

    if not driver and driver_id != None:
        return jsonify({"error": "Driver not found"}), 404
    
    new_truck = Truck(plate_number=data["plate_number"], driver_id=driver_id)
    db.session.add(new_truck)
    db.session.commit()

    return jsonify(
        {
            "id": new_truck.id,
            "plate_number": new_truck.plate_number
        }
    ), 201

@app.route("/trucks/<int:id>", methods=["PATCH", "PUT"])
def update_truck(id):
    data = request.get_json()
    truck = Truck.query.filter_by(id=id).first()

    if not truck:
        return jsonify({"error":"Truck not found"})
    
    driver_id = data.get("driver_id", None)
    driver = Driver.query.filter_by(id=driver_id).first()

    if not driver and driver_id != None:
        return jsonify({"error": "Driver not found"}), 404
    
    for key, value in data.items():
        if hasattr(truck, key):
            setattr(truck, key, value)

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
        "id": truck.id,
        "plate_number": truck.plate_number
    }), 201

@app.route("/trucks/<int:id>", methods=["DELETE"])
def delete_truck(id):
    truck = Truck.query.filter_by(id=id).first()
    if not truck:
        return jsonify({"error":"Truck not found"})
    db.session.delete(truck)
    db.session.commit()
    return jsonify({
        "id": truck.id,
        "plate_number": truck.plate_number
    }), 201

#Revenue
@app.route('/revenue', methods=['GET'])
def get_revenue():
    revenue = Revenue.query.all()

    return jsonify([{'id' : r.id, 'amount' : r.amount, 'trip_id' : r.trip_id} for r in revenue]), 200


@app.route('/revenue', methods=['POST'])
def add_revenue():
    data = request.get_json()
    new_rev = Revenue(amount=data['amount'], trip_id=data['trip_id'])
    db.session.add(new_rev)
    db.session.commit()

    return jsonify({
        'id' : new_rev.id,
        'amount' : new_rev.amount,
        'trip_id' : new_rev.trip_id
    })


@app.route('/revenue/<int:id>', methods=['PATCH', 'PUT'])
def update_revenue(id) :
    data = request.get_json()
    revenue = Revenue.query.filter_by(id=id).first()

    if revenue :
        if 'trip_id' in data:
            trip = Trip.query.filter_by(id=data['trip_id']).first()
            if not trip :
                return jsonify({'error' : f'Trip with id {data['trip_id']} not found'})
            
        for key, value in data.items():
            if hasattr(revenue, key):
                setattr(revenue, key, value)

        db.commit()

        return jsonify({
            'id' : revenue.id,
            'amount' : revenue.amount,
            'trip_id' : revenue.trip_id
        }), 200
    else :
        return jsonify({'error':f'Revenue {id} not found'})
    

@app.route('/revenue/<int:id>', methods=['DELETE'])
def delete_revenue(id) :
    revenue = Revenue.query.filter_by(id=id).first()

    if not revenue:
        return jsonify({'error' : f'Revenue {id} not found'})
    
    db.session.delete(revenue)
    db.session.commit()

    return jsonify({
        'id' : revenue.id,
        'amount' : revenue.amount,
        'trip_id' : revenue.trip_id
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)
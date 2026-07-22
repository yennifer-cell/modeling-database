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

@app.route("/trucks", methods=["GET"])
def get_trcuks():
    trucks = Truck.query.all()
    return jsonify([{"id": truck.id, "plate_number": truck.plate_number} for truck in trucks])

@app.route("/trucks", methods=['POST'])
def add_truck():
    data = request.get_json()
    
    driver_id = data.get("driver_id", None)

    if driver_id is None:
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

    if driver_id is None:
        return jsonify({"error": "Driver not found"}), 404
    
    for key, value in data.items():
        if hasattr(truck, key):
            setattr(truck, key, value)

    db.session.commit()

    return jsonify({
        "id": truck.id,
        "plate_number": truck.plate_number
    }), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
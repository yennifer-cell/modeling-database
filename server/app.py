from flask import Flask, jsonify, request
from flask_migrate import Migrate

from models import db, Truck, Driver, Expense, Trip, Revenue

app = Flask(__name__)


# Configure a connection to our local database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tomashi_logistics.db"

# Disable modification tracking to use less memory
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)


# Drivers
@app.route("/drivers", methods=["GET"])
def get_drivers():
    drivers = Driver.query.all()
    return jsonify([{"id": driver.id, "name": driver.name} for driver in drivers])


@app.route("/drivers", methods=["POST"])
def add_driver():
    data = request.get_json() or {}

    new_driver = Driver(name=data["name"])
    db.session.add(new_driver)
    db.session.commit()

    return jsonify({"id": new_driver.id, "name": new_driver.name}), 201


@app.route("/drivers/<int:id>", methods=["PATCH", "PUT"])
def update_driver(id):
    data = request.get_json() or {}
    driver = Driver.query.filter_by(id=id).first()

    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    for key, value in data.items():
        if hasattr(driver, key):
            setattr(driver, key, value)

    db.session.commit()

    return jsonify({"id": driver.id, "name": driver.name}), 200


@app.route("/drivers/<int:id>", methods=["DELETE"])
def delete_driver(id):
    driver = Driver.query.filter_by(id=id).first()

    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    db.session.delete(driver)
    db.session.commit()

    return jsonify({"id": driver.id, "name": driver.name}), 200


# ==========================================
# TRIP CRUD OPERATIONS
# ==========================================

@app.route("/trips", methods=["GET"])
def get_trips():
    trips = Trip.query.all()
    return jsonify([
        {
            "id": trip.id,
            "trip_date": trip.trip_date,
            "origin": trip.origin,
            "distance": trip.distance,
            "destination": trip.destination,
            "driver_id": trip.driver_id,
            "truck_id": trip.truck_id,
        }
        for trip in trips
    ])


@app.route("/trips", methods=["POST"])
def add_trip():
    data = request.get_json() or {}

    new_trip = Trip(
        trip_date=data["trip_date"],
        origin=data["origin"],
        distance=data["distance"],
        destination=data["destination"],
        driver_id=data["driver_id"],
        truck_id=data["truck_id"],
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
            "truck_id": new_trip.truck_id,
        }
    ), 201


@app.route("/trips/<int:id>", methods=["PATCH", "PUT"])
def update_trip(id):
    data = request.get_json() or {}
    trip = Trip.query.filter_by(id=id).first()

    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    for key, value in data.items():
        if hasattr(trip, key):
            setattr(trip, key, value)

    db.session.commit()

    return jsonify(
        {
            "id": trip.id,
            "trip_date": trip.trip_date,
            "origin": trip.origin,
            "distance": trip.distance,
            "destination": trip.destination,
            "driver_id": trip.driver_id,
            "truck_id": trip.truck_id,
        }
    ), 200


@app.route("/trips/<int:id>", methods=["DELETE"])
def delete_trip(id):
    trip = Trip.query.filter_by(id=id).first()

    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    db.session.delete(trip)
    db.session.commit()

    return jsonify(
        {
            "id": trip.id,
            "trip_date": trip.trip_date,
            "origin": trip.origin,
            "distance": trip.distance,
            "destination": trip.destination,
            "driver_id": trip.driver_id,
            "truck_id": trip.truck_id,
        }
    ), 200


@app.route("/trucks", methods=["GET"])
def get_trucks():
    trucks = Truck.query.all()
    return jsonify([{"id": truck.id, "plate_number": truck.plate_number} for truck in trucks])


@app.route("/trucks", methods=["POST"])
def add_truck():
    data = request.get_json() or {}

    driver_id = data.get("driver_id", None)
    driver = Driver.query.filter_by(id=driver_id).first()

    if not driver and driver_id is not None:
        return jsonify({"error": "Driver not found"}), 404

    new_truck = Truck(plate_number=data["plate_number"], driver_id=driver_id)
    db.session.add(new_truck)
    db.session.commit()

    return jsonify({"id": new_truck.id, "plate_number": new_truck.plate_number}), 201


@app.route("/trucks/<int:id>", methods=["PATCH", "PUT"])
def update_truck(id):
    data = request.get_json() or {}
    truck = Truck.query.filter_by(id=id).first()

    if not truck:
        return jsonify({"error": "Truck not found"}), 404

    driver_id = data.get("driver_id", None)
    driver = Driver.query.filter_by(id=driver_id).first()

    if not driver and driver_id is not None:
        return jsonify({"error": "Driver not found"}), 404

    for key, value in data.items():
        if hasattr(truck, key):
            setattr(truck, key, value)

    db.session.commit()

    return jsonify({"id": truck.id, "plate_number": truck.plate_number}), 200


@app.route("/trucks/<int:id>", methods=["DELETE"])
def delete_truck(id):
    truck = Truck.query.filter_by(id=id).first()

    if not truck:
        return jsonify({"error": "Truck not found"}), 404

    db.session.delete(truck)
    db.session.commit()

    return jsonify({"id": truck.id, "plate_number": truck.plate_number}), 200


# Expenses
@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([
        {
            "id": expense.id,
            "description": expense.description,
            "expense_date": expense.expense_date,
            "truck_id": expense.truck_id,
        }
        for expense in expenses
    ])


@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json() or {}

    truck = Truck.query.filter_by(id=data.get("truck_id")).first()
    if not truck:
        return jsonify({"error": "Truck not found"}), 404

    new_expense = Expense(
        description=data["description"],
        expense_date=data["expense_date"],
        truck_id=data["truck_id"],
    )
    db.session.add(new_expense)
    db.session.commit()

    return jsonify(
        {
            "id": new_expense.id,
            "description": new_expense.description,
            "expense_date": new_expense.expense_date,
            "truck_id": new_expense.truck_id,
        }
    ), 201


@app.route("/expenses/<int:id>", methods=["PATCH", "PUT"])
def update_expense(id):
    data = request.get_json() or {}
    expense = Expense.query.filter_by(id=id).first()

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    if "truck_id" in data:
        truck = Truck.query.filter_by(id=data["truck_id"]).first()
        if not truck:
            return jsonify({"error": "Truck not found"}), 404

    for key, value in data.items():
        if hasattr(expense, key):
            setattr(expense, key, value)

    db.session.commit()

    return jsonify(
        {
            "id": expense.id,
            "description": expense.description,
            "expense_date": expense.expense_date,
            "truck_id": expense.truck_id,
        }
    ), 200


@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    expense = Expense.query.filter_by(id=id).first()

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify(
        {
            "id": expense.id,
            "description": expense.description,
            "expense_date": expense.expense_date,
            "truck_id": expense.truck_id,
        }
    ), 200


# Revenue
@app.route("/revenue", methods=["GET"])
def get_revenue():
    revenue = Revenue.query.all()
    return jsonify([{"id": r.id, "amount": r.amount, "trip_id": r.trip_id} for r in revenue]), 200


@app.route("/revenue", methods=["POST"])
def add_revenue():
    data = request.get_json() or {}
    new_rev = Revenue(amount=data["amount"], trip_id=data["trip_id"])
    db.session.add(new_rev)
    db.session.commit()

    return jsonify({"id": new_rev.id, "amount": new_rev.amount, "trip_id": new_rev.trip_id}), 201


@app.route("/revenue/<int:id>", methods=["PATCH", "PUT"])
def update_revenue(id):
    data = request.get_json() or {}
    revenue = Revenue.query.filter_by(id=id).first()

    if not revenue:
        return jsonify({"error": f"Revenue {id} not found"}), 404

    if "trip_id" in data:
        trip = Trip.query.filter_by(id=data["trip_id"]).first()
        if not trip:
            return jsonify({"error": f"Trip with id {data['trip_id']} not found"}), 404

    for key, value in data.items():
        if hasattr(revenue, key):
            setattr(revenue, key, value)

    db.session.commit()

    return jsonify({"id": revenue.id, "amount": revenue.amount, "trip_id": revenue.trip_id}), 200


@app.route("/revenue/<int:id>", methods=["DELETE"])
def delete_revenue(id):
    revenue = Revenue.query.filter_by(id=id).first()

    if not revenue:
        return jsonify({"error": f"Revenue {id} not found"}), 404

    db.session.delete(revenue)
    db.session.commit()

    return jsonify({"id": revenue.id, "amount": revenue.amount, "trip_id": revenue.trip_id}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
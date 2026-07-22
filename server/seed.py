from app import app
from models import db, Driver, Truck, Trip

with app.app_context():
    # 1. Create Drivers (from the original code)
    sam = Driver(name="Sam")
    peter = Driver(name="Peter")
    Trisha= Driver(name="Trisha")

    db.session.add_all([sam, peter, Trisha])
    db.session.commit()

    # 2. Create a Mock Truck so we have a valid truck_id
    truck1 = Truck(plate_number="DRC-9982")
    db.session.add(truck1)
    db.session.commit() 

    # 3. Create Mock Trips to test your API routes
    trip1 = Trip(
        trip_date="2026-07-21",
        origin="Kinshasa",
        distance="350km",
        destination="Matadi",
        driver_id=sam.id,
        truck_id=truck1.id
    )
    
    trip2 = Trip(
        trip_date="2026-07-22",
        origin="Lubumbashi",
        distance="120km",
        destination="Likasi",
        driver_id=peter.id,
        truck_id=truck1.id
    )

    db.session.add_all([trip1, trip2])
    db.session.commit()
    
    print("Database seeded successfully with Drivers, Trucks, and Trips!")
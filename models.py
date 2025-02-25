from flask_pymongo import PyMongo
from bson import ObjectId

class User:
    def __init__(self, mongo, username, email, phone, address, password):
        self.mongo = mongo
        self.username = username
        self.email = email
        self.phone = phone
        self.address = address
        self.password = password

    @staticmethod
    def create_user(mongo, username, email, phone, address, password):
        """Inserts a new user document into the 'users' collection."""
        user = User(mongo, username, email, phone, address, password)
        mongo.db.users.insert_one({
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "password": user.password
        })
        return user
    
    @staticmethod
    def get_all_users(mongo):
        """Retrieve all users from the database."""
        users = mongo.db.users.find()
        return users
    
    @staticmethod
    def get_user_by_email(mongo, email):
        """Retrieve a user by email."""
        return mongo.db.users.find_one({"email": email})
    
    @staticmethod
    def user_exists(mongo, username=None, email=None):
        """Check if a user with the given username or email exists in the database."""
        if username:
            existing_user = mongo.db.users.find_one({"username": username})
        elif email:
            existing_user = mongo.db.users.find_one({"email": email})
        else:
            existing_user = None
        return existing_user


class Booking:
    def __init__(self, username, bike, status, start_time, end_time):
        self.user = username
        self.bike = bike
        self.status = status
        self.start_time = start_time
        self.end_time = end_time

    @staticmethod
    def from_dict(data):
        """Convert a dictionary to a Booking object."""
        return Booking(
            user=data.get('user'),
            bike=data.get('bike'),
            status=data.get('status'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time')
        )

    
    @staticmethod
    def get_all_bookings(mongo):
        bookings = list(mongo.db.bookings.find({}))

        for booking in bookings:
            print(f"\n🔹 Booking Document: {booking}")  # Debugging

            # ✅ Fetch User Name from 'users' Collection
            user_id = booking.get("user_id")  # Use .get() to avoid KeyError
            if user_id:
                try:
                    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
                    print(f"🔹 Found User: {user}")  # Debugging
                    booking["user"] = user.get("username", "Unknown User")  # Ensure "username" key exists
                except Exception as e:
                    print(f"❌ Error fetching user: {e}")
                    booking["user"] = "Unknown User"
            else:
                print(f"❌ user_id missing in booking: {booking.get('_id', 'Unknown ID')}")
                booking["user"] = "Unknown User"

            # ✅ Fetch Bike Name from 'bikes' Collection
            bike_id = booking.get("bike_id")
            if bike_id:
                try:
                    bike = mongo.db.bikes.find_one({"_id": ObjectId(bike_id)})
                    print(f"🔹 Found Bike: {bike}")  # Debugging
                    booking["bike"] = bike.get("name", "Unknown Bike")  # Ensure "name" key exists
                except Exception as e:
                    print(f"❌ Error fetching bike: {e}")
                    booking["bike"] = "Unknown Bike"
            else:
                print(f"❌ bike_id missing in booking: {booking.get('_id', 'Unknown ID')}")
                booking["bike"] = "Unknown Bike"

        return bookings


    @staticmethod
    def get_booking_by_id(mongo, booking_id):
        """Retrieve a booking by its ObjectId."""
        booking = mongo.db.bookings.find_one({"_id": ObjectId(booking_id)})
        if booking:
            return Booking.from_dict(booking)
        return None

    @staticmethod
    def create_booking(mongo, user, bike, status, start_time, end_time):
        """Create a new booking and insert it into the database."""
        booking_data = {
            "user": user,
            "bike": bike,
            "status": status,
            "start_time": start_time,
            "end_time": end_time
        }
        result = mongo.db.bookings.insert_one(booking_data)
        return Booking.from_dict(booking_data)

    @staticmethod
    def update_booking_status(mongo, booking_id, new_status):
        """Update the status of a booking."""
        mongo.db.bookings.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": {"status": new_status}}
        )
    @staticmethod
    def cancel_booking(mongo, booking_id):
        db = mongo.db  # Access MongoDB database instance

        try:
            object_id = ObjectId(booking_id)  # Convert booking_id to ObjectId
        except Exception as e:
            print(f"Invalid booking ID: {booking_id}, Error: {e}")
            return False

        # Update the booking status to "Cancelled"
        result = db.bookings.update_one(
            {"_id": object_id},
            {"$set": {"status": "Cancelled"}}
        )

        if result.matched_count == 0:
            print(f"Booking ID {booking_id} not found.")
            return False

        # After canceling the booking, make the bike available again
        # Retrieve the booking data to get the bike ID
        booking = db.bookings.find_one({"_id": object_id})
        if booking:
            bike_id = booking.get('bike')  # Assuming 'bike' field stores the bike ID

            # Update the bike status to "available"
            bike_result = db.bikes.update_one(
                {"_id": ObjectId(bike_id)},
                {"$set": {"status": "available"}}
            )

            if bike_result.matched_count == 0:
                print(f"Bike ID {bike_id} not found.")
                return False
            elif bike_result.modified_count == 0:
                print(f"Bike ID {bike_id} status update failed.")
                return False

            print(f"Bike ID {bike_id} successfully marked as available.")
            return True
        else:
            print(f"Booking ID {booking_id} doesn't contain a valid bike ID.")
            return False    
    @staticmethod
    def confirm_booking(mongo, booking_id):
        db = mongo.db  # Get the MongoDB database instance
        
        try:
            object_id = ObjectId(booking_id)  # Ensure the ID is in ObjectId format
        except Exception as e:
            print(f"Invalid booking ID: {booking_id}, Error: {e}")
            return False
        
        result = db.bookings.update_one(
            {"_id": object_id}, {"$set": {"status": "Started"}}
        )
        
        if result.matched_count == 0:
            print(f"Booking ID {booking_id} does not exist in the database.")
            return False
        elif result.modified_count == 0:
            print(f"Booking ID {booking_id} status was not updated.")
            return False
        
        print(f"Booking ID {booking_id} successfully confirmed.")
        return True

class Bike:
    @staticmethod
    def get_all_bikes(mongo):
        bikes = list(mongo.db.bikes.find({}, {"_id": 1, "name": 1, "rent_per_hour": 1}))

        for bike in bikes:
            # Check if the bike is booked
            booking = mongo.db.bookings.find_one({"bike_id": str(bike["_id"]), "status": "Confirmed"})
            
            if booking:
                bike["status"] = "Booked"
            else:
                bike["status"] = "Available"

        return bikes


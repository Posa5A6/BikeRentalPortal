from flask import Flask, jsonify, render_template, request, redirect, session, url_for, flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from models import Bike, Booking, User  # Import User model from models.py
from bson import ObjectId
import datetime
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId
import urllib.parse


app = Flask(__name__, template_folder='templates')

# MongoDB URI
app.config["MONGO_URI"] = "mongodb+srv://narisnarendras6:Posa%401432@cluster0.n7htm.mongodb.net/"
app.secret_key = 'your_secret_key'  # Secret key for sessions and flash messages

# Initialize PyMongo with the Flask app
mongo = PyMongo(app)

# Connect to MongoDB
client = MongoClient("mongodb+srv://narisnarendras6@gmail.com:Posa@1432@your-cluster.mongodb.net/?retryWrites=true&w=majority")
db = client['bike_rental']
users_collection = db['users']
bookings_collection = db["bookings"]

username = "narisnarendras6@gmail.com"
password = urllib.parse.quote_plus("Posa@1432")  # Encodes special characters

uri = f"mongodb+srv://{username}:{password}@your-cluster.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

@app.before_request
def before_request():
    if mongo.db is None:
        print("MongoDB connection not initialized.")
    else:
        print("MongoDB connection initialized successfully.")


# Home route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        print(f"Form Data: {username}, {email}, {phone}, {address}, {password}, {confirm_password}")

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('signup'))

        if User.user_exists(mongo, username=username) or User.user_exists(mongo, email=email):
            flash('Username or Email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))

        # Insert the user into MongoDB
        User.create_user(mongo, username, email, phone, address, password)

        flash('Registration successful! Redirecting to login page...', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if admin credentials are entered
        if email == "brp@gmail.com" and password == "1432":
            session['user'] = 'admin'  # Store admin in session
            print("Admin login successful! Redirecting...")  # Debugging
            return redirect(url_for('admin_dashboard'))

        # Check for normal user login
        user = users_collection.find_one({'email': email})
        
        if user and user.get('password') == password:
            session['user'] = email  # Store user in session
            print("User login successful! Redirecting...")  # Debugging
            return redirect(url_for('user_dashboard'))
        
        flash("Invalid email or password!", "danger")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' in session:
        return render_template('admin_dashboard.html')
    return redirect(url_for('login'))


@app.route('/admin')
def admin():
    return render_template('admin_dashboard.html')

@app.route('/view_users')
def manage_users():
    users = mongo.db.users.find()
    return render_template('view_users.html', users=users)

@app.route('/admin/bookings')
def manage_bookings():
    bookings = Booking.get_all_bookings(mongo)
    print("Fetched Bookings:", bookings)  # Debugging log
    return render_template('manage_bookings.html', bookings=bookings)

@app.route('/cancel_booking/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    print(f"Attempting to cancel booking with ID: {booking_id}")  # Debugging

    success = Booking.cancel_booking(mongo, booking_id)
    if success:
        flash("Booking cancelled successfully.", 'success')  # Flash message (optional)
        return jsonify({"success": True})  # Return JSON response
    else:
        print(f"Cancellation failed for booking ID: {booking_id}")
        flash("Booking cancellation failed.", 'error')
        return jsonify({"success": False}), 400  # Return error response

@app.route('/confirm_booking/<booking_id>', methods=['POST'])
def confirm_booking(booking_id):
    print(f"Booking ID to confirm: {booking_id}")  # Debugging

    success = Booking.confirm_booking(mongo, booking_id)
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 400
@app.route('/manage_bikes')
def manage_bikes():
    bikes = mongo.db.bikes.find()  # Fetch all bikes from the database
    return render_template('manage_bikes.html', bikes=bikes)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/admin/users')
def view_users():
    try:
        # Fetch users from MongoDB (ensure the correct database and collection)
        users = mongo.db.users.find()

        users_list = []
        for user in users:
            print(f"User Found: {user}")  # Debugging: Print each user to check if they are being fetched
            user['_id'] = str(user['_id'])  # Convert ObjectId to string for template rendering
            users_list.append(user)

        if not users_list:
            print("No users found.")
        else:
            print(f"Users List: {users_list}")

        return render_template('view_users.html', users=users_list)  # Pass the list of users to the template
    except Exception as e:
        print(f"Error fetching users: {e}")
        flash('Error fetching users from database.', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/bikes')
def view_bikes():
    bikes = Bike.get_all_bikes(mongo)
    print("Fetched Bikes:", bikes)  # Debugging log
    return render_template('view_bikes.html', bikes=bikes)


@app.route('/add_bike', methods=['GET', 'POST'])
def add_bike():
    if request.method == 'POST':
        # Get data from the form
        bike_name = request.form['bike_name']
        rent_per_hour = request.form['rent_per_hour']
        available = 'available' in request.form  # If checkbox is checked, this will be True

        # Save the bike data to the database
        mongo.db.bikes.insert_one({
            'name': bike_name,
            'rent_per_hour': rent_per_hour,
            'available': available
        })

        flash('Bike added successfully!', 'success')
        return redirect(url_for('manage_bikes'))  # Redirect to the manage bikes page

    return render_template('add_bike.html')  # Render the form for adding a bike


@app.route('/edit_bike/<bike_id>', methods=['GET', 'POST'])
def edit_bike(bike_id):
    # Fetch the bike data from the database using the bike_id
    bike = mongo.db.bikes.find_one({'_id': ObjectId(bike_id)})

    if request.method == 'POST':
        # Update bike data here (e.g., bike name, rent, availability)
        bike_name = request.form['bike_name']
        rent_per_hour = request.form['rent_per_hour']
        available = 'available' in request.form

        mongo.db.bikes.update_one({'_id': ObjectId(bike_id)}, {
            '$set': {
                'name': bike_name,
                'rent_per_hour': rent_per_hour,
                'available': available
            }
        })
        flash('Bike updated successfully!', 'success')
        return redirect(url_for('manage_bikes'))  # Redirect back to manage bikes

    return render_template('edit_bike.html', bike=bike)

@app.route('/delete_bike/<bike_id>', methods=['GET', 'POST'])
def delete_bike(bike_id):
    # Delete the bike from the database using the bike_id
    mongo.db.bikes.delete_one({'_id': ObjectId(bike_id)})
    flash('Bike deleted successfully!', 'success')
    return redirect(url_for('manage_bikes'))  # Redirect back to manage bikes


# Define collections properly
users_collection = mongo.db.users  # Assuming 'users' is the collection name
bikes_collection = mongo.db.bikes  # Add this line for the 'bikes' collection
bookings_collection = mongo.db.bookings  # Add this for 'bookings' collection

@app.route('/user_dashboard')
def user_dashboard():
    user_email = session.get('user')  # Get user email from session
    if not user_email:
        return redirect(url_for('login'))  # Redirect if not logged in

    # Fetch user from the database
    user = users_collection.find_one({'email': user_email})

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for('login'))  # Redirect to login if user is missing

    # Fetch available bikes
    available_bikes = bikes_collection.find({'available': True})  # Ensure bikes_collection is defined

    # Fetch bookings for the logged-in user
    bookings = bookings_collection.find({'user_id': user['_id']})  # Ensure user['_id'] exists

    # Fetch wallet balance
    wallet_balance = user.get('balance', 0)  # Default to 0 if balance is missing

    # Fetch bike preferences
    bike_preferences = user.get('preferences', [])

    # Check for an active ride
    active_ride = bookings_collection.find_one({'user_id': user['_id'], 'status': 'active'})

    return render_template('user_dashboard.html', 
                           user=user, 
                           bookings=bookings, 
                           wallet_balance=wallet_balance, 
                           available_bikes=available_bikes, 
                           bike_preferences=bike_preferences,
                           active_ride=active_ride)



@app.route('/book_bike', methods=['POST'])
def book_bike():
    # Ensure user is logged in
    user_email = session.get('user')
    if not user_email:
        return redirect(url_for('login'))  # Redirect to login if user is not authenticated

    # Get user details
    user = mongo.db.users.find_one({'email': user_email})
    if not user:
        return redirect(url_for('login'))

    # Get booking time
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    try:
        bike_id = request.form['bike_id']
        bike_id = ObjectId(bike_id)  # Ensure it's a valid ObjectId
        booking_amount = float(request.form['amount'])
    except (KeyError, ValueError):
        flash("Invalid request data!", "error")
        return redirect(url_for('user_dashboard'))

    # Check user balance
    current_balance = user.get('balance', 0)  # Default to 0 if missing
    if current_balance < booking_amount:
        flash("Insufficient funds for the booking.", "error")
        return redirect(url_for('user_dashboard'))

    # Deduct balance
    new_balance = current_balance - booking_amount
    mongo.db.users.update_one({'email': user_email}, {'$set': {'balance': new_balance}})

    # Get bike details
    bike = mongo.db.bikes.find_one({'_id': bike_id})
    if not bike:
        flash("Bike not found!", "error")
        return redirect(url_for('user_dashboard'))

    if bike.get('available') is True:
        # Create booking record
        booking = {
            'user_id': user['_id'],
            'bike_id': bike['_id'],
            'bike_name': bike['name'],
            'start_time': start_time,
            'end_time': end_time,
            'status': 'In Progress',
            'amount_paid': booking_amount,
        }
        
        # Insert booking
        mongo.db.bookings.insert_one(booking)

        # Mark bike as unavailable
        mongo.db.bikes.update_one({'_id': bike['_id']}, {'$set': {'available': False}})

        # Flash success message
        flash("Bike booked successfully!", "success")
        return redirect(url_for('user_dashboard'))
    
    flash("This bike is no longer available.", "error")
    return redirect(url_for('user_dashboard'))

@app.route('/end_ride/<booking_id>', methods=['POST'])
def end_ride(booking_id):
    # Find the booking by its ID
    booking = mongo.db.bookings.find_one({'_id': ObjectId(booking_id)})
    if booking and booking['status'] == 'In Progress':  # Only update if the ride is in progress
        # Set the end_time to now
        end_time = datetime.now()

        # Update the booking document with the end_time
        mongo.db.bookings.update_one({'_id': ObjectId(booking_id)}, {'$set': {'end_time': end_time, 'status': 'Completed'}})

    return redirect(url_for('user_dashboard'))


# Example function to calculate end_time from start_time
def calculate_end_time(start_time):
    # Assuming start_time is a datetime object
    return start_time + timedelta(hours=1)

# Example of how this would be used when creating a booking
def create_booking(start_time):
    end_time = calculate_end_time(start_time)
    # Save the booking with the start_time and calculated end_time
    booking = {
        'start_time': start_time,
        'end_time': end_time,
        # other booking details...
    }
    # Save the booking to the database or wherever necessary
    return booking


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    email = session['user']
    user = mongo.db.users.find_one({'email': email})

    if request.method == 'POST':
        # Get the updated data from the form
        updated_username = request.form['username']
        updated_phone = request.form['phone']
        updated_address = request.form['address']
        
        # Update the user's profile in the database
        mongo.db.users.update_one(
            {'email': email},
            {'$set': {'username': updated_username, 'phone': updated_phone, 'address': updated_address}}
        )
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('edit_profile.html', user=user)


@app.route('/add_funds', methods=['GET', 'POST'])
def add_funds():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    email = session['user']
    user = mongo.db.users.find_one({'email': email})

    if request.method == 'POST':
        amount = request.form['amount']
        
        # Add the funds to the user's account
        new_balance = (user.get('balance', 0)) + float(amount)  # Default balance is 0 if not found

        # Update the user's balance in the database
        mongo.db.users.update_one(
            {'email': email},
            {'$set': {'balance': new_balance}}
        )
        flash('Funds added successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('add_funds.html', user=user)

@app.route('/update_bike_preferences', methods=['GET', 'POST'])
def update_bike_preferences():
    # Get the user information (assumes user is logged in and email is stored in session)
    user = mongo.db.users.find_one({'email': session['user']})

    if 'bike_preferences' not in user:
        # If bike_preferences is not present, initialize it with default values
        user['bike_preferences'] = {'type': '', 'color': ''}  # Adjust default values as needed

    return render_template('update_bike_preferences.html', user=user)

    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    email = session['user']
    user = mongo.db.users.find_one({'email': email})

    if request.method == 'POST':
        # Here you will process the form data and update the user's bike preferences
        bike_type = request.form['bike_type']
        bike_color = request.form['bike_color']

        # Update the user's bike preferences in the database
        mongo.db.users.update_one(
            {'email': email},
            {'$set': {'bike_preferences': {'type': bike_type, 'color': bike_color}}}
        )
        flash('Bike preferences updated successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('update_bike_preferences.html', user=user)

@app.route('/edit_password', methods=['GET', 'POST'])
def edit_password():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    email = session['user']
    user = mongo.db.users.find_one({'email': email})

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Verify current password and match new passwords
        if user['password'] == current_password and new_password == confirm_password:
            mongo.db.users.update_one(
                {'email': email},
                {'$set': {'password': new_password}}
            )
            flash('Password updated successfully!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Password update failed. Check your current password or confirm the new password.', 'danger')

    return render_template('edit_password.html', user=user)

    # Get the bike details from the database
    bike = mongo.db.bikes.find_one({'_id': ObjectId(bike_id)})
    
    if bike:
        # Process booking logic (check wallet balance, available funds, etc.)
        user = mongo.db.users.find_one({'email': session['user']})
        if user['balance'] >= bike['rent_per_hour']:
            # Deduct balance and create a booking record
            new_balance = user['balance'] - bike['rent_per_hour']
            mongo.db.users.update_one({'email': session['user']}, {'$set': {'balance': new_balance}})
            
            booking = {
                'user_id': user['_id'],
                'bike_id': bike['_id'],
                'bike_name': bike['name'],
                'start_time': datetime.datetime.now(),
                'status': 'Confirmed',
                'amount_paid': bike['rent_per_hour']
            }
            mongo.db.bookings.insert_one(booking)
            
            flash(f'Booking confirmed for {bike["name"]}!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Insufficient balance to book the bike.', 'danger')
            return redirect(url_for('user_dashboard'))
    
    flash('Bike not found.', 'danger')
    return redirect(url_for('user_dashboard'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' in session:
        user_id = session["user_id"]  # Get user ID from session
        print(f"🔹 User ID from session: {user_id}")  # Debugging
        
        # Check if the user exists
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            print(f"🔹 User found: {user}")  # Debugging
            
            # Delete the user
            result = users_collection.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count > 0:
                print("✅ User deleted successfully.")  # Debugging
                session.clear()  # Log the user out
                flash("Your account has been deleted successfully.", "success")
                return redirect(url_for('index'))  # Redirect to home page
            else:
                print("❌ User deletion failed.")  # Debugging
                flash("Account deletion failed. Please try again.", "danger")
        else:
            print("❌ User not found in the database.")  # Debugging
            flash("Account not found.", "danger")

    return redirect(url_for('home'))  # Redirect if deletion fails

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

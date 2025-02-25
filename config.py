import os

class Config:
    # MongoDB URI configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/bike_rental")  # Replace with your MongoDB URI
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Secret key for Flask sessions and flash messages

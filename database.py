from flask import Flask
from flask_pymongo import PyMongo
from config import Config

# Initialize the Flask app and load configuration from config.py
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the PyMongo extension for MongoDB
mongo = PyMongo(app)

# This function can be used to get the database connection from elsewhere in the app
def get_db():
    return mongo.db

# Optionally, expose `app` if needed for importing directly
if __name__ == "__main__":
    app.run(debug=True)

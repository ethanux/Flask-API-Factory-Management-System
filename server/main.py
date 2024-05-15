# Importing necessary modules from Flask and its extensions.
from flask import Flask, redirect, url_for
from ext.ext import db
from flask_migrate import Migrate
from flask_cors import CORS



# Creating a Flask app api instance.
app = Flask(__name__)

# Setting a secret key for the app.
app.secret_key = "super secret key"

# Configuring the database URI and track modifications for SQLAlchemy.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Changed from 'flask_migrate' to 'False'.

# Initializing SQLAlchemy with the Flask app instance.
db.init_app(app)

CORS(app)
# Setting up Flask-Migrate with the app and the SQLAlchemy instance.
migrate = Migrate(app, db)

# Importing the auth blueprint from the auth module.
from api.api import api 

# Registering the auth blueprint with the app, with a URL prefix '/auth'.
app.register_blueprint(api, url_prefix='/api')
api.secret_password = 'react-flask-password'
api.secret_key = app.secret_key


# Redirecting the root route to the 'index' route of the auth blueprint.
@app.route('/')
def Redirect():
	return redirect(url_for('api.login'))

# Running the Flask app if this script is executed directly.
if __name__ == '__main__':
	with app.app_context():
        # Creating database tables based on the defined models.
		db.create_all()
        # Running the app in debug mode.
		app.run(debug=True, port=8080)

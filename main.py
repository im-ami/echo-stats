import os
from flask import Flask, render_template
from flask_session import Session
from app.auth import sp_oauth, get_spotify
from app.routes import main_routes

app = Flask(__name__, template_folder="app/templates")
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'  # Add this line
app.config['SESSION_PERMANENT'] = False  # Add this line
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Add this line (1 hour)

Session(app)

# Register routes
app.register_blueprint(main_routes)

if __name__ == '__main__':
    # Create session directory if it doesn't exist
    os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
    app.run(debug=True)

import os
from flask import Flask, render_template
from flask_session import Session
from auth import sp_oauth, get_spotify
from routes import main_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

# Register routes
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)

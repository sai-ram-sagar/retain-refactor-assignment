from flask import Flask
from app.routes.users import users_bp

app = Flask(__name__)
app.register_blueprint(users_bp)

@app.route('/')
def home():
    return "User Management System Refactored"

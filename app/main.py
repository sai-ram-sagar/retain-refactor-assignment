# app/main.py

from flask import Flask
from app.routes.users import users_bp

app = Flask(__name__)
app.register_blueprint(users_bp)

@app.route('/')
def home():
    return "User Management System Refactored"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)

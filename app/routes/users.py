# app/routes/users.py

from flask import Blueprint, request, jsonify
from app.database import get_db_connection
from app.utils.validators import is_valid_email, is_strong_password
import bcrypt
from flask import abort

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users]), 200

@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']

        if not name or not email or not password:
            return jsonify({'error': 'Missing fields'}), 400
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email'}), 400
        if not is_strong_password(password):
            return jsonify({'error': 'Weak password'}), 400

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        conn = get_db_connection()
        conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                     (name, email, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode(), user['password']):
            return jsonify({'status': 'success', 'user_id': user['id']}), 200
        else:
            return jsonify({'status': 'failed'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    if user:
        return jsonify(dict(user)), 200
    else:
        return jsonify({"error": "User not found"}), 404


@users_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Name and email required"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        conn = get_db_connection()
        conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "User updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"User {user_id} deleted"}), 200


@users_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name query param is required"}), 400

    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()
    conn.close()

    return jsonify([dict(user) for user in users]), 200

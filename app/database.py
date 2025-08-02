# app/database.py

import sqlite3

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # to return dict-like rows
    return conn

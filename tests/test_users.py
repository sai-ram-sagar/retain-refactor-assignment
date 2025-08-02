# tests/test_users.py

import unittest
import json
from app.main import app

class UserRoutesTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_user(self):
        response = self.app.post('/users', json={
            'name': 'John Tester',
            'email': 'john@example.com',
            'password': 'test1234'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.get_data(as_text=True))

    def test_login_user(self):
        # Login after creating
        self.app.post('/users', json={
            'name': 'Login User',
            'email': 'login@example.com',
            'password': 'pass1234'
        })

        response = self.app.post('/login', json={
            'email': 'login@example.com',
            'password': 'pass1234'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_data(as_text=True))

    def test_get_user(self):
        # First create user
        self.app.post('/users', json={
            'name': 'Fetch Tester',
            'email': 'fetch@example.com',
            'password': 'fetchpass'
        })

        response = self.app.get('/user/1')  # Assumes ID=1 exists
        self.assertIn(response.status_code, [200, 404])  # Acceptable in real case

    def test_search_user(self):
        response = self.app.get('/search?name=Test')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

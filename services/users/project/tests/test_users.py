# services/users/project/tests/test_users.py


import json
import unittest

from flask import Blueprint, jsonify, request
from project.api.models import User
from project import db
from project.tests.base import BaseTestCase
from sqlalchemy import exc

def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """Tests para el servicio Users."""

    def test_users(self):
        """Asegurando que la ruta /ping  se comporta correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Puede ser agregado"""
        with self.client:
            response = self.client.post(
                '/users',
                data = json.dumps({
                    'username' : 'diego',
                    'email' : 'diegohuarcaya@upeu.edu.pe'
                }),
                content_type = 'application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('diegohuarcaya@upeu.edu.pe was added', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        with self.client:
            response = self.client.post(
                '/users',
                data = json.dumps({'email' : 'diego.huarcaya@upeu.edu.pe'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        with self.client:
            self.client.post(
                '/users',
                data = json.dumps({
                    'username': 'diego',
                    'email': 'diegocrafter@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data = json.dumps({
                    'username': 'diego',
                    'email': 'diegocrafter@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('That mail already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        user = add_user('diego','diegohuarcaya@upeu.edu.pe')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('diego', data['data']['username'])
            self.assertIn('diegohuarcaya@upeu.edu.pe', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('Fail', data['status'])

    def test_single_user_incorrect_id(self):
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('Fail', data['status'])

    def test_all_users(self):
        add_user('luis', 'luis@upeu.edu.pe')
        add_user('daniel','daniel@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']),2)
            self.assertIn('luis', data['data']['users'][0]['username'])
            self.assertIn('luis@upeu.edu.pe', data['data']['users'][0]['email'])
            self.assertIn('daniel', data['data']['users'][1]['username'])
            self.assertIn('daniel@gmail.com', data['data']['users'][1]['email'])




if __name__ == '__main__':
    unittest.main()
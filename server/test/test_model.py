import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from main import app, db 
from models.model import Device, Parameter, DataReading


class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask application context
        cls.app_context = app.app_context()
        cls.app_context.push()

        # Initialize the database for testing
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Clean up the database after testing
        db.drop_all()

        # Pop the Flask application context
        cls.app_context.pop()


    def test_device_model(self):
        device = Device(name='Tests Devices')
        db.session.add(device)
        db.session.commit()

        self.assertIsNotNone(device.id)
        self.assertEqual(device.name, 'Tests Devices')

    def test_parameter_model(self):
        device = Device(name='Test Devices')
        parameter = Parameter(name='Test Parameters', type_='Test Types', device=device)
        db.session.add(parameter)
        db.session.commit()

        self.assertIsNotNone(parameter.id)
        self.assertEqual(parameter.name, 'Test Parameters')
        self.assertEqual(parameter.type_, 'Test Types')
        self.assertEqual(parameter.device, device)

    def test_data_reading_model(self):
        device = Device(name='Test Devices')
        parameter = Parameter(name='Test Parameters', type_='Test Types', device=device)
        data_reading = DataReading(value='Test Values', timestamp='2024-05-13', parameter=parameter)
        db.session.add(data_reading)
        db.session.commit()

        self.assertIsNotNone(data_reading.id)
        self.assertEqual(data_reading.value, 'Test Values')
        self.assertEqual(data_reading.timestamp, '2024-05-13')
        self.assertEqual(data_reading.parameter, parameter)

if __name__ == '__main__':
    unittest.main()

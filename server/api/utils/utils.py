import json
import os
from datetime import datetime
from models.model import Device, Parameter, DataReading
from ext.ext import db
from flask import abort 


class FetchData:

	def __init__(self, data = None ,filename='sample.json'):
		"""
		Construct and initialize the the dataset
		"""
		if data is None:
			self.data = self.load_file(filename)
		else:
			self.data = data

	def load_file(self,filename):
		"""
		Load the file and retrive that dataset contents within the file
		"""
		try:
			current_dir = os.path.dirname(os.path.abspath(__file__))
			parent_dir = os.path.dirname(current_dir)
			json_file_path = os.path.join(parent_dir, 'json_data', filename)

			with open(json_file_path, 'r') as f:
				data = json.load(f)
			
			return data
		except FileNotFoundError :
			abort(404,"Data File Not Found")


	def getDevices(self):
		"""
		Get the list of Devices and its parameter
		"""
		devices = []
		for device_name in self.data.keys():
			devices.append((device_name,self.data[device_name]))			
		return devices
				

class AddToDatabase:

	def add_device_to_database(device_name):
		"""
		Add a device to the database if it does not exist.
		"""
		existing_device = Device.query.filter_by(name=device_name).first()
		if not existing_device:
			new_device = Device(name=device_name)
			db.session.add(new_device)
			db.session.commit()
			return new_device
		return existing_device

	def add_parameter_to_database(device_id, parameter_name, parameter_type):
		"""
		Add a parameter to the database.
		"""
		new_parameter = Parameter(name=parameter_name, type_=parameter_type, device_id=device_id)
		db.session.add(new_parameter)
		db.session.commit()
		return new_parameter

	def add_data_reading_to_database(parameter_id, value, timestamp):
		"""
		Add a data reading to the database.
	    """
		new_data_reading = DataReading(value=value, timestamp=timestamp, parameter_id=parameter_id)
		db.session.add(new_data_reading)
		db.session.commit()

	def parse_iso_timestamp(iso_timestamp):
		"""
		Parse ISO format timestamp string to datetime object.
		"""
		try:
			timestamp = datetime.fromisoformat(iso_timestamp)
			formatted_timestamp = datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
			return formatted_timestamp
		except ValueError:
	        # Handle datetime parsing error
			return None
	
	def check_if_exists_in_database(timestamp, value):
		"""
		Check if the data readings Exists
		"""
		exist = DataReading.query.filter_by(timestamp=timestamp, value=value).first()
		if exist:
			return True
		return False
# api = FetchData()
# print(api.getDevices()[1])
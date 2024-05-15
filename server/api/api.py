# Import necessary modules and components from Flask
from flask import Blueprint, request, jsonify, make_response
from models.model import Device, Parameter, DataReading
from .utils.utils import FetchData, AddToDatabase
import datetime
import jwt

from functools import wraps


# Create a Blueprint for the API endpoints
api = Blueprint("api", __name__, template_folder="templates", static_folder="static")


def token_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		data = request.get_json()
		token = data.get('token')
		if not token or token == None:
			return jsonify({'message':'Token is missing', 'status':'error'})
		try:
			_ = jwt.decode(token, api.secret_key, algorithms=["HS256"])
		except Exception as e:
			return jsonify({'message': f'Token  {e} , try request new token', 'status':'error'})

		return f(*args, **kwargs)
	return wrapper



@api.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == "POST":
		data = request.get_json()
		user = data.get('user')
		password = data.get('password')
		if not password or not user:
			return jsonify({'message': 'Please provide the user and password as request body data ', 'status':'success'})
		if password == api.secret_password:

			token = jwt.encode({'user':user, 'exp': datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)},api.secret_key)


			return jsonify({'token': token, 'status':'success'}), 201

		return jsonify({'message':'Authentication failed', 'status':'error' }), 401

	return jsonify({'message':'Error Could not verify', 'status':'error' }), 401



# Endpoint for loading data into the database
@api.route('/load_data', methods=['POST'])
@token_required
def initialize_data():
    # Instantiate FetchData class to fetch data
    fetch_data = FetchData()
    # Retrieve devices and their parameters
    devices = fetch_data.getDevices()
    exists = None
    count = 0
    # Loop through each device and its parameters
    for device_info in devices:
        device_name, parameters_info = device_info
        
        # Add device to the database
        device = AddToDatabase.add_device_to_database(device_name)
        
        # Add parameters for the device
        for parameter_info in parameters_info:
            parameter_name = parameter_info['parameter']
            parameter_type = parameter_info['type']
            
         	# Parse timestamp and add data reading for the parameter
            timestamp = AddToDatabase.parse_iso_timestamp(parameter_info['timestamp'])
            if timestamp:
	    		#check of the timestamp and the value exists in the database
	            if AddToDatabase.check_if_exists_in_database(timestamp, parameter_info['value']) == True:
	                count += 1
	                exists = True
	            else:
	            	#add  add data reading for the parameter 
	                parameter = AddToDatabase.add_parameter_to_database(device.id, parameter_name, parameter_type)
	                AddToDatabase.add_data_reading_to_database(parameter.id, parameter_info['value'], timestamp)
    if exists:
    	return jsonify({'message':'data readings already exists', "status":"warning", "count":count}), 401

    return jsonify({'message':'data loaded succssfully','status': 'success'}), 200

# Function to retrieve numeric or text data for parameters
def get_numeric_or_text(devices, type_):
    parameters = [param.name for param in devices.parameters if param.type_ == type_]
    values = []
    timestamps = []
    
    # Retrieve values and timestamps for parameters
    for param in devices.parameters:
        if param.type_ == type_:
            readings = param.data_readings
            if readings:
                values.append(readings[0].value)
                timestamps.append(readings[0].timestamp)
    
    return {"parameters": parameters, "values": values, "timestamp": timestamps}, 200

# Endpoint for visualizing data
@api.route('/visualize', methods=["POST", "GET"])
@token_required
def visualize():
    # Check request method
    if request.method == 'POST':
        data = request.get_json()
    else:
        # Default data for visualization if not provided in the request
        data = {
            'device_name': 'device.foo',
            'parameter_name': 'parameter.foo',
            'start_time': '2024-03-05',
            'end_time': '2024-05-08',
        }

    # Retrieve device based on device name
    try:
    	_ = data['device_name']
    	_ = data['parameter_name']
    	_ = data['start_time']
    	_ = data['end_time']
    except KeyError as e:
    	return jsonify({"message":"Falid to Load device", "status":"error", "errMessage":f"{e} Key not found"})
    except Exception as e:
    	return jsonify({"message":"Falid to Load device", "status":"error", "errMessage":f"{e}"})
    # Check if device exists

    device = Device.query.filter_by(name=data['device_name']).first()
    if device:
        
        # If parameter name is not provided, retrieve numeric and text data for all parameters
        if data['parameter_name'] == "":
            numeric_values = get_numeric_or_text(device, 'numeric')
            text_values = get_numeric_or_text(device, 'text')
            return jsonify({"parameter_numeric": numeric_values, "parameter_text": text_values}), 200
        else:
            # If parameter name is provided, retrieve data for the specified parameter
            parameter_name = data['parameter_name']
            parameter = Parameter.query.filter_by(name=parameter_name, device_id=device.id).all()
            
            # Check if parameter exists
            if parameter:
                readings = [data for data in [param.data_readings for param in parameter]  ]
                
                values = [reading[0].value for reading in readings if (datetime.datetime.strptime(reading[0].timestamp, '%Y-%m-%d %H:%M:%S.%f')>=datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S.%f') and datetime.datetime.strptime(reading[0].timestamp, '%Y-%m-%d %H:%M:%S.%f') <=datetime.datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S.%f') )]
                timestamps = [reading[0].timestamp for reading in readings if (datetime.datetime.strptime(reading[0].timestamp, '%Y-%m-%d %H:%M:%S.%f')>=datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S.%f') and datetime.datetime.strptime(reading[0].timestamp, '%Y-%m-%d %H:%M:%S.%f') <=datetime.datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S.%f' ))]
                
                try:
                    _ = list(map(float, values))
                    # Check if values are numeric
                    return jsonify({"parameter_name": parameter_name, "values": values[::-1], "timestamp": timestamps[::-1], "type": "numeric"}), 200
                except ValueError:
                    # If values are not numeric, treat them as text
                    return jsonify({"parameter_name": parameter_name, "values": values[::-1], "timestamp": timestamps[::-1], "type": "text"}), 200
            else:
                # Return error if parameter not found
                return jsonify({"message": f"Provided Parameter '{data['parameter_name']}' not found in device '{data['device_name']}'", 'status':'error'}), 404
    else:
        # Return error if device not found
        return jsonify({"error": "Device not found"}), 404

# Endpoint for retrieving devices and their parameters
@api.route('/device', methods =["POST", "GET"])
@token_required
def get_device():
    data = {}
    # Retrieve all devices
    devices = Device.query.all()
    if len(devices) <= 0 :
    	return jsonify({"message": " Database Empty No Devices Found","status": "info"})
    # Store device names and their parameters in dictionary
    data['devices'] = [device.name for device in devices]
    for device in devices:
        parameters = Parameter.query.filter_by(device_id=device.id).all()
        data[device.name] = [param.name for param in parameters]

    return jsonify(data)

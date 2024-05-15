This API provides endpoints for loading data into a database, visualizing data, and retrieving information about devices and their parameters.

## Setup

### For sever side

0. Open new terminal

1. Navigate to the `server` folder

2. start the virtual environment using command	
-> ` source venv/bin/activate `

3. start the sever using command 
-> `python main.py`

4. the server will run on `localhost` `port 8080`


==========for Frontend============ 

0. open new terminal window 

1. navigate to the Frontend dir

4. run the client by using command
-> ` npm run dev `

markdown


## Endpoints
### LOG IN
- **URL:** `/api/login`
- **Method:** POST
- **Description:** Loads data into the database from an external data source.
- **Usage:** Access this endpoint to initialize the database with data.


### Load Data
- **URL:** `/api/load_data`
- **Method:** POST
- **Description:** Loads data into the database from an external data source.
- **Usage:** Access this endpoint to initialize the database with data.

### Visualize Data
- **URL:** `/api/visualize`
- **Method:** POST 
- **Description:** Visualizes data based on device and parameter name.
- **Usage:** 
- Provide JSON data with device and parameter name to visualize specific data.
- If no parameters are provided, numeric and text data for all parameters will be returned.

### Device Information
- **URL:** `/api/device`
- **Method:** POST
- **Description:** Retrieves information about devices and their parameters.
- **Usage:** Access this endpoint to get a list of devices and their associated parameters.





### API Routes Usage Guide

This guide provides an overview of the routes available in the API along with instructions on how to interact with each route.
Authentication

**Before using any other routes, authentication is required. This is done via a token-based authentication system.**
- **URL:** `/api/login` - POST

    Description: Authenticate and obtain a token for accessing protected routes.
    Request Method: POST
    Request Body:

    - **request json**

    {
        "user": "username",
        "password": "user_password"
    }

    -**Response**:
        token: JWT token for authentication.
        status: Status of the request (success or error).

## Data Loading

This route is used to load data into the database.
- **URL:** `/api/load_data` - POST

    Description: Load data into the database.
    Request Method: POST
    Authorization: Token required

     - **request json**

    	{
        	"token": "token_here_as_value"
        }

    - **Response**:
        message: Message indicating the status of data loading.
        status: Status of the request (success, error, or warning).
        count: Count of existing data readings if any.

## Visualization

This route allows visualization of data.
- **URL:** `/api/visualize` - POST 

    Description: Visualize data based on device name, parameter name, start time, and end time.
    Request Method: POST or GET
    Authorization: Token required
    Request Body (POST):

    - **request json**

    {
        "device_name": "device_name",
        "parameter_name": "parameter_name",
        "start_time": "start_time",         - time format ( %Y-%M-%D %H:%M:%S.%f ) ( 2024-05-07 20:21:1.0 ) 
        "end_time": "end_time",				- time format ( %Y-%M-%D %H:%M:%S.%f ) ( 2024-05-07 20:21:1.0 )
        "token": "token_here"
    }

    - **Response**:
        parameter_numeric: Numeric data for parameters.
        parameter_text: Textual data for parameters.
        status: Status of the request (success or error).

## Device Information

This route provides information about devices and their parameters.
- **URL:** `/api/device` - POST 

    Description: Retrieve devices and their parameters.
    Request Method: POST or GET
    Authorization: Token required
     - **request json**

    {
        "token": "token_here"
        
    }
    Response:
        devices: List of device names.
        Device-wise parameters.
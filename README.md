# Cab System

## Description
This web application allows users to book cabs by entering their source and destination, and provides the shortest time and estimated cost for the trip.

## Technologies used
Frontend: Vue.Js, TailwindCSS <br>
Backend: Flask(Python), SQLite3 (database)

## Features
- Shortest possible time calculation
- Estimated cost calculation
- Cab booking 
- Cab and pricing management
- Email notification

## Database Schema
![DB Schema](https://user-images.githubusercontent.com/81559176/229356864-f31dde54-9c7b-449a-8555-23dd0b0928a7.png)

## Installation Guide
### Frontend Installation (Works for both Windows and Linux):
#### Prerequisites:
- Node.js installed on your computer
- A code editor of your choice (e.g. Visual Studio Code)

#### Step 1: Clone the repository
Clone the repository from GitHub by running the following command in your terminal:
```
git clone https://github.com/Aakarshit-Dhuria/Cab-System-Scaler-Project.git
```

#### Step 2: Navigate to the project directory:
```
cd Cab-System-Scaler-Project
```
```
cd frontend
```

#### Step 3: Install dependencies
Navigate to the project directory by running cd frontend and install the dependencies by running the following command:
```
npm install
```
This command installs all the dependencies required for the project to run.

#### Step 4: Start the development server
To start the development server, run the following command:
```
npm run serve
```
This command compiles and serves your project, and you should see a message indicating that the server is running. You can now access your Vue application by visiting http://localhost:8080 in your web browser.


### Backend Installation (For Windows):
#### Prerequisites:
- Python 3.x installed on your computer
- A code editor of your choice (e.g. Visual Studio Code)

#### Step 1: Clone the repository
Clone the repository from GitHub by running the following command in your terminal:
```
git clone https://github.com/Aakarshit-Dhuria/Cab-System-Scaler-Project.git
```

#### Step 2: Navigate to the project directory:
```
cd Cab-System-Scaler-Project
```
```
cd backend
```

#### Step 3: Create a virtual environment for the Cab System project:
```
python -m venv env
```

#### Step 4: Activate the virtual environment:
```
.\env\Scripts\activate
```

#### Step 5: Install the required Python packages:
```
pip install -r requirements.txt
```

#### Step 6: Set the FLASK_APP environment variable to main.py:
```
set FLASK_APP=main.py
```

#### Step 7: Start the Flask server and run the Cab System application:
```
python main.py
```
The backend should now be accessible at http://localhost:8000/


### Backend Installation (For Linux):
#### Prerequisites:
- Python 3.x installed on your computer
- A code editor of your choice (e.g. Visual Studio Code)

#### Step 1: Clone the repository
Clone the repository from GitHub by running the following command in your terminal:
```
git clone https://github.com/your-username/cab-system.git
```

#### Step 2: Navigate to the project directory:
Navigate to the project directory by running cd backend:
```
cd backend
```

#### Step 3: Run these two commands:
```
sh local_setup.sh
```
```
sh local_run.sh
```
These two files contain all the required commands to be run for setting up and running the backend.

The backend should now be accessible at http://localhost:8000/

## Pages
### Home Page
The home page displays a booking form where users can enter their email, source, destination, and select a cab. On selecting the source and destination, the application displays the cost for each cab and estimated time it will take to reach the destination. When the user clicks the "Book Now" button, the selected cab will get booked.

### Cabs Page
The cabs page displays a list of cabs and their pricing. Admins can view and edit the cabs and their pricing on this page.

## API Documentation
The API documentation for the Cab System project is included in the file `api_documentation.yml` in the root directory of this repository. This file contains detailed information on all the endpoints used in the project, as well as example requests and responses.

To view the API documentation, you can either open the `api_documentation.yml` file in a text editor or use a tool like [Swagger UI](https://swagger.io/tools/swagger-ui/) to render the documentation in a more user-friendly format.

## Usage
- Open the web application in a browser.
- On the home page, enter your email, source, and destination in the booking form and select a cab.
- The estimated time and cost will be displayed on the screen.
- Click the "Book Now" button to book the cab.
- On the cabs page, you can view and edit the cabs and their pricing.


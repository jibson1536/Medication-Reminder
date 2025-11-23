# Flask Project

## Overview
This is a Flask web application designed to serve as a medication reminder system. The application allows users to manage their medication schedules, receive reminders, and track adherence.

## Project Structure
```
flask-project
├── app
│   ├── __init__.py
│   ├── main
│   │   ├── __init__.py
│   │   ├── routes.py
│   └── templates
│       └── base.html
│   └── static
│       ├── css
│       │   └── styles.css
│       ├── js
│       │   └── scripts.js
│       └── images
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd flask-project
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python run.py
   ```
2. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

## Features
- User authentication
- Medication management
- Reminder notifications
- Adherence tracking

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
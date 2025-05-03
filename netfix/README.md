# NetFix - Home Services Management System

NetFix is a Django-based web application that connects homeowners with service providers for various home maintenance and repair needs.

## Features

- User authentication (Customers and Service Providers)
- Service listing and management
- Service request system
- Multiple service categories including:
  - Air Conditioning
  - Carpentry
  - Electricity
  - Gardening
  - Home Machines
  - Housekeeping
  - Interior Design
  - Locks
  - Painting
  - Plumbing
  - Water Heaters

## Prerequisites

- Python 3.8 or higher
- pip3 (Python package manager)
- SQLite3

## Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/netfix.git
cd netfix
```

2. Create a virtual environment:
```sh
python3 -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```sh
venv\Scripts\activate
```
- On macOS/Linux:
```sh
source venv/bin/activate
```

4. Change into the netfix project directory (where requirements.txt is located):
```sh
cd netfix
```

5. Install dependencies from requirements.txt:
```sh
pip3 install -r requirements.txt
```

6. Apply database migrations:
```sh
python3 manage.py migrate
```

7. Create a superuser:
```sh
python3 manage.py createsuperuser
```

8. Run the development server:
```sh
python3 manage.py runserver
```

The application will be available at `http://localhost:8000`

## Project Structure

```
netfix/
├── main/           # Main application module
├── services/       # Services management module
├── users/          # User authentication and management
├── static/         # Static files (CSS, JS, images)
├── templates/      # HTML templates
└── netfix/         # Project configuration
```

## Database Configuration

The project uses SQLite3 as the default database. Database settings can be found in `netfix/settings.py`.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
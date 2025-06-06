# BCityAssesmment2025
Basic Data Capturing App Binary City June 2025


# ClientContactApp

A basic Flask app for managing clients and contacts, with many-to-many relationships and AJAX-based linking/unlinking.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.
pip install flask flask_sqlalchemy
export FLASK_APP=app:create_app

from powershell
$env:FLASK_APP = "app.py"
flask run
```

## Features

- Create & list clients and contacts
- Link/unlink contacts and clients (many-to-many, AJAX)
- Auto-generated client codes based on initials
- Clean HTML UI with simple CSS
- SQLite default database (easy to swap for PostgreSQL, etc.)

## Deployment (Heroku/Fly.io/etc)

- Make sure `requirements.txt` and `Procfile` are present.
- Change `SQLALCHEMY_DATABASE_URI` to use PostgreSQL for production!

## Summary

ClientContactApp is a simple Flask web application designed to manage clients and their associated contacts. It follows the MVC (Model-View-Controller) pattern using Flask and SQLAlchemy for database interactions. The app allows users to:

- Add, edit, and delete clients and contacts
- Link and unlink clients to contacts
- View lists of all clients and contacts
- Display linked clients with the ability to unlink
- Validate email addresses and handle errors gracefully

The application uses SQLite for storage, Jinja2 templates for rendering views, and provides a clean, user-friendly interface for managing client-contact relationships.

## Summary Table

Step	Command / Action	Purpose
- 1	cd path/to/your/project	Go to project folder
- 2	python -m venv venv<br>source venv/bin/activate	Create & activate virtual environment
- 3	pip install -r requirements.txt	Install dependencies
- 4	python sample_data.py	Create/populate database with test data
- 5	flask run or python app.py	Start the Flask development server
- 6	Visit http://localhost:5000/	See your app in the browser
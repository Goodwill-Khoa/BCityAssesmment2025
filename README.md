# BCityAssesmment2025
Basic Data Capturing App Binary City June 2025


# ClientContactApp

A basic Flask app for managing clients and contacts, with many-to-many relationships and AJAX-based linking/unlinking.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app:create_app
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

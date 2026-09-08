# web-programming-2026-template

A lightweight Django starter with one neutral homepage, SQLite, and Django's
standard admin, authentication, sessions, and staticfiles support.

`requirements.txt` pins Django 6.1.1, asgiref 3.12.1, and sqlparse 0.6.0.

## Local setup

Requires Python 3.12 or newer (tested with Python 3.14). Run these commands
from the project directory containing `manage.py`.

1. Create and activate a virtual environment (Linux/macOS):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Apply migrations to create the local SQLite database:

   ```bash
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Endpoints

With the server running at `http://127.0.0.1:8000`:

| URL | Page |
| --- | --- |
| http://127.0.0.1:8000/ | Homepage: “Your project starts here” |
| http://127.0.0.1:8000/admin/ | Django admin (requires an admin account) |

To create an account for the admin site, run this after applying migrations:

```bash
python manage.py createsuperuser
```

## Development only

The included settings use `DEBUG = True`, a development secret key, and a local
SQLite database. This configuration and Django's development server are not
suitable for production deployment.
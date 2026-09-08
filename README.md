# web-programming-2026-template

A Django project with greeting pages and a to-do list.

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
| http://127.0.0.1:8000/ | Basic greeting |
| http://127.0.0.1:8000/fancy-hello | Greeting with a header |
| http://127.0.0.1:8000/Ada | Personal greeting (`Ada` can be replaced with another name) |
| http://127.0.0.1:8000/todolist/ | Task list |
| http://127.0.0.1:8000/todolist/add/ | Add a task |
| http://127.0.0.1:8000/admin/ | Django admin (requires an admin account) |

The greeting routes `/fancy-hello` and `/<name>` do not have trailing slashes.

## Development only

The included settings use `DEBUG = True`, a development secret key, and a local
SQLite database. This configuration and Django's development server are not
suitable for production deployment.
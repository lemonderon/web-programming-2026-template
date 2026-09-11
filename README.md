# web-programming-2026-template

A reusable Django project with no bundled application, SQLite, and Django's
standard admin, authentication, sessions, messages, and staticfiles support.

## Local setup

Requires the latest patch release of Python 3.12, 3.13, or 3.14, with SQLite
3.37.0 or newer. Run these commands from the project directory containing
`manage.py`.

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   
   # for linux/macos
   source .venv/bin/activate
   # for Windows:
   .venv\Scripts\activate.ps1 
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements-dev.txt
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

| URL | Behavior |
| --- | --- |
| http://127.0.0.1:8000/ | No application homepage; may show Django's development welcome page while `DEBUG = True` |
| http://127.0.0.1:8000/admin/ | Django admin, available after applying migrations |

With `DEBUG = False`, unmatched URLs such as `/` return HTTP 404.

To create an account for admin login, run this after applying migrations:

```bash
python manage.py createsuperuser
```

## Add your first application

1. Create an app from the directory containing `manage.py` (replace `myapp`
   with your application name):

   ```bash
   python manage.py startapp myapp
   ```

2. Add its generated configuration class, `myapp.apps.MyappConfig`, to
   `INSTALLED_APPS` in `mysite/settings.py`.
3. Define your views and create `myapp/urls.py` with their URL patterns.
4. Register that URLconf in `mysite/urls.py` using `path()` and `include()`,
   choosing a URL prefix for the app and retaining the admin route.

See the official Django 6.1 tutorial for
[views and URL registration](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)
and [app registration and models](https://docs.djangoproject.com/en/6.1/intro/tutorial02/).

## Code style and submission verification

All submissions are required to adhere to PEP-8, Django best practices, and standard HTML/CSS/JS formatting. A deterministic cross-platform utility is provided to help you check and format your code.

### 1. Verification (Check Mode)
Before submitting, verify that all files adhere to the required standards:

```bash
python check_submission.py
```

If all checks pass, you are ready to submit! If any checks fail, review the error output or run the auto-formatter below.

### 2. Auto-Formatting
To automatically format Python files, fix safe PEP-8 rules, format Django HTML templates, and format CSS/JS static files:

```bash
python check_submission.py --format
```

### 3. PyCharm Integration
If you use PyCharm:
- **One-Click Run:** In the top-right toolbar run configurations dropdown, select **"Verify Submission"** or **"Format Project"** and click the green **Play** button.

## Development only

The included settings use `DEBUG = True`, a development secret key, and a local
SQLite database. The default mailer uses the console backend: email is printed
to the process's console instead of being delivered.

This configuration and Django's development server are not suitable for
production deployment.

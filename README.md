# USIU-A Lost & Found System

A Flask web application for reporting, tracking, and reclaiming lost items on the
USIU-A campus. Students report found items and file ownership claims; security
officers verify items into the vault and adjudicate claims. All data is stored in
a local SQLite database.

## Features

- **Role-based portal** — separate dashboards for **students** (finders/owners) and
  **security officers**, with login and self-service signup.
- **Item lifecycle** — every reported item moves through
  `Pending Security → Checked-In → Claimed`.
- **Claim workflow** — ownership claims are linked to the item being claimed;
  security can **approve** (which releases the item and marks it `Claimed`) or **deny** them.
- **Photo uploads** — finders attach a photo of the item; images render in both dashboards.
- **Security hardening**
  - Passwords are stored hashed (never in plain text).
  - Sensitive routes require the correct logged-in role.
  - Uploads are restricted to images (`png/jpg/jpeg/webp/gif`), capped at 5 MB, and
    saved with unique filenames.
  - Account signup requires an official `@usiu.ac.ke` email address.

## Tech stack

- Python 3 + Flask (Werkzeug)
- SQLite (standard library `sqlite3`)
- Server-rendered Jinja2 templates, plain CSS/JS (no build step)

## Project structure

```
usiulostnfound_app.py         # Flask app: routes, auth, upload handling
usiulostnfound_database.py    # Schema + connection helper (init_db, get_connection)
seed_mockdata.py              # Populates demo items, claims, and student accounts
requirements.txt              # Python dependencies
lostandfound.db               # SQLite database (created automatically at runtime)
static/
  templates/Lostandfound.html # Main UI (login, student, and security views)
  usiulostnfound.css          # Styles
  usiulostnfound.js           # Client-side interactions
  uploads/                    # Item photos
```

## Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
```

## Running

```bash
python usiulostnfound_app.py
```

The database and tables are created automatically on first run. Then open:

- **http://127.0.0.1:5000/** — redirects to the portal login / dashboard

## Loading demo data (optional)

To populate the app with realistic sample items (with photos), demo claims, and
test student accounts:

```bash
python seed_mockdata.py
```

This resets the items/claims tables to a fresh demo set each time; user accounts are preserved.

## Test accounts

| Role     | ID          | Password      |
|----------|-------------|---------------|
| Security | `123456789` | `password123` |
| Student  | `100200`    | `pass123`     |
| Student  | `205311`    | `pass123`     |

> Student IDs are 6 digits; security officer badge IDs are 9 digits.

## Configuration

The Flask session secret key is read from the `SECRET_KEY` environment variable,
falling back to a development default. Set your own in any real deployment:

```bash
export SECRET_KEY="your-own-long-random-value"
```

## Notes

- This runs on Flask's built-in development server (`debug=True`) — for local/demo
  use only, not production.
- `lostandfound.db` and uploaded files are created at runtime.

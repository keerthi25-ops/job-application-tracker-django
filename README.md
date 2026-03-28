# Job Application Tracker

A simple and efficient **Job Application Tracker** to manage, monitor, and organise job applications in one place.  
This project helps job seekers track application status, deadlines, interviews, and follow-ups systematically

🔗 Live Demo: https://job-application-tracker-django-2.onrender.com/

## Tech Stack
- Django
- SQLite
- Bootstrap

## 🚀 Features

- Add new job applications
- Track application status (Applied, Interview, Offer, Rejected)
- Store company and role details
- Application date tracking
- Notes & follow-up reminders
- Easy data viewing and updating
- Clean and beginner-friendly structure

---

## 🛠️ Tech Stack

- **Language:** Python   
- Django
- SQLite
- Bootstrap
---

## 📂 Project Structure
## Database Configuration

The project uses `SQLite` by default for local development.

To switch to `Render Postgres`, set this environment variable before starting Django:

- `DATABASE_URL`

Example:

```text
DATABASE_URL=postgresql://postgres:password@host:5432/jobtracker
```

To switch to `MySQL`, set these environment variables before starting Django:

- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`

Database priority is:

1. `DATABASE_URL` for Postgres
2. `MYSQL_DATABASE` for MySQL
3. local `db.sqlite3` fallback

## Render Deployment Notes

For Render Postgres, add this environment variable in your Render web service:

- `DATABASE_URL`

Render provides this connection string from the Postgres dashboard.

For MySQL, add these environment variables in your Render web service:

- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`

After saving the environment variables, run migrations on the deployed service:

```bash
python manage.py migrate
```

If you need a local reference, copy the values pattern from `.env.example`.

## Backup Workflow

To create a local backup of your project data, run:

```bash
python manage.py backup_project_data
```

This creates two files inside `backups/`:

- a timestamped copy of `db.sqlite3`
- a timestamped JSON export of users and tracker data

To restore JSON data into a fresh database, run:

```bash
python manage.py loaddata backups/data_backup_YYYYMMDD_HHMMSS.json
```

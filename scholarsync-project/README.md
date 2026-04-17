# ScholarSync (Decoupled Django + React)

ScholarSync is a decoupled full-stack project:

- `backend/core` -> Django REST API
- `frontend` -> React application

The UI flow matches the provided screenshots:

- Login
- Signup
- Dashboard
- Search students
- Add/Edit/Delete student modals
- Logout

## Project Structure

```text
scholarsync-project/
|-- backend/
|   `-- core/
|       |-- core/                  # Django settings + URLs
|       |-- accounts/              # Auth APIs
|       |-- students/              # Student CRUD APIs
|       |-- manage.py
|       `-- db.sqlite3
|-- frontend/
|   |-- src/
|   |   |-- api/
|   |   |-- components/
|   |   |-- pages/
|   |   `-- utils/
|   `-- package.json
`-- README.md
```

## Backend Setup (Django)

```powershell
cd backend\core
..\venv\Scripts\python.exe manage.py migrate
..\venv\Scripts\python.exe manage.py runserver
```

Backend runs on `http://127.0.0.1:8000/`.

## Frontend Setup (React)

```powershell
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000/`.

## Render Deployment

This repo includes [render.yaml](</c:/Users/Sudeepa Satapathy/Desktop/scholarsync-project/render.yaml>) for backend deployment.

If you deploy manually on Render, use:

- Root directory: `backend`
- Build command: `pip install -r requirements.txt && cd core && python manage.py migrate && python manage.py collectstatic --no-input`
- Start command: `cd core && gunicorn core.wsgi:application`

Set environment variables in Render:

- `DJANGO_SECRET_KEY` -> any strong secret
- `DJANGO_DEBUG` -> `False`
- `CORS_ALLOW_ALL_ORIGINS` -> `False`
- `CORS_ALLOWED_ORIGINS` -> your frontend URL, for example `https://your-frontend.onrender.com`
- Optional: `DATABASE_URL` -> Render Postgres connection string

Important:
- If `DATABASE_URL` is not set, Django falls back to SQLite.
- `ALLOWED_HOSTS` auto-includes `RENDER_EXTERNAL_HOSTNAME`, so host errors are avoided.

## API Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `GET /api/students/?user_id=<id>&search=<query>`
- `POST /api/students/add/?user_id=<id>`
- `PUT /api/students/update/<student_id>/?user_id=<id>`
- `DELETE /api/students/delete/<student_id>/?user_id=<id>`

## Tests

### Backend tests

```powershell
cd backend\core
..\venv\Scripts\python.exe manage.py test
```

### Frontend tests

```powershell
cd frontend
cmd /c "set CI=true && npm test -- --watchAll=false --runInBand"
```

`--runInBand` is used to ensure stable test execution in restricted environments.

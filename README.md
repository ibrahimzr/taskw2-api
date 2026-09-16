# TaskFlow API

TaskFlow API is a FastAPI task manager with JWT authentication, role-based permissions, SQLModel, and SQLite.

## Features

- User registration and OAuth2 password login
- Argon2 password hashing
- JWT access tokens
- Current-user endpoint
- User and admin roles
- Task create, list, retrieve, update, complete, and delete endpoints
- Task ownership protection for regular users
- Admin access to all tasks
- Status and priority filters
- Pagination with `skip` and `limit`
- Request validation for email, title, priority, and due date
- Interactive Swagger documentation
- CLI script for creating an admin account

## Project Structure

```text
task-manager/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── main.py
├── create_admin.py
└── app/
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── enums.py
    ├── models.py
    ├── security.py
    ├── dependencies.py
    ├── dtos/
    │   ├── __init__.py
    │   ├── requests.py
    │   └── responses.py
    └── routers/
        ├── __init__.py
        ├── auth.py
        └── tasks.py
```

## Setup

Create and activate a virtual environment:

```powershell
py -3.13 -m venv venv313
venv313\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create `.env` from `.env.example` and set a secure `SECRET_KEY`.

Example:

```env
DATABASE_URL=sqlite:///taskflow.db
SECRET_KEY=replace-with-a-secure-secret-key
ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=45
```

## Create an Admin

```powershell
python create_admin.py
```

Enter the admin username, email, and password when prompted.

## Run

```powershell
python -m uvicorn main:app --reload
```

Open Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

## Main Endpoints

### Authentication

- `POST /auth/register` - Register a regular user
- `POST /auth/login` - Login and receive a JWT access token
- `GET /auth/me` - Get the authenticated user

### Tasks

- `POST /tasks` - Create a task
- `GET /tasks` - List accessible tasks with filters and pagination
- `GET /tasks/{task_id}` - Get one task
- `PATCH /tasks/{task_id}` - Partially update a task
- `PATCH /tasks/{task_id}/complete` - Mark a task as done
- `DELETE /tasks/{task_id}` - Delete a task

Regular users can access only their own tasks. Admin users can access all tasks. Requests for another user's task return `404`.

## Notes

- Passwords are never stored or returned as plain text.
- User roles and task ownership are controlled by the server.
- `.env`, SQLite database files, virtual environments, and Python cache files are excluded from Git.

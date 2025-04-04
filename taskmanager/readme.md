### Task Management API

A robust RESTful API for managing tasks, built with Django and Django REST Framework. This API allows users to create, read, update, and delete tasks, as well as mark them as complete or incomplete. It includes user authentication, task filtering, and sorting capabilities.

## Features

- **User Authentication**: Secure JWT-based authentication system
- **Task Management**: Complete CRUD operations for tasks
- **Task Status**: Mark tasks as complete or incomplete with timestamps
- **Filtering & Sorting**: Filter tasks by status, priority, and due date; sort by various fields
- **Data Validation**: Ensures tasks have valid due dates, priorities, and statuses
- **User Ownership**: Users can only access their own tasks
- **RESTful Design**: Follows REST principles with appropriate HTTP methods and status codes


## Prerequisites

- Python 3.8+
- Django 4.2+
- Django REST Framework
- PostgreSQL (recommended for production) or SQLite (development)


## Installation

1. **Clone the repository**


```shellscript
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api
```

2. **Create and activate a virtual environment**


```shellscript
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**


```shellscript
pip install -r requirements.txt
```

4. **Configure environment variables**


Create a `.env` file in the root directory with the following variables:

```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # For development
```

5. **Run migrations**


```shellscript
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser**


```shellscript
python manage.py createsuperuser
```

7. **Run the development server**


```shellscript
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`.

## API Endpoints

### Authentication

| Method | Endpoint | Description
|-----|-----|-----
| POST | `/api/users/` | Register a new user
| POST | `/api/token/` | Obtain JWT token
| POST | `/api/token/refresh/` | Refresh JWT token


### Tasks

| Method | Endpoint | Description
|-----|-----|-----
| GET | `/api/tasks/` | List all tasks for the authenticated user
| POST | `/api/tasks/` | Create a new task
| GET | `/api/tasks/{id}/` | Retrieve a specific task
| PUT | `/api/tasks/{id}/` | Update a specific task
| DELETE | `/api/tasks/{id}/` | Delete a specific task
| PATCH | `/api/tasks/{id}/mark_complete/` | Mark a task as complete
| PATCH | `/api/tasks/{id}/mark_incomplete/` | Mark a task as incomplete


### Filtering and Sorting

- Filter by status: `/api/tasks/?status=pending` or `/api/tasks/?status=completed`
- Filter by priority: `/api/tasks/?priority=high`, `/api/tasks/?priority=medium`, or `/api/tasks/?priority=low`
- Filter by due date: `/api/tasks/?due_date=2023-12-31`
- Sort by due date: `/api/tasks/?ordering=due_date` or `/api/tasks/?ordering=-due_date` (descending)
- Sort by priority: `/api/tasks/?ordering=priority` or `/api/tasks/?ordering=-priority` (descending)
- Sort by creation date: `/api/tasks/?ordering=created_at` or `/api/tasks/?ordering=-created_at` (descending)


## Usage Examples

### Register a new user

```shellscript
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

### Get JWT token

```shellscript
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

### Create a task

```shellscript
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the Task Management API",
    "due_date": "2023-12-31T23:59:59Z",
    "priority": "high"
  }'
```

### List all tasks

```shellscript
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer <your_token>"
```

### Mark a task as complete

```shellscript
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/mark_complete/ \
  -H "Authorization: Bearer <your_token>"
```

## Project Structure

```plaintext
taskmanager/
├── manage.py
├── requirements.txt
├── README.md
├── taskmanager/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tasks/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── permissions.py
    ├── serializers.py
    ├── urls.py
    ├── views.py
    └── tests.py
```

## Data Models

### Task Model

- `title`: The title of the task (required)
- `description`: Detailed description of the task (optional)
- `due_date`: When the task is due (required, must be in the future for new tasks)
- `priority`: Task priority level (`low`, `medium`, or `high`, default is `medium`)
- `status`: Task status (`pending` or `completed`, default is `pending`)
- `created_at`: When the task was created (auto-generated)
- `updated_at`: When the task was last updated (auto-generated)
- `completed_at`: When the task was marked as complete (null if not completed)
- `user`: The owner of the task (foreign key to User model)


## Technologies Used

- **Django**: Web framework
- **Django REST Framework**: API toolkit
- **Simple JWT**: JWT authentication
- **Django Filter**: Advanced filtering
- **PostgreSQL**: Database (recommended for production)
- **Gunicorn**: WSGI HTTP Server (for production)
- **Whitenoise**: Static file serving (for production)


## Deployment

### Deploying to Heroku

1. **Install Heroku CLI and login**


```shellscript
# Install Heroku CLI (if not already installed)
# Follow instructions at: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login
```

2. **Create a Procfile**


```shellscript
echo "web: gunicorn taskmanager.wsgi --log-file -" > Procfile
```

3. **Create a runtime.txt file**


```shellscript
echo "python-3.11.6" > runtime.txt
```

4. **Create a new Heroku app**


```shellscript
heroku create task-management-api
```

5. **Add PostgreSQL add-on**


```shellscript
heroku addons:create heroku-postgresql:mini
```

6. **Configure environment variables**


```shellscript
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DEBUG=False
```

7. **Deploy to Heroku**


```shellscript
git add .
git commit -m "Initial deployment"
git push heroku main
```

8. **Run migrations on Heroku**


```shellscript
heroku run python manage.py migrate
```

9. **Create a superuser on Heroku**


```shellscript
heroku run python manage.py createsuperuser
```

## Testing

Run the tests with:

```shellscript
python manage.py test
```

### Testing with Postman

1. Import the provided Postman collection (if available)
2. Set up environment variables:

1. `base_url`: `http://127.0.0.1:8000` (for local testing)
2. `token`: Leave empty (will be filled automatically)



3. Run the "Get Token" request first to authenticate
4. Test other endpoints as needed


## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Django and Django REST Framework documentation
- JWT authentication implementation based on Simple JWT
- Task management concepts inspired by productivity applications
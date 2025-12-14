# Task Tracker API

A production-ready RESTful API for managing tasks with JWT authentication stored in HTTP-only cookies, built with Django REST Framework.

## Features

- **Cookie-based JWT Authentication**: Secure HTTP-only cookies for token storage (XSS protection)
- **Email Login**: Login using email and password
- **User Registration**: Create new accounts with validated passwords
- **Task Management**: Full CRUD operations for personal tasks
- **Task Privacy**: Each user can only access their own tasks
- **Filtering**: Filter tasks by status, priority, due date, and overdue status
- **Search**: Search tasks by title and description
- **Ordering**: Sort tasks by creation date, due date, priority, or status
- **Pagination**: Paginated responses for efficient data loading
- **API Documentation**: Interactive Scalar-powered API documentation
- **Statistics**: Get task statistics by status and priority

## Installation

### Prerequisites

- Python 3.10+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kunalsinghdadhwal/dj-track
   cd dj-track
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - API: http://localhost:8000/api/
   - Documentation: http://localhost:8000/docs/
   - Admin: http://localhost:8000/admin/

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login with email & password |
| POST | `/api/auth/logout/` | Logout and clear cookies |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET | `/api/auth/verify/` | Verify token validity |
| GET | `/api/auth/me/` | Get current user profile |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List all tasks |
| POST | `/api/tasks/` | Create new task |
| GET | `/api/tasks/{id}/` | Get task details |
| PUT | `/api/tasks/{id}/` | Update task |
| PATCH | `/api/tasks/{id}/` | Partial update task |
| DELETE | `/api/tasks/{id}/` | Delete task |
| GET | `/api/tasks/stats/` | Get task statistics |
| POST | `/api/tasks/{id}/complete/` | Mark task as complete |

### Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/docs/` | Scalar interactive docs |
| GET | `/api/schema/` | OpenAPI schema (JSON) |
| GET | `/api/docs/swagger/` | Swagger UI |
| GET | `/api/docs/redoc/` | ReDoc |

## Authentication

### Cookie-based Authentication (Recommended for Browsers)

The API uses HTTP-only cookies for secure token storage:

1. **Login** at `/api/auth/login/` with email and password
2. Cookies are automatically set:
   - `access_token`: Short-lived access token (30 min)
   - `refresh_token`: Long-lived refresh token (7 days)
3. Include cookies in subsequent requests (automatic in browsers)
4. **Refresh** tokens at `/api/auth/refresh/` before access token expires
5. **Logout** at `/api/auth/logout/` to clear cookies and blacklist tokens

### Bearer Token Authentication (For API Clients)

For non-browser clients, use the Authorization header:

```
Authorization: Bearer <access_token>
```

## Configuration

### Cookie Settings (in settings.py)

```python
SIMPLE_JWT = {
    'AUTH_COOKIE': 'access_token',
    'AUTH_COOKIE_REFRESH': 'refresh_token',
    'AUTH_COOKIE_SECURE': True,       # HTTPS only in production
    'AUTH_COOKIE_HTTP_ONLY': True,    # XSS protection
    'AUTH_COOKIE_SAMESITE': 'Lax',    # CSRF protection
}
```

### Token Lifetimes

- Access Token: 30 minutes
- Refresh Token: 7 days

### Pagination

Default page size: 10 items per page

## API Documentation

Visit `/docs/` for interactive API documentation powered by Scalar. This provides:
- Complete endpoint documentation
- Request/response examples
- Authentication testing
- Code snippets in multiple languages

Alternative documentation:
- Swagger UI: `/api/docs/swagger/`
- ReDoc: `/api/docs/redoc/`
- Raw OpenAPI Schema: `/api/schema/`

## Security Features

- **HTTP-only Cookies**: Tokens stored in HTTP-only cookies prevent XSS attacks
- **Short-lived Access Tokens**: 30 minute lifetime limits exposure
- **Token Rotation**: Refresh tokens are rotated on use
- **Token Blacklisting**: Logout invalidates refresh tokens
- **SameSite Cookies**: Protection against CSRF attacks
- **User Isolation**: Users can only access their own tasks
- **Password Validation**: Django's built-in password validators

## Production Deployment

1. Set `DEBUG=False`
2. Configure a proper `SECRET_KEY`
3. Switch to PostgreSQL
4. Set up HTTPS (required for secure cookies)
5. Configure `ALLOWED_HOSTS`
6. Set `AUTH_COOKIE_SECURE=True`
7. Use environment variables for sensitive data
8. Set up proper CORS settings
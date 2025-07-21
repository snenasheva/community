# Community Business Directory

A full-featured Flask web application for listing and discovering local businesses — developed as a community project for Pardes Hanna-Karkur, Israel.

## Platform Overview

The platform allows:

- Business owners to create and manage their own pages  
- Local residents to browse and find services easily

Designed with a clean UI, secure authentication, and scalable architecture using Docker and SQLite.

---

## Key Features

- User registration and login with secure password hashing (`Flask-Login`, `Flask-Bcrypt`)
- Add and manage local business listings
- Categorized business browsing (e.g., construction, food, entertainment)
- Full-text search with partial match support
- Email verification, password reset, and account deletion (`Flask-Mail`, `JWT`)
- SQLAlchemy ORM + Alembic for migrations
- Google OAuth2 integration ready
- Docker support for containerized deployment

---

## Business Listings Overview

- Users can create one or more listings  
- Listings are organized by predefined categories  
- Business cards appear on:
  - Home carousel
  - Category pages
  - Search results

---

## Getting Started

### Clone and Run with Docker

```bash
git clone https://github.com/snenasheva/community.git
cd community
docker build -t community-app .
docker run -p 5000:5000 community-app
```

Development Setup (Without Docker)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Configuration

Create a .env file or set environment variables manually:

```env
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=sqlite:///community.db
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_key
```

# Email settings (for Flask-Mail)

```
MAIL_SERVER=smtp.googlemail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_password
```
 Database Migrations

```
flask db init   	# Run once to initialize
flask db migrate -m "Add something"
flask db upgrade
```

Business Form Fields
| Field         | Type          | Validation                          |
| ------------- | ------------- | ----------------------------------- |
| Business Name | `StringField` | Required, unique                    |
| Category      | `SelectField` | Required, 30+ predefined categories |
| Description   | `StringField` | Optional, max 120 characters        |
| Owner Name    | `StringField` | Required, unique among businesses   |
| Phone         | `StringField` | Optional, numeric, 10–13 characters |
| Address       | `StringField` | Optional, min 3 characters          |
| Web Page      | `StringField` | Optional                            |

Routes Overview

| Route                   | Method(s) | Description                            |
| ----------------------- | --------- | -------------------------------------- |
| `/business`             | GET/POST  | Business creation form                 |
| `/service/<url>`        | GET       | View a specific business profile       |
| `/service/edit/<url>`   | GET/POST  | Edit an existing business (owner only) |
| `/service/delete/<url>` | POST      | Delete a business listing (owner only) |


Contributing

Feel free to open an issue, submit a pull request, or reach out with questions or suggestions. Contributions, feedback, and collaboration are always welcome!




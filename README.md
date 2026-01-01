# Employee Management System - Flask CRUD Application

A complete, production-ready CRUD (Create, Read, Update, Delete) application built with Flask and MySQL for managing employee records.

## Features

✨ **Full CRUD Operations**
- Create new employee records
- Read/View all employees in a responsive table
- Update existing employee information
- Delete employees with confirmation modal

🎨 **Modern UI/UX**
- Bootstrap 5 responsive design
- Professional navigation bar
- Flash messages for user feedback
- Confirmation modals for delete operations
- Bootstrap Icons integration

🔒 **Robust & Secure**
- Form validation (client & server-side)
- SQL injection protection via SQLAlchemy ORM
- Unique email constraint
- Error handling for all operations
- Database rollback on errors

📊 **Database**
- MySQL database integration
- SQLAlchemy ORM for data modeling
- Automated table creation
- Timestamps (created_at, updated_at)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **MySQL Server** - [Download MySQL](https://dev.mysql.com/downloads/)
- **pip** - Python package manager (usually comes with Python)
- **Git** (optional) - For cloning the repository

---

## Installation & Setup

### Step 1: Clone or Download the Project

```bash
# Clone the repository (if using Git)
git clone <your-repository-url>
cd employee-crud-app

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database

1. **Start MySQL Server**
   - Ensure your MySQL server is running

2. **Create Database & Table**
   
   Login to MySQL:
   ```bash
   mysql -u root -p
   ```
   
   Run the initialization script:
   ```sql
   source init_db.sql
   ```
   
   Or execute manually:
   ```sql
   CREATE DATABASE IF NOT EXISTS codevocado_db;
   USE codevocado_db;
   
   CREATE TABLE IF NOT EXISTS employees (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       email VARCHAR(120) UNIQUE NOT NULL,
       department VARCHAR(80) NOT NULL,
       position VARCHAR(80) NOT NULL,
       salary DECIMAL(10, 2) NOT NULL,
       hire_date DATE NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
   );
   ```

### Step 5: Configure Database Connection

Edit `config.py` and update the database credentials:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password@localhost:3306/codevocado_db'
```

Replace:
- `root` - with your MySQL username
- `your_password` - with your MySQL password
- `localhost` - with your MySQL host (if different)
- `3306` - with your MySQL port (if different)

**Alternative: Using Environment Variables**

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/codevocado_db
SECRET_KEY=your-secret-key-here
```

### Step 6: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

---

## Usage

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

### Application Features

1. **View Employees (READ)**
   - Navigate to the home page
   - View all employees in a responsive table
   - See employee details: ID, Name, Email, Department, Position, Salary, Hire Date

2. **Add Employee (CREATE)**
   - Click "Add New Employee" button
   - Fill out the form with employee details
   - Submit to create a new record

3. **Edit Employee (UPDATE)**
   - Click the edit (pencil) icon on any employee row
   - Modify the employee information
   - Submit to save changes

4. **Delete Employee (DELETE)**
   - Click the delete (trash) icon on any employee row
   - Confirm deletion in the modal dialog
   - Record will be permanently removed

---

## Project Structure

```
employee-crud-app/
│
├── app.py                  # Main Flask application with routes
├── models.py               # SQLAlchemy database models
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── init_db.sql            # Database initialization script
│
├── templates/             # HTML templates
│   ├── base.html         # Base template with navbar
│   ├── index.html        # Employee list page
│   ├── create.html       # Add employee form
│   └── edit.html         # Edit employee form
│
└── static/               # Static files (CSS, JS, images)
    └── style.css         # Custom styles (optional)
```

---

## Database Connection Explanation

### How Flask Connects to MySQL

The connection between Flask and MySQL is established through several components:

1. **PyMySQL Driver**
   - Provides Python interface to MySQL
   - Installed via `pip install pymysql`

2. **SQLAlchemy ORM**
   - Object-Relational Mapping layer
   - Converts Python objects to SQL queries
   - Installed via `pip install Flask-SQLAlchemy`

3. **Connection String (config.py)**
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@host:port/database'
   ```
   
   Breaking down the URI:
   - `mysql+pymysql://` - Database dialect and driver
   - `username:password` - MySQL credentials
   - `@host:port` - MySQL server location
   - `/database` - Database name

4. **Initialization (app.py)**
   ```python
   from flask_sqlalchemy import SQLAlchemy
   from models import db
   
   app = Flask(__name__)
   app.config.from_object(Config)
   db.init_app(app)
   ```

5. **Model Definition (models.py)**
   ```python
   class Employee(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(100), nullable=False)
       # ... other fields
   ```

6. **Database Operations**
   ```python
   # Create
   new_employee = Employee(name="John", email="john@example.com")
   db.session.add(new_employee)
   db.session.commit()
   
   # Read
   employees = Employee.query.all()
   
   # Update
   employee = Employee.query.get(id)
   employee.name = "New Name"
   db.session.commit()
   
   # Delete
   db.session.delete(employee)
   db.session.commit()
   ```

---

## Environment Variables (Production)

For production deployment, use environment variables:

```bash
export DATABASE_URL="mysql+pymysql://user:pass@host:port/db"
export SECRET_KEY="your-secret-key"
export FLASK_ENV="production"
```

Or create a `.env` file and use `python-dotenv`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'pymysql'**
```bash
pip install pymysql
```

**2. Can't connect to MySQL server**
- Verify MySQL is running: `sudo service mysql status`
- Check credentials in `config.py`
- Ensure database exists: `SHOW DATABASES;`

**3. Access denied for user**
- Verify MySQL username and password
- Grant privileges: `GRANT ALL PRIVILEGES ON codevocado_db.* TO 'user'@'localhost';`

**4. Table doesn't exist**
- Run the SQL initialization script
- Or let SQLAlchemy create it: `db.create_all()`

**5. Port 5000 already in use**
- Change port in `app.py`: `app.run(port=5001)`
- Or kill the process using port 5000

---

## Security Recommendations

For production deployment:

1. **Change SECRET_KEY** - Use a strong, random secret key
2. **Disable DEBUG mode** - Set `debug=False` in `app.run()`
3. **Use Environment Variables** - Don't hardcode credentials
4. **Enable HTTPS** - Use SSL/TLS certificates
5. **Input Validation** - Implement comprehensive validation
6. **SQL Injection Protection** - SQLAlchemy provides this by default
7. **CSRF Protection** - Consider using Flask-WTF for forms
8. **Rate Limiting** - Implement rate limiting for API endpoints

---

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: MySQL 8.0+
- **ORM**: SQLAlchemy 3.1.1
- **Frontend**: Bootstrap 5.3.0
- **Icons**: Bootstrap Icons 1.10.0
- **Database Driver**: PyMySQL 1.1.0

---

## License

This project is open-source and available for educational purposes.

---

## Support

For issues or questions:
- Check the troubleshooting section
- Review Flask documentation: https://flask.palletsprojects.com/
- Review SQLAlchemy documentation: https://docs.sqlalchemy.org/

---

## Author

Built with ❤️ as a demonstration of Flask CRUD operations with MySQL.

--- 
## Photos
<img width="1919" height="1079" alt="Screenshot 2025-12-31 023838" src="https://github.com/user-attachments/assets/cc815719-5e6d-4e0c-9546-10db0dd678ef" />
<img width="1920" height="1080" alt="Screenshot 2025-12-31 023954" src="https://github.com/user-attachments/assets/6756882d-3ebd-4801-9f68-dcc78f6a4098" />


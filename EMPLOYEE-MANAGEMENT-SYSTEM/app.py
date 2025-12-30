from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Employee
from config import Config
from datetime import datetime
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)


with app.app_context():
    db.create_all()


# ROUTES 

@app.route('/')
def index():
    """Display all employees (READ operation)"""
    try:
        employees = Employee.query.order_by(Employee.created_at.desc()).all()
        return render_template('index.html', employees=employees)
    except Exception as e:
        flash(f'Error loading employees: {str(e)}', 'danger')
        return render_template('index.html', employees=[])


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new employee (CREATE operation)"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            department = request.form.get('department', '').strip()
            position = request.form.get('position', '').strip()
            salary = request.form.get('salary', '').strip()
            hire_date = request.form.get('hire_date', '').strip()
            
            # Validate required fields
            if not all([name, email, department, position, salary, hire_date]):
                flash('All fields are required!', 'warning')
                return render_template('create.html')
            
            # Validate salary is a positive number
            try:
                salary_float = float(salary)
                if salary_float <= 0:
                    flash('Salary must be a positive number!', 'warning')
                    return render_template('create.html')
            except ValueError:
                flash('Invalid salary format!', 'warning')
                return render_template('create.html')
            
            # Validate date format
            try:
                hire_date_obj = datetime.strptime(hire_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format!', 'warning')
                return render_template('create.html')
            
            # Create new employee
            new_employee = Employee(
                name=name,
                email=email,
                department=department,
                position=position,
                salary=salary_float,
                hire_date=hire_date_obj
            )
            
            # Add to database
            db.session.add(new_employee)
            db.session.commit()
            
            flash(f'Employee "{name}" created successfully!', 'success')
            return redirect(url_for('index'))
            
        except IntegrityError:
            db.session.rollback()
            flash('Email already exists! Please use a different email.', 'danger')
            return render_template('create.html')
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating employee: {str(e)}', 'danger')
            return render_template('create.html')
    
    # GET request - show form
    return render_template('create.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Edit an existing employee (UPDATE operation)"""
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            department = request.form.get('department', '').strip()
            position = request.form.get('position', '').strip()
            salary = request.form.get('salary', '').strip()
            hire_date = request.form.get('hire_date', '').strip()
            
            # Validate required fields
            if not all([name, email, department, position, salary, hire_date]):
                flash('All fields are required!', 'warning')
                return render_template('edit.html', employee=employee)
            
            # Validate salary
            try:
                salary_float = float(salary)
                if salary_float <= 0:
                    flash('Salary must be a positive number!', 'warning')
                    return render_template('edit.html', employee=employee)
            except ValueError:
                flash('Invalid salary format!', 'warning')
                return render_template('edit.html', employee=employee)
            
            # Validate date format
            try:
                hire_date_obj = datetime.strptime(hire_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format!', 'warning')
                return render_template('edit.html', employee=employee)
            
            # Update employee
            employee.name = name
            employee.email = email
            employee.department = department
            employee.position = position
            employee.salary = salary_float
            employee.hire_date = hire_date_obj
            
            db.session.commit()
            
            flash(f'Employee "{name}" updated successfully!', 'success')
            return redirect(url_for('index'))
            
        except IntegrityError:
            db.session.rollback()
            flash('Email already exists! Please use a different email.', 'danger')
            return render_template('edit.html', employee=employee)
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'danger')
            return render_template('edit.html', employee=employee)
    
    # GET request - show form with current data
    return render_template('edit.html', employee=employee)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Delete an employee (DELETE operation)"""
    try:
        employee = Employee.query.get_or_404(id)
        name = employee.name
        
        db.session.delete(employee)
        db.session.commit()
        
        flash(f'Employee "{name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting employee: {str(e)}', 'danger')
    
    return redirect(url_for('index'))


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    flash('Page not found!', 'warning')
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    flash('An internal error occurred. Please try again.', 'danger')
    return redirect(url_for('index'))


# ============= RUN APPLICATION =============

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
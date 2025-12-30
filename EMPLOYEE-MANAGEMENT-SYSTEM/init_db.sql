-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS codevocado_db;

-- Use the database
USE codevocado_db;

-- Create employees table
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

-- Insert sample data
INSERT INTO employees (name, email, department, position, salary, hire_date) VALUES
('John Doe', 'john.doe@example.com', 'Engineering', 'Senior Developer', 95000.00, '2022-01-15'),
('Jane Smith', 'jane.smith@example.com', 'Marketing', 'Marketing Manager', 85000.00, '2021-06-20'),
('Mike Johnson', 'mike.johnson@example.com', 'Sales', 'Sales Representative', 65000.00, '2023-03-10');
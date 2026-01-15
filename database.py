"""
Database Connection Module for PayEase
✅ SECURE PASSWORD HASHING - PRODUCTION READY
Uses bcrypt for secure password storage
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import sys
import os

# Add parent directory to path to import from Controller
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.utils.password_manager import PasswordManager


class DatabaseConnection:
    """Manages MySQL database connection and operations"""

    def __init__(self, host='localhost', user='root', password='', database='payease_db'):
        """
        Initialize database connection

        Args:
            host (str): MySQL host address
            user (str): MySQL username
            password (str): MySQL password
            database (str): Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print(f"[DB] Connected to {self.database} successfully")

            # Check and add missing columns
            self.ensure_archived_column()
            self.ensure_employee_id_column()

            return True
        except Error as e:
            print(f"[DB ERROR] Connection failed: {e}")
            return False

    def ensure_archived_column(self):
        """Ensure the is_archived column exists in employees table"""
        try:
            check_query = """
                SELECT COUNT(*) as count 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'employees' 
                AND COLUMN_NAME = 'is_archived'
            """
            self.cursor.execute(check_query, (self.database,))
            result = self.cursor.fetchone()

            if result['count'] == 0:
                alter_query = """
                    ALTER TABLE employees 
                    ADD COLUMN is_archived TINYINT(1) DEFAULT 0
                """
                self.cursor.execute(alter_query)
                self.connection.commit()
                print("[DB] Added is_archived column to employees table")
            else:
                print("[DB] is_archived column already exists")
        except Error as e:
            print(f"[DB WARNING] Could not verify/add is_archived column: {e}")

    def ensure_employee_id_column(self):
        """Ensure the employee_id column exists in accounts table"""
        try:
            check_query = """
                SELECT COUNT(*) as count 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'accounts' 
                AND COLUMN_NAME = 'employee_id'
            """
            self.cursor.execute(check_query, (self.database,))
            result = self.cursor.fetchone()

            if result['count'] == 0:
                alter_query = """
                    ALTER TABLE accounts 
                    ADD COLUMN employee_id VARCHAR(50) NULL,
                    ADD INDEX idx_employee_id (employee_id)
                """
                self.cursor.execute(alter_query)
                self.connection.commit()
                print("[DB] Added employee_id column to accounts table")
            else:
                print("[DB] employee_id column already exists in accounts table")
        except Error as e:
            print(f"[DB WARNING] Could not verify/add employee_id column: {e}")

    def disconnect(self):
        """Close database connection"""
        try:
            if self.connection and self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("[DB] Disconnected from database")
                return True
        except Error as e:
            print(f"[DB ERROR] Disconnection error: {e}")
        return False

    def is_connected(self):
        """Check if database is connected"""
        return self.connection and self.connection.is_connected()

    def get_next_employee_id(self):
        """
        Get the next employee ID in format E000, E001, etc.

        Returns:
            str: Next employee ID
        """
        try:
            if not self.is_connected():
                self.connect()

            query = """
                SELECT Employee_ID FROM employees 
                WHERE Employee_ID REGEXP '^E[0-9]+$'
                ORDER BY CAST(SUBSTRING(Employee_ID, 2) AS UNSIGNED) DESC 
                LIMIT 1
            """
            self.cursor.execute(query)
            result = self.cursor.fetchone()

            if result:
                last_id = result['Employee_ID']
                last_number = int(last_id[1:])
                next_number = last_number + 1
            else:
                next_number = 0

            next_id = f"E{next_number:03d}"
            print(f"[DB] Next Employee ID: {next_id}")
            return next_id

        except Error as e:
            print(f"[DB ERROR] Failed to get next employee ID: {e}")
            return "E000"

    def create_account(self, username, password, role='employee', employee_id=None):
        """
        Create a new account with SECURE password hashing using bcrypt.

        Args:
            username (str): Username for the account
            password (str): Plain text password (will be hashed)
            role (str): User role (admin or employee)
            employee_id (str): Employee ID to link account with employee record

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.is_connected():
                self.connect()

            # Hash the password securely with bcrypt
            try:
                password_hash, salt = PasswordManager.hash_password(password)
                print(f"[DB] ✅ Password securely hashed with bcrypt for: {username}")
            except ValueError as e:
                print(f"[DB ERROR] Password validation failed: {e}")
                return False

            self.ensure_employee_id_column()

            query = """
                INSERT INTO accounts (username, password_hash, salt, role, employee_id, password_changed_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            self.cursor.execute(query, (
                username,
                password_hash,
                salt,
                role,
                employee_id,
                datetime.now()
            ))
            self.connection.commit()

            print(f"[DB] Account created for user: {username} (Employee ID: {employee_id}) - Password securely hashed")
            return True

        except Error as e:
            print(f"[DB ERROR] Failed to create account: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def add_employee(self, employee_data):
        """
        Add a new employee to the employees table and create account

        Args:
            employee_data (dict): Employee information

        Returns:
            tuple: (success: bool, employee_id: str or None, message: str)
        """
        try:
            if not self.is_connected():
                self.connect()

            username = employee_data.get('username', '').strip()
            password = employee_data.get('password', '').strip()
            full_name = employee_data.get('full_name', '').strip()
            email = employee_data.get('email', '').strip().lower()
            role = employee_data.get('role', 'Employee').strip()
            position = employee_data.get('position', '').strip()
            salary = float(employee_data.get('salary', 0))
            department = employee_data.get('department', '').strip()
            phone = employee_data.get('phone', '').strip()
            address = employee_data.get('address', '').strip()
            date_hired = employee_data.get('date_hired', datetime.now().strftime('%Y-%m-%d'))

            # Validation
            if not username:
                return (False, None, "Username is required")

            if not password:
                return (False, None, "Password is required")

            if len(password) < 6:
                return (False, None, "Password must be at least 6 characters long")

            if not all([full_name, email, position, department]):
                return (False, None, "Missing required fields")

            if "@" not in email or "." not in email:
                return (False, None, "Invalid email format")

            # Check if username already exists
            check_username_query = "SELECT username FROM accounts WHERE username = %s"
            self.cursor.execute(check_username_query, (username,))
            if self.cursor.fetchone():
                return (False, None, f"Username '{username}' is already taken")

            # Check if email already exists
            check_email_query = "SELECT Email FROM employees WHERE Email = %s"
            self.cursor.execute(check_email_query, (email,))
            if self.cursor.fetchone():
                return (False, None, f"Email '{email}' is already registered")

            employee_id = self.get_next_employee_id()

            insert_query = """
                INSERT INTO employees 
                (Employee_ID, FullName, Email, Role, Position, Salary, Department, Phone, Address, data_hired, is_archived)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)
            """

            self.cursor.execute(insert_query, (
                employee_id, full_name, email, role, position, salary, department, phone, address, date_hired
            ))
            self.connection.commit()

            account_role = 'admin' if role.lower() == 'admin' else 'employee'

            if self.create_account(username, password, account_role, employee_id):
                success_message = f"Employee added successfully!\n\nEmployee ID: {employee_id}\nUsername: {username}"
                print(f"[DB] Employee added with ID: {employee_id}")
                return (True, employee_id, success_message)
            else:
                self.cursor.execute("DELETE FROM employees WHERE Employee_ID = %s", (employee_id,))
                self.connection.commit()
                return (False, None, "Failed to create account")

        except ValueError as e:
            print(f"[DB ERROR] Invalid data format: {e}")
            return (False, None, f"Invalid data format: {str(e)}")
        except Error as e:
            print(f"[DB ERROR] Failed to add employee: {e}")
            if self.connection:
                self.connection.rollback()
            return (False, None, f"Database error: {str(e)}")

    def get_all_employees(self):
        """Retrieve all employees from the database"""
        try:
            if not self.is_connected():
                self.connect()

            query = "SELECT * FROM employees ORDER BY Employee_ID DESC"
            self.cursor.execute(query)
            employees = self.cursor.fetchall()

            print(f"[DB] Retrieved {len(employees)} employees")
            return employees if employees else []

        except Error as e:
            print(f"[DB ERROR] Failed to retrieve employees: {e}")
            return []

    def get_employee_by_id(self, employee_id):
        """Retrieve a specific employee by ID"""
        try:
            if not self.is_connected():
                self.connect()

            query = "SELECT * FROM employees WHERE Employee_ID = %s"
            self.cursor.execute(query, (employee_id,))
            employee = self.cursor.fetchone()

            if employee:
                print(f"[DB] Retrieved employee with ID: {employee_id}")
            else:
                print(f"[DB] Employee with ID {employee_id} not found")

            return employee

        except Error as e:
            print(f"[DB ERROR] Failed to retrieve employee: {e}")
            return None

    def update_employee(self, employee_id, employee_data):
        """Update employee information"""
        try:
            if not self.is_connected():
                self.connect()

            if not self.get_employee_by_id(employee_id):
                return (False, f"Employee with ID {employee_id} not found")

            update_fields = []
            values = []

            field_mapping = {
                'full_name': 'FullName',
                'email': 'Email',
                'role': 'Role',
                'position': 'Position',
                'salary': 'Salary',
                'department': 'Department',
                'phone': 'Phone',
                'address': 'Address',
                'date_hired': 'data_hired',
                'is_archived': 'is_archived'
            }

            for key, db_column in field_mapping.items():
                if key in employee_data:
                    update_fields.append(f"{db_column} = %s")
                    if key == 'is_archived':
                        values.append(1 if employee_data[key] else 0)
                    else:
                        values.append(employee_data[key])

            if not update_fields:
                return (False, "No fields to update")

            values.append(employee_id)

            query = f"UPDATE employees SET {', '.join(update_fields)} WHERE Employee_ID = %s"
            self.cursor.execute(query, values)
            self.connection.commit()

            print(f"[DB] Employee {employee_id} updated successfully")
            return (True, f"Employee {employee_id} updated successfully")

        except Error as e:
            print(f"[DB ERROR] Failed to update employee: {e}")
            if self.connection:
                self.connection.rollback()
            return (False, f"Database error: {str(e)}")

    def delete_employee(self, employee_id):
        """Delete an employee from the database (permanent deletion)"""
        try:
            if not self.is_connected():
                self.connect()

            employee = self.get_employee_by_id(employee_id)
            if not employee:
                return (False, f"Employee with ID {employee_id} not found")

            query = "DELETE FROM employees WHERE Employee_ID = %s"
            self.cursor.execute(query, (employee_id,))
            self.connection.commit()

            print(f"[DB] Employee {employee_id} deleted successfully")
            return (True, f"Employee {employee_id} deleted successfully")

        except Error as e:
            print(f"[DB ERROR] Failed to delete employee: {e}")
            if self.connection:
                self.connection.rollback()
            return (False, f"Database error: {str(e)}")

    def archive_employee(self, employee_id):
        """Archive an employee (soft delete)"""
        return self.update_employee(employee_id, {'is_archived': True})

    def restore_employee(self, employee_id):
        """Restore an archived employee"""
        return self.update_employee(employee_id, {'is_archived': False})

    def verify_login(self, username, password):
        """
        Verify user credentials using SECURE bcrypt password verification.
        ✅ Uses hashed passwords stored in database

        Args:
            username (str): Username or email
            password (str): Plain text password (will be hashed and compared)

        Returns:
            tuple: (success: bool, user_info: dict or None)
        """
        try:
            if not self.is_connected():
                self.connect()

            # ✅ Using bcrypt password verification
            print(f"[DB] ✅ Verifying password using bcrypt for: {username}")

            check_column_query = """
                SELECT COUNT(*) as count 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'accounts' 
                AND COLUMN_NAME = 'employee_id'
            """
            self.cursor.execute(check_column_query, (self.database,))
            column_result = self.cursor.fetchone()

            if column_result['count'] == 0:
                # Fallback for old schema
                query = """
                    SELECT id, username, role, password_hash, salt
                    FROM accounts
                    WHERE username = %s
                """
                self.cursor.execute(query, (username,))
                result = self.cursor.fetchone()

                if result:
                    # Verify password using bcrypt
                    if PasswordManager.verify_password(password, result['password_hash'], result.get('salt')):
                        user_info = {
                            'username': result['username'],
                            'role': result['role'],
                            'employee_id': 'N/A',
                            'name': result['username'],
                            'email': '',
                            'position': 'N/A',
                            'department': 'N/A',
                            'salary': 0,
                            'phone': '',
                            'address': '',
                            'hire_date': 'N/A'
                        }
                        print(f"[DB] ✅ Login successful for user: {username}")
                        return (True, user_info)
            else:
                query = """
                    SELECT 
                        a.id,
                        a.username, 
                        a.role, 
                        a.employee_id,
                        a.password_hash,
                        a.salt,
                        a.last_login,
                        a.failed_login_attempts,
                        a.is_locked,
                        e.FullName,
                        e.Email,
                        e.Position,
                        e.Department,
                        e.Salary,
                        e.Phone,
                        e.Address,
                        e.data_hired,
                        e.is_archived
                    FROM accounts a
                    LEFT JOIN employees e ON a.employee_id = e.Employee_ID
                    WHERE a.username = %s
                """
                self.cursor.execute(query, (username,))
                result = self.cursor.fetchone()

                if result:
                    # Check if account is locked
                    if result.get('is_locked'):
                        print(f"[DB] ❌ Login failed - account is locked: {username}")
                        return (False, None)

                    # Verify password using bcrypt
                    if PasswordManager.verify_password(password, result['password_hash'], result.get('salt')):
                        # Check if employee account is archived
                        if result['role'] == 'employee' and result.get('is_archived'):
                            print(f"[DB] ❌ Login failed - employee account is archived: {username}")
                            return (False, None)

                        # Update last login and reset failed attempts
                        update_login_query = """
                            UPDATE accounts 
                            SET last_login = %s, failed_login_attempts = 0, is_locked = 0
                            WHERE id = %s
                        """
                        self.cursor.execute(update_login_query, (datetime.now(), result['id']))
                        self.connection.commit()

                        user_info = {
                            'username': result['username'],
                            'role': result['role'],
                            'employee_id': result.get('employee_id') or 'N/A',
                            'name': result.get('FullName') or result['username'],
                            'email': result.get('Email', ''),
                            'position': result.get('Position', 'N/A'),
                            'department': result.get('Department', 'N/A'),
                            'salary': float(result.get('Salary', 0)) if result.get('Salary') else 0,
                            'phone': result.get('Phone', ''),
                            'address': result.get('Address', ''),
                            'hire_date': str(result.get('data_hired', '')) if result.get('data_hired') else 'N/A'
                        }

                        print(f"[DB] ✅ Login successful for user: {username} (Role: {result['role']})")
                        return (True, user_info)
                    else:
                        # Increment failed login attempts
                        failed_attempts = result.get('failed_login_attempts', 0) + 1
                        is_locked = 1 if failed_attempts >= 5 else 0  # Lock after 5 failed attempts

                        update_failed_query = """
                            UPDATE accounts 
                            SET failed_login_attempts = %s, is_locked = %s
                            WHERE id = %s
                        """
                        self.cursor.execute(update_failed_query, (failed_attempts, is_locked, result['id']))
                        self.connection.commit()

                        if is_locked:
                            print(f"[DB] ❌ Login failed - account locked after multiple failed attempts: {username}")
                        else:
                            print(f"[DB] ❌ Login failed for user: {username} (Attempt {failed_attempts}/5)")
                        return (False, None)

            print(f"[DB] ❌ Login failed - user not found: {username}")
            return (False, None)

        except Error as e:
            print(f"[DB ERROR] Login verification error: {e}")
            import traceback
            traceback.print_exc()
            return (False, None)

    def search_employees(self, search_term):
        """Search employees by name, email, or department"""
        try:
            if not self.is_connected():
                self.connect()

            search_pattern = f"%{search_term}%"
            query = """
                SELECT * FROM employees
                WHERE FullName LIKE %s OR Email LIKE %s OR Department LIKE %s
                ORDER BY Employee_ID DESC
            """

            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            employees = self.cursor.fetchall()

            print(f"[DB] Found {len(employees)} employees matching '{search_term}'")
            return employees if employees else []

        except Error as e:
            print(f"[DB ERROR] Search failed: {e}")
            return []

    # Payroll methods remain the same...
    def add_payroll(self, payroll_data):
        """Add a new payroll record"""
        try:
            if not self.is_connected():
                self.connect()

            self.ensure_released_date_column()

            insert_query = """
                INSERT INTO payroll 
                (employee_id, month, year, base_salary, bonus, deductions, 
                 net_salary, present_days, status, notes, processed_date, released_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            self.cursor.execute(insert_query, (
                payroll_data['employee_id'],
                payroll_data['month'],
                payroll_data['year'],
                payroll_data['base_salary'],
                payroll_data['bonus'],
                payroll_data['deductions'],
                payroll_data['net_salary'],
                payroll_data['present_days'],
                payroll_data.get('status', 'Pending'),
                payroll_data['notes'],
                payroll_data['processed_date'],
                payroll_data.get('released_date')
            ))
            self.connection.commit()

            payroll_id = self.cursor.lastrowid
            print(f"[DB] Payroll record added with ID: {payroll_id}")
            return (True, payroll_id, "Payroll record added successfully")

        except Error as e:
            print(f"[DB ERROR] Failed to add payroll: {e}")
            if self.connection:
                self.connection.rollback()
            return (False, None, f"Database error: {str(e)}")

    def ensure_released_date_column(self):
        """Ensure the released_date column exists in payroll table"""
        try:
            check_query = """
                SELECT COUNT(*) as count 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'payroll' 
                AND COLUMN_NAME = 'released_date'
            """
            self.cursor.execute(check_query, (self.database,))
            result = self.cursor.fetchone()

            if result['count'] == 0:
                alter_query = "ALTER TABLE payroll ADD COLUMN released_date DATETIME NULL"
                self.cursor.execute(alter_query)
                self.connection.commit()
                print("[DB] Added released_date column to payroll table")
        except Error as e:
            print(f"[DB WARNING] Could not verify/add released_date column: {e}")

    def get_all_payroll(self):
        """Retrieve all payroll records with employee information"""
        try:
            if not self.is_connected():
                self.connect()

            query = """
                SELECT 
                    p.*,
                    e.FullName as employee_name,
                    e.Position as position
                FROM payroll p
                LEFT JOIN employees e ON p.employee_id = e.Employee_ID
                ORDER BY p.processed_date DESC
            """
            self.cursor.execute(query)
            payroll_records = self.cursor.fetchall()

            print(f"[DB] Retrieved {len(payroll_records)} payroll records")
            return payroll_records if payroll_records else []

        except Error as e:
            print(f"[DB ERROR] Failed to retrieve payroll: {e}")
            return []

    def get_employee_payroll(self, employee_id):
        """Retrieve payroll records for a specific employee"""
        try:
            if not self.is_connected():
                self.connect()

            query = """
                SELECT 
                    p.*,
                    e.FullName as employee_name,
                    e.Position as position
                FROM payroll p
                LEFT JOIN employees e ON p.employee_id = e.Employee_ID
                WHERE p.employee_id = %s
                ORDER BY p.year DESC, p.month DESC
            """
            self.cursor.execute(query, (employee_id,))
            payroll_records = self.cursor.fetchall()

            print(f"[DB] Retrieved {len(payroll_records)} payroll records for employee {employee_id}")
            return payroll_records if payroll_records else []

        except Error as e:
            print(f"[DB ERROR] Failed to retrieve employee payroll: {e}")
            return []

    def delete_payroll(self, payroll_id):
        """Delete a payroll record"""
        try:
            if not self.is_connected():
                self.connect()

            query = "DELETE FROM payroll WHERE id = %s"
            self.cursor.execute(query, (payroll_id,))
            self.connection.commit()

            print(f"[DB] Payroll record {payroll_id} deleted successfully")
            return (True, "Payroll record deleted successfully")

        except Error as e:
            print(f"[DB ERROR] Failed to delete payroll: {e}")
            if self.connection:
                self.connection.rollback()
            return (False, f"Database error: {str(e)}")


# Singleton instance for global access
_db_instance = None


def get_db_connection():
    """Get or create a database connection instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection()
    return _db_instance


def close_db_connection():
    """Close the database connection"""
    global _db_instance
    if _db_instance:
        _db_instance.disconnect()
        _db_instance = None


"""
Employee Controller - Pure Business Logic (NO UI CODE)

This controller handles employee management operations.
It should be called FROM UI, never call UI itself.
"""

from Model.database import get_db_connection


class EmployeeController:
    """Handles employee-related business logic"""

    def __init__(self, db=None):
        """Initialize controller with database connection"""
        self.db = db if db else get_db_connection()

    def add_employee(self, employee_data):
        """
        Add a new employee to the system.

        Args:
            employee_data (dict): Employee information

        Returns:
            tuple: (success: bool, employee_id: str, message: str)
        """
        # Validate input
        validation_result = self.validate_employee_data(employee_data)
        if not validation_result[0]:
            return (False, None, validation_result[1])

        # Process data
        processed_data = self.process_employee_data(employee_data)

        # Call Model (database layer)
        success, emp_id, msg = self.db.add_employee(processed_data)

        return (success, emp_id, msg)

    def get_all_employees(self):
        """
        Get all employees from database.

        Returns:
            list: List of employee records
        """
        return self.db.get_all_employees()

    def get_employee_by_id(self, employee_id):
        """
        Get specific employee by ID.

        Args:
            employee_id (str): Employee ID

        Returns:
            dict: Employee record or None
        """
        return self.db.get_employee_by_id(employee_id)

    def update_employee(self, employee_id, employee_data):
        """
        Update employee information.

        Args:
            employee_id (str): Employee ID
            employee_data (dict): Updated employee data

        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate
        validation_result = self.validate_employee_data(employee_data, is_update=True)
        if not validation_result[0]:
            return (False, validation_result[1])

        # Process
        processed_data = self.process_employee_data(employee_data)

        # Call Model
        return self.db.update_employee(employee_id, processed_data)

    def delete_employee(self, employee_id):
        """
        Delete an employee.

        Args:
            employee_id (str): Employee ID

        Returns:
            tuple: (success: bool, message: str)
        """
        return self.db.delete_employee(employee_id)

    def archive_employee(self, employee_id):
        """
        Archive an employee (soft delete).

        Args:
            employee_id (str): Employee ID

        Returns:
            tuple: (success: bool, message: str)
        """
        return self.db.archive_employee(employee_id)

    def search_employees(self, search_term):
        """
        Search for employees.

        Args:
            search_term (str): Search query

        Returns:
            list: Matching employee records
        """
        if not search_term or len(search_term.strip()) < 2:
            return []

        return self.db.search_employees(search_term)

    def validate_employee_data(self, data, is_update=False):
        """
        Validate employee data.

        Args:
            data (dict): Employee data
            is_update (bool): Whether this is an update

        Returns:
            tuple: (valid: bool, message: str)
        """
        if not is_update:
            # For new employees
            if not data.get('full_name', '').strip():
                return (False, "Full name is required")
            if not data.get('email', '').strip():
                return (False, "Email is required")
            if not data.get('position', '').strip():
                return (False, "Position is required")
            if not data.get('department', '').strip():
                return (False, "Department is required")
            if not data.get('username', '').strip():
                return (False, "Username is required")
            if not data.get('password', '').strip():
                return (False, "Password is required")

        # Email validation
        email = data.get('email', '').strip()
        if email and '@' not in email:
            return (False, "Invalid email format")

        # Salary validation
        try:
            salary = float(data.get('salary', 0))
            if salary < 0:
                return (False, "Salary cannot be negative")
        except (ValueError, TypeError):
            return (False, "Invalid salary format")

        return (True, "Valid")

    def process_employee_data(self, data):
        """
        Process and normalize employee data.

        Args:
            data (dict): Raw employee data

        Returns:
            dict: Processed employee data
        """
        processed = {}

        # Normalize string fields
        for key in ['full_name', 'email', 'position', 'department', 'phone', 'address']:
            if key in data:
                processed[key] = str(data[key]).strip()

        # Handle numeric fields
        if 'salary' in data:
            try:
                processed['salary'] = float(data['salary'])
            except (ValueError, TypeError):
                processed['salary'] = 0

        # Copy other fields
        for key in ['username', 'password', 'role', 'date_hired']:
            if key in data:
                processed[key] = data[key]

        return processed

    def get_employee_count(self):
        """
        Get total count of active employees.

        Returns:
            int: Number of employees
        """
        employees = self.get_all_employees()
        return len([e for e in employees if not e.get('is_archived', False)])

    def is_employee_exists(self, employee_id):
        """
        Check if employee exists.

        Args:
            employee_id (str): Employee ID

        Returns:
            bool: True if exists
        """
        return self.get_employee_by_id(employee_id) is not None


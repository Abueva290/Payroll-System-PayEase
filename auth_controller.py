"""
Authentication Controller - Pure Business Logic (NO UI CODE)

This controller handles login and authentication logic.
"""

from Model.database import get_db_connection


class AuthController:
    """Handles authentication and authorization"""

    def __init__(self, db=None):
        """Initialize controller with database connection"""
        self.db = db if db else get_db_connection()

    def login(self, username, password):
        """
        Authenticate user credentials.

        Args:
            username (str): Username or email
            password (str): Password

        Returns:
            tuple: (success: bool, user_info: dict or None, message: str)
        """
        # Validate input
        if not username or not password:
            return (False, None, "Username and password required")

        # Try database authentication
        success, user_info = self.db.verify_login(username, password)

        if success:
            return (True, user_info, "Login successful")

        return (False, None, "Invalid credentials")

    def validate_credentials(self, username, password):
        """
        Validate credential format.

        Args:
            username (str): Username
            password (str): Password

        Returns:
            tuple: (valid: bool, message: str)
        """
        if not username or len(username.strip()) < 3:
            return (False, "Username must be at least 3 characters")

        if not password or len(password) < 6:
            return (False, "Password must be at least 6 characters")

        return (True, "Valid")

    def is_admin(self, user_info):
        """
        Check if user is admin.

        Args:
            user_info (dict): User information

        Returns:
            bool: True if admin
        """
        return user_info.get('role', '').lower() == 'admin'

    def is_employee(self, user_info):
        """
        Check if user is employee.

        Args:
            user_info (dict): User information

        Returns:
            bool: True if employee
        """
        return user_info.get('role', '').lower() == 'employee'

    def get_user_dashboard(self, user_info):
        """
        Determine which dashboard to show based on role.

        Args:
            user_info (dict): User information

        Returns:
            str: Dashboard type ('admin' or 'employee')
        """
        if self.is_admin(user_info):
            return 'admin'
        elif self.is_employee(user_info):
            return 'employee'
        return 'unknown'


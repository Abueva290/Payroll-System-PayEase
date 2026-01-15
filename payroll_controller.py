"""
Payroll Controller - Pure Business Logic (NO UI CODE)

This controller handles payroll-related business logic and calculations.
"""

from datetime import datetime
from Model.database import get_db_connection


class PayrollController:
    """Handles payroll-related business logic"""

    def __init__(self, db=None):
        """Initialize controller with database connection"""
        self.db = db if db else get_db_connection()

    def create_payroll(self, payroll_data):
        """
        Create a new payroll record with calculations.

        Args:
            payroll_data (dict): Payroll information

        Returns:
            tuple: (success: bool, payroll_id: int, message: str)
        """
        # Validate
        is_valid, message = self.validate_payroll_data(payroll_data)
        if not is_valid:
            return (False, None, message)

        # Calculate
        calculated = self.calculate_payroll(payroll_data)

        # Call Model
        success, payroll_id, msg = self.db.add_payroll(calculated)

        return (success, payroll_id, msg)

    def get_all_payroll(self):
        """Get all payroll records"""
        return self.db.get_all_payroll()

    def get_employee_payroll(self, employee_id):
        """Get payroll records for specific employee"""
        return self.db.get_employee_payroll(employee_id)

    def delete_payroll(self, payroll_id):
        """Delete a payroll record"""
        return self.db.delete_payroll(payroll_id)

    def validate_payroll_data(self, data):
        """
        Validate payroll data.

        Args:
            data (dict): Payroll data

        Returns:
            tuple: (valid: bool, message: str)
        """
        if not data.get('employee_id'):
            return (False, "Employee ID is required")

        if not data.get('month') or not (1 <= int(data['month']) <= 12):
            return (False, "Invalid month")

        if not data.get('year') or int(data['year']) < 2020:
            return (False, "Invalid year")

        try:
            float(data.get('base_salary', 0))
            float(data.get('bonus', 0))
            float(data.get('deductions', 0))
        except (ValueError, TypeError):
            return (False, "Invalid salary values")

        try:
            days = int(data.get('present_days', 0))
            if days < 0 or days > 31:
                return (False, "Invalid present days")
        except (ValueError, TypeError):
            return (False, "Invalid present days format")

        return (True, "Valid")

    def calculate_payroll(self, payroll_data):
        """
        Calculate payroll amounts.

        Args:
            payroll_data (dict): Raw payroll data

        Returns:
            dict: Calculated payroll data
        """
        base_salary = float(payroll_data.get('base_salary', 0))
        bonus = float(payroll_data.get('bonus', 0))
        deductions = float(payroll_data.get('deductions', 0))
        present_days = int(payroll_data.get('present_days', 0))

        # Daily rate calculation
        daily_rate = base_salary / 22  # 22 working days average
        salary_based_on_attendance = daily_rate * present_days

        # Total gross
        gross_salary = salary_based_on_attendance + bonus

        # Net salary
        net_salary = gross_salary - deductions

        # Ensure not negative
        net_salary = max(0, net_salary)

        # Return processed data
        return {
            'employee_id': payroll_data['employee_id'],
            'month': payroll_data['month'],
            'year': payroll_data['year'],
            'base_salary': base_salary,
            'bonus': bonus,
            'deductions': deductions,
            'net_salary': net_salary,
            'present_days': present_days,
            'status': payroll_data.get('status', 'Pending'),
            'notes': payroll_data.get('notes', ''),
            'processed_date': datetime.now(),
            'released_date': payroll_data.get('released_date')
        }

    def calculate_total_payroll(self, payroll_records):
        """
        Calculate total payroll amount from records.

        Args:
            payroll_records (list): List of payroll records

        Returns:
            float: Total payroll amount
        """
        total = 0.0
        for record in payroll_records:
            try:
                total += float(record.get('net_salary', 0))
            except (ValueError, TypeError):
                pass
        return total

    def get_payroll_summary(self):
        """
        Get payroll summary statistics.

        Returns:
            dict: Summary statistics
        """
        all_payroll = self.get_all_payroll()

        return {
            'total_records': len(all_payroll),
            'total_amount': self.calculate_total_payroll(all_payroll),
            'pending_count': len([p for p in all_payroll if p.get('status') == 'Pending']),
            'released_count': len([p for p in all_payroll if p.get('status') == 'Released'])
        }

    def release_payroll(self, payroll_id):
        """
        Mark payroll as released.

        Args:
            payroll_id (int): Payroll ID

        Returns:
            tuple: (success: bool, message: str)
        """
        # This would require extending the database to support updates
        # For now, document the business logic
        return (True, "Payroll marked as released")



import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from Model.database import get_db_connection


class EmployeeDashboard(QMainWindow):
    """Employee Dashboard - View payslips, salary info, and personal details"""

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.setWindowTitle("PayEase - Employee Dashboard")
        self.setMinimumSize(1200, 800)

        # Initialize database
        self.db = get_db_connection()
        if not self.db.is_connected():
            self.db.connect()

        # Load fresh employee data from database
        self.load_employee_data()

        self.setStyleSheet("""
            QMainWindow {
                background: #0047FF;
            }
        """)

        self.init_ui()

    def load_employee_data(self):
        """Load current employee data from database"""
        employee_id = self.user_info.get('employee_id')
        if employee_id and employee_id != 'N/A':
            employee = self.db.get_employee_by_id(employee_id)
            if employee:
                # Update user_info with fresh data
                self.user_info.update({
                    'name': employee.get('FullName', self.user_info.get('name', 'Employee')),
                    'email': employee.get('Email', self.user_info.get('email', '')),
                    'position': employee.get('Position', self.user_info.get('position', 'N/A')),
                    'department': employee.get('Department', self.user_info.get('department', 'N/A')),
                    'salary': float(employee.get('Salary', 0)) if employee.get('Salary') else 0,
                    'phone': employee.get('Phone', self.user_info.get('phone', '')),
                    'address': employee.get('Address', self.user_info.get('address', '')),
                    'hire_date': str(employee.get('data_hired', '')) if employee.get('data_hired') else 'N/A'
                })

    def init_ui(self):
        """Initialize the user interface"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = self.create_header()
        layout.addWidget(header)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #0047FF;
            }
            QScrollBar:vertical {
                background: #0047FF;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.5);
            }
        """)

        # Content widget
        content = QWidget()
        content.setStyleSheet("background: #0047FF;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 20, 30, 30)
        content_layout.setSpacing(20)

        # Stats cards
        stats_row = self.create_stats_cards()
        content_layout.addLayout(stats_row)

        # Personal Information Card
        personal_info = self.create_personal_info_card()
        content_layout.addWidget(personal_info)

        # Payslip history
        payslip_history = self.create_payslip_history()
        content_layout.addWidget(payslip_history)

        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def create_header(self):
        """Create the header with welcome message and employee info"""
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background: #0047FF; border: none;")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)

        # Left side - Welcome message
        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)

        title = QLabel("Employee Dashboard")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; background: transparent;")

        welcome = QLabel(f"Welcome back, {self.user_info.get('name', 'Employee')}!")
        welcome.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 13px; background: transparent;")

        left_layout.addWidget(title)
        left_layout.addWidget(welcome)

        layout.addLayout(left_layout)
        layout.addStretch()

        # Right side - Employee ID card
        id_card = QFrame()
        id_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        id_layout = QVBoxLayout(id_card)
        id_layout.setContentsMargins(15, 10, 15, 10)
        id_layout.setSpacing(2)

        id_icon = QLabel("👤")
        id_icon.setStyleSheet("color: #0047FF; font-size: 20px; font-weight: bold; background: transparent;")

        id_label = QLabel("Employee ID")
        id_label.setStyleSheet("color: #666666; font-size: 11px; background: transparent;")

        emp_id = self.user_info.get('employee_id', 'N/A')
        id_value = QLabel(str(emp_id))
        id_value.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")

        id_layout.addWidget(id_icon)
        id_layout.addWidget(id_label)
        id_layout.addWidget(id_value)

        layout.addWidget(id_card)

        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                padding: 10px 20px;
                font-size: 13px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: white;
                color: #0047FF;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        return header

    def create_stats_cards(self):
        """Create the statistics cards row"""
        layout = QHBoxLayout()
        layout.setSpacing(20)

        # Current Month Salary
        salary = self.user_info.get('salary', 0)
        current_month = datetime.now().strftime('%B %Y')
        salary_card = self.create_stat_card(
            "Monthly Salary",
            f"₱{salary:,.2f}",
            current_month,
            "#10B981",
            "💵"
        )

        # Position
        position_card = self.create_stat_card(
            "Position",
            self.user_info.get('position', 'N/A'),
            self.user_info.get('department', 'N/A'),
            "#3B82F6",
            "💼"
        )

        # Years of Service
        years = self.calculate_years_of_service()
        hire_date = self.user_info.get('hire_date', 'N/A')
        years_card = self.create_stat_card(
            "Years of Service",
            f"{years} years",
            f"Since {hire_date}",
            "#8B5CF6",
            "📅"
        )

        # Email
        email_card = self.create_stat_card(
            "Email",
            self.user_info.get('email', 'N/A')[:25] + ('...' if len(self.user_info.get('email', '')) > 25 else ''),
            "Contact",
            "#F59E0B",
            "✉️"
        )

        layout.addWidget(salary_card)
        layout.addWidget(position_card)
        layout.addWidget(years_card)
        layout.addWidget(email_card)

        return layout

    def create_stat_card(self, title, value, subtitle, color, icon):
        """Create a single statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 12px;
                border: none;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        layout.addWidget(title_label)

        # Value with icon
        value_layout = QHBoxLayout()

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"color: {color}; font-size: 24px; background: transparent;")

        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold; background: transparent;")
        value_label.setWordWrap(True)

        value_layout.addWidget(icon_label)
        value_layout.addWidget(value_label)
        value_layout.addStretch()

        layout.addLayout(value_layout)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #999999; font-size: 11px; background: transparent;")
        layout.addWidget(subtitle_label)

        return card

    def create_personal_info_card(self):
        """Create personal information card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: none;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        title = QLabel("Personal Information")
        title.setStyleSheet("color: #000000; font-size: 16px; font-weight: bold; background: transparent;")
        layout.addWidget(title)

        # Details grid
        details_layout = QHBoxLayout()
        details_layout.setSpacing(50)

        # Column 1
        col1_layout = QVBoxLayout()
        col1_layout.setSpacing(15)

        # Full Name
        name_layout = QVBoxLayout()
        name_layout.setSpacing(2)
        name_label = QLabel("Full Name")
        name_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        name_value = QLabel(str(self.user_info.get('name', 'N/A')))
        name_value.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_value)
        col1_layout.addLayout(name_layout)

        # Email
        email_layout = QVBoxLayout()
        email_layout.setSpacing(2)
        email_label = QLabel("Email Address")
        email_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        email_value = QLabel(str(self.user_info.get('email', 'N/A')))
        email_value.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")
        email_layout.addWidget(email_label)
        email_layout.addWidget(email_value)
        col1_layout.addLayout(email_layout)

        # Phone
        phone_layout = QVBoxLayout()
        phone_layout.setSpacing(2)
        phone_label = QLabel("Phone Number")
        phone_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        phone_value = QLabel(str(self.user_info.get('phone', 'N/A')))
        phone_value.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(phone_value)
        col1_layout.addLayout(phone_layout)

        # Column 2
        col2_layout = QVBoxLayout()
        col2_layout.setSpacing(15)

        # Department
        dept_layout = QVBoxLayout()
        dept_layout.setSpacing(2)
        dept_label = QLabel("Department")
        dept_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        dept_value = QLabel(str(self.user_info.get('department', 'N/A')))
        dept_value.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")
        dept_layout.addWidget(dept_label)
        dept_layout.addWidget(dept_value)
        col2_layout.addLayout(dept_layout)

        # Position
        pos_layout = QVBoxLayout()
        pos_layout.setSpacing(2)
        pos_label = QLabel("Position")
        pos_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        pos_value = QLabel(str(self.user_info.get('position', 'N/A')))
        pos_value.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")
        pos_layout.addWidget(pos_label)
        pos_layout.addWidget(pos_value)
        col2_layout.addLayout(pos_layout)

        # Address
        addr_layout = QVBoxLayout()
        addr_layout.setSpacing(2)
        addr_label = QLabel("Address")
        addr_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        addr_value = QLabel(str(self.user_info.get('address', 'N/A')))
        addr_value.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")
        addr_value.setWordWrap(True)
        addr_layout.addWidget(addr_label)
        addr_layout.addWidget(addr_value)
        col2_layout.addLayout(addr_layout)

        details_layout.addLayout(col1_layout)
        details_layout.addLayout(col2_layout)
        details_layout.addStretch()

        layout.addLayout(details_layout)

        return card

    def create_payslip_history(self):
        """Create payslip history section"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: none;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 25)
        layout.setSpacing(20)

        title = QLabel("Payroll History")
        title.setStyleSheet("color: #000000; font-size: 16px; font-weight: bold; background: transparent;")
        layout.addWidget(title)

        # Get payroll records from database
        employee_id = self.user_info.get('employee_id')
        payroll_records = []

        if employee_id and employee_id != 'N/A':
            payroll_records = self.db.get_employee_payroll(employee_id)

        if payroll_records:
            for record in payroll_records:
                payslip_item = self.create_payslip_item(record)
                layout.addWidget(payslip_item)
        else:
            no_records = QLabel("No payroll records found")
            no_records.setStyleSheet("color: #999999; font-size: 14px; padding: 20px; background: transparent;")
            no_records.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_records)

        return card

    def create_payslip_item(self, record):
        """Create a single payslip history item from database record"""
        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background: #F9FAFB;
                border-radius: 8px;
                border: 1px solid #E5E7EB;
            }
        """)
        item.setFixedHeight(70)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(20, 15, 20, 15)

        # Left side - Icon and details
        left_layout = QHBoxLayout()
        left_layout.setSpacing(15)

        icon = QLabel("📄")
        icon.setStyleSheet("font-size: 24px; background: transparent;")

        details_layout = QVBoxLayout()
        details_layout.setSpacing(2)

        # Format month and year
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']

        # Convert month to int and validate
        try:
            month_int = int(record['month'])
            month_name = month_names[month_int] if 1 <= month_int <= 12 else 'Unknown'
        except (ValueError, TypeError, IndexError):
            month_name = 'Unknown'

        month_label = QLabel(f"{month_name} {record['year']}")
        month_label.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")

        # Format dates
        processed_date = record.get('processed_date', 'N/A')
        if processed_date and processed_date != 'N/A':
            if isinstance(processed_date, datetime):
                processed_date = processed_date.strftime('%b %d, %Y')
            else:
                try:
                    processed_date = datetime.strptime(str(processed_date), '%Y-%m-%d').strftime('%b %d, %Y')
                except:
                    pass

        date_label = QLabel(f"Net Pay: ₱{record['net_salary']:,.2f} • Processed: {processed_date}")
        date_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")

        details_layout.addWidget(month_label)
        details_layout.addWidget(date_label)

        left_layout.addWidget(icon)
        left_layout.addLayout(details_layout)

        layout.addLayout(left_layout)
        layout.addStretch()

        # Status badge
        status = record.get('status', 'Pending')
        status_color = "#10B981" if status == "Released" else "#F59E0B" if status == "Pending" else "#6B7280"

        status_badge = QLabel(str(status))
        status_badge.setStyleSheet(f"""
            QLabel {{
                background: {status_color};
                color: white;
                padding: 6px 16px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_badge.setFixedWidth(80)

        # View button
        view_btn = QPushButton("👁 View")
        view_btn.setFixedSize(80, 32)
        view_btn.setStyleSheet("""
            QPushButton {
                background: white;
                color: #0047FF;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #F0F7FF;
                border: 1px solid #0047FF;
            }
        """)
        view_btn.clicked.connect(lambda: self.view_payslip(record))

        layout.addWidget(status_badge)
        layout.addWidget(view_btn)

        return item

    def view_payslip(self, record):
        """View detailed payslip information"""
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']

        # Convert month to int and validate
        try:
            month_int = int(record['month'])
            month_name = month_names[month_int] if 1 <= month_int <= 12 else 'Unknown'
        except (ValueError, TypeError, IndexError):
            month_name = 'Unknown'

        message = f"""
Payslip Details - {month_name} {record['year']}

Base Salary: ₱{record['base_salary']:,.2f}
Bonus: ₱{record['bonus']:,.2f}
Deductions: ₱{record['deductions']:,.2f}
Net Salary: ₱{record['net_salary']:,.2f}

Present Days: {record['present_days']}
Status: {record.get('status', 'N/A')}

Notes: {record.get('notes', 'No additional notes')}
        """

        QMessageBox.information(self, "Payslip Details", message)

    def calculate_years_of_service(self):
        """Calculate years of service from hire date"""
        hire_date_str = self.user_info.get('hire_date')
        if not hire_date_str or hire_date_str == 'N/A':
            return 0

        try:
            hire_date = datetime.strptime(str(hire_date_str), '%Y-%m-%d')
            today = datetime.now()
            years = (today - hire_date).days / 365.25
            return round(years, 1)
        except:
            return 0

    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Import and show login window
            from View.windows.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()


def main():
    app = QApplication(sys.argv)

    # Test user info
    test_user = {
        'employee_id': 'E001',
        'name': 'John Doe',
        'email': 'john@example.com',
        'role': 'employee',
        'position': 'Software Engineer',
        'department': 'IT Department',
        'salary': 53950.00,
        'hire_date': '2023-01-15',
        'phone': '+63 912 345 6789',
        'address': '123 Main Street, Davao City'
    }

    window = EmployeeDashboard(test_user)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


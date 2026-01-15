import sys
import hashlib
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QScrollArea, QComboBox,
    QDateEdit, QMessageBox, QGridLayout
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from Model.database import get_db_connection


def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


class AddEmployeeModule(QMainWindow):
    def __init__(self, user_info=None):
        super().__init__()
        self.setWindowTitle("PayEase - Add New Staff Member")
        self.setMinimumSize(900, 800)
        self.user_info = user_info

        # Initialize database connection
        self.db = get_db_connection()
        if not self.db.is_connected():
            self.db.connect()

        # Field references (will be set during form creation)
        self.username_input = None
        self.password_input = None
        self.fullname_input = None
        self.email_input = None
        self.role_combo = None
        self.position_input = None
        self.salary_input = None
        self.department_combo = None
        self.hiredate_input = None
        self.phone_input = None
        self.address_input = None

        self.setStyleSheet("""
            QMainWindow {
                background: #F5F7FA;
            }
        """)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #F5F7FA;
            }
            QScrollBar:vertical {
                background: #F5F7FA;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #AAAAAA;
            }
        """)

        # Content widget
        content_widget = QWidget()
        content_widget.setStyleSheet("background: #F5F7FA;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)

        # Form container
        form_container = self.create_form_container()
        content_layout.addWidget(form_container)
        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def create_header(self):
        """Create the top header"""
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background: #0047FF;
                border: none;
            }
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)

        # Left side - Title
        left_layout = QHBoxLayout()
        left_layout.setSpacing(15)

        icon = QLabel("👤")
        icon.setStyleSheet("font-size: 24px; background: transparent;")
        left_layout.addWidget(icon)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        title = QLabel("Add New Staff Member")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; background: transparent;")
        title_layout.addWidget(title)

        left_layout.addLayout(title_layout)
        layout.addLayout(left_layout)

        layout.addStretch()

        # Right side - Back button
        back_btn = QPushButton("← Back to Staff")
        back_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                padding: 8px 20px;
                font-size: 13px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: white;
                color: #0047FF;
            }
        """)
        back_btn.clicked.connect(self.close)
        layout.addWidget(back_btn)

        return header

    def create_form_container(self):
        """Create the main form container"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: none;
            }
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Section 1: Account Information
        section1_header = self.create_section_header("Account Information")
        layout.addWidget(section1_header)

        section1_content = self.create_account_section()
        layout.addWidget(section1_content)

        # Divider
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.Shape.HLine)
        divider1.setStyleSheet("background: #E0E0E0;")
        divider1.setFixedHeight(1)
        layout.addWidget(divider1)

        # Section 2: Employment Details
        section2_header = self.create_section_header("Employment Details")
        layout.addWidget(section2_header)

        section2_content = self.create_employment_section()
        layout.addWidget(section2_content)

        # Divider
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.Shape.HLine)
        divider2.setStyleSheet("background: #E0E0E0;")
        divider2.setFixedHeight(1)
        layout.addWidget(divider2)

        # Section 3: Additional Information
        section3_header = self.create_section_header("Additional Information")
        layout.addWidget(section3_header)

        section3_content = self.create_additional_section()
        layout.addWidget(section3_content)

        # Buttons section
        button_section = self.create_button_section()
        layout.addWidget(button_section)

        return container

    def create_section_header(self, title):
        """Create a section header"""
        header = QFrame()
        header.setStyleSheet("background: white; border: none;")
        header.setFixedHeight(50)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 15, 30, 15)
        layout.setSpacing(12)

        icon = QLabel("📋")
        icon.setStyleSheet("font-size: 18px; background: transparent;")
        icon.setFixedWidth(30)

        label = QLabel(title)
        label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        label.setStyleSheet("color: #111827; background: transparent;")

        layout.addWidget(icon)
        layout.addWidget(label)
        layout.addStretch()

        return header

    def create_account_section(self):
        """Create account information section"""
        section = QFrame()
        section.setStyleSheet("background: white; border: none;")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Grid layout for form fields
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        # Row 1: Username and Password
        username_label = QLabel("Username *")
        username_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username for login")
        self.username_input.setMinimumHeight(45)
        self.username_input.setMinimumWidth(200)
        self.username_input.setClearButtonEnabled(True)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #0047FF;
                background: #F8F9FF;
            }
            QLineEdit:hover {
                border: 2px solid #91B3FA;
            }
        """)

        password_label = QLabel("Password *")
        password_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password for login")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.setMinimumWidth(200)
        self.password_input.setClearButtonEnabled(True)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #5B6FD8;
                background: #F8F9FF;
            }
            QLineEdit:hover {
                border: 2px solid #BCCEF7;
            }
        """)

        grid.addWidget(username_label, 0, 0)
        grid.addWidget(self.username_input, 1, 0)
        grid.addWidget(password_label, 0, 1)
        grid.addWidget(self.password_input, 1, 1)

        # Row 2: Full Name and Email
        fullname_label = QLabel("Full Name *")
        fullname_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter full name")
        self.fullname_input.setMinimumHeight(45)
        self.fullname_input.setMinimumWidth(200)
        self.fullname_input.setClearButtonEnabled(True)
        self.fullname_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #5B6FD8;
                background: #F8F9FF;
            }
            QLineEdit:hover {
                border: 2px solid #BCCEF7;
            }
        """)

        email_label = QLabel("Email *")
        email_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setMinimumHeight(45)
        self.email_input.setMinimumWidth(200)
        self.email_input.setClearButtonEnabled(True)
        self.email_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #5B6FD8;
                background: #F8F9FF;
            }
            QLineEdit:hover {
                border: 2px solid #BCCEF7;
            }
        """)

        grid.addWidget(fullname_label, 3, 0)
        grid.addWidget(self.fullname_input, 4, 0)
        grid.addWidget(email_label, 3, 1)
        grid.addWidget(self.email_input, 4, 1)

        # Row 3: Role
        role_label = QLabel("Role *")
        role_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Employee", "Manager", "HR", "Finance", "Admin"])
        self.role_combo.setMinimumHeight(45)
        self.role_combo.setMinimumWidth(200)
        self.role_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QComboBox:focus {
                border: 2px solid #0047FF;
                background: #F8F9FF;
            }
            QComboBox:hover {
                border: 2px solid #91B3FA;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #E0E0E0;
                background: white;
                selection-background-color: #0047FF;
                selection-color: white;
            }
        """)

        grid.addWidget(role_label, 5, 0)
        grid.addWidget(self.role_combo, 6, 0)

        layout.addLayout(grid)

        return section

    def create_employment_section(self):
        """Create employment details section"""
        section = QFrame()
        section.setStyleSheet("background: white; border: none;")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        # Row 1: Position and Salary
        position_label = QLabel("Position *")
        position_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("e.g., Senior Manager")
        self.position_input.setMinimumHeight(45)
        self.position_input.setMinimumWidth(200)
        self.position_input.setClearButtonEnabled(True)
        self.position_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #5B6FD8;
                background: #F8F9FF;
            }
            QLineEdit:hover {
                border: 2px solid #BCCEF7;
            }
        """)

        salary_label = QLabel("Salary *")
        salary_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("e.g., 50000")
        self.salary_input.setMinimumHeight(45)
        self.salary_input.setMinimumWidth(200)
        self.salary_input.setClearButtonEnabled(True)
        self.salary_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #5B6FD8;
                background: #F8F9FF;
            }
            QLineEdit:hover {
                border: 2px solid #BCCEF7;
            }
        """)

        salary_note = QLabel("Monthly salary in PHP")
        salary_note.setStyleSheet("color: #999999; font-size: 11px; background: transparent;")

        grid.addWidget(position_label, 0, 0)
        grid.addWidget(self.position_input, 1, 0)
        grid.addWidget(salary_label, 0, 1)
        grid.addWidget(self.salary_input, 1, 1)
        grid.addWidget(salary_note, 2, 1)

        # Row 2: Department and Hire Date
        department_label = QLabel("Department *")
        department_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.department_combo = QComboBox()
        self.department_combo.addItems(["Engineering", "Sales", "HR", "Finance", "Operations", "Marketing"])
        self.department_combo.setMinimumHeight(45)
        self.department_combo.setMinimumWidth(200)
        self.department_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QComboBox:focus {
                border: 2px solid #5B6FD8;
                background: #F8F9FF;
            }
            QComboBox:hover {
                border: 2px solid #BCCEF7;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #E0E0E0;
                background: white;
                selection-background-color: #5B6FD8;
                selection-color: white;
            }
        """)

        hiredate_label = QLabel("Hire Date *")
        hiredate_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.hiredate_input = QDateEdit()
        self.hiredate_input.setDate(QDate.currentDate())
        self.hiredate_input.setMinimumHeight(45)
        self.hiredate_input.setMinimumWidth(200)
        self.hiredate_input.setCalendarPopup(True)
        self.hiredate_input.setStyleSheet("""
            QDateEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QDateEdit:focus {
                border: 2px solid #0047FF;
                background: #F8F9FF;
            }
            QDateEdit:hover {
                border: 2px solid #91B3FA;
            }
            QDateEdit::drop-down {
                border: none;
                padding-right: 10px;
            }
        """)

        grid.addWidget(department_label, 3, 0)
        grid.addWidget(self.department_combo, 4, 0)
        grid.addWidget(hiredate_label, 3, 1)
        grid.addWidget(self.hiredate_input, 4, 1)

        layout.addLayout(grid)

        return section

    def create_additional_section(self):
        """Create additional information section"""
        section = QFrame()
        section.setStyleSheet("background: white; border: none;")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        # Phone and Address
        phone_label = QLabel("Phone Number")
        phone_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+63 912 345 6789")
        self.phone_input.setMinimumHeight(45)
        self.phone_input.setMinimumWidth(200)
        self.phone_input.setClearButtonEnabled(True)
        self.phone_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #5B6FD8;
                background: #F8F9FF;
            }
            QLineEdit:hover {
                border: 2px solid #BCCEF7;
            }
        """)

        address_label = QLabel("Address")
        address_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold;")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("123 Main Street, City")
        self.address_input.setMinimumHeight(45)
        self.address_input.setMinimumWidth(200)
        self.address_input.setClearButtonEnabled(True)
        self.address_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #5B6FD8;
                background: #F8F9FF;
            }
            QLineEdit:hover {
                border: 2px solid #BCCEF7;
            }
        """)

        grid.addWidget(phone_label, 0, 0)
        grid.addWidget(self.phone_input, 1, 0)
        grid.addWidget(address_label, 0, 1)
        grid.addWidget(self.address_input, 1, 1)

        layout.addLayout(grid)

        return section

    def create_button_section(self):
        """Create action buttons section"""
        section = QFrame()
        section.setStyleSheet("background: white; border: none;")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(15)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(140, 45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #F5F5F5;
                color: #374151;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #E5E7EB;
            }
        """)

        # Save button
        save_btn = QPushButton("Save Employee")
        save_btn.setFixedSize(140, 45)
        save_btn.setStyleSheet("""
            QPushButton {
                background: #0047FF;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0039CC;
            }
            QPushButton:pressed {
                background: #002E99;
            }
        """)

        save_btn.clicked.connect(self.save_employee)
        cancel_btn.clicked.connect(self.cancel_action)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

        return section

    def save_employee(self):
        """Handle employee save to database"""
        # Validate required fields
        if not self.username_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Username is required")
            self.username_input.setFocus()
            return

        if not self.password_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Password is required")
            self.password_input.setFocus()
            return

        if len(self.password_input.text()) < 6:
            QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters long")
            self.password_input.setFocus()
            return

        if not self.fullname_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Full Name is required")
            self.fullname_input.setFocus()
            return

        if not self.email_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Email is required")
            self.email_input.setFocus()
            return

        if "@" not in self.email_input.text() or "." not in self.email_input.text():
            QMessageBox.warning(self, "Validation Error", "Invalid email format. Please enter a valid email address")
            self.email_input.setFocus()
            return

        if not self.position_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Position is required")
            self.position_input.setFocus()
            return

        if not self.salary_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Salary is required")
            self.salary_input.setFocus()
            return

        try:
            salary = float(self.salary_input.text())
            if salary <= 0:
                QMessageBox.warning(self, "Validation Error", "Salary must be greater than 0")
                self.salary_input.setFocus()
                return
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Salary must be a valid number")
            self.salary_input.setFocus()
            return

        # Store plain text password to show user later
        plain_password = self.password_input.text().strip()

        # Prepare employee data
        employee_data = {
            'username': self.username_input.text().strip(),
            'password': plain_password,  # Pass as plain text - database will hash it
            'full_name': self.fullname_input.text().strip(),
            'email': self.email_input.text().strip().lower(),
            'role': self.role_combo.currentText(),
            'position': self.position_input.text().strip(),
            'salary': salary,
            'department': self.department_combo.currentText(),
            'phone': self.phone_input.text().strip(),
            'address': self.address_input.text().strip(),
            'date_hired': self.hiredate_input.date().toString('yyyy-MM-dd')
        }

        # Add employee to database
        success, employee_id, message = self.db.add_employee(employee_data)

        if success:
            QMessageBox.information(
                self,
                "Success",
                f"Employee added successfully!\n\n"
                f"Employee ID: {employee_id}\n"
                f"Username: {employee_data['username']}\n"
                f"Email: {employee_data['email']}\n"
                f"Password: {plain_password}\n\n"
                f"⚠️ IMPORTANT: Please save these credentials and share them with the new employee.\n"
                f"The employee can login with their username or email."
            )
            # Clear form
            self.clear_form()
        else:
            QMessageBox.critical(self, "Error", f"Failed to add employee:\n{message}")

    def clear_form(self):
        """Clear all form fields"""
        self.username_input.clear()
        self.password_input.clear()
        self.fullname_input.clear()
        self.email_input.clear()
        self.position_input.clear()
        self.salary_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.role_combo.setCurrentIndex(0)
        self.department_combo.setCurrentIndex(0)
        self.hiredate_input.setDate(QDate.currentDate())

    def cancel_action(self):
        """Handle cancel action"""
        self.close()


def main():
    app = QApplication(sys.argv)
    window = AddEmployeeModule()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
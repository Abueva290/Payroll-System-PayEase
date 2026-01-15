"""
Login Window Module - Part of View Layer

This module contains the login interface for PayEase application.
All database operations are delegated to the Model layer.
"""

import sys
import hashlib
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from Model.database import get_db_connection


def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.password_visible = False
        self.main_window = None
        self.setWindowTitle("PayEase - Login")
        self.setFixedSize(950, 720)

        # Initialize database connection
        self.db = get_db_connection()
        if not self.db.is_connected():
            if not self.db.connect():
                QMessageBox.critical(self, "Database Error", "Failed to connect to database")
                return

        # Set blue background for entire window
        self.setStyleSheet("""
            QMainWindow {
                background: #0047FF;
            }
        """)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout to center the card
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create white card container
        card = QWidget()
        card.setFixedSize(460, 680)
        card.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 20px;
            }
        """)

        # Card layout
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(50, 30, 50, 40)
        card_layout.setSpacing(10)

        # Logo/Icon at the top
        logo_container = QWidget()
        logo_container.setStyleSheet("background: transparent;")
        logo_container.setFixedHeight(140)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 10, 0, 10)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo icon
        logo_icon = QLabel()
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_icon.setScaledContents(False)

        # Load the image from Asset folder in PayEase
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "PayEase", "Asset", "Payease.png")

        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            print(f"Original logo size: {pixmap.width()}x{pixmap.height()}")

            # Scale to show full logo
            scaled_pixmap = pixmap.scaled(
                180, 120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_icon.setPixmap(scaled_pixmap)
            logo_icon.setFixedSize(scaled_pixmap.size())
            logo_icon.setStyleSheet("background: transparent;")
            print(f"Scaled logo to: {scaled_pixmap.width()}x{scaled_pixmap.height()}")
        else:
            logo_icon.setFixedSize(120, 80)
            logo_icon.setText("💳")
            logo_icon.setStyleSheet("""
                background: #0047FF;
                color: white;
                font-size: 48px;
                border-radius: 20px;
            """)
            print(f"Warning: Logo not found at {logo_path}")

        logo_layout.addWidget(logo_icon)

        card_layout.addWidget(logo_container)
        card_layout.addSpacing(15)

        # Title
        title = QLabel("Welcome Back")
        title.setStyleSheet("color: #000000; font-size: 28px; font-weight: bold; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Sign in to continue to PayEase")
        subtitle.setStyleSheet("color: #666666; font-size: 14px; background: transparent;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(20)

        # Email/Username label
        email_label = QLabel("Email or Username")
        email_label.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")
        card_layout.addWidget(email_label)

        # Email/Username input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email or username")
        self.email_input.setFixedHeight(50)
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                border: 1px solid #E0E0E0;
                color: #000000;
            }
            QLineEdit:focus {
                border: 2px solid #0047FF;
            }
        """)
        card_layout.addWidget(self.email_input)

        card_layout.addSpacing(10)

        # Password label
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")
        card_layout.addWidget(password_label)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setFixedHeight(50)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                border: 1px solid #E0E0E0;
                color: #000000;
            }
            QLineEdit:focus {
                border: 2px solid #0047FF;
            }
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        self.email_input.returnPressed.connect(self.password_input.setFocus)
        card_layout.addWidget(self.password_input)

        card_layout.addSpacing(10)

        # Login button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setFixedHeight(50)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: #0047FF;
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background: #0039CC;
            }
            QPushButton:pressed {
                background: #002E99;
            }
            QPushButton:disabled {
                background: #A0A0A0;
                color: #E0E0E0;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)

        card_layout.addSpacing(20)

        # Footer text
        footer = QLabel("Contact your administrator for account access")
        footer.setStyleSheet("color: #999999; font-size: 12px; background: transparent;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(footer)

        card_layout.addStretch()

        card.setLayout(card_layout)
        main_layout.addWidget(card)
        central_widget.setLayout(main_layout)

        # Display test credentials in console
        self.print_credentials()

    def print_credentials(self):
        """Print test credentials to console"""
        print("\n" + "=" * 65)
        print("  PayEase Payroll Management System - Login")
        print("=" * 65)
        print("\n📧 DEFAULT ADMIN CREDENTIALS:")
        print("-" * 65)
        print("  Username : admin")
        print("  Password : admin123")
        print()
        print("  Database Login:")
        print("  Use credentials from your database")
        print("  Login with either username or email")
        print("=" * 65 + "\n")

    def handle_login(self):
        """Handle login authentication with database"""
        username_or_email = self.email_input.text().strip()
        password = self.password_input.text()

        # Validation
        if not username_or_email:
            self.show_error("Please enter your email or username")
            self.email_input.setFocus()
            return

        if not password:
            self.show_error("Please enter your password")
            self.password_input.setFocus()
            return

        # Disable button during authentication
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Signing in...")

        try:
            # Check for static admin credentials first
            if username_or_email.lower() == 'admin' and password == 'admin123':
                admin_info = {
                    'username': 'admin',
                    'role': 'admin',
                    'employee_id': 'ADMIN-001',
                    'name': 'System Administrator',
                    'email': 'admin@payease.com',
                    'position': 'System Admin',
                    'department': 'Administration',
                    'salary': 0,
                    'phone': '',
                    'address': '',
                    'hire_date': 'N/A'
                }
                self.login_success(admin_info)
                return

            # Check credentials in database
            success, user_info = self.db.verify_login(username_or_email, password)

            # If failed and input looks like email, try as email
            if not success and "@" in username_or_email:
                success, user_info = self.verify_by_email(username_or_email, password)

            if success and user_info:
                self.login_success(user_info)
            else:
                self.login_failed()
        except Exception as e:
            print(f"[LOGIN ERROR] Unexpected error: {e}")
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Sign In")
            self.show_error(f"An unexpected error occurred: {str(e)}")

    def verify_by_email(self, email, password):
        """Verify login using email instead of username"""
        try:
            if not self.db.is_connected():
                self.db.connect()

            # Use plain text password (no hashing for consistency)
            query = """
                    SELECT a.username,
                           a.role,
                           a.employee_id,
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
                    WHERE e.Email = %s \
                      AND a.password = %s \
                    """
            self.db.cursor.execute(query, (email.lower(), password))
            result = self.db.cursor.fetchone()

            if result:
                # Check if employee is archived
                if result['role'] == 'employee' and result.get('is_archived'):
                    return (False, None)

                user_info = {
                    'username': result['username'],
                    'role': result['role'],
                    'employee_id': result['employee_id'] or 'N/A',
                    'name': result.get('FullName', result['username']),
                    'email': result.get('Email', ''),
                    'position': result.get('Position', 'N/A'),
                    'department': result.get('Department', 'N/A'),
                    'salary': float(result.get('Salary', 0)) if result.get('Salary') else 0,
                    'phone': result.get('Phone', ''),
                    'address': result.get('Address', ''),
                    'hire_date': str(result.get('data_hired', '')) if result.get('data_hired') else 'N/A'
                }
                return (True, user_info)

            return (False, None)

        except Exception as e:
            print(f"[LOGIN ERROR] Email verification error: {e}")
            return (False, None)

    def login_success(self, user_info):
        """Handle successful login"""
        try:
            # Close login window first
            self.close()

            # Route to appropriate dashboard based on role
            if user_info['role'] == 'employee':
                from View.windows.employee_dashboard import EmployeeDashboard
                self.main_window = EmployeeDashboard(user_info)
            else:
                from View.windows.admin_dashboard import AdminDashboard
                self.main_window = AdminDashboard(user_info)

            self.main_window.show()

        except ImportError as e:
            QMessageBox.critical(None, "Error", f"Failed to load dashboard: {str(e)}")
            # Reopen login window
            self.show()
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Sign In")
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"[LOGIN ERROR] Full traceback:\n{error_details}")
            QMessageBox.critical(None, "Error", f"Unexpected error: {str(e)}\n\nCheck console for details.")
            # Reopen login window
            self.show()
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Sign In")

    def login_failed(self):
        """Handle failed login"""
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Sign In")
        self.show_error("Invalid email/username or password.\nPlease try again.")
        self.password_input.clear()
        self.password_input.setFocus()

    def show_error(self, message):
        """Show error message"""
        QMessageBox.warning(self, "Login Error", message)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


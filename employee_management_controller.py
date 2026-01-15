import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QHeaderView, QDialog,
    QScrollArea, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from Model.database import get_db_connection

"""employee_management.py - Improved version"""


class AddEmployeeDialog(QDialog):
    """Dialog for adding/editing employees - matches add_employee.py design"""

    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.employee = employee
        self.setWindowTitle("Add Employee" if not employee else "Edit Employee")
        self.setMinimumSize(900, 750)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #F5F7FA;
            }
        """)

        self.init_ui()

    def init_ui(self):
        from PyQt6.QtWidgets import QGridLayout, QDateEdit
        from PyQt6.QtCore import QDate

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background: #0047FF;
                border: none;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 0, 30, 0)

        title = QLabel("Add New Employee" if not self.employee else "Edit Employee")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; background: transparent;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addWidget(header)

        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #F5F7FA; }")

        content = QWidget()
        content.setStyleSheet("background: #F5F7FA;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Form container
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: none;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(25)

        # Grid layout for fields
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        row = 0

        # Username
        grid.addWidget(self.create_label("Username *"), row, 0)
        self.username_input = self.create_input_field("Enter username")
        if self.employee:
            # When editing, username should be read-only since it's the login credential
            username = self.employee.get('username', '')
            if not username or str(username) == '0':
                # If no username in employee data, derive from full name or email
                full_name = self.employee.get('FullName') or self.employee.get('full_name', '')
                if full_name and str(full_name) != '0':
                    # Generate username from full name (lowercase, no spaces)
                    username = full_name.lower().replace(' ', '')
                else:
                    email = self.employee.get('Email') or self.employee.get('email', '')
                    if email and str(email) != '0' and '@' in email:
                        username = email.split('@')[0]
            self.username_input.setText(str(username))
            self.username_input.setReadOnly(True)
            self.username_input.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #E0E0E0;
                    border-radius: 8px;
                    padding: 12px 15px;
                    font-size: 14px;
                    background: #F5F5F5;
                    color: #666666;
                }
            """)
        grid.addWidget(self.username_input, row + 1, 0)

        # Password (only for new employees)
        if not self.employee:
            grid.addWidget(self.create_label("Password *"), row, 1)
            self.password_input = self.create_input_field("Enter password")
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            grid.addWidget(self.password_input, row + 1, 1)
            row += 2
        else:
            self.password_input = None
            row += 2

        # Full Name
        grid.addWidget(self.create_label("Full Name *"), row, 0)
        self.fullname_input = self.create_input_field("Enter full name")
        if self.employee:
            self.fullname_input.setText(self.employee.get('FullName') or self.employee.get('full_name', ''))
        grid.addWidget(self.fullname_input, row + 1, 0)

        # Email
        grid.addWidget(self.create_label("Email *"), row, 1)
        self.email_input = self.create_input_field("Enter email address")
        if self.employee:
            self.email_input.setText(self.employee.get('Email') or self.employee.get('email', ''))
        grid.addWidget(self.email_input, row + 1, 1)
        row += 2

        # Role
        grid.addWidget(self.create_label("Role *"), row, 0)
        self.role_combo = self.create_combo_box(["Employee", "Manager", "HR", "Finance", "Admin"])
        if self.employee:
            role = self.employee.get('Role') or self.employee.get('role', '')
            index = self.role_combo.findText(role.capitalize() if role else 'Employee')
            if index >= 0:
                self.role_combo.setCurrentIndex(index)
        grid.addWidget(self.role_combo, row + 1, 0)

        # Position
        grid.addWidget(self.create_label("Position *"), row, 1)
        self.position_input = self.create_input_field("e.g., Senior Manager")
        if self.employee:
            self.position_input.setText(self.employee.get('Position') or self.employee.get('position', ''))
        grid.addWidget(self.position_input, row + 1, 1)
        row += 2

        # Salary
        grid.addWidget(self.create_label("Salary *"), row, 0)
        self.salary_input = self.create_input_field("e.g., 50000")
        if self.employee:
            salary = self.employee.get('Salary') or self.employee.get('salary', '')
            self.salary_input.setText(str(salary) if salary and str(salary) != '0' else '')
        grid.addWidget(self.salary_input, row + 1, 0)

        # Department
        grid.addWidget(self.create_label("Department *"), row, 1)
        self.department_combo = self.create_combo_box(
            ["Engineering", "Sales", "HR", "Finance", "Operations", "Marketing"])
        if self.employee:
            dept = self.employee.get('Department') or self.employee.get('department', '')
            index = self.department_combo.findText(dept)
            if index >= 0:
                self.department_combo.setCurrentIndex(index)
        grid.addWidget(self.department_combo, row + 1, 1)
        row += 2

        # Phone (optional)
        grid.addWidget(self.create_label("Phone Number"), row, 0)
        self.phone_input = self.create_input_field("+1 (555) 000-0000")
        if self.employee:
            phone = self.employee.get('Phone') or self.employee.get('phone', '')
            self.phone_input.setText(str(phone) if phone and str(phone) != '0' else '')
        grid.addWidget(self.phone_input, row + 1, 0)

        # Address (optional)
        grid.addWidget(self.create_label("Address"), row, 1)
        self.address_input = self.create_input_field("123 Main Street, City, State")
        if self.employee:
            address = self.employee.get('Address') or self.employee.get('address', '')
            self.address_input.setText(str(address) if address and str(address) != '0' else '')
        grid.addWidget(self.address_input, row + 1, 1)

        form_layout.addLayout(grid)
        content_layout.addWidget(form_container)

        # Buttons
        button_container = QFrame()
        button_container.setStyleSheet("background: transparent; border: none;")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.addStretch()

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
        cancel_btn.clicked.connect(self.reject)

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
        save_btn.clicked.connect(self.accept)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)

        content_layout.addWidget(button_container)
        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            color: #111827; 
            font-size: 13px; 
            font-weight: bold; 
            background: transparent;
        """)
        return label

    def create_input_field(self, placeholder=""):
        input_field = QLineEdit()
        input_field.setMinimumHeight(45)
        input_field.setPlaceholderText(placeholder)
        input_field.setClearButtonEnabled(True)
        input_field.setStyleSheet("""
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
                background: #F0F7FF;
            }
            QLineEdit:hover {
                border: 2px solid #80A3FF;
            }
        """)
        return input_field

    def create_combo_box(self, items):
        combo = QComboBox()
        combo.addItems(items)
        combo.setMinimumHeight(45)
        combo.setStyleSheet("""
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
                background: #F0F7FF;
            }
            QComboBox:hover {
                border: 2px solid #80A3FF;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #6B7280;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #E0E0E0;
                background: white;
                selection-background-color: #0047FF;
                selection-color: white;
            }
        """)
        return combo

    def validate_data(self):
        if not self.username_input.text().strip():
            return False, "Username is required"
        if not self.fullname_input.text().strip():
            return False, "Full Name is required"
        if not self.email_input.text().strip():
            return False, "Email is required"
        if "@" not in self.email_input.text():
            return False, "Invalid email format"
        if not self.position_input.text().strip():
            return False, "Position is required"
        if not self.salary_input.text().strip():
            return False, "Salary is required"
        try:
            float(self.salary_input.text().strip())
        except ValueError:
            return False, "Salary must be a valid number"
        if self.password_input and not self.password_input.text().strip():
            return False, "Password is required"
        return True, ""

    def get_data(self):
        return {
            'username': self.username_input.text().strip(),
            'password': self.password_input.text() if self.password_input else '',
            'full_name': self.fullname_input.text().strip(),
            'email': self.email_input.text().strip(),
            'role': self.role_combo.currentText().lower(),
            'position': self.position_input.text().strip(),
            'salary': self.salary_input.text().strip(),
            'department': self.department_combo.currentText(),
            'phone': self.phone_input.text().strip(),
            'address': self.address_input.text().strip(),
            'hire_date': '',
        }


class EmployeeManagementWindow(QMainWindow):
    """Main window for employee management"""

    employee_updated = pyqtSignal()  # Signal to notify when employees are updated

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PayEase - Employee Management")
        self.setMinimumSize(1400, 800)

        # Store reference to dashboard parent
        self.dashboard_parent = None

        # Initialize database connection
        self.db = get_db_connection()
        if not self.db.is_connected():
            self.db.connect()

        # Load employees from database
        self.employees = self.db.get_all_employees()
        if not self.employees:
            self.employees = []

        # Filter to show only active (non-archived) employees by default
        self.show_archived = False

        self.setStyleSheet("""
            QMainWindow {
                background: #F5F7FA;
            }
        """)

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Content (no header - will be embedded in dashboard)
        content = QWidget()
        content.setStyleSheet("background: #F5F7FA;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(25)

        # Title and Add button
        title_row = QHBoxLayout()

        title_container = QHBoxLayout()
        title_icon = QLabel("👥")
        title_icon.setStyleSheet("font-size: 28px; background: transparent;")
        title_label = QLabel("Manage Staff Members")
        title_label.setStyleSheet("""
            color: #000000;
            font-size: 24px;
            font-weight: bold;
            background: transparent;
        """)
        title_container.addWidget(title_icon)
        title_container.addWidget(title_label)
        title_container.addStretch()

        # View Archived button
        self.view_archived_btn = QPushButton("📁 View Archived")
        self.view_archived_btn.setStyleSheet("""
            QPushButton {
                background: #F59E0B;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #D97706;
            }
        """)
        self.view_archived_btn.clicked.connect(self.toggle_archived_view)

        add_btn = QPushButton("➕ Add New Staff")
        add_btn.setStyleSheet("""
            QPushButton {
                background: #0047FF;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0039CC;
            }
        """)
        add_btn.clicked.connect(self.add_employee)

        title_row.addLayout(title_container)
        title_row.addWidget(self.view_archived_btn)
        title_row.addSpacing(10)
        title_row.addWidget(add_btn)
        content_layout.addLayout(title_row)

        # Search and filter
        search_row = QHBoxLayout()
        search_row.setSpacing(15)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search staff by name, email...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                font-size: 14px;
                background: white;
                color: #1F2937;
            }
            QLineEdit:focus {
                border: 2px solid #0047FF;
            }
        """)
        self.search_input.textChanged.connect(self.search_employees)

        self.role_filter = QComboBox()
        self.role_filter.addItems(["All Roles", "Admin", "Manager", "Employee"])
        self.role_filter.setStyleSheet("""
            QComboBox {
                padding: 12px 15px;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                font-size: 14px;
                background: white;
                color: #1F2937;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #E0E0E0;
                selection-background-color: #0047FF;
                color: #1F2937;
            }
        """)
        self.role_filter.currentTextChanged.connect(self.filter_by_role)

        search_row.addWidget(self.search_input, 3)
        search_row.addWidget(self.role_filter, 1)
        content_layout.addLayout(search_row)

        # Table
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "FULL NAME", "EMAIL", "ROLE",
            "POSITION", "DEPARTMENT", "ACTIONS"
        ])

        # IMPROVED TABLE STYLING
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background: white;
                gridline-color: #E5E7EB;
                border-radius: 12px;
                font-size: 13px;
                color: #1F2937;
            }
            QTableWidget::item {
                padding: 15px 10px;
                border-bottom: 1px solid #E5E7EB;
                color: #1F2937;
            }
            QTableWidget::item:selected {
                background: #E3F2FD;
                color: #1F2937;
            }
            QHeaderView::section {
                background: #0047FF;
                color: white;
                padding: 16px 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 12px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 12px;
            }
            QScrollBar:vertical {
                border: none;
                background: #F9FAFB;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #D1D5DB;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9CA3AF;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # Configure header - CENTERED AND IMPROVED COLUMN WIDTHS
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        # Set specific column widths for better layout
        self.table.setColumnWidth(0, 80)  # ID - fixed
        self.table.setColumnWidth(1, 200)  # Full Name
        self.table.setColumnWidth(2, 250)  # Email
        self.table.setColumnWidth(3, 100)  # Role - fixed
        self.table.setColumnWidth(4, 180)  # Position
        self.table.setColumnWidth(5, 120)  # Department - fixed
        self.table.setColumnWidth(6, 330)  # Actions - INCREASED for better button spacing with new design

        # Set resize modes - allow some columns to stretch
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Full Name - stretch
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Email - stretch
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Role
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)  # Position
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Department
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Actions

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(True)  # Show grid for better readability

        # Set consistent row height - INCREASED to show buttons properly
        self.table.verticalHeader().setDefaultSectionSize(70)  # Increased from 60 to 70

        table_layout.addWidget(self.table)
        content_layout.addWidget(table_frame)

        layout.addWidget(content)

        # Load and display employees
        self.load_employees()

    def toggle_archived_view(self):
        """Toggle between active and archived employees"""
        self.show_archived = not self.show_archived
        if self.show_archived:
            self.view_archived_btn.setText("👥 View Active")
            self.view_archived_btn.setStyleSheet("""
                QPushButton {
                    background: #10B981;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    font-size: 14px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #059669;
                }
            """)
        else:
            self.view_archived_btn.setText("📁 View Archived")
            self.view_archived_btn.setStyleSheet("""
                QPushButton {
                    background: #F59E0B;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    font-size: 14px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #D97706;
                }
            """)
        self.load_employees()

    def load_employees(self, role_filter=None):
        """Load employees into table"""
        # Reload from database to get fresh data
        self.employees = self.db.get_all_employees()
        if not self.employees:
            self.employees = []

        # Filter by archived status
        filtered_employees = []
        for e in self.employees:
            is_archived = e.get('is_archived', False) or e.get('archived', False)

            # Skip invalid entries
            full_name = e.get('FullName') or e.get('full_name', '')
            email = e.get('Email') or e.get('email', '')
            if str(full_name) == '0' and str(email) == '0':
                continue

            # Check if most fields are empty/zero
            non_empty = sum([
                bool(str(e.get('username', '')).strip() and str(e.get('username', '')) != '0'),
                bool(str(full_name).strip() and str(full_name) != '0'),
                bool(str(email).strip() and str(email) != '0'),
            ])
            if non_empty < 2:
                continue

            if self.show_archived:
                if is_archived:
                    filtered_employees.append(e)
            else:
                if not is_archived:
                    filtered_employees.append(e)

        if role_filter and role_filter != "All Roles":
            filtered_employees = [e for e in filtered_employees if
                                  (e.get('Role') or e.get('role', '')).lower() == role_filter.lower()]

        self.display_employees(filtered_employees)

    def display_employees(self, employees):
        """Display employees in table"""
        self.table.setRowCount(0)

        for employee in employees:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Get employee data
            emp_id = employee.get('Employee_ID') or employee.get('id', '')
            full_name = employee.get('FullName') or employee.get('full_name', '') or ''
            email = employee.get('Email') or employee.get('email', '') or ''
            role = employee.get('Role') or employee.get('role', '') or ''
            position = employee.get('Position') or employee.get('position', '') or ''
            department = employee.get('Department') or employee.get('department', '') or ''
            is_archived = employee.get('is_archived', False) or employee.get('archived', False)

            # Format the ID
            if emp_id and str(emp_id) != '0':
                if isinstance(emp_id, int) or (isinstance(emp_id, str) and emp_id.isdigit()):
                    formatted_id = f"E{int(emp_id):03d}"
                else:
                    formatted_id = str(emp_id)
            else:
                formatted_id = f"E{row + 1:03d}"

            # Create table items with proper alignment and styling - ALL CENTERED
            id_item = QTableWidgetItem(formatted_id)
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            id_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))

            name_item = QTableWidgetItem(str(full_name) if full_name and str(full_name) != '0' else '')
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            name_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))

            email_item = QTableWidgetItem(str(email) if email and str(email) != '0' else '')
            email_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

            role_text = str(role).upper() if role and str(role) != '0' else ''
            role_item = QTableWidgetItem(role_text)
            role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

            # Color code roles
            if role_text == 'ADMIN':
                role_item.setForeground(QColor('#DC2626'))
            elif role_text == 'MANAGER':
                role_item.setForeground(QColor('#2563EB'))
            else:
                role_item.setForeground(QColor('#059669'))

            position_item = QTableWidgetItem(str(position) if position and str(position) != '0' else '')
            position_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

            dept_item = QTableWidgetItem(str(department) if department and str(department) != '0' else '')
            dept_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

            # Set items in table (7 columns total)
            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, email_item)
            self.table.setItem(row, 3, role_item)
            self.table.setItem(row, 4, position_item)
            self.table.setItem(row, 5, dept_item)

            # IMPROVED ACTION BUTTONS WITH MODERN DESIGN
            action_widget = QWidget()
            action_widget.setStyleSheet("background: transparent; border: none;")
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 8, 5, 8)  # Adjusted margins to fit in row
            action_layout.setSpacing(10)  # Good spacing between buttons
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if is_archived:
                # Restore button for archived employees
                restore_btn = QPushButton("↩️ Restore")
                restore_btn.setFixedSize(110, 42)  # Good size that fits in 70px row
                restore_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                restore_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #10B981, stop:1 #059669);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 700;
                        padding: 10px 14px;
                        text-align: center;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #059669, stop:1 #047857);
                        transform: translateY(-1px);
                    }
                    QPushButton:pressed {
                        background: #047857;
                        transform: translateY(0px);
                    }
                """)
                restore_btn.setToolTip("Restore Employee")
                restore_btn.clicked.connect(lambda checked, e=employee: self.restore_employee(e))
                action_layout.addWidget(restore_btn)
            else:
                # Records button (green) - navigates to attendance
                records_btn = QPushButton("📋 Records")
                records_btn.setFixedSize(100, 42)  # Good size that fits in 70px row
                records_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                records_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #10B981, stop:1 #059669);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 700;
                        padding: 10px 12px;
                        text-align: center;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #059669, stop:1 #047857);
                        transform: translateY(-1px);
                    }
                    QPushButton:pressed {
                        background: #047857;
                        transform: translateY(0px);
                    }
                """)
                records_btn.setToolTip("View Attendance Records")
                records_btn.clicked.connect(lambda checked, e=employee: self.view_attendance(e))

                # Edit button
                edit_btn = QPushButton("✏️ Edit")
                edit_btn.setFixedSize(80, 42)  # Good size that fits in 70px row
                edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #0047FF, stop:1 #0039CC);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 700;
                        padding: 10px 12px;
                        text-align: center;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #0039CC, stop:1 #002E99);
                        transform: translateY(-1px);
                    }
                    QPushButton:pressed {
                        background: #002E99;
                        transform: translateY(0px);
                    }
                """)
                edit_btn.setToolTip("Edit Employee")
                edit_btn.clicked.connect(lambda checked, e=employee: self.edit_employee(e))

                # Archive button
                archive_btn = QPushButton("📁 Archive")
                archive_btn.setFixedSize(100, 42)  # Good size that fits in 70px row
                archive_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                archive_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #F59E0B, stop:1 #D97706);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 700;
                        padding: 10px 12px;
                        text-align: center;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #D97706, stop:1 #B45309);
                        transform: translateY(-1px);
                    }
                    QPushButton:pressed {
                        background: #B45309;
                        transform: translateY(0px);
                    }
                """)
                archive_btn.setToolTip("Archive Employee")
                archive_btn.clicked.connect(lambda checked, e=employee: self.archive_employee(e))

                action_layout.addWidget(records_btn)
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(archive_btn)

            self.table.setCellWidget(row, 6, action_widget)

        if self.table.rowCount() == 0:
            self.table.setRowCount(1)
            message = "No archived employees found" if self.show_archived else "No active employees found"
            no_data_item = QTableWidgetItem(message)
            no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_item.setFlags(Qt.ItemFlag.NoItemFlags)
            no_data_item.setForeground(QColor('#6B7280'))
            font = QFont("Arial", 13)
            font.setItalic(True)
            no_data_item.setFont(font)
            self.table.setSpan(0, 0, 1, 7)
            self.table.setItem(0, 0, no_data_item)

    def add_employee(self):
        """Open dialog to add new employee"""
        dialog = AddEmployeeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            is_valid, message = dialog.validate_data()
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", message)
                return

            data = dialog.get_data()

            # Prepare employee data for database
            employee_data = {
                'username': data['username'],
                'full_name': data['full_name'],
                'email': data['email'],
                'role': data['role'],
                'position': data['position'],
                'salary': data['salary'],
                'department': data['department'],
                'phone': data.get('phone', ''),
                'address': data.get('address', ''),
                'date_hired': data.get('date_hired', ''),
                'password': data.get('password', ''),
                'is_archived': False
            }

            # Add to database
            success, employee_id, db_message = self.db.add_employee(employee_data)

            if success:
                # Reload and emit signal
                self.load_employees()
                self.employee_updated.emit()
                QMessageBox.information(self, "Success", f"Employee added successfully!\n\n{db_message}")
            else:
                QMessageBox.critical(self, "Error", f"Failed to add employee:\n{db_message}")

    def edit_employee(self, employee):
        """Open dialog to edit employee"""
        print(f"[DEBUG] Editing employee: {employee}")  # Debug print

        dialog = AddEmployeeDialog(self, employee)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            is_valid, message = dialog.validate_data()
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", message)
                return

            data = dialog.get_data()
            print(f"[DEBUG] Form data: {data}")  # Debug print

            # Get the employee ID from the record
            emp_id = employee.get('Employee_ID') or employee.get('id')
            print(f"[DEBUG] Employee ID: {emp_id}")  # Debug print

            # Prepare update data (excluding username and password for edits)
            update_data = {
                'full_name': data['full_name'],
                'email': data['email'],
                'role': data['role'],
                'position': data['position'],
                'salary': data['salary'],
                'department': data['department'],
                'phone': data.get('phone', ''),
                'address': data.get('address', '')
            }

            print(f"[DEBUG] Update data: {update_data}")  # Debug print

            # Update in database
            success, db_message = self.db.update_employee(emp_id, update_data)

            if success:
                # Reload and emit signal
                self.load_employees()
                self.employee_updated.emit()
                QMessageBox.information(self, "Success", "Employee updated successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to update employee:\n{db_message}")

    def archive_employee(self, employee):
        """Archive employee instead of deleting"""
        emp_id = employee.get('Employee_ID') or employee.get('id')
        emp_name = employee.get('FullName') or employee.get('full_name', 'this employee')

        reply = QMessageBox.question(
            self, "Confirm Archive",
            f"Are you sure you want to archive {emp_name}?\n\nArchived employees can be restored later.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Update employee to archived status
            update_data = {'is_archived': True}

            # Update in database
            success, message = self.db.update_employee(emp_id, update_data)

            if success:
                self.load_employees()
                self.employee_updated.emit()
                QMessageBox.information(self, "Success", f"{emp_name} has been archived successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to archive employee:\n{message}")

    def restore_employee(self, employee):
        """Restore archived employee"""
        emp_id = employee.get('Employee_ID') or employee.get('id')
        emp_name = employee.get('FullName') or employee.get('full_name', 'this employee')

        reply = QMessageBox.question(
            self, "Confirm Restore",
            f"Are you sure you want to restore {emp_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Update employee to active status
            update_data = {'is_archived': False}

            # Update in database
            success, message = self.db.update_employee(emp_id, update_data)

            if success:
                self.load_employees()
                self.employee_updated.emit()
                QMessageBox.information(self, "Success", f"{emp_name} has been restored successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to restore employee:\n{message}")

    def search_employees(self, search_term):
        """Search employees"""
        if search_term.strip():
            filtered = []
            for e in self.employees:
                # Check archived status
                is_archived = e.get('is_archived', False) or e.get('archived', False)
                if self.show_archived != is_archived:
                    continue

                full_name = e.get('FullName') or e.get('full_name', '')
                email = e.get('Email') or e.get('email', '')

                # Skip invalid entries
                if str(full_name) == '0' and str(email) == '0':
                    continue

                search_lower = search_term.lower()
                if (search_lower in str(full_name).lower() or
                        search_lower in str(email).lower()):
                    filtered.append(e)

            self.display_employees(filtered)
        else:
            self.load_employees()

    def view_attendance(self, employee):
        """Navigate to attendance management for this employee"""
        print(f"[DEBUG] Viewing attendance for employee: {employee.get('FullName')}")

        # Use the stored dashboard parent reference
        if self.dashboard_parent and hasattr(self.dashboard_parent, 'open_attendance_for_employee'):
            print("[DEBUG] Using dashboard_parent, opening attendance for specific employee")
            self.dashboard_parent.open_attendance_for_employee(employee)
            return

        # Fallback: Show message if can't access dashboard
        print("[DEBUG] No dashboard_parent reference found")
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Attendance",
            f"Opening attendance records for {employee.get('FullName') or 'employee'}..."
        )

    def filter_by_role(self, role):
        """Filter employees by role"""
        self.load_employees(role if role != "All Roles" else None)


def main():
    app = QApplication(sys.argv)
    window = EmployeeManagementWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
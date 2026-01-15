import sys
from datetime import datetime, date
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QHeaderView, QDialog,
    QScrollArea, QDateEdit, QTimeEdit, QGridLayout
)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont, QColor


class AddAttendanceDialog(QDialog):
    """Dialog for adding attendance records"""

    def __init__(self, parent=None, employees=None, selected_employee=None):
        super().__init__(parent)
        self.employees = employees or []
        self.selected_employee = selected_employee
        self.setWindowTitle("Add Attendance Record")
        self.setMinimumSize(900, 650)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #F5F7FA;
            }
        """)

        self.init_ui()

    def init_ui(self):
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

        title = QLabel("Add Attendance Record")
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

        # Common styles
        label_style = "color: #111827; font-size: 13px; font-weight: bold;"
        input_style = """
            QComboBox, QDateEdit, QTimeEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #111827;
                min-height: 45px;
            }
            QComboBox:focus, QDateEdit:focus, QTimeEdit:focus {
                border: 2px solid #0047FF;
                background: #F0F7FF;
            }
            QComboBox:hover, QDateEdit:hover, QTimeEdit:hover {
                border: 2px solid #80A3FF;
            }
            QComboBox::drop-down, QDateEdit::drop-down, QTimeEdit::drop-down {
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
                border: 2px solid #E0E0E0;
                background: white;
                color: #111827;
                selection-background-color: #0047FF;
                selection-color: white;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                color: #111827;
                min-height: 30px;
            }
            QComboBox QAbstractItemView::item:hover {
                background: #E3F2FD;
                color: #0047FF;
            }
        """

        # Employee selection
        grid.addWidget(self.create_label("Select Employee *"), row, 0)
        self.employee_combo = QComboBox()
        self.employee_combo.addItem("Select an employee...", None)

        # If specific employee is selected, only show that employee
        if self.selected_employee:
            name = self.selected_employee.get('FullName') or self.selected_employee.get('full_name', 'Unknown')
            emp_id = self.selected_employee.get('Employee_ID') or self.selected_employee.get('id')
            self.employee_combo.addItem(name, emp_id)
            self.employee_combo.setCurrentIndex(1)  # Select the employee
            self.employee_combo.setEnabled(False)  # Disable changing
        else:
            for emp in self.employees:
                name = emp.get('FullName') or emp.get('full_name', 'Unknown')
                emp_id = emp.get('Employee_ID') or emp.get('id')
                if name and str(name) != '0':
                    self.employee_combo.addItem(name, emp_id)

        self.employee_combo.setStyleSheet(input_style)
        grid.addWidget(self.employee_combo, row + 1, 0, 1, 2)
        row += 2

        # Date
        grid.addWidget(self.create_label("Date *"), row, 0)
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setStyleSheet(input_style)
        grid.addWidget(self.date_edit, row + 1, 0)

        # Status
        grid.addWidget(self.create_label("Status *"), row, 1)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Present", "Absent", "Late", "Half Day", "Leave"])
        self.status_combo.setStyleSheet(input_style)
        grid.addWidget(self.status_combo, row + 1, 1)
        row += 2

        # Check In Time
        grid.addWidget(self.create_label("Check In Time"), row, 0)
        self.checkin_edit = QTimeEdit()
        self.checkin_edit.setTime(QTime(9, 0))
        self.checkin_edit.setDisplayFormat("hh:mm AP")
        self.checkin_edit.setStyleSheet(input_style)
        grid.addWidget(self.checkin_edit, row + 1, 0)

        # Check Out Time
        grid.addWidget(self.create_label("Check Out Time"), row, 1)
        self.checkout_edit = QTimeEdit()
        self.checkout_edit.setTime(QTime(17, 0))
        self.checkout_edit.setDisplayFormat("hh:mm AP")
        self.checkout_edit.setStyleSheet(input_style)
        grid.addWidget(self.checkout_edit, row + 1, 1)

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

        save_btn = QPushButton("Save Attendance")
        save_btn.setFixedSize(160, 45)
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
        label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold; background: transparent;")
        return label

    def get_data(self):
        """Get form data"""
        return {
            'employee_id': self.employee_combo.currentData(),
            'employee_name': self.employee_combo.currentText(),
            'date': self.date_edit.date().toString('yyyy-MM-dd'),
            'status': self.status_combo.currentText(),
            'clock_in': self.checkin_edit.time().toString('HH:mm:ss'),
            'clock_out': self.checkout_edit.time().toString('HH:mm:ss')
        }


class AttendanceManagementWindow(QMainWindow):
    """Attendance Management - can show all employees or specific employee"""

    def __init__(self, user_info=None, db_manager=None, selected_employee=None):
        super().__init__()
        self.user_info = user_info or {'name': 'Admin', 'role': 'admin'}
        self.db = db_manager
        self.selected_employee = selected_employee  # Specific employee to show
        self.setWindowTitle("PayEase - Attendance Management")
        self.setMinimumSize(1400, 800)

        # Ensure attendance table exists
        if self.db:
            self.ensure_attendance_table()

        # Load data
        self.employees = self.get_employees()
        self.attendance_records = []
        self.filtered_records = []

        self.setStyleSheet("""
            QMainWindow {
                background: #F5F7FA;
            }
        """)

        self.init_ui()
        self.load_attendance()

    def ensure_attendance_table(self):
        """Ensure attendance table exists"""
        try:
            if not self.db.is_connected():
                self.db.connect()

            create_table_query = """
                                 CREATE TABLE IF NOT EXISTS attendance \
                                 ( \
                                     id \
                                     INT \
                                     AUTO_INCREMENT \
                                     PRIMARY \
                                     KEY, \
                                     employee_id \
                                     VARCHAR \
                                 ( \
                                     50 \
                                 ) NOT NULL,
                                     date DATE NOT NULL,
                                     clock_in TIME,
                                     clock_out TIME,
                                     status VARCHAR \
                                 ( \
                                     20 \
                                 ) DEFAULT 'Present',
                                     notes TEXT,
                                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                     INDEX idx_employee_id \
                                 ( \
                                     employee_id \
                                 ),
                                     INDEX idx_date \
                                 ( \
                                     date \
                                 ),
                                     UNIQUE KEY unique_attendance \
                                 ( \
                                     employee_id, \
                                     date \
                                 )
                                     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 \
                                 """
            self.db.cursor.execute(create_table_query)
            self.db.connection.commit()
            print("[ATTENDANCE] Table checked/created successfully")
        except Exception as e:
            print(f"[ATTENDANCE] Error creating table: {e}")

    def get_employees(self):
        """Get active employees from database"""
        if self.db:
            try:
                employees = self.db.get_all_employees()
                active_employees = []
                for emp in employees:
                    is_archived = emp.get('is_archived', False) or emp.get('archived', False)
                    if not is_archived:
                        full_name = emp.get('FullName') or emp.get('full_name', '')
                        if full_name and str(full_name) != '0':
                            active_employees.append(emp)
                return active_employees
            except Exception as e:
                print(f"[ATTENDANCE] Error getting employees: {e}")
        return []

    def load_attendance(self):
        """Load attendance records from database"""
        if self.db:
            try:
                # If specific employee, filter by that employee
                if self.selected_employee:
                    emp_id = self.selected_employee.get('Employee_ID') or self.selected_employee.get('id')
                    query = """
                            SELECT a.*, \
                                   e.FullName as employee_name, \
                                   e.Position as position,
                            e.Department as department
                            FROM attendance a
                                LEFT JOIN employees e \
                            ON a.employee_id = e.Employee_ID
                            WHERE a.employee_id = %s
                            ORDER BY a.date DESC, a.clock_in DESC \
                            """
                    self.db.cursor.execute(query, (emp_id,))
                else:
                    # Show all employees
                    query = """
                            SELECT a.*, \
                                   e.FullName as employee_name, \
                                   e.Position as position,
                            e.Department as department
                            FROM attendance a
                                LEFT JOIN employees e \
                            ON a.employee_id = e.Employee_ID
                            ORDER BY a.date DESC, a.clock_in DESC \
                            """
                    self.db.cursor.execute(query)

                self.attendance_records = self.db.cursor.fetchall()
                self.filtered_records = self.attendance_records
                self.display_attendance(self.filtered_records)
            except Exception as e:
                print(f"[ATTENDANCE] Error loading attendance: {e}")
                self.display_attendance([])

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Content
        content = QWidget()
        content.setStyleSheet("background: #F5F7FA;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(25)

        # Title and Add button
        title_row = QHBoxLayout()

        title_container = QHBoxLayout()
        title_icon = QLabel("📅")
        title_icon.setStyleSheet("font-size: 28px; background: transparent;")

        # Change title if specific employee
        if self.selected_employee:
            emp_name = self.selected_employee.get('FullName') or self.selected_employee.get('full_name', 'Employee')
            title_text = f"Attendance - {emp_name}"
        else:
            title_text = "Attendance Management"

        title_label = QLabel(title_text)
        title_label.setStyleSheet("""
            color: #000000;
            font-size: 24px;
            font-weight: bold;
            background: transparent;
        """)
        title_container.addWidget(title_icon)
        title_container.addWidget(title_label)
        title_container.addStretch()

        add_btn = QPushButton("➕ Add Attendance")
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
        add_btn.clicked.connect(self.add_attendance)

        title_row.addLayout(title_container)
        title_row.addWidget(add_btn)
        content_layout.addLayout(title_row)

        # Filters section (only show if not specific employee)
        if not self.selected_employee:
            filters_frame = self.create_filters_section()
            content_layout.addWidget(filters_frame)

        # Table section
        table_frame = self.create_table_section()
        content_layout.addWidget(table_frame)

        layout.addWidget(content)

    def create_filters_section(self):
        """Create filters section"""
        filters_frame = QFrame()
        filters_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: none;
            }
        """)
        filters_layout = QVBoxLayout(filters_frame)
        filters_layout.setContentsMargins(25, 20, 25, 20)
        filters_layout.setSpacing(15)

        # Filter title
        filter_title = QLabel("▼ Filters")
        filter_title.setStyleSheet("color: #000000; font-size: 16px; font-weight: bold; background: transparent;")
        filters_layout.addWidget(filter_title)

        # Filter controls
        filter_row = QHBoxLayout()
        filter_row.setSpacing(15)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search employees...")
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
        self.search_input.textChanged.connect(self.search_attendance)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Status", "Present", "Absent", "Late", "Half Day", "Leave"])
        self.status_filter.setStyleSheet("""
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
        self.status_filter.currentTextChanged.connect(self.filter_by_status)

        filter_row.addWidget(self.search_input, 3)
        filter_row.addWidget(self.status_filter, 1)
        filters_layout.addLayout(filter_row)

        return filters_frame

    def create_table_section(self):
        """Create table section"""
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)

        # Table header with count
        table_header_widget = QWidget()
        table_header_widget.setStyleSheet("background: transparent;")
        table_header_layout = QHBoxLayout(table_header_widget)
        table_header_layout.setContentsMargins(30, 20, 30, 10)

        attendance_title_layout = QHBoxLayout()
        attendance_icon = QLabel("📋")
        attendance_icon.setStyleSheet("font-size: 18px; background: transparent;")
        attendance_title = QLabel("Attendance Records")
        attendance_title.setStyleSheet("color: #000000; font-size: 16px; font-weight: bold; background: transparent;")
        self.count_label = QLabel("Showing 0 of 0 records")
        self.count_label.setStyleSheet("color: #999999; font-size: 13px; background: transparent; margin-left: 10px;")

        attendance_title_layout.addWidget(attendance_icon)
        attendance_title_layout.addWidget(attendance_title)
        attendance_title_layout.addWidget(self.count_label)
        attendance_title_layout.addStretch()

        table_header_layout.addLayout(attendance_title_layout)
        table_layout.addWidget(table_header_widget)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Name", "Position", "Date", "Clock In", "Clock Out", "Status", "Actions"
        ])

        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background: white;
                gridline-color: #E5E7EB;
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
                background: #F9FAFB;
                color: #6B7280;
                padding: 16px 10px;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                font-weight: 600;
                font-size: 12px;
                text-align: left;
            }
            QScrollBar:vertical {
                border: none;
                background: #F9FAFB;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #D1D5DB;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9CA3AF;
            }
        """)

        # Configure header
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Set column widths
        self.table.setColumnWidth(0, 180)  # Name
        self.table.setColumnWidth(1, 150)  # Position
        self.table.setColumnWidth(2, 120)  # Date
        self.table.setColumnWidth(3, 100)  # Clock In
        self.table.setColumnWidth(4, 100)  # Clock Out
        self.table.setColumnWidth(5, 120)  # Status
        self.table.setColumnWidth(6, 100)  # Actions

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(True)
        self.table.verticalHeader().setDefaultSectionSize(55)

        table_layout.addWidget(self.table)
        return table_frame

    def display_attendance(self, records):
        """Display attendance records in table"""
        self.table.setRowCount(0)

        for record in records:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Get data
            employee_name = record.get('employee_name', 'Unknown') or 'Unknown'
            position = record.get('position', '') or ''
            date_val = record.get('date', '')
            clock_in = record.get('clock_in', '') or '-'
            clock_out = record.get('clock_out', '') or '-'
            status = record.get('status', 'Present')

            # Name
            name_item = QTableWidgetItem(str(employee_name))
            name_item.setFont(QFont("Arial", 12))
            self.table.setItem(row, 0, name_item)

            # Position
            self.table.setItem(row, 1, QTableWidgetItem(str(position)))

            # Date
            self.table.setItem(row, 2, QTableWidgetItem(str(date_val)))

            # Clock in
            self.table.setItem(row, 3, QTableWidgetItem(str(clock_in)))

            # Clock out
            self.table.setItem(row, 4, QTableWidgetItem(str(clock_out)))

            # Status - colored text
            status_item = QTableWidgetItem(status)
            if status == 'Present':
                status_item.setForeground(QColor('#059669'))
            elif status == 'Absent':
                status_item.setForeground(QColor('#DC2626'))
            elif status == 'Late':
                status_item.setForeground(QColor('#F59E0B'))
            else:
                status_item.setForeground(QColor('#3B82F6'))
            status_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            self.table.setItem(row, 5, status_item)

            # Actions
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            delete_btn = QPushButton("🗑")
            delete_btn.setFixedSize(32, 32)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background: #EF4444;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #DC2626;
                }
            """)
            delete_btn.setToolTip("Delete Record")
            delete_btn.clicked.connect(lambda checked, r=record: self.delete_attendance(r))

            action_layout.addWidget(delete_btn)
            self.table.setCellWidget(row, 6, action_widget)

        # Update count
        self.count_label.setText(f"Showing {len(records)} of {len(self.attendance_records)} records")

        # Empty state
        if len(records) == 0:
            self.table.setRowCount(1)
            no_data_item = QTableWidgetItem("No attendance records found")
            no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_item.setForeground(QColor("#6B7280"))
            font = QFont("Arial", 13)
            font.setItalic(True)
            no_data_item.setFont(font)
            self.table.setSpan(0, 0, 1, 7)
            self.table.setItem(0, 0, no_data_item)

    def add_attendance(self):
        """Open dialog to add attendance"""
        dialog = AddAttendanceDialog(self, self.employees, self.selected_employee)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            if not data['employee_id']:
                QMessageBox.warning(self, "Validation Error", "Please select an employee")
                return

            # Save to database
            if self.db:
                try:
                    query = """
                            INSERT INTO attendance (employee_id, date, clock_in, clock_out, status)
                            VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY \
                            UPDATE \
                                clock_in = \
                            VALUES (clock_in), clock_out = \
                            VALUES (clock_out), status = \
                            VALUES (status) \
                            """
                    self.db.cursor.execute(query, (
                        data['employee_id'],
                        data['date'],
                        data['clock_in'],
                        data['clock_out'],
                        data['status']
                    ))
                    self.db.connection.commit()

                    QMessageBox.information(
                        self,
                        "Success",
                        "Attendance record added successfully!"
                    )

                    # Reload data
                    self.load_attendance()

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to add attendance:\n{str(e)}")

    def delete_attendance(self, record):
        """Delete attendance record"""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete this attendance record?\n\n"
            f"Employee: {record.get('employee_name')}\n"
            f"Date: {record.get('date')}\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.db and 'id' in record:
                try:
                    query = "DELETE FROM attendance WHERE id = %s"
                    self.db.cursor.execute(query, (record['id'],))
                    self.db.connection.commit()

                    QMessageBox.information(self, "Success", "Attendance record deleted successfully!")
                    self.load_attendance()

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete record:\n{str(e)}")

    def search_attendance(self, search_term):
        """Search attendance records"""
        if search_term.strip():
            search_lower = search_term.lower()
            filtered = [
                r for r in self.attendance_records
                if search_lower in str(r.get('employee_name', '')).lower()
            ]
            self.display_attendance(filtered)
        else:
            self.filter_by_status(self.status_filter.currentText() if hasattr(self, 'status_filter') else "All Status")

    def filter_by_status(self, status):
        """Filter by status"""
        if status == "All Status":
            self.filtered_records = self.attendance_records
        else:
            self.filtered_records = [
                r for r in self.attendance_records
                if r.get('status', '') == status
            ]
        self.display_attendance(self.filtered_records)

    @staticmethod
    def get_attendance_count(db, employee_id, month=None, year=None):
        """
        Get attendance count for an employee (for payroll integration)
        Returns number of present/working days
        """
        try:
            if month and year:
                query = """
                        SELECT COUNT(*) as days
                        FROM attendance
                        WHERE employee_id = %s
                            AND MONTH ( \
                            date) = %s
                          AND YEAR (date) = %s
                          AND status IN ('Present' \
                            , 'Late' \
                            , 'Half Day') \
                        """
                db.cursor.execute(query, (employee_id, month, year))
            else:
                query = """
                        SELECT COUNT(*) as days
                        FROM attendance
                        WHERE employee_id = %s
                          AND status IN ('Present', 'Late', 'Half Day') \
                        """
                db.cursor.execute(query, (employee_id,))

            result = db.cursor.fetchone()
            return result['days'] if result else 0
        except Exception as e:
            print(f"[ATTENDANCE] Error getting attendance count: {e}")
            return 0


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    test_user = {
        'name': 'Admin User',
        'employee_id': 'ADM001',
        'role': 'admin',
        'email': 'admin@payease.com'
    }

    window = AttendanceManagementWindow(test_user)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
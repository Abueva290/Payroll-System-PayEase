import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QSizePolicy, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class StatCard(QFrame):
    """A card widget for displaying statistics"""

    def __init__(self, icon_text, title, value, change_text, change_color):
        super().__init__()
        self.setMinimumSize(240, 130)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: none;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 15)
        layout.setSpacing(5)

        # Icon and Title row
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        icon = QLabel(icon_text)
        icon.setStyleSheet(f"""
            QLabel {{
                background: {self.get_icon_bg_color(icon_text)};
                color: {self.get_icon_color(icon_text)};
                border-radius: 8px;
                padding: 6px;
                font-size: 18px;
                border: none;
            }}
        """)
        icon.setFixedSize(36, 36)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_row.addWidget(icon)
        top_row.addStretch()

        layout.addLayout(top_row)
        layout.addSpacing(8)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(
            "color: #666666; font-size: 13px; background: transparent; border: none; padding: 0px; margin: 0px;")
        title_label.setWordWrap(True)
        title_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(title_label)
        layout.addSpacing(4)

        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(
            "color: #000000; font-size: 26px; font-weight: bold; background: transparent; border: none; padding: 0px; margin: 0px;")
        value_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(value_label)
        layout.addSpacing(4)

        # Change indicator
        change_label = QLabel(change_text)
        change_label.setStyleSheet(
            f"color: {change_color}; font-size: 12px; background: transparent; border: none; padding: 0px; margin: 0px;")
        change_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(change_label)

        self.setLayout(layout)

    def get_icon_bg_color(self, icon_text):
        colors = {
            "👥": "#E3F2FD",
            "💵": "#E3F2FD",
            "⏱": "#FFF9E6",
            "✅": "#E8F5E9"
        }
        return colors.get(icon_text, "#F5F5F5")

    def get_icon_color(self, icon_text):
        colors = {
            "👥": "#1976D2",
            "💵": "#1976D2",
            "⏱": "#F57C00",
            "✅": "#388E3C"
        }
        return colors.get(icon_text, "#666666")


class ActionCard(QFrame):
    """A card widget for action buttons with hover effects"""

    def __init__(self, icon_text, title, subtitle, is_primary=False, color="#0047FF"):
        super().__init__()
        self.setMinimumSize(240, 130)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.is_primary = is_primary
        self.color = color
        self.hovered = False

        self.update_card_style()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 15)
        layout.setSpacing(8)

        # Icon
        self.icon = QLabel(icon_text)
        self.update_icon_style()
        self.icon.setFixedSize(48, 48)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon)
        layout.addSpacing(8)

        # Title
        self.title_label = QLabel(title)
        self.update_title_style()
        self.title_label.setWordWrap(True)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.title_label)
        layout.addSpacing(2)

        # Subtitle
        self.subtitle_label = QLabel(subtitle)
        self.update_subtitle_style()
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.subtitle_label)

        layout.addStretch()
        self.setLayout(layout)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def update_card_style(self):
        """Update the card background based on hover state"""
        if self.hovered:
            self.setStyleSheet(f"""
                QFrame {{
                    background: {self.color};
                    border-radius: 12px;
                    border: none;
                }}
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 12px;
                    border: none;
                }
            """)

    def update_icon_style(self):
        """Update icon styling based on hover state"""
        if self.hovered:
            self.icon.setStyleSheet(f"""
                QLabel {{
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 24px;
                    border: none;
                }}
            """)
        else:
            self.icon.setStyleSheet(f"""
                QLabel {{
                    background: {self.color}33;
                    color: {self.color};
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 24px;
                    border: none;
                }}
            """)

    def update_title_style(self):
        """Update title styling based on hover state"""
        if self.hovered:
            self.title_label.setStyleSheet("""
                color: white; 
                font-size: 16px; 
                font-weight: bold; 
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            """)
        else:
            self.title_label.setStyleSheet("""
                color: #000000; 
                font-size: 16px; 
                font-weight: bold; 
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            """)

    def update_subtitle_style(self):
        """Update subtitle styling based on hover state"""
        if self.hovered:
            self.subtitle_label.setStyleSheet("""
                color: rgba(255, 255, 255, 0.9); 
                font-size: 12px; 
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            """)
        else:
            self.subtitle_label.setStyleSheet("""
                color: #666666; 
                font-size: 12px; 
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            """)

    def enterEvent(self, event):
        """Handle mouse enter event"""
        self.hovered = True
        self.update_card_style()
        self.update_icon_style()
        self.update_title_style()
        self.update_subtitle_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave event"""
        self.hovered = False
        self.update_card_style()
        self.update_icon_style()
        self.update_title_style()
        self.update_subtitle_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse click"""
        super().mousePressEvent(event)


class ActivityItem(QFrame):
    """A widget for displaying recent activity"""

    def __init__(self, icon_text, title, subtitle, time_text):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
                padding: 5px 0px;
            }
        """)
        self.setMinimumHeight(70)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(15)

        # Icon
        icon = QLabel(icon_text)
        icon.setStyleSheet("""
            QLabel {
                background: #E3F2FD;
                color: #0047FF;
                border-radius: 8px;
                padding: 8px;
                font-size: 20px;
            }
        """)
        icon.setFixedSize(48, 48)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        # Text container
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold; background: transparent;")
        text_layout.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        text_layout.addWidget(subtitle_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Time
        time_label = QLabel(time_text)
        time_label.setStyleSheet("color: #999999; font-size: 12px; background: transparent;")
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(time_label)

        self.setLayout(layout)


class AdminDashboard(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.setWindowTitle("PayEase - Admin Dashboard")
        self.setMinimumSize(1200, 800)

        # Initialize database connection
        from Model.database import get_db_connection
        self.db = get_db_connection()
        if not self.db.is_connected():
            self.db.connect()

        # Initialize navigation state early
        self.current_view = "dashboard"
        self.nav_buttons = {}

        # Store reference to employee management widget
        self.employee_widget = None
        self.payroll_widget = None
        self.attendance_widget = None

        # Set window background
        self.setStyleSheet("""
            QMainWindow {
                background: #F5F7FA;
            }
        """)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Content area with scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
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

        # Create dashboard content
        self.dashboard_widget = self.create_dashboard_content()
        self.scroll.setWidget(self.dashboard_widget)
        main_layout.addWidget(self.scroll)

    def get_dashboard_stats(self):
        """Fetch real stats from database"""
        try:
            # Total active employees
            total_employees = 0
            total_payroll = 0.0
            payroll_records = 0

            if self.db:
                # Count active employees
                employees = self.db.get_all_employees()
                for emp in employees:
                    is_archived = emp.get('is_archived', False) or emp.get('archived', False)
                    if not is_archived:
                        full_name = emp.get('FullName') or emp.get('full_name', '')
                        if full_name and str(full_name) != '0':
                            total_employees += 1

                # Get payroll stats
                payroll_records_list = self.db.get_all_payroll()
                payroll_records = len(payroll_records_list)

                # Calculate total payroll amount
                for record in payroll_records_list:
                    try:
                        net_salary = float(record.get('net_salary', 0))
                        total_payroll += net_salary
                    except (ValueError, TypeError):
                        pass

            return {
                'total_employees': total_employees,
                'total_payroll': total_payroll,
                'payroll_records': payroll_records
            }
        except Exception as e:
            print(f"[DASHBOARD] Error fetching stats: {e}")
            return {
                'total_employees': 0,
                'total_payroll': 0.0,
                'payroll_records': 0
            }

    def create_dashboard_content(self):
        """Create the dashboard content widget"""
        content_widget = QWidget()
        content_widget.setStyleSheet("background: #F5F7FA;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(30)

        # Welcome banner
        banner = self.create_welcome_banner()
        content_layout.addWidget(banner)

        # Get real stats from database
        stats = self.get_dashboard_stats()

        # Stats cards
        stats_container = QWidget()
        stats_container.setStyleSheet("background: transparent;")
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(20)

        # Real data from database
        stat1 = StatCard("👥", "Total Employees", str(stats['total_employees']),
                         "Active staff members", "#4CAF50")
        stat2 = StatCard("💵", "Total Payroll", f"₱{stats['total_payroll']:,.2f}",
                         f"{stats['payroll_records']} processed", "#4CAF50")
        stat3 = StatCard("⏱", "Attendance Records", "Track & Manage",
                         "Mark employee attendance", "#FFC107")
        stat4 = StatCard("✅", "Data Synced", "Live",
                         "Real-time database updates", "#4CAF50")

        stats_layout.addWidget(stat1, 1)
        stats_layout.addWidget(stat2, 1)
        stats_layout.addWidget(stat3, 1)
        stats_layout.addWidget(stat4, 1)
        content_layout.addWidget(stats_container)

        # Action cards
        actions_container = QWidget()
        actions_container.setStyleSheet("background: transparent;")
        actions_layout = QHBoxLayout(actions_container)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(20)

        self.action1 = ActionCard("👤+", "Add Employee", "Register new staff members", True, "#0047FF")
        self.action1.mousePressEvent = lambda event: self.open_add_employee()

        self.action2 = ActionCard("🧮", "Calculate Salaries", "Process monthly payroll", True, "#0047FF")
        self.action2.mousePressEvent = lambda event: self.open_payroll_management()

        self.action3 = ActionCard("📅", "Manage Attendance", "Track employee attendance", True, "#0047FF")
        self.action3.mousePressEvent = lambda event: self.open_employee_management()

        actions_layout.addWidget(self.action1, 1)
        actions_layout.addWidget(self.action2, 1)
        actions_layout.addWidget(self.action3, 1)
        content_layout.addWidget(actions_container)

        # Recent Activity
        activity_frame = self.create_activity_section()
        content_layout.addWidget(activity_frame)

        content_layout.addStretch()
        return content_widget

    def create_header(self):
        """Create the top navigation header"""
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background: white;
                border: none;
                border-bottom: 1px solid #E0E0E0;
            }
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)

        # Logo and title
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(12)

        logo = QLabel("💼")
        logo.setStyleSheet("font-size: 28px; background: transparent;")
        logo_layout.addWidget(logo)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        title = QLabel("PayEase Payroll")
        title.setStyleSheet("color: #000000; font-size: 20px; font-weight: bold; background: transparent;")
        subtitle = QLabel("Employee Management System")
        subtitle.setStyleSheet("color: #666666; font-size: 11px; background: transparent;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        logo_layout.addLayout(title_layout)
        layout.addLayout(logo_layout)

        layout.addStretch()

        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(5)

        nav_buttons = [
            ("🏠", "Dashboard"),
            ("👥", "Employees"),
            ("📋", "Payroll")
        ]

        for icon, text in nav_buttons:
            btn = QPushButton(f"{icon} {text}")
            self.nav_buttons[text] = btn

            # Add click handlers
            if text == "Dashboard":
                btn.clicked.connect(self.show_dashboard)
            elif text == "Employees":
                btn.clicked.connect(self.open_employee_management)
            elif text == "Payroll":
                btn.clicked.connect(self.open_payroll_management)

            nav_layout.addWidget(btn)

        # Update button styles for current view
        self.update_nav_button_styles()

        layout.addLayout(nav_layout)
        layout.addStretch()

        # User profile
        user_btn = QPushButton(f"🅰 {self.user_info['role'].capitalize()}")
        user_btn.setStyleSheet("""
            QPushButton {
                background: #0047FF;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0039CC;
            }
        """)
        layout.addWidget(user_btn)

        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 0, 0, 0.1);
                color: #DC2626;
                border: 2px solid #DC2626;
                padding: 8px 20px;
                font-size: 13px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #DC2626;
                color: white;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        return header

    def create_welcome_banner(self):
        """Create the welcome banner"""
        banner = QFrame()
        banner.setFixedHeight(120)
        banner.setStyleSheet("""
            QFrame {
                background: #0047FF;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(banner)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(8)

        title = QLabel(f"Welcome Back, {self.user_info['name']}!")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold; background: transparent;")
        layout.addWidget(title)

        subtitle = QLabel("Here's what's happening with your payroll system today.")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.95); font-size: 14px; background: transparent;")
        layout.addWidget(subtitle)

        return banner

    def create_activity_section(self):
        """Create the recent activity section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: none;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(5)

        # Header
        header_layout = QHBoxLayout()
        header_icon = QLabel("🕐")
        header_icon.setStyleSheet("font-size: 20px; background: transparent;")
        header_title = QLabel("Recent Activity")
        header_title.setStyleSheet("color: #000000; font-size: 18px; font-weight: bold; background: transparent;")
        header_layout.addWidget(header_icon)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        layout.addSpacing(10)

        # Activity items - from database
        activities = []

        try:
            if self.db:
                # Get recent payroll records
                payroll_records = self.db.get_all_payroll()
                for i, record in enumerate(payroll_records[:4]):
                    employee_name = record.get('employee_name', 'Employee')
                    month = record.get('month', '')
                    activities.append(("💰", "Payroll Processed", f"{employee_name} - {month}", "Recently"))

                # If we don't have 4 items, add default activities
                while len(activities) < 4:
                    activities.append(("📊", "System Ready", "Waiting for payroll data", "Ready"))
        except Exception as e:
            print(f"[DASHBOARD] Error loading activities: {e}")
            activities = [
                ("📊", "System Ready", "Connected to database", "Live"),
                ("🔄", "Real-time Sync", "Data updates automatically", "Active"),
                ("✅", "All Systems", "Online and operational", "Running"),
                ("📋", "Dashboard", "View all staff and payroll", "Available")
            ]

        for i, (icon, title, subtitle, time) in enumerate(activities):
            activity = ActivityItem(icon, title, subtitle, time)
            layout.addWidget(activity)

            # Add separator line except for last item
            if i < len(activities) - 1:
                separator = QFrame()
                separator.setFrameShape(QFrame.Shape.HLine)
                separator.setStyleSheet("background: #F0F0F0; max-height: 1px;")
                layout.addWidget(separator)

        return frame

    def open_add_employee(self):
        """Open the add employee window"""
        try:
            from Controller.handlers.add_employee_controller import AddEmployeeModule

            # Create and show the add employee window
            self.add_employee_window = AddEmployeeModule(self.user_info)
            self.add_employee_window.show()

            # Connect the window's close event to refresh employee list if needed
            self.add_employee_window.destroyed.connect(self.refresh_employee_list)

        except ImportError as e:
            print(f"Error importing AddEmployeeModule: {e}")
            QMessageBox.warning(self, "Error", f"Could not open Add Employee form: {e}")

    def refresh_employee_list(self):
        """Refresh the employee list if we're on the employees view"""
        if self.current_view == "employees" and self.employee_widget:
            try:
                # Reload employees in the employee widget
                self.employee_widget.load_employees()
            except Exception as e:
                print(f"Error refreshing employee list: {e}")

    def open_employee_management(self):
        """Load the employee management UI inside the dashboard window"""
        try:
            # Import the ACTUAL employee management module
            from Controller.handlers.employee_management_controller import EmployeeManagementWindow

            # Create a container widget for the employee management content
            container = QWidget()
            container.setStyleSheet("background: #F5F7FA;")
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(0)

            # Create the employee management window (but we'll extract just the content)
            emp_window = EmployeeManagementWindow()

            # Store reference to the employee widget
            self.employee_widget = emp_window

            # Set dashboard parent reference so employee management can navigate to attendance
            emp_window.dashboard_parent = self

            # Get the central widget from the employee management window
            emp_content = emp_window.centralWidget()

            # Add it to our container
            container_layout.addWidget(emp_content)

            # Replace the current content in the scroll area
            self.scroll.setWidget(container)
            self.current_view = "employees"

            # Connect the employee_updated signal to refresh if needed
            if hasattr(emp_window, 'employee_updated'):
                emp_window.employee_updated.connect(self.on_employee_updated)

            # Update button styles to highlight Employees button
            self.update_nav_button_styles()

        except ImportError as e:
            print(f"Error importing employee_management: {e}")
            QMessageBox.warning(self, "Error", f"Could not load Employee Management:\n{e}")

    def on_employee_updated(self):
        """Handle employee updates"""
        # This can be used to refresh statistics or other parts of the dashboard
        pass

    def open_payroll_management(self):
        """Load the payroll management UI inside the dashboard window"""
        try:
            # Import the payroll management module
            from Controller.handlers.payroll_controller import PayrollManagementWindow

            # Create a container widget for the payroll management content
            container = QWidget()
            container.setStyleSheet("background: #F5F7FA;")
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(0)

            # Create the payroll management window and pass db and user info
            payroll_window = PayrollManagementWindow(
                user_info=self.user_info,
                db_manager=self.db
            )

            # Store reference to the payroll widget
            self.payroll_widget = payroll_window

            # Get the central widget from the payroll management window
            payroll_content = payroll_window.centralWidget()

            # Add it to our container
            container_layout.addWidget(payroll_content)

            # Replace the current content in the scroll area
            self.scroll.setWidget(container)
            self.current_view = "payroll"

            # Update button styles to highlight Payroll button
            self.update_nav_button_styles()

        except ImportError as e:
            print(f"Error importing payroll: {e}")
            QMessageBox.warning(self, "Error", f"Could not load Payroll Management:\n{e}")
        except Exception as e:
            print(f"Error loading payroll: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred:\n{e}")

    def open_attendance_management(self):
        """Load the attendance management UI inside the dashboard window"""
        self.open_attendance_for_employee(None)  # None = show all employees

    def open_attendance_for_employee(self, employee=None):
        """Load attendance for specific employee or all employees"""
        try:
            # Import the attendance management module
            from Controller.handlers.attendance_controller import AttendanceManagementWindow

            # Create a container widget for the attendance management content
            container = QWidget()
            container.setStyleSheet("background: #F5F7FA;")
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(0)

            # Create the attendance management window and pass db, user info AND selected employee
            attendance_window = AttendanceManagementWindow(
                user_info=self.user_info,
                db_manager=self.db,
                selected_employee=employee  # Pass the specific employee or None for all
            )

            # Store reference to the attendance widget
            self.attendance_widget = attendance_window

            # Get the central widget from the attendance management window
            attendance_content = attendance_window.centralWidget()

            # Add it to our container
            container_layout.addWidget(attendance_content)

            # Replace the current content in the scroll area
            self.scroll.setWidget(container)
            self.current_view = "attendance"

            # Update button styles to highlight Attendance button
            self.update_nav_button_styles()

        except ImportError as e:
            print(f"Error importing attendance: {e}")
            QMessageBox.warning(self, "Error", f"Could not load Attendance Management:\n{e}")
        except Exception as e:
            print(f"Error loading attendance: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred:\n{e}")

    def show_dashboard(self):
        """Load the dashboard content and update button styles"""
        # Create dashboard content
        dashboard_content = self.create_dashboard_content()

        # Replace the current content in the scroll area
        self.scroll.setWidget(dashboard_content)
        self.current_view = "dashboard"

        # Clear widget references
        self.employee_widget = None
        self.payroll_widget = None
        self.attendance_widget = None

        # Update button styles to highlight Dashboard button
        self.update_nav_button_styles()

    def update_nav_button_styles(self):
        """Update navigation button styles based on current view"""
        for button_name, button in self.nav_buttons.items():
            if button_name == self.current_view.capitalize():
                # Highlighted style for active button
                button.setStyleSheet("""
                    QPushButton {
                        background: #E3F2FD;
                        color: #0047FF;
                        border: 2px solid #0047FF;
                        padding: 8px 20px;
                        font-size: 14px;
                        border-radius: 6px;
                        font-weight: bold;
                    }
                """)
            else:
                # Normal style for inactive buttons
                button.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        color: #666666;
                        border: none;
                        padding: 8px 20px;
                        font-size: 14px;
                        border-radius: 6px;
                    }
                    QPushButton:hover {
                        background: #F5F5F5;
                        color: #0047FF;
                    }
                """)

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
    """Test the dashboard"""
    print("Starting PayEase Admin Dashboard...")

    try:
        print("Creating QApplication...")
        app = QApplication(sys.argv)

        # Test user info
        test_user = {
            'name': 'Admin User',
            'employee_id': 'ADM001',
            'role': 'admin',
            'email': 'admin@payease.com'
        }

        print("Creating main window...")
        window = AdminDashboard(test_user)

        print("Showing window...")
        window.showMaximized()

        print("Starting event loop...")
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == '__main__':
    main()

import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QSizePolicy, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class StatCard(QFrame):
    """A card widget for displaying statistics"""

    def __init__(self, icon_text, title, value, subtitle, color="#0047FF"):
        super().__init__()
        self.setMinimumSize(220, 120)
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
        layout.setSpacing(8)

        # Icon and Title row
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        icon = QLabel(icon_text)
        icon.setStyleSheet(f"""
            QLabel {{
                background: {color}22;
                color: {color};
                border-radius: 8px;
                padding: 8px;
                font-size: 20px;
                border: none;
            }}
        """)
        icon.setFixedSize(40, 40)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_row.addWidget(icon)
        top_row.addStretch()

        layout.addLayout(top_row)
        layout.addSpacing(5)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666666; font-size: 12px; background: transparent;")
        layout.addWidget(title_label)

        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold; background: transparent;")
        layout.addWidget(value_label)

        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #999999; font-size: 11px; background: transparent;")
        layout.addWidget(subtitle_label)

        self.setLayout(layout)


class QuickActionCard(QFrame):
    """A card widget for quick actions"""

    def __init__(self, icon_text, title, description, color="#0047FF"):
        super().__init__()
        self.color = color
        self.hovered = False
        self.setMinimumSize(200, 110)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.update_style()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 15)
        layout.setSpacing(8)

        # Icon
        self.icon = QLabel(icon_text)
        self.update_icon_style()
        self.icon.setFixedSize(42, 42)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon)

        # Title
        self.title_label = QLabel(title)
        self.update_title_style()
        layout.addWidget(self.title_label)

        # Description
        self.desc_label = QLabel(description)
        self.update_desc_style()
        layout.addWidget(self.desc_label)

        self.setLayout(layout)

    def update_style(self):
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
        if self.hovered:
            self.icon.setStyleSheet(f"""
                QLabel {{
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 20px;
                }}
            """)
        else:
            self.icon.setStyleSheet(f"""
                QLabel {{
                    background: {self.color}22;
                    color: {self.color};
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 20px;
                }}
            """)

    def update_title_style(self):
        if self.hovered:
            self.title_label.setStyleSheet("""
                color: white; 
                font-size: 15px; 
                font-weight: bold; 
                background: transparent;
            """)
        else:
            self.title_label.setStyleSheet("""
                color: #000000; 
                font-size: 15px; 
                font-weight: bold; 
                background: transparent;
            """)

    def update_desc_style(self):
        if self.hovered:
            self.desc_label.setStyleSheet("""
                color: rgba(255, 255, 255, 0.95); 
                font-size: 11px; 
                background: transparent;
            """)
        else:
            self.desc_label.setStyleSheet("""
                color: #666666; 
                font-size: 11px; 
                background: transparent;
            """)

    def enterEvent(self, event):
        self.hovered = True
        self.update_style()
        self.update_icon_style()
        self.update_title_style()
        self.update_desc_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.update_style()
        self.update_icon_style()
        self.update_title_style()
        self.update_desc_style()
        super().leaveEvent(event)


class UserDashboard(QMainWindow):
    """User Dashboard - For regular employees"""

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.setWindowTitle("PayEase - My Dashboard")
        self.setMinimumSize(1200, 800)

        self.setStyleSheet("""
            QMainWindow {
                background: #F5F7FA;
            }
        """)

        # Sample data - Replace with database calls
        self.employee_data = self.get_employee_data()
        self.payroll_history = self.get_payroll_history()
        self.leave_requests = self.get_leave_requests()

        self.init_ui()

    def get_employee_data(self):
        """Get current employee data - Replace with DB query"""
        return {
            'employee_id': self.user_info.get('employee_id', 'EMP001'),
            'full_name': self.user_info.get('name', 'John Doe'),
            'email': self.user_info.get('email', 'john.doe@payease.com'),
            'position': 'Software Developer',
            'department': 'Engineering',
            'salary': 65000.00,
            'hire_date': '2023-01-15',
            'leave_balance': 12,
            'pending_requests': 1
        }

    def get_payroll_history(self):
        """Get payroll history - Replace with DB query"""
        return [
            {
                'month': 'November',
                'year': 2024,
                'base_salary': 65000.00,
                'bonus': 500.00,
                'deductions': 150.00,
                'net_salary': 65350.00,
                'status': 'Paid',
                'date': '2024-11-30'
            },
            {
                'month': 'October',
                'year': 2024,
                'base_salary': 65000.00,
                'bonus': 0.00,
                'deductions': 150.00,
                'net_salary': 64850.00,
                'status': 'Paid',
                'date': '2024-10-31'
            },
            {
                'month': 'September',
                'year': 2024,
                'base_salary': 65000.00,
                'bonus': 1000.00,
                'deductions': 150.00,
                'net_salary': 65850.00,
                'status': 'Paid',
                'date': '2024-09-30'
            }
        ]

    def get_leave_requests(self):
        """Get leave requests - Replace with DB query"""
        return [
            {
                'type': 'Vacation',
                'start_date': '2024-12-20',
                'end_date': '2024-12-27',
                'days': 5,
                'status': 'Pending',
                'reason': 'Holiday vacation'
            },
            {
                'type': 'Sick Leave',
                'start_date': '2024-11-15',
                'end_date': '2024-11-15',
                'days': 1,
                'status': 'Approved',
                'reason': 'Medical appointment'
            }
        ]

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

        # Content area with scroll
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

        # Content
        content = self.create_content()
        scroll.setWidget(content)
        layout.addWidget(scroll)

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

        # Logo
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(12)

        logo = QLabel("💼")
        logo.setStyleSheet("font-size: 28px; background: transparent;")
        logo_layout.addWidget(logo)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        title = QLabel("PayEase")
        title.setStyleSheet("color: #000000; font-size: 20px; font-weight: bold; background: transparent;")
        subtitle = QLabel("Employee Self-Service Portal")
        subtitle.setStyleSheet("color: #666666; font-size: 11px; background: transparent;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        logo_layout.addLayout(title_layout)
        layout.addLayout(logo_layout)

        layout.addStretch()

        # Navigation
        nav_buttons = [
            ("🏠", "Dashboard"),
            ("💰", "My Payroll"),
            ("📅", "Leave Requests"),
            ("👤", "My Profile")
        ]

        for icon, text in nav_buttons:
            btn = QPushButton(f"{icon} {text}")
            if text == "Dashboard":
                btn.setStyleSheet("""
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
                btn.setStyleSheet("""
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
            layout.addWidget(btn)

        layout.addStretch()

        # User profile
        user_btn = QPushButton(f"👤 {self.user_info['name']}")
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

        return header

    def create_content(self):
        """Create dashboard content"""
        content = QWidget()
        content.setStyleSheet("background: #F5F7FA;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(25)

        # Welcome banner
        banner = self.create_welcome_banner()
        content_layout.addWidget(banner)

        # Stats cards
        stats = self.create_stats_section()
        content_layout.addWidget(stats)

        # Quick actions
        actions = self.create_quick_actions()
        content_layout.addWidget(actions)

        # Two column layout
        two_col = QHBoxLayout()
        two_col.setSpacing(25)

        # Recent payroll
        recent_payroll = self.create_recent_payroll()
        two_col.addWidget(recent_payroll, 3)

        # Leave summary
        leave_summary = self.create_leave_summary()
        two_col.addWidget(leave_summary, 2)

        content_layout.addLayout(two_col)

        content_layout.addStretch()
        return content

    def create_welcome_banner(self):
        """Create welcome banner"""
        banner = QFrame()
        banner.setFixedHeight(110)
        banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0047FF, stop:1 #0039CC);
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(banner)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(8)

        title = QLabel(f"Welcome back, {self.employee_data['full_name']}! 👋")
        title.setStyleSheet("color: white; font-size: 26px; font-weight: bold; background: transparent;")
        layout.addWidget(title)

        subtitle = QLabel(f"{self.employee_data['position']} • {self.employee_data['department']}")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.95); font-size: 14px; background: transparent;")
        layout.addWidget(subtitle)

        return banner

    def create_stats_section(self):
        """Create statistics cards"""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Monthly salary
        stat1 = StatCard(
            "💵",
            "Monthly Salary",
            f"${self.employee_data['salary']:,.2f}",
            "Base salary amount",
            "#0047FF"
        )

        # Leave balance
        stat2 = StatCard(
            "🌴",
            "Leave Balance",
            f"{self.employee_data['leave_balance']} days",
            "Available leave days",
            "#4CAF50"
        )

        # Pending requests
        stat3 = StatCard(
            "⏳",
            "Pending Requests",
            str(self.employee_data['pending_requests']),
            "Awaiting approval",
            "#FF9800"
        )

        # Years of service
        hire_year = int(self.employee_data['hire_date'].split('-')[0])
        years = datetime.now().year - hire_year
        stat4 = StatCard(
            "🎯",
            "Years of Service",
            f"{years} years",
            f"Since {self.employee_data['hire_date']}",
            "#9C27B0"
        )

        layout.addWidget(stat1, 1)
        layout.addWidget(stat2, 1)
        layout.addWidget(stat3, 1)
        layout.addWidget(stat4, 1)

        return container

    def create_quick_actions(self):
        """Create quick action cards"""
        section = QFrame()
        section.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # Title
        title = QLabel("⚡ Quick Actions")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #000000; background: transparent;")
        layout.addWidget(title)

        # Action cards
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(20)

        action1 = QuickActionCard("📄", "View Payslips", "Access payment history", "#0047FF")
        action1.mousePressEvent = lambda e: self.view_payslips()

        action2 = QuickActionCard("📅", "Request Leave", "Submit time-off request", "#4CAF50")
        action2.mousePressEvent = lambda e: self.request_leave()

        action3 = QuickActionCard("👤", "Update Profile", "Edit personal information", "#9C27B0")
        action3.mousePressEvent = lambda e: self.update_profile()

        action4 = QuickActionCard("📊", "View Reports", "Access your reports", "#FF9800")
        action4.mousePressEvent = lambda e: self.view_reports()

        actions_layout.addWidget(action1, 1)
        actions_layout.addWidget(action2, 1)
        actions_layout.addWidget(action3, 1)
        actions_layout.addWidget(action4, 1)

        layout.addLayout(actions_layout)

        return section

    def create_recent_payroll(self):
        """Create recent payroll section"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Header
        header = QHBoxLayout()
        title_icon = QLabel("💰")
        title_icon.setStyleSheet("font-size: 20px; background: transparent;")
        title = QLabel("Recent Payroll")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        header.addWidget(title_icon)
        header.addWidget(title)
        header.addStretch()

        view_all = QPushButton("View All →")
        view_all.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #0047FF;
                border: none;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        view_all.clicked.connect(self.view_all_payroll)
        header.addWidget(view_all)

        layout.addLayout(header)

        # Table
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["PERIOD", "BASE", "BONUS", "NET SALARY", "STATUS"])
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                background: white;
                gridline-color: #F0F0F0;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #F0F0F0;
            }
            QHeaderView::section {
                background: #F9FAFB;
                color: #374151;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
        """)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Populate table
        for record in self.payroll_history[:3]:
            row = table.rowCount()
            table.insertRow(row)

            table.setItem(row, 0, QTableWidgetItem(f"{record['month']} {record['year']}"))
            table.setItem(row, 1, QTableWidgetItem(f"${record['base_salary']:,.2f}"))
            table.setItem(row, 2, QTableWidgetItem(f"${record['bonus']:,.2f}"))
            table.setItem(row, 3, QTableWidgetItem(f"${record['net_salary']:,.2f}"))

            status_item = QTableWidgetItem(record['status'])
            if record['status'] == 'Paid':
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            table.setItem(row, 4, status_item)

        layout.addWidget(table)

        return section

    def create_leave_summary(self):
        """Create leave summary section"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Header
        header = QHBoxLayout()
        title_icon = QLabel("📅")
        title_icon.setStyleSheet("font-size: 20px; background: transparent;")
        title = QLabel("Leave Requests")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        header.addWidget(title_icon)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        # Leave requests
        for request in self.leave_requests:
            item = self.create_leave_item(request)
            layout.addWidget(item)

        layout.addStretch()

        # Request button
        request_btn = QPushButton("➕ Request New Leave")
        request_btn.setFixedHeight(45)
        request_btn.setStyleSheet("""
            QPushButton {
                background: #0047FF;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0039CC;
            }
        """)
        request_btn.clicked.connect(self.request_leave)
        layout.addWidget(request_btn)

        return section

    def create_leave_item(self, request):
        """Create leave request item"""
        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background: #F9FAFB;
                border-radius: 8px;
                border: 1px solid #E5E7EB;
            }
        """)

        layout = QVBoxLayout(item)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # Type and status
        top_row = QHBoxLayout()

        type_label = QLabel(request['type'])
        type_label.setStyleSheet("color: #111827; font-size: 13px; font-weight: bold; background: transparent;")
        top_row.addWidget(type_label)

        top_row.addStretch()

        status_label = QLabel(request['status'])
        if request['status'] == 'Approved':
            status_label.setStyleSheet("""
                background: #D1FAE5;
                color: #065F46;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
            """)
        else:
            status_label.setStyleSheet("""
                background: #FEF3C7;
                color: #92400E;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
            """)
        top_row.addWidget(status_label)

        layout.addLayout(top_row)

        # Dates
        date_label = QLabel(f"{request['start_date']} to {request['end_date']} ({request['days']} days)")
        date_label.setStyleSheet("color: #6B7280; font-size: 12px; background: transparent;")
        layout.addWidget(date_label)

        return item

    def view_payslips(self):
        """View all payslips"""
        QMessageBox.information(self, "View Payslips", "Opening payslip history...")

    def request_leave(self):
        """Request leave"""
        QMessageBox.information(self, "Request Leave", "Opening leave request form...")

    def update_profile(self):
        """Update profile"""
        QMessageBox.information(self, "Update Profile", "Opening profile editor...")

    def view_reports(self):
        """View reports"""
        QMessageBox.information(self, "View Reports", "Opening reports section...")

    def view_all_payroll(self):
        """View all payroll records"""
        QMessageBox.information(self, "All Payroll", "Opening complete payroll history...")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Test user info
    test_user = {
        'name': 'John Doe',
        'employee_id': 'EMP001',
        'role': 'employee',
        'email': 'john.doe@payease.com'
    }

    window = UserDashboard(test_user)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
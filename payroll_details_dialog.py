
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class PayrollDetailsWindow(QMainWindow):
    """Window for displaying detailed payroll information with status management"""

    # Signal to notify when payroll is updated
    payroll_updated = pyqtSignal()

    def __init__(self, payroll_data=None, user_info=None, db_manager=None):
        super().__init__()
        self.payroll_data = payroll_data or self.get_sample_data()
        self.user_info = user_info or {'name': 'Admin', 'role': 'admin'}
        self.db = db_manager

        self.setWindowTitle("PayEase - Payroll Details")
        self.setMinimumSize(1200, 900)

        self.setStyleSheet("""
            QMainWindow {
                background: #F5F7FA;
            }
        """)

        self.init_ui()

    def get_sample_data(self):
        """Return sample payroll data"""
        return {
            'id': 1,
            'employee_name': 'Anu',
            'position': 'staff',
            'month': 'August',
            'year': '2025',
            'present_days': '2 days',
            'base_salary': 1000000.00,
            'daily_rate': 45454.55,
            'basic_salary': 90909.09,
            'bonus': 1000.00,
            'deductions': 100.00,
            'net_salary': 91809.09,
            'status': 'Pending',
            'notes': 'salary',
            'released_date': None
        }

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
        content = QWidget()
        content.setStyleSheet("background: #F5F7FA;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(25)

        # Page header with buttons
        page_header = self.create_page_header()
        content_layout.addWidget(page_header)

        # Main payroll card
        payroll_card = self.create_payroll_card()
        content_layout.addWidget(payroll_card)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def create_header(self):
        """Create the top navigation header"""
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

        # Logo and title
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(12)

        logo = QLabel("💼")
        logo.setStyleSheet("font-size: 28px; background: transparent;")
        logo_layout.addWidget(logo)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        title = QLabel("PayEase")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; background: transparent;")
        subtitle = QLabel("Employee Management System")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 11px; background: transparent;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        logo_layout.addLayout(title_layout)
        layout.addLayout(logo_layout)

        layout.addStretch()

        # User badge
        user_btn = QPushButton(f"🅰 {self.user_info['role'].capitalize()}")
        user_btn.setStyleSheet("""
            QPushButton {
                background: white;
                color: #0047FF;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #F0F0F0;
            }
        """)
        layout.addWidget(user_btn)

        return header

    def create_page_header(self):
        """Create page title and action buttons"""
        container = QWidget()
        container.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Title
        title_layout = QHBoxLayout()
        title_icon = QLabel("📄")
        title_icon.setStyleSheet("font-size: 28px; background: transparent;")
        title_label = QLabel("Payroll Details")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000; background: transparent;")

        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        layout.addLayout(title_layout)
        layout.addStretch()

        # Action buttons
        print_btn = QPushButton("🖨 Print Slip")
        print_btn.setFixedSize(140, 45)
        print_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #45A049;
            }
        """)
        print_btn.clicked.connect(self.print_slip)

        back_btn = QPushButton("← Back to Payroll")
        back_btn.setFixedSize(160, 45)
        back_btn.setStyleSheet("""
            QPushButton {
                background: white;
                color: #374151;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #F9FAFB;
            }
        """)
        back_btn.clicked.connect(self.back_to_payroll)

        layout.addWidget(print_btn)
        layout.addWidget(back_btn)

        return container

    def create_payroll_card(self):
        """Create the main payroll details card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: none;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Employee header
        emp_header = self.create_employee_header()
        layout.addWidget(emp_header)

        # Content area
        content_area = QWidget()
        content_area.setStyleSheet("background: white;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(25)

        # Top section - Period and Attendance
        top_section = self.create_top_section()
        content_layout.addWidget(top_section)

        # Status management section
        status_section = self.create_status_section()
        content_layout.addWidget(status_section)

        # Salary calculation section
        calc_section = self.create_calculation_section()
        content_layout.addWidget(calc_section)

        # Notes section
        notes_section = self.create_notes_section()
        content_layout.addWidget(notes_section)

        layout.addWidget(content_area)

        return card

    def create_employee_header(self):
        """Create employee name and status header"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: #F9FAFB;
                border: none;
                border-bottom: 1px solid #E5E7EB;
            }
        """)
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(40, 20, 40, 20)

        # Employee name
        name_layout = QHBoxLayout()
        name_icon = QLabel("👤")
        name_icon.setStyleSheet("font-size: 24px; background: transparent;")
        name_label = QLabel(self.payroll_data['employee_name'])
        name_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #111827; background: transparent;")

        name_layout.addWidget(name_icon)
        name_layout.addWidget(name_label)
        layout.addLayout(name_layout)

        layout.addStretch()

        # Current status badge
        status = self.payroll_data.get('status', 'Pending')
        status_badge = QLabel(status)

        # Status-specific styling
        if status == 'Pending':
            badge_style = """
                QLabel {
                    background: #FEF3C7;
                    color: #92400E;
                    padding: 8px 20px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: bold;
                }
            """
        elif status == 'Released':
            badge_style = """
                QLabel {
                    background: #D1FAE5;
                    color: #065F46;
                    padding: 8px 20px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: bold;
                }
            """
        else:  # Canceled
            badge_style = """
                QLabel {
                    background: #FEE2E2;
                    color: #991B1B;
                    padding: 8px 20px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: bold;
                }
            """

        status_badge.setStyleSheet(badge_style)
        layout.addWidget(status_badge)

        return header

    def create_status_section(self):
        """Create status management section with action buttons"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background: #F0F9FF;
                border-radius: 12px;
                border: 2px solid #0047FF;
            }
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Title
        title_label = QLabel("📋 Status Management")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0047FF; background: transparent; border: none;")
        layout.addWidget(title_label)

        # Current status info
        current_status = self.payroll_data.get('status', 'Pending')
        status_info = QLabel(f"Current Status: {current_status}")
        status_info.setStyleSheet("color: #374151; font-size: 13px; background: transparent; border: none;")
        layout.addWidget(status_info)

        # Release date if available
        released_date = self.payroll_data.get('released_date')
        if released_date:
            date_label = QLabel(f"Released on: {released_date}")
            date_label.setStyleSheet("color: #6B7280; font-size: 12px; background: transparent;")
            layout.addWidget(date_label)

        layout.addSpacing(10)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # Set Pending button
        self.pending_btn = QPushButton("⏱ Set Pending")
        self.pending_btn.setFixedHeight(45)
        self.pending_btn.setStyleSheet("""
            QPushButton {
                background: #F59E0B;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: #D97706;
            }
            QPushButton:disabled {
                background: #D1D5DB;
                color: #9CA3AF;
            }
        """)
        self.pending_btn.clicked.connect(self.set_pending)

        # Release button
        self.release_btn = QPushButton("✅ Release Payroll")
        self.release_btn.setFixedHeight(45)
        self.release_btn.setStyleSheet("""
            QPushButton {
                background: #10B981;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: #059669;
            }
            QPushButton:disabled {
                background: #D1D5DB;
                color: #9CA3AF;
            }
        """)
        self.release_btn.clicked.connect(self.release_payroll)

        # Cancel button
        self.cancel_btn = QPushButton("❌ Cancel Payroll")
        self.cancel_btn.setFixedHeight(45)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: #EF4444;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: #DC2626;
            }
            QPushButton:disabled {
                background: #D1D5DB;
                color: #9CA3AF;
            }
        """)
        self.cancel_btn.clicked.connect(self.cancel_payroll)

        button_layout.addWidget(self.pending_btn)
        button_layout.addWidget(self.release_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Update button states based on current status
        self.update_button_states()

        # Status workflow info
        workflow_info = QLabel(
            "💡 Workflow: Pending → Released (approved for payment) | "
            "Pending → Canceled (rejected/void)"
        )
        workflow_info.setStyleSheet("""
            color: #6B7280;
            font-size: 11px;
            background: transparent;
            border: none;
            padding: 10px;
        """)
        workflow_info.setWordWrap(True)
        layout.addWidget(workflow_info)

        return section

    def update_button_states(self):
        """Update button enabled/disabled states based on current status"""
        current_status = self.payroll_data.get('status', 'Pending')

        if current_status == 'Pending':
            self.pending_btn.setEnabled(False)
            self.release_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)
        elif current_status == 'Released':
            self.pending_btn.setEnabled(True)
            self.release_btn.setEnabled(False)
            self.cancel_btn.setEnabled(True)
        elif current_status == 'Canceled':
            self.pending_btn.setEnabled(True)
            self.release_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)

    def set_pending(self):
        """Set payroll status to Pending"""
        reply = QMessageBox.question(
            self,
            "Confirm Status Change",
            f"Change payroll status to Pending?\n\n"
            f"Employee: {self.payroll_data['employee_name']}\n"
            f"Period: {self.payroll_data['month']} {self.payroll_data['year']}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.update_payroll_status('Pending')

    def release_payroll(self):
        """Release payroll for payment"""
        reply = QMessageBox.question(
            self,
            "Confirm Release",
            f"Release this payroll for payment?\n\n"
            f"Employee: {self.payroll_data['employee_name']}\n"
            f"Period: {self.payroll_data['month']} {self.payroll_data['year']}\n"
            f"Amount: ${self.payroll_data['net_salary']:,.2f}\n\n"
            "This will mark the payroll as ready for payment processing.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            from datetime import datetime
            released_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.update_payroll_status('Released', released_date)

    def cancel_payroll(self):
        """Cancel payroll"""
        reply = QMessageBox.warning(
            self,
            "Confirm Cancellation",
            f"Cancel this payroll?\n\n"
            f"Employee: {self.payroll_data['employee_name']}\n"
            f"Period: {self.payroll_data['month']} {self.payroll_data['year']}\n\n"
            "⚠️ This will void the payroll record.\n"
            "Are you sure you want to proceed?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.update_payroll_status('Canceled')

    def update_payroll_status(self, new_status, released_date=None):
        """Update payroll status in database and UI"""
        if not self.db or 'id' not in self.payroll_data:
            QMessageBox.critical(self, "Error", "Cannot update status: Database not available")
            return

        try:
            # Update in database
            payroll_id = self.payroll_data['id']

            if not self.db.is_connected():
                self.db.connect()

            # Build update query
            if released_date and new_status == 'Released':
                query = "UPDATE payroll SET status = %s, released_date = %s WHERE id = %s"
                self.db.cursor.execute(query, (new_status, released_date, payroll_id))
            else:
                query = "UPDATE payroll SET status = %s WHERE id = %s"
                self.db.cursor.execute(query, (new_status, payroll_id))

            self.db.connection.commit()

            # Update local data
            self.payroll_data['status'] = new_status
            if released_date:
                self.payroll_data['released_date'] = released_date

            # Show success message
            QMessageBox.information(
                self,
                "Status Updated",
                f"Payroll status changed to: {new_status}"
            )

            # Refresh UI
            self.refresh_ui()

            # Emit signal to parent window
            self.payroll_updated.emit()

        except Exception as e:
            print(f"[PAYROLL DETAILS] Error updating status: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to update status:\n{str(e)}")

    def refresh_ui(self):
        """Refresh the UI after status update"""
        # Recreate the main content
        self.centralWidget().deleteLater()
        self.init_ui()

    def create_top_section(self):
        """Create payroll period and attendance section"""
        container = QWidget()
        container.setStyleSheet("background: transparent;")

        layout = QGridLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Payroll Period card
        period_card = self.create_info_card(
            "📅 Payroll Period",
            [
                ("Month/Year:", f"{self.payroll_data['month']} {self.payroll_data['year']}"),
                ("Position:", self.payroll_data['position'])
            ],
            "#EEF2FF"
        )

        # Attendance card
        attendance_card = self.create_info_card(
            "📊 Attendance",
            [
                ("Present Days:", self.payroll_data['present_days']),
                ("Base Salary:", f"${self.payroll_data['base_salary']:,.2f}"),
                ("Daily Rate:", f"${self.payroll_data.get('daily_rate', 0):,.2f}")
            ],
            "#EEF2FF"
        )

        layout.addWidget(period_card, 0, 0)
        layout.addWidget(attendance_card, 0, 1)

        return container

    def create_info_card(self, title, items, bg_color):
        """Create an information card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {bg_color};
                border-radius: 12px;
                border: none;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0047FF; background: transparent;")
        layout.addWidget(title_label)

        # Items
        for label, value in items:
            item_layout = QHBoxLayout()

            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: #6B7280; font-size: 13px; background: transparent;")

            value_widget = QLabel(value)
            value_widget.setStyleSheet("color: #111827; font-size: 14px; font-weight: bold; background: transparent;")
            if "$" in value or "₱" in value:
                value_widget.setStyleSheet(
                    "color: #0047FF; font-size: 14px; font-weight: bold; background: transparent;")

            item_layout.addWidget(label_widget)
            item_layout.addStretch()
            item_layout.addWidget(value_widget)

            layout.addLayout(item_layout)

        return card

    def create_calculation_section(self):
        """Create salary calculation section"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background: #EEF2FF;
                border-radius: 12px;
                border-left: 4px solid #0047FF;
            }
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("💰 Salary Calculation")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0047FF; background: transparent;")
        layout.addWidget(title_label)

        layout.addSpacing(10)

        # Calculation items
        basic_salary = self.payroll_data.get('basic_salary', self.payroll_data.get('base_salary', 0))
        items = [
            ("Basic Salary:", f"${basic_salary:,.2f}", "#111827"),
            ("Bonus:", f"+ ${self.payroll_data['bonus']:,.2f}", "#059669"),
            ("Deductions:", f"- ${self.payroll_data['deductions']:,.2f}", "#DC2626")
        ]

        for label, value, color in items:
            item_layout = QHBoxLayout()

            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: #374151; font-size: 14px; background: transparent;")

            value_widget = QLabel(value)
            value_widget.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            value_widget.setStyleSheet(f"color: {color}; background: transparent;")

            item_layout.addWidget(label_widget)
            item_layout.addStretch()
            item_layout.addWidget(value_widget)

            layout.addLayout(item_layout)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background: #C7D2FE; max-height: 2px;")
        layout.addWidget(divider)

        # Net salary
        net_layout = QHBoxLayout()
        net_label = QLabel("Net Salary:")
        net_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        net_label.setStyleSheet("color: #0047FF; background: transparent;")

        net_value = QLabel(f"${self.payroll_data['net_salary']:,.2f}")
        net_value.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        net_value.setStyleSheet("color: #0047FF; background: transparent;")

        net_layout.addWidget(net_label)
        net_layout.addStretch()
        net_layout.addWidget(net_value)

        layout.addLayout(net_layout)

        return section

    def create_notes_section(self):
        """Create notes section"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background: #F9FAFB;
                border-radius: 12px;
                border: none;
            }
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("📝 Notes")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0047FF; background: transparent;")
        layout.addWidget(title_label)

        # Notes content
        notes = self.payroll_data.get('notes', '') or 'No notes added'
        notes_content = QLabel(notes)
        notes_content.setStyleSheet("""
            QLabel {
                color: #374151;
                font-size: 13px;
                background: white;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #E5E7EB;
            }
        """)
        notes_content.setWordWrap(True)
        layout.addWidget(notes_content)

        return section

    def print_slip(self):
        """Handle print slip action"""
        from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
        from PyQt6.QtGui import QPainter

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            painter = QPainter(printer)
            self.render(painter)
            painter.end()

    def back_to_payroll(self):
        """Handle back to payroll action"""
        self.close()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Sample payroll data
    sample_data = {
        'id': 1,
        'employee_name': 'Anu',
        'position': 'staff',
        'month': 'August',
        'year': '2025',
        'present_days': '2 days',
        'base_salary': 1000000.00,
        'daily_rate': 45454.55,
        'basic_salary': 90909.09,
        'bonus': 1000.00,
        'deductions': 100.00,
        'net_salary': 91809.09,
        'status': 'Pending',
        'notes': 'salary',
        'released_date': None
    }

    window = PayrollDetailsWindow(sample_data)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
import os
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QMenuBar, QAction, QStatusBar, 
    QLabel, QMessageBox, QApplication, QFileDialog, QDialog, QVBoxLayout,
    QTableView, QLineEdit, QHBoxLayout, QPushButton, QComboBox, QFormLayout
)
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from nepali_datetime import date as nepali_date
from models.user_model import get_user_role, get_user, update_user, delete_user, get_all_users
from models.database import get_database_path, get_connection
from models.organization_model import get_organization_profile
from utils.excel_handler import ExcelHandler
from styles.app_styles import AppStyles
from ui.message_boxes import StandardMessageBox
from ui.personal_info_tab import PersonalInfoTab
from ui.loan_info_tab import LoanInfoTab
from ui.collateral_tab import CollateralTab
from ui.approval_tab import ApprovalTab
from ui.reports_tab import ReportsTab
from ui.setting_tab import SettingsTab
from ui.loan_scheme_window import LoanSchemeManager
from ui.report_history_tab import ReportHistoryTab
from ui.project_tab import ProjectTab
from ui.loan_list_tab import LoanListTab
from ui.organization_profile_tab import OrganizationProfileTab
from ui.member_manager_dialog import MemberManagerDialog
from ui.user_management_dialog import UserManagementDialog
from models.collateral_model import (
    get_collateral_basic, get_collateral_properties, get_collateral_family_details,
    get_collateral_income_expense, get_collateral_projects, get_approved_loans
)

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.role = get_user_role(username)

        # Setup window properties first
        self.setup_window()
        
        # Apply uniform styling
        self.apply_styles()
        
        # Setup UI components
        self.setup_ui()
        
        # Setup menu bar
        self.setup_menu_bar()
        
        # Setup status bar
        self.setup_status_bar()
        
        # Setup tabs
        self.setup_tabs()
        
        # Setup timer for time updates
        self.setup_timer()

    def setup_window(self):
        """Setup window properties with uniform behavior"""
        self.setWindowTitle("Loan Application Management System")
        self.setWindowIcon(QIcon("icons/logo.ico"))
        
        # Set minimum size
        self.setMinimumSize(1200, 800)
        
        # Always start maximized for consistency
        # self.showMaximized()
        
        # Center window if not maximized (fallback)
        self.center_window()

    def center_window(self):
        """Center the window on screen"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        self.move(
            int((screen.width() - window.width()) / 2),
            int((screen.height() - window.height()) / 2)
        )

    def apply_styles(self):
        """Apply uniform styles to the entire window"""
        self.setStyleSheet(AppStyles.get_main_stylesheet())

    def setup_ui(self):
        """Setup main UI components"""
        # Create central tab widget with uniform styling
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

    def setup_menu_bar(self):
        """Setup menu bar with uniform styling"""
        menu_bar = self.menuBar()
        
        # File Menu
        file_menu = menu_bar.addMenu("📁 File")
        
        logout_action = QAction("🚪 Logout", self)
        logout_action.triggered.connect(self.logout)
        logout_action.setStatusTip("Logout from the application")
        file_menu.addAction(logout_action)

        # Member View Menu
        member_view_menu = menu_bar.addMenu("Member Manager")
        member_manager_action = QAction("👥 Member Manager", self)
        member_manager_action.triggered.connect(self.open_member_manager)
        member_view_menu.addAction(member_manager_action)
                
        # View Collaterals Menu
        view_collaterals_menu = menu_bar.addMenu("🏷️ View Collateral")
        view_collaterals_menu.setStyleSheet(AppStyles.get_main_stylesheet())
        
        actions = [
            ("Basic Details", self.show_basic_details, "View basic member details",
             "collateral_basic", get_collateral_basic),
            ("Collateral Details", self.show_collateral_details, "View land/home collateral details",
             "collateral_properties", get_collateral_properties),
            ("Family Details", self.show_family_details, "View family details",
             "collateral_family_details", get_collateral_family_details),
            ("Income/Expenses", self.show_income_expenses, "View income and expenses",
             "collateral_income_expense", get_collateral_income_expense),
            ("Project Details", self.show_project_details, "View project details",
             "collateral_projects", get_collateral_projects),
            ("Members with Loan Amount", self.show_member_loans, "View members and approved loan amounts",
             "approval_info", get_approved_loans),   
        ]
        for name, slot, tooltip, table, fetch_func in actions:
            action = QAction(f"📄 {name}", self)
            action.triggered.connect(lambda checked, t=table, f=fetch_func: [print(f"Triggering {name} with table={t}, func={f.__name__}"), slot(t, f)])
            action.setStatusTip(tooltip)
            view_collaterals_menu.addAction(action)

        # User Management Menu (Admin only)
        if self.role == "admin":
            user_menu = menu_bar.addMenu("👤 User Management")
            update_action = QAction("✏️ Update User", self)
            update_action.triggered.connect(self.open_user_management_dialog)
            update_action.setStatusTip("Update user profile")
            user_menu.addAction(update_action)

            delete_action = QAction("🗑️ Delete User", self)
            delete_action.triggered.connect(self.open_user_management_dialog)
            delete_action.setStatusTip("Delete user profile")
            user_menu.addAction(delete_action)

        # Admin Menu
        if self.role == "admin":
            self.add_admin_menu()
            
    def open_member_manager(self):
        dlg = MemberManagerDialog(self)
        dlg.exec_()

    def add_admin_menu(self):
        """Add admin-specific menu items"""
        menu_bar = self.menuBar()
        setup_menu = menu_bar.addMenu("🔧 Setup")

        loan_scheme_action = QAction("💰 Loan Scheme", self)
        loan_scheme_action.triggered.connect(self.open_loan_scheme_window)
        loan_scheme_action.setStatusTip("Manage loan schemes")
        setup_menu.addAction(loan_scheme_action)

        # Excel Operations Menu
        excel_menu = menu_bar.addMenu("Excel Tools")
        
        # Download Template
        template_action = QAction("Download Template", self)
        template_action.triggered.connect(self.download_template)
        excel_menu.addAction(template_action)
        
        # Import Data
        import_action = QAction("Import Data", self)
        import_action.triggered.connect(self.import_members)
        excel_menu.addAction(import_action)

    def setup_status_bar(self):
        """Setup status bar with uniform styling and consistent information"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Load custom font
        font_path = os.path.join("fonts", "Mukta.ttf")
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                mukta_family = families[0]
            else:
                mukta_family = "Arial"
        else:
            mukta_family = "Arial"

        # Load Organization Profile
        org_profile = get_organization_profile()
        if org_profile:
            company_name = org_profile["company_name"]
            address = org_profile["address"]
            logo_path = org_profile["logo_path"]

            # Company Logo
            if logo_path and os.path.exists(logo_path):
                from PyQt5.QtGui import QPixmap
                logo_pixmap = QPixmap(logo_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.company_logo_label = QLabel()
                self.company_logo_label.setPixmap(logo_pixmap)
                status_bar.addPermanentWidget(self.company_logo_label)

            # Company Name
            self.company_name_label = QLabel(f"{company_name}")
            font_name = QFont(mukta_family, 12)
            font_name.setBold(True)
            self.company_name_label.setFont(font_name)
            self.company_name_label.setStyleSheet("color: #2c3e50; margin-left: 8px;")
            status_bar.addPermanentWidget(self.company_name_label)

            # Company Address
            self.company_address_label = QLabel(f"{address}")
            font_address = QFont(mukta_family, 10)
            self.company_address_label.setFont(font_address)
            self.company_address_label.setStyleSheet("color: #2c3e50; margin-left: 8px;")
            status_bar.addPermanentWidget(self.company_address_label)

        # User label with styling
        self.user_label = QLabel(f"👤 {self.username} ({self.role.title()})")
        self.user_label.setProperty('statusType', 'user')
        
        # Date label with styling
        nepali_today = nepali_date.today().strftime('%Y-%m-%d')
        self.date_label = QLabel(f"📅 {nepali_today}")
        self.date_label.setProperty('statusType', 'date')

        # Time label with styling
        self.time_label = QLabel()
        self.time_label.setProperty('statusType', 'time')

        # Add labels to status bar
        status_bar.addPermanentWidget(self.user_label)
        status_bar.addPermanentWidget(self.date_label)
        status_bar.addPermanentWidget(self.time_label)
        
        # Set status bar message
        self.statusBar().showMessage("Ready", 5000)

    def setup_tabs(self):
        """Setup all tabs with consistent styling"""
        tab_configs = [
            (PersonalInfoTab(), "👤 व्यक्तिगत विवरण (Personal Info)", "Personal information management"),
            (LoanInfoTab(), "💰 ऋण माग (Loan Info)", "Loan information management"),
            (CollateralTab(), "🏠 धितो विवरण (Collateral Info)", "Collateral information management"),
            (ProjectTab(), "📋 परियोजनाको विवरण (Project Details)", "Project details management"),
            (ApprovalTab(self.username), "✅ ऋण स्वीकृत (Approval)", "Loan approval management"),
        ]
        
        for widget, title, tooltip in tab_configs:
            index = self.tabs.addTab(widget, title)
            self.tabs.setTabToolTip(index, tooltip)

        self.reports_tab = ReportsTab(username=self.username)
        reports_index = self.tabs.addTab(self.reports_tab, "📊 Reports")
        self.tabs.setTabToolTip(reports_index, "Generate and view reports")

        self.history_tab = ReportHistoryTab()
        history_index = self.tabs.addTab(self.history_tab, "📂 Report History")
        self.tabs.setTabToolTip(history_index, "View report history")

        self.loan_list_tab = LoanListTab()
        loan_index = self.tabs.addTab(self.loan_list_tab, "📋 View Loans")
        self.tabs.setTabToolTip(loan_index, "View loan history")

        if self.role == "admin":
            self.settings_tab = SettingsTab()
            settings_index = self.tabs.addTab(self.settings_tab, "⚙️ Settings")
            self.tabs.setTabToolTip(settings_index, "Application settings and configuration")

            self.org_profile_tab = OrganizationProfileTab()
            index = self.tabs.addTab(self.org_profile_tab, "🏢 Org Profile")
            self.tabs.setTabToolTip(index, "Manage organization details")

    def show_basic_details(self, table, fetch_func):
        dialog = CollateralViewDialog("Basic Details", table, fetch_func, self)
        dialog.setStyleSheet(AppStyles.get_main_stylesheet())
        dialog.exec_()
    
    def show_collateral_details(self, table, fetch_func):
        dialog = CollateralViewDialog("Collateral Details", table, fetch_func, self)
        dialog.setStyleSheet(AppStyles.get_main_stylesheet())
        dialog.exec_()
    
    def show_family_details(self, table, fetch_func):
        dialog = CollateralViewDialog("Family Details", table, fetch_func, self)
        dialog.setStyleSheet(AppStyles.get_main_stylesheet())
        dialog.exec_()
    
    def show_income_expenses(self, table, fetch_func):
        dialog = CollateralViewDialog("Income/Expenses", table, fetch_func, self)
        dialog.setStyleSheet(AppStyles.get_main_stylesheet())
        dialog.exec_()
    
    def show_project_details(self, table, fetch_func):
        dialog = CollateralViewDialog("Project Details", table, fetch_func, self)
        dialog.setStyleSheet(AppStyles.get_main_stylesheet())
        dialog.exec_()
    
    def show_member_loans(self, table, fetch_func):
        dialog = CollateralViewDialog("Members with Loan Amounts", table, fetch_func, self)
        dialog.setStyleSheet(AppStyles.get_main_stylesheet())
        dialog.exec_()

    def open_loan_scheme_window(self):
        self.loan_scheme_window = LoanSchemeManager()
        self.loan_scheme_window.show()
        
    def setup_timer(self):
        """Setup timer for real-time updates"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second
        
        # Initial time update
        self.update_time()

    def update_time(self):
        """Update time display in status bar"""
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.time_label.setText(f"🕒 {current_time}")

    def logout(self):
        """Handle logout with confirmation"""
        reply = QMessageBox.question(
            self, 
            "Logout Confirmation",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.hide()
            self.cleanup_before_logout()
            self.show_login_window()

    def closeEvent(self, event):
        """Only handle actual exit attempts"""
        if self.isVisible():
            reply = QMessageBox.question(
                self,
                "Exit Application",
                "Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No
            )
        
        if reply == QMessageBox.Yes:
            self.cleanup_before_logout()
            event.accept()
        else:
            event.ignore()

    def cleanup_before_logout(self):
        """Perform cleanup operations before logout"""
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
    
    def show_login_window(self):
        """Create and show the login window"""
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow(on_login_success=self.handle_successful_login)
        screen_geometry = QApplication.desktop().screenGeometry()
        self.login_window.move(
            (screen_geometry.width() - self.login_window.width()) // 2,
            (screen_geometry.height() - self.login_window.height()) / 2
        )
        self.login_window.show()

    def handle_successful_login(self, username):
        """Handle successful login by showing main window again"""
        self.username = username
        self.role = get_user_role(username)
        self.user_label.setText(f"👤 {self.username} ({self.role.title()})")
        self.show()
        self.statusBar().showMessage(f"Welcome back, {self.username}!", 5000)
        if hasattr(self, 'login_window'):
            self.login_window.close()

    def showEvent(self, event):
        """Handle window show event"""
        super().showEvent(event)
        self.statusBar().showMessage(f"Welcome, {self.username}!", 5000)

    def resizeEvent(self, event):
        """Handle window resize event"""
        super().resizeEvent(event)

    def download_template(self):
        """Generate and save Excel template"""
        try:
            wb = ExcelHandler.generate_template(get_database_path())
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                "Save Template As",
                "member_import_template.xlsx",
                "Excel Files (*.xlsx)"
            )
            if filepath:
                wb.save(filepath)
                self.statusBar().showMessage(f"Template saved to {filepath}", 5000)
                QMessageBox.information(self, "Success", "Template generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate template:\n{str(e)}")

    def import_members(self):
        """Handle Excel import process"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File to Import",
            "",
            "Excel Files (*.xlsx)"
        )
        if filepath:
            success, message = ExcelHandler.import_data(get_database_path(), filepath)
            if success:
                QMessageBox.information(self, "Success", message)
                self.refresh_member_data()
            else:
                QMessageBox.critical(self, "Import Failed", message)

    def refresh_member_data(self):
        """Refresh member data in all tabs"""
        if hasattr(self, 'personal_info_tab'):
            self.personal_info_tab.load_data()
        self.statusBar().showMessage("Member data refreshed", 3000)

    def open_user_management_dialog(self):
        """Open dialog for user management"""
        dialog = UserManagementDialog(self)
        dialog.exec_()

class CollateralViewDialog(QDialog):
    def __init__(self, title, table_name, fetch_func, parent=None):
        super().__init__(parent)
        print(f"Creating CollateralViewDialog for {title}, table={table_name}")  # Debug
        self.setWindowTitle(title)
        self.setMinimumSize(800, 500)
        self.table_name = table_name
        self.fetch_func = fetch_func
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel(f"{self.windowTitle()}")
        header_label.setStyleSheet(f"""
            font-size: {AppStyles.FONT_MEDIUM};
            font-weight: bold;
            color: {AppStyles.PRIMARY_COLOR};
            padding: {AppStyles.PADDING_MEDIUM}px;        
        """)
        layout.addWidget(header_label)

        # Filter by Member Number
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by Member Number:")
        filter_layout.addWidget(filter_label)
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Enter member number")
        self.filter_input.setMaximumWidth(200)
        self.filter_input.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.filter_input)
        # filter_layout.addStretch()
        
        # Save Button
        self.save_button = QPushButton("Save Changes")
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.SUCCESS_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: {AppStyles.FONT_NORMAL};
                font-weight: bold;
                min-height: {AppStyles.BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color:#17a673;
            }}
            QPushButton:pressed {{
                background-color: #138f64;
            }}
        """)
        self.save_button.clicked.connect(self.save_changes)
        filter_layout.addWidget(self.save_button)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Table View
        self.table = QTableView()
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setStyleSheet(f"""
            QTableView {{
                background-color: white;
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 6px;
                gridline-color: {AppStyles.BORDER_COLOR};
            }}
            QTableView::item:selected {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
            }}
        """)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        # Initialize QSqlDatabase
        db = QSqlDatabase.addDatabase("QSQLITE", f"{self.table_name}_conn")
        db.setDatabaseName(get_database_path())
        if not db.open():
            QMessageBox.critical(self, "Error", "Failed to connect to database", QMessageBox.Ok)
            return

        # Initialize QSqlTableModel
        self.model = QSqlTableModel(self, db)
        self.model.setTable(self.table_name)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit) #Require manual save

        
        # Define column selections (including id for updates, but hidden)
        column_maps = {
            "collateral_basic": ["id", "member_number", "monthly_saving", "child_saving", "total_saving"],
            "collateral_properties": ["id", "member_number", "owner_name", "father_or_spouse", "grandfather_or_father_inlaw",
                                     "district", "municipality_vdc", "sheet_no", "ward_no", "plot_no", "area", "land_type"],
            "collateral_family_details": ["id", "member_number", "name", "age", "relation", "member_of_org", "occupation", "monthly_income"],
            "collateral_income_expense": ["id", "member_number", "field", "amount", "type"],
            "collateral_projects": ["id", "member_number", "project_name", "self_investment", "requested_loan_amount", "total_cost", "remarks"],
            "approval_info": ["id", "member_number", "approved_loan_amount", "approved_loan_amount_words"]
        }
        
        # Get columns for the current table
        columns = column_maps.get(self.table_name, [])
        if not columns:
            QMessageBox.critical(self, "Error", f"Unknown table: {self.table_name}",
                                 QMessageBox.Ok)
            return

        # Set custom query to include id (for updates) but hide it later
        query = QSqlQuery(db)
        query_str = f"SELECT {', '.join(columns)} FROM {self.table_name}"
        query.exec_(query_str)
        
        self.model.setQuery(query)
        
        # Set headers from fetch_func (excluding id)
        headers = self.fetch_func(headers_only=True)
        for col, header in enumerate(headers, 1): # Start from 1 to skip id
            self.model.setHeaderData(col, Qt.Horizontal, header)
        
        #Make member_number read-only
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.table.setModel(self.model)
        self.table.hideColumn(0) # Hide id column
        self.table.setItemDelegateForColumn(1, ReadOnlyDelegate(self)) # Make member_number read-only
        self.table.resizeColumnsToContents()

    def apply_filter(self):
        filter_text = self.filter_input.text().strip()
        if not self.model:
            return
        
        # Rebuild query with filter
        columns = {
            "collateral_basic": ["member_number", "monthly_saving", "child_saving", "total_saving"],
            "collateral_properties": ["member_number", "owner_name", "father_or_spouse", "grandfather_or_father_inlaw",
                                     "district", "municipality_vdc", "sheet_no", "ward_no", "plot_no", "area", "land_type"],
            "collateral_family_details": ["member_number", "name", "age", "relation", "member_of_org", "occupation", "monthly_income"],
            "collateral_income_expense": ["member_number", "field", "amount", "type"],
            "collateral_projects": ["member_number", "project_name", "self_investment", "requested_loan_amount", "total_cost", "remarks"],
            "approval_info": ["member_number", "approved_loan_amount", "approved_loan_amount_words"]
        }.get(self.table_name, [])
        
        query = QSqlQuery(self.model.database())
        query_str = f"SELECT {', '.join(columns)} FROM {self.table_name}"
        if filter_text:
            query_str += f" WHERE member_number LIKE '%{filter_text}%'"
        query.exec_(query_str)
        
        self.model.setQuery(query)
        self.table.hideColumn(0) # Hide id column again after filter
        self.table.setItemDelegateForColumn(1, ReadOnlyDelegate(self)) # Reapply read-only delegate
        self.table.resizeColumnsToContents()

    def save_changes(self):
        # Validate numeric fields
        numeric_fields = {
            "collateral_basic": ["monthly_saving", "child_saving", "total_saving"],
            "collateral_properties": ["area"],
            "collateral_family_details": ["age", "monthly_income"],
            "collateral_income_expense": ["amount"],
            "collateral_projects": ["self_investment", "requested_loan_amount", "total_cost"],
            "approval_info": ["approved_loan_amount"]
        }

        columns = {
            "collateral_basic": ["id", "member_number", "monthly_saving", "child_saving", "total_saving"],
            "collateral_properties": ["id", "member_number", "owner_name", "father_or_spouse", "grandfather_or_father_inlaw",
                                     "district", "municipality_vdc", "sheet_no", "ward_no", "plot_no", "area", "land_type"],
            "collateral_family_details": ["id", "member_number", "name", "age", "relation", "member_of_org", "occupation", "monthly_income"],
            "collateral_income_expense": ["id", "member_number", "field", "amount", "type"],
            "collateral_projects": ["id", "member_number", "project_name", "self_investment", "requested_loan_amount", "total_cost", "remarks"],
            "approval_info": ["id", "member_number", "approved_loan_amount", "approved_loan_amount_words"]
        }.get(self.table_name, [])

        for row in range(self.model.rowCount()):
            for col, field in enumerate(columns[1:], 1):  # Skip id
                if field in numeric_fields.get(self.table_name, []):
                    value = self.model.data(self.model.index(row, col))
                    try:
                        if value and float(value) < 0:
                            QMessageBox.critical(self, "Validation Error",
                                                 f"Invalid value in {field} at row {row + 1}: Must be a non-negative number",
                                                 QMessageBox.Ok)
                            return
                    except ValueError:
                        QMessageBox.critical(self, "Validation Error",
                                             f"Invalid value in {field} at row {row + 1}: Must be a valid number",
                                             QMessageBox.Ok)
                        return

        # Save changes
        if self.model.submitAll():
            QMessageBox.information(self, "Success", "Changes saved successfully!",
                                    QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Error", f"Failed to save changes: {self.model.lastError().text()}",
                                 QMessageBox.Ok)

from PyQt5.QtWidgets import QItemDelegate
from PyQt5.QtCore import Qt

class ReadOnlyDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        return None  # Prevent editing this column

class UserManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Management")
        self.setMinimumSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                 AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)

        # Username Dropdown
        self.username_combo = QComboBox()
        users = get_all_users()
        print(f"Number of users retrieved: {len(users)}")
        print(f"Usernames: {[user['username'] for user in users]}")
        self.username_combo.addItems([user['username'] for user in users])
        self.username_combo.currentTextChanged.connect(self.load_user_details)
        layout.addRow(QLabel("Username:"), self.username_combo)

        # Role Field
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Enter role")
        layout.addRow(QLabel("Role:"), self.role_input)

        # Post Field
        self.post_input = QLineEdit()
        self.post_input.setPlaceholderText("Enter post")
        layout.addRow(QLabel("Post:"), self.post_input)

        # Full Name (Nepali) Field
        self.full_name_nepali_input = QLineEdit()
        self.full_name_nepali_input.setPlaceholderText("Enter full name (Nepali)")
        layout.addRow(QLabel("Full Name (Nepali):"), self.full_name_nepali_input)

        # Email Field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        layout.addRow(QLabel("Email:"), self.email_input)

        # Buttons
        button_layout = QHBoxLayout()
        update_btn = QPushButton("Update")
        update_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.SUCCESS_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: {AppStyles.FONT_NORMAL};
                font-weight: bold;
                min-height: {AppStyles.BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: #17a673;
            }}
            QPushButton:pressed {{
                background-color: #138f64;
            }}
        """)
        update_btn.clicked.connect(self.update_user)
        button_layout.addWidget(update_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.DANGER_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: {AppStyles.FONT_NORMAL};
                font-weight: bold;
                min-height: {AppStyles.BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
            QPushButton:pressed {{
                background-color: #a93226;
            }}
        """)
        delete_btn.clicked.connect(self.delete_user)
        button_layout.addWidget(delete_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.INFO_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: {AppStyles.FONT_NORMAL};
                font-weight: bold;
                min-height: {AppStyles.BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: #2c9faf;
            }}
            QPushButton:pressed {{
                background-color: #218da0;
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addRow(button_layout)
        self.setLayout(layout)
        self.load_user_details(self.username_combo.currentText())

    def load_user_details(self, username):
        if not username:
            return
        user = get_user(username)
        if user:
            self.role_input.setText(user['role'])
            self.post_input.setText(user['post'])
            self.full_name_nepali_input.setText(user['full_name_nepali'])
            self.email_input.setText(user['email'])

    def update_user(self):
        username = self.username_combo.currentText()
        if not username:
            QMessageBox.warning(self, "Error", "Please select a username.")
            return

        role = self.role_input.text() if self.role_input.text() else None
        post = self.post_input.text() if self.post_input.text() else None
        full_name_nepali = self.full_name_nepali_input.text() if self.full_name_nepali_input.text() else None
        email = self.email_input.text() if self.email_input.text() else None

        if update_user(username, role=role, post=post, full_name_nepali=full_name_nepali, email=email):
            QMessageBox.information(self, "Success", "User updated successfully.")
            self.load_user_details(username)  # Refresh fields
        else:
            QMessageBox.warning(self, "Error", "Failed to update user.")

    def delete_user(self):
        username = self.username_combo.currentText()
        if not username:
            QMessageBox.warning(self, "Error", "Please select a username.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete {username}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if delete_user(username):
                QMessageBox.information(self, "Success", "User deleted successfully.")
                self.username_combo.removeItem(self.username_combo.currentIndex())
                self.role_input.clear()
                self.post_input.clear()
                self.full_name_nepali_input.clear()
                self.email_input.clear()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete user.")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setStyleSheet(AppStyles.get_main_stylesheet())
    username = "admin"  # This would come from your login system
    window = MainWindow(username)
    window.show()
    
    sys.exit(app.exec_())

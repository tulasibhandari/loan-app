# ui/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QMenuBar, QAction, QStatusBar, 
    QLabel, QMessageBox, QApplication, QFileDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QTimer, QTime

from nepali_datetime import date as nepali_date

from models.user_model import get_user_role
from models.user_model import get_user_role
from models.database import DB_PATH

from utils.excel_handler import ExcelHandler


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



# -- Old UI code --
# class MainWindow(QMainWindow):
#     def __init__(self, username):
#         super().__init__()
#         self.username = username
#         self.role = get_user_role(username)


#         self.setWindowTitle("Loan Application Management")
#         self.setWindowIcon(QIcon("icons/logo.ico"))
#         self.resize(1000, 700)

#         self.tabs = QTabWidget()
#         self.setCentralWidget(self.tabs)
        
#         self.setStatusBar(QStatusBar())

#         # --- Menu Bar ---
#         menu_bar = self.menuBar()
#         file_menu = menu_bar.addMenu("File")

#         logout_action = QAction("Logout", self)
#         logout_action.triggered.connect(self.logout)
#         file_menu.addAction(logout_action)

#         # if self.role == "admin":
#         #     self.menu_bar = self.menuBar()
#         #     setup_menu = self.menu_bar.addMenu("Setup")

#         #     loan_scheme_action = QAction("Loan Scheme", self)
#         #     loan_scheme_action.triggered.connect(self.open_loan_scheme_window)
#         #     setup_menu.addaction(loan_scheme_action)
#         if self.role == "admin":
#             self.add_admin_menu()
#         # --- Status Bar ---
#         self.status_bar = QStatusBar()
#         self.setStatusBar(self.status_bar)

#         self.user_label = QLabel(f"👤 {self.username}")
#         self.date_label = QLabel(f"📅 {nepali_date.today().strftime('%Y-%m-%d')}")

#         self.status_bar.addPermanentWidget(self.user_label)
#         self.status_bar.addPermanentWidget(self.date_label)

#         # Optional: Add current time (updates every second)
#         self.time_label = QLabel()
#         self.status_bar.addPermanentWidget(self.time_label)

#         timer = QTimer(self)
#         timer.timeout.connect(self.update_time)
#         timer.start(1000)  # 1000 ms = 1 second
        
        

        
#         # Adding each tab
#         self.tabs.addTab(PersonalInfoTab(), "व्यक्तिगत विवरण")
#         self.tabs.addTab(LoanInfoTab(), "Loan Info")
#         self.tabs.addTab(CollateralTab(), "Collateral Info")
#         self.tabs.addTab(ProjectTab(), "परियोजनाको विवरण")
#         self.tabs.addTab(ApprovalTab(self.username), "Approval")
#         # self.tabs.addTab(ReportsTab(), "Reports")
#         self.reports_tab = ReportsTab(username=self.username)
#         self.tabs.addTab(self.reports_tab, "Reports")

#         #--Add Report history viewer Tab
#         self.history_tab = ReportHistoryTab()
#         self.tabs.addTab(ReportHistoryTab(), "📂 Report History")


#         if self.role == "admin":
#             self.settings_tab = SettingsTab()
#             self.tabs.addTab(self.settings_tab, "Settings")


#     def update_time(self):
#         current_time = QTime.currentTime().toString("hh:mm:ss AP")
#         self.time_label.setText(f"🕒 {current_time}")

#     def logout(self):
#         confirm = QMessageBox.question(self, "Logout", "Are you sure you want to logout?")
#         if confirm == QMessageBox.Yes:
#             self.close()
#             # Optionally, re-open LoginWindow here

#     def add_admin_menu(self):
#         menu_bar = self.menuBar()
#         setup_menu = menu_bar.addMenu("🔧 Setup")

#         loan_scheme_action = QAction("Loan Scheme", self)
#         loan_scheme_action.triggered.connect(self.open_loan_scheme_window)  # ✅ You need this method

#         setup_menu.addAction(loan_scheme_action)

#     def open_loan_scheme_window(self):
#         self.loan_scheme_window = LoanSchemeManager()
#         self.loan_scheme_window.show()

#     def refresh_member_header_in_all_tabs(self):
#         for i in range(self.tabs.count()):
#             widget = self.tabs.widget(i)
#             if hasattr(widget, 'update_header'):
#                 widget.update_header()

# -- End of Old UI  ---

# ui/main_window.py (Refactored)
# from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMenuBar, QAction, QStatusBar, QLabel, QApplication
# from PyQt5.QtGui import QIcon, QFont
# from PyQt5.QtCore import QTimer, QTime, Qt

# from nepali_datetime import date as nepali_date
# from models.user_model import get_user_role

# from ui.personal_info_tab import PersonalInfoTab
# from ui.loan_info_tab import LoanInfoTab
# from ui.collateral_tab import CollateralTab
# from ui.approval_tab import ApprovalTab
# from ui.reports_tab import ReportsTab
# from ui.setting_tab import SettingsTab
# from ui.loan_scheme_window import LoanSchemeManager
# from ui.report_history_tab import ReportHistoryTab
# from ui.project_tab import ProjectTab

from styles.app_styles import AppStyles
from ui.message_boxes import StandardMessageBox


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
        
        # Admin Menu
        if self.role == "admin":
            self.add_admin_menu()

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
        # self.status_bar = QStatusBar()
        # self.setStatusBar(self.status_bar)
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

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
        # Add tabs with uniform icons and consistent naming
        tab_configs = [
            (PersonalInfoTab(), "👤 व्यक्तिगत विवरण", "Personal information management"),
            (LoanInfoTab(), "💰 Loan Info", "Loan information management"),
            (CollateralTab(), "🏠 Collateral Info", "Collateral information management"),
            (ProjectTab(), "📋 परियोजनाको विवरण", "Project details management"),
            (ApprovalTab(self.username), "✅ Approval", "Loan approval management"),
        ]
        
        # Add basic tabs
        for widget, title, tooltip in tab_configs:
            index = self.tabs.addTab(widget, title)
            self.tabs.setTabToolTip(index, tooltip)

        # Add Reports tab with username
        self.reports_tab = ReportsTab(username=self.username)
        reports_index = self.tabs.addTab(self.reports_tab, "📊 Reports")
        self.tabs.setTabToolTip(reports_index, "Generate and view reports")

        # Add Report History tab
        self.history_tab = ReportHistoryTab()
        history_index = self.tabs.addTab(self.history_tab, "📂 Report History")
        self.tabs.setTabToolTip(history_index, "View report history")

        # Add Loan List View Tab
        self.loan_list_tab = LoanListTab()
        loan_index = self.tabs.addTab(self.loan_list_tab, "📋 View Loans")
        self.tabs.setTabToolTip(loan_index, "View loan history")


        # Add Settings tab for admin only
        if self.role == "admin":
            self.settings_tab = SettingsTab()
            settings_index = self.tabs.addTab(self.settings_tab, "⚙️ Settings")
            self.tabs.setTabToolTip(settings_index, "Application settings and configuration")

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
        """ Handle logout  with confirmation"""
        reply = QMessageBox.question(
            self, 
            "Logout Confirmation",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply ==  QMessageBox.Yes:
            # Hide the window instead of closing it
            self.hide()

            # Clean up resources
            self.cleanup_before_logout()

            # Show login window
            self.show_login_window()

    def closeEvent(self, event):
        """Only handle actual exit attempts"""
        # Only show exit confirmation if the window is visible
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
        """ Perform cleanup  operations before logout"""
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        
        # Can be added any other cleanup operations such as database connection close
    
            
    def show_login_window(self):
        """Create and show the login window"""
        from ui.login_window import LoginWindow
    
        # Create login window with required callback
        self.login_window = LoginWindow(on_login_success=self.handle_successful_login)
        
        # Center the window
        screen_geometry = QApplication.desktop().screenGeometry()
        self.login_window.move(
            (screen_geometry.width() - self.login_window.width()) // 2,
            (screen_geometry.height() - self.login_window.height()) // 2
        )
        
        # Show the login window
        self.login_window.show()

    def handle_successful_login(self, username):
        """Handle successful login by showing main window again"""
        # Update the current window with new user
        self.username = username
        self.role = get_user_role(username)
        self.user_label.setText(f"👤 {self.username} ({self.role.title()})")
        
        # Show the window again
        self.show()
        self.statusBar().showMessage(f"Welcome back, {self.username}!", 5000)
        
        # Close the login window
        if hasattr(self, 'login_window'):
            self.login_window.close()


    def showEvent(self, event):
        """Handle window show event"""
        super().showEvent(event)
        # self.status_bar.showMessage(f"Welcome, {self.username}!", 5000)
        self.statusBar().showMessage(f"Welcome, {self.username}!", 5000)

    def resizeEvent(self, event):
        """Handle window resize event"""
        super().resizeEvent(event)
        # You can add any resize-specific logic here if needed

    def download_template(self):
            """Generate and save Excel template"""
            try:
                wb = ExcelHandler.generate_template(DB_PATH)
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
            success, message = ExcelHandler.import_data(DB_PATH, filepath)
            if success:
                QMessageBox.information(self, "Success", message)
                self.refresh_member_data()  # Refresh your UI
            else:
                QMessageBox.critical(self, "Import Failed", message)

    def refresh_member_data(self):
        """Refresh member data in all tabs"""
        # Implement this to update your UI after import
        if hasattr(self, 'personal_info_tab'):
            self.personal_info_tab.load_data()
        # Add refreshes for other tabs as needed
        self.statusBar().showMessage("Member data refreshed", 3000)

# Example of how to use the refactored MainWindow
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Set application-wide font for consistency
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Apply global stylesheet
    app.setStyleSheet(AppStyles.get_main_stylesheet())
    
    # Create and show main window
    username = "admin"  # This would come from your login system
    window = MainWindow(username)
    window.show()
    
    sys.exit(app.exec_())
    
    
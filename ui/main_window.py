# ui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMenuBar, QAction, QStatusBar, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QTime

from nepali_datetime import date as nepali_date
from models.user_model import get_user_role


from ui.personal_info_tab import PersonalInfoTab
from ui.loan_info_tab import LoanInfoTab
from ui.collateral_tab import CollateralTab
from ui.approval_tab import ApprovalTab
from ui.reports_tab import ReportsTab
from ui.setting_tab import SettingsTab
from ui.loan_scheme_window import LoanSchemeManager

from models.user_model import get_user_role


class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.role = get_user_role(username)


        self.setWindowTitle("Loan Application Management")
        self.setWindowIcon(QIcon("icons/logo.ico"))
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.setStatusBar(QStatusBar())

        # --- Menu Bar ---
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)

        # if self.role == "admin":
        #     self.menu_bar = self.menuBar()
        #     setup_menu = self.menu_bar.addMenu("Setup")

        #     loan_scheme_action = QAction("Loan Scheme", self)
        #     loan_scheme_action.triggered.connect(self.open_loan_scheme_window)
        #     setup_menu.addaction(loan_scheme_action)
        if self.role == "admin":
            self.add_admin_menu()
        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.user_label = QLabel(f"👤 {self.username}")
        self.date_label = QLabel(f"📅 {nepali_date.today().strftime('%Y-%m-%d')}")

        self.status_bar.addPermanentWidget(self.user_label)
        self.status_bar.addPermanentWidget(self.date_label)

        # Optional: Add current time (updates every second)
        self.time_label = QLabel()
        self.status_bar.addPermanentWidget(self.time_label)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)  # 1000 ms = 1 second
        
        

        
        # Adding each tab
        self.tabs.addTab(PersonalInfoTab(), "व्यक्तिगत विवरण")
        self.tabs.addTab(LoanInfoTab(), "Loan Info")
        self.tabs.addTab(CollateralTab(), "Collateral Info")
        self.tabs.addTab(ApprovalTab(self.username), "Approval")
        self.tabs.addTab(ReportsTab(), "Reports")

        if self.role == "admin":
            self.settings_tab = SettingsTab()
            self.tabs.addTab(self.settings_tab, "Settings")


    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.time_label.setText(f"🕒 {current_time}")

    def logout(self):
        confirm = QMessageBox.question(self, "Logout", "Are you sure you want to logout?")
        if confirm == QMessageBox.Yes:
            self.close()
            # Optionally, re-open LoginWindow here

    def add_admin_menu(self):
        menu_bar = self.menuBar()
        setup_menu = menu_bar.addMenu("🔧 Setup")

        loan_scheme_action = QAction("Loan Scheme", self)
        loan_scheme_action.triggered.connect(self.open_loan_scheme_window)  # ✅ You need this method

        setup_menu.addAction(loan_scheme_action)

    def open_loan_scheme_window(self):
        self.loan_scheme_window = LoanSchemeManager()
        self.loan_scheme_window.show()

    def refresh_member_header_in_all_tabs(self):
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, 'update_header'):
                widget.update_header()

   
    
    
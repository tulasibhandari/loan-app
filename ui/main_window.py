from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon

from ui.personal_info_tab import PersonalInfoTab
from ui.loan_info_tab import LoanInfoTab
from ui.collateral_tab import CollateralTab
from ui.approval_tab import ApprovalTab
from ui.reports_tab import ReportsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Application Management")
        self.setWindowIcon(QIcon("icons/logo.ico"))
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Adding each tab
        self.tabs.addTab(PersonalInfoTab(), "व्यक्तिगत विवरण")
        self.tabs.addTab(LoanInfoTab(), "Loan Info")
        self.tabs.addTab(CollateralTab(), "Collateral Info")
        self.tabs.addTab(ApprovalTab(), "Approval")
        self.tabs.addTab(ReportsTab(), "Reports")
# ui/loan_info_tab.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class LoanInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Loan Info Tab"))
        self.setLayout(layout)

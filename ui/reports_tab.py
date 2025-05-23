# ui/reports_tab.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Reports Tab"))
        self.setLayout(layout)

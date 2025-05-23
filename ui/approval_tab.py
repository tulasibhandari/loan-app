# ui/approval_tab.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class ApprovalTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Approval Tab"))
        self.setLayout(layout)

# ui/personal_info_tab.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class PersonalInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Personal Info Tab"))
        self.setLayout(layout)

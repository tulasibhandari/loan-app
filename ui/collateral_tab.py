# ui/collateral_tab.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class CollateralTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Collateral Tab"))
        self.setLayout(layout)

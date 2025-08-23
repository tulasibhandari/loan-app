from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QFormLayout, QPushButton, QMessageBox,    
)
from PyQt5.QtCore import Qt
from models.loan_model import save_guranteer_details
from context import current_session
from styles.app_styles import AppStyles

class GuranteerFormDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("व्यक्तिगत जमानी विवरण")
        self.setMinimumSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                  AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)
        self.guranteer_
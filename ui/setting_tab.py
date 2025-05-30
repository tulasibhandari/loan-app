from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from ui.add_user_dialog import AddUserDialog

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        add_user_btn = QPushButton("➕ Add New User")
        add_user_btn.clicked.connect(self.show_add_user_dialog)
        layout.addWidget(add_user_btn)

        self.setLayout(layout)

    def show_add_user_dialog(self):
        dialog = AddUserDialog()
        dialog.exec_()

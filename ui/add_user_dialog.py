from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QMessageBox
from models.user_model import add_user

class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New User")

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.role = QComboBox()
        self.role.addItems(["admin", "user"])
        self.post = QLineEdit()

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.role)
        layout.addWidget(QLabel("Post:"))
        layout.addWidget(self.post)

        btn = QPushButton("Create User")
        btn.clicked.connect(self.create_user)
        layout.addWidget(btn)

        self.setLayout(layout)

    def create_user(self):
        add_user(
            self.username.text(),
            self.password.text(),
            self.role.currentText(),
            self.post.text()
        )
        QMessageBox.information(self, "Success", "User added successfully.")
        self.accept()

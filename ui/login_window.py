from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from models.user_model import verify_user
from PyQt5.QtGui import QIcon

class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.setWindowTitle("Login | Loan")
        self.setWindowIcon(QIcon("icons/logo.ico"))
        self.resize(300, 100)
        self.on_login_success = on_login_success

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if verify_user(username, password):
            QMessageBox.information(self, "Success", "Login Successful")
            self.on_login_success(username)
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password!")
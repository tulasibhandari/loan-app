from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QMessageBox, QHBoxLayout, QDialog, QFormLayout
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from models.organization_model import get_organization_profile
from models.user_model import verify_user, generate_reset_code, reset_password
from styles.app_styles import AppStyles
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.setWindowTitle("Login | Loan")
        self.setWindowIcon(QIcon("icons/logo.ico"))
        self.resize(400, 300)
        self.on_login_success = on_login_success
        self.org_profile = get_organization_profile()
       
        # Apply global styles
        self.setStyleSheet(AppStyles.get_main_stylesheet())

        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            AppStyles.SPACING_LARGE,
            AppStyles.SPACING_LARGE,
            AppStyles.SPACING_LARGE,
            AppStyles.SPACING_LARGE
        )
        main_layout.setSpacing(AppStyles.SPACING_MEDIUM)

        # Organization Info Section
        org_layout = QHBoxLayout()
        org_layout.setSpacing(AppStyles.SPACING_MEDIUM)

        # Logo display
        if self.org_profile and self.org_profile.get("logo_path"):
            logo_label = QLabel()
            pixmap = QPixmap(self.org_profile["logo_path"])
            logo_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))
            org_layout.addWidget(logo_label)

        # Organization name
        org_name = QLabel(self.org_profile["company_name"] if self.org_profile else
                          "Loan Management System")
        org_name.setStyleSheet(f"""
            font-size: {AppStyles.FONT_LARGE};
            font-weight: bold;
            color: {AppStyles.TEXT_PRIMARY}
        """)
        org_layout.addWidget(org_name, alignment=Qt.AlignCenter)
        org_layout.addStretch()

        main_layout.addLayout(org_layout)
        main_layout.addSpacing(AppStyles.SPACING_LARGE)

        # Login Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(AppStyles.SPACING_SMALL)

        # Username Field
        username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Your username")
        self.username_input.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        
        # Password Field
        password_layout = QHBoxLayout()
        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        
        # Toggle Password Visibility Button
        self.toggle_password_btn = QPushButton()
        self.toggle_password_btn.setIcon(QIcon("icons/eye-closed.png")) # Use an eye-closed icon
        self.toggle_password_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: 0px;
                min-width:30px;
                max-width:30px;
                min-height: {AppStyles.INPUT_HEIGHT}px;  /* Corrected property */
            }}
            QPushButton:hover {{
                background-color:{AppStyles.BACKGROUND_COLOR};
            }}
        """)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_btn)
        
        # Forgot Password Button
        self.forgot_password_btn = QPushButton("Forgot Password?")
        self.forgot_password_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.INFO_COLOR};
                color: white;
                font-size: {AppStyles.FONT_SMALL};
                border-radius: 4px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #2c9faf;
            }}
        """)
        self.forgot_password_btn.clicked.connect(self.open_forgot_password_dialog)

        # Login Button
        login_btn = QPushButton("Login")
        login_btn.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        login_btn.clicked.connect(self.login)

        # Add widgets to form layout       
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(AppStyles.SPACING_SMALL)
        form_layout.addWidget(password_label)
        # form_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)
        form_layout.addWidget(self.forgot_password_btn)  # Add button here
        form_layout.addSpacing(AppStyles.SPACING_MEDIUM)
        form_layout.addWidget(login_btn)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

        # Connect returnPressed signals to login method
        self.password_input.returnPressed.connect(self.login)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setIcon(QIcon("icons/eye-open.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setIcon(QIcon("icons/eye-closed.png"))
        logging.debug(f"Password visibility toggled to: {self.password_input.echoMode()}")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if verify_user(username, password):
            QMessageBox.information(self, "Success", "Login Successful")
            self.on_login_success(username)
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password!")

    def open_forgot_password_dialog(self):
        dialog = ForgotPasswordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.show_status_message("Password reset successful. Please log in with the new password.")

    def show_status_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Login Status")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reset Password")
        self.setMinimumSize(300, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                 AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)

        # Username Field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.username_input.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL}; padding: 5px;")
        layout.addRow(QLabel("Username:"), self.username_input)

        # Send Code Button
        send_code_btn = QPushButton("Send Reset Code")
        send_code_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
                font-size: {AppStyles.FONT_NORMAL};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #375a7f;
            }}
        """)
        send_code_btn.clicked.connect(self.send_reset_code)
        layout.addRow(send_code_btn)

        # Code Field
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter reset code from email")
        self.code_input.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.code_input.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL}; padding: 5px;")
        layout.addRow(QLabel("Reset Code:"), self.code_input)

        # New Password Field
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.new_password_input.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL}; padding: 5px;")
        layout.addRow(QLabel("New Password:"), self.new_password_input)

        # Re-enter New Password Field
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Re-enter new password")
        self.confirm_password_input.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.confirm_password_input.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL}; padding: 5px;")
        layout.addRow(QLabel("Confirm Password:"), self.confirm_password_input)

        # Buttons
        button_layout = QHBoxLayout()
        reset_btn = QPushButton("Reset Password")
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.SUCCESS_COLOR};
                color: white;
                font-size: {AppStyles.FONT_NORMAL};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #17a673;
            }}
        """)
        reset_btn.clicked.connect(self.reset_password)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.DANGER_COLOR};
                color: white;
                font-size: {AppStyles.FONT_NORMAL};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)

        self.setLayout(layout)

    def send_reset_code(self):
        username = self.username_input.text()
        if not username:
            QMessageBox.warning(self, "Error", "Username is required.")
            return

        success, msg = generate_reset_code(username)
        QMessageBox.information(self, "Reset Code", msg) if success else QMessageBox.warning(self, "Error", msg)

    def reset_password(self):
        username = self.username_input.text()
        code = self.code_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not code or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        if reset_password(username, code, new_password):
            QMessageBox.information(self, "Success", "Password reset successful.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid code or username.")

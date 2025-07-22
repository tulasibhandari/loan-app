from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QMessageBox
from models.user_model import add_user

class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New User")
        # Apply styles
        self.setStyleSheet("""
            QWidget {
                    font-family: Arial;
                    font-size: 14px
           }
            
            QLabel {
                    color: #333;
                    min-width: 150px;
            }
            QLineEdit, QDateEdit {
                           border: 1px solid #ddd;
                           border-radius: 4px;
                           padding: 8px;
                           min-width:250px;
                           background-color: white;
            }
            QLineEdit:focus, QDateEdit:focus {
                        border: 1px solid #3498db;
            }
            QPushButton {
                           background-color: #4CAF50;
                           color: white;
                           border: none;
                           padding: 10px 15px;
                           border-radius: 4px;
                           min-width: 100px;
                           }
            QPushButton:hover {
                           background-color: #45a049;
                           }                        
        """)

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.role = QComboBox()
        self.role.addItems(["admin", "user"])
        self.post = QLineEdit()
        self.nepali_name = QLineEdit()
        

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.role)
        layout.addWidget(QLabel("Post:"))
        layout.addWidget(self.post)
        layout.addWidget(QLabel("Full Name in Nepali"))
        layout.addWidget(self.nepali_name)

        btn = QPushButton("Create User")
        btn.clicked.connect(self.create_user)
        layout.addWidget(btn)

        self.setLayout(layout)

    def create_user(self):
        add_user(
            self.username.text(),
            self.password.text(),
            self.role.currentText(),
            self.post.text(),
            self.nepali_name.text()
        )
        QMessageBox.information(self, "Success", "User added successfully.")
        self.accept()

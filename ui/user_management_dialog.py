from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QHBoxLayout, QWidget, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from styles.app_styles import AppStyles
from models.user_model import get_all_users, get_user

class UserManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Management")
        self.setMinimumSize(400, 600)
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Top Bar
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)

        # Back Arrow Button
        back_btn = QPushButton()
        back_btn.setIcon(QIcon("icons/back_arrow.png"))
        back_btn.setStyleSheet(f"""
            QPushButton {{
                border:none;
                background: transparent;
                padding: 5px;
                min-width; 40px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
                border: 20px;
            }}        
        """)
        back_btn.clicked.connect(self.reject)
        top_bar.addWidget(back_btn)

        # Title
        title_label = QLabel("Select User")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        top_bar.addWidget(title_label, stretch=1)

        main_layout.addLayout(top_bar)

        # User Suggestions List
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid #ddd;
                border-radius: 8px;
                background: white;
            }}
            QListWidget::item {{
                border-bottom: 1px solid #eee;
                padding: 10px;
            }}
            QListWidget::item:selected {{
                background-color: #e6f3ff; 
            }}
        """)
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.load_users()
        main_layout.addWidget(self.list_widget)

        self.setLayout(main_layout)
    
    def load_users(self):
        self.list_widget.clear()
        users = get_all_users()
        colors = ["#3498db", "#2ecc71", "#e74c3c", "#9b59b6"] # Blue, Green, Red, Purple
        for i, user in enumerate(users):
            item = QListWidgetItem()
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)

            # Circular Badge
            badge = QLabel()
            initials = user['username'][:2] if user['username'] else "XX"
            badge.setText(initials)
            badge.setAlignment(Qt.AlignCenter)
            badge.setStyleSheet(f"""
                background-color: {colors[i % len(colors)]};
                border-radius: 15px;
                color: white;
                font-weight: bold;
                width: 30px;
                height: 30px;            
            """)
            layout.addWidget(badge)

            # User Name
            name_label = QLabel(user['username'].upper() if user['username'] else "UNKNOWN")
            name_label.setFont(QFont("Arial", 12, QFont.Bold))
            layout.addWidget(name_label, stretch=1)

            # Role (Replacing masked text)
            user_details = get_user(user["username"])
            role_label = QLabel(user_details['role'] if user_details else "Unknown Role")
            role_label.setStyleSheet("color: #7f8c8d;")
            layout.addWidget(role_label)

            # Chevron Icon
            chevron = QLabel()
            chevron.setPixmap(QPixmap("icons/chevron_right.png").scaled(16, 16, 
                                    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(chevron)
            
            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)
    
    def reject(self):
        self.close()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(AppStyles.get_main_stylesheet())
    dialog = UserManagementDialog()
    dialog.show()
    sys.exit(app.exec_())


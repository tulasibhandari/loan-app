from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from ui.add_user_dialog import AddUserDialog

from services.import_service import import_members_from_excel

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        # -- Previous Design ---
        # layout = QVBoxLayout()
        # # Apply styles
        # self.setStyleSheet("""
                  
        # """)

        # import_member_btn = QPushButton("📥 Import Members from Excel")
        # import_member_btn.clicked.connect(self.import_members_from_excel)
        # layout.addWidget(import_member_btn)


        # add_user_btn = QPushButton("➕ Add New User")
        # add_user_btn.clicked.connect(self.show_add_user_dialog)
        # layout.addWidget(add_user_btn)

        # self.setLayout(layout)
        # -- End of Previous design codes
        self.setup_ui()

    def setup_ui(self):
        # Main layout with spacing
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Create a grid layout for cards
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(0,0,0,0)

        # Apply stylesheet
        self.setStyleSheet("""
            /* Card Styles */
            QWidget[cardWidget="true"] {
                background: white;
                border-radius: 8px;
                border: 1px solid #e3e6f0;
                padding: 20px;
                min-width: 250px;
            }
            
            QWidget[cardWidget="true"]:hover {
                border-color: #bac8f3;
            }
            
            QLabel[cardTitle="true"] {
                font-size: 16px;
                font-weight: bold;
                color: #5a5c69;
                margin-bottom: 8px;
            }
            
            QLabel[cardIcon="true"] {
                font-size: 24px;
                margin-bottom: 12px;
            }
            
            QLabel[cardDesc="true"] {
                font-size: 14px;
                color: #858796;
                margin-bottom: 16px;
            }
            
            QPushButton[cardButton="true"] {
                background: transparent;
                border: 1px solid;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: bold;
                min-height:30px;
            }
            
            QPushButton[cardButton="true":hover {
                text-decoration: underline;
                font-weight: bold;
            }
        """)

        # Card 1 - Import Members
        import_card = self.create_card(
            icon = "📁",
            title = "Import Members",
            description = "Import Members data from Excel",
            button_text = "Import Members",
            callback = self.import_members_from_excel,
            color = "#4e73df"
        )
        grid_layout.addWidget(import_card, 0, 0)

        # Card 2: Add New User
        add_user_card = self.create_card(
            icon = "🙎🏻‍♂️",
            title = "User Management",
            description = "Add new system users or administrators",
            button_text = "Add New User",
            callback = self.show_add_user_dialog,
            color = "#1cc88a"
        )
        grid_layout.addWidget(add_user_card, 0, 1)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

        
    def create_card(self, icon, title, description, button_text, callback, color):
        """Create a bootstrap inspired card design"""
        card = QWidget()
        card.setProperty('cardWidget', True)
        # card.setObjectName('card')
        card.setProperty('color', color)

        # Set minimum size for better appearance
        card.setMinimumSize(280, 200)
        card.setMaximumSize(350, 250)

        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        layout.setContentsMargins(20,20,20,20)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setProperty('cardIcon', True)
        icon_label.setStyleSheet(f"color:{color}; font-size:32px;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Title
        title_label = QLabel(title)
        title_label.setProperty("cardTitle", True)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(description)
        desc_label.setProperty('cardDesc', True)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        layout.addStretch()

        # Button
        button = QPushButton(button_text)
        button.setProperty('cardButton', True)
        button.setStyleSheet(f"""
            QPushButton[cardButton="true"] {{
                color: {color};
                border-color: {color};
                background-color: transparent;
                border: 2px solid {color};
                border-radius: 6px;
                padding: 10px 16px;
                font-size: 13px;
                font-weight: bold;
                min-height: 20px;
            }}
            QPushButton[cardButton="true"]:hover {{
                background-color: {color};
                color: white;
                border-color: {color};
            }}
        """)
        button.clicked.connect(callback)
        layout.addWidget(button, 0, Qt.AlignLeft)

        return card

    def import_members_from_excel(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        
        if path:
            print(f"📁 Importing members from: {path}")
            try:
                count = import_members_from_excel(path)
                QMessageBox.information(self, "Import Complete", f"{count} सदस्यहरू सफलतापूर्वक इम्पोर्ट गरियो।")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"⚠ त्रुटि भयो:\n{str(e)}")


            

    def show_add_user_dialog(self):
        dialog = AddUserDialog()
        dialog.exec_()

# ui/organization_profile_tab.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog,
    QMessageBox, QFormLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from models.organization_model import save_organization_profile, get_organization_profile

class OrganizationProfileTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏢 Organization Profile")
        self.logo_path =  None
        self.init_ui()
        self.load_profile()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("🏢 Organization Profile")
        title_label.setStyleSheet("font-size: 20px; font-weight:bold; color:#2c3e50;")
        layout.addWidget(title_label)

        # Form
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        form_layout.addRow("संस्थाको नाम:", self.name_input)
        
        self.address_input = QTextEdit()
        form_layout.addRow("ठेगानाः", self.address_input)
        
        self.logo_label = QLabel("No logo selected.")
        self.logo_label.setFixedSize(200, 200)
        self.logo_label.setStyleSheet("border:1px solid #ddd")
        self.logo_label.setScaledContents(True)

        choose_logo_btn = QPushButton("📂 Choose Logo")
        choose_logo_btn.clicked.connect(self.choose_logo)

        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(choose_logo_btn)

        form_layout.addRow("Logo:", logo_layout)
        layout.addLayout(form_layout)

        # Save Button
        save_btn = QPushButton("💾 Save Profile")
        save_btn.clicked.connect(self.save_profile)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def choose_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Logo", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.logo_path = file_path
            pixmap = QPixmap(file_path)
            self.logo_label.setPixmap(pixmap)          
        
    def save_profile(self):
        """ Save organization profile to DB """
        name = self.name_input.text().strip()
        address = self.address_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Missing Info", "संस्थाको नाम भेटिएन!")
            return
        save_organization_profile(name, address, self.logo_path)
        QMessageBox.information(self, "Success", "संस्थाको विवरण सफलतापूर्वक सुरक्षित गरियो!")

    def load_profile(self):
        """ Load existing profile from DB"""
        profile = get_organization_profile()
        if profile:
            self.name_input.setText(profile["company_name"])
            self.address_input.setText(profile["address"])
            if profile["logo_path"]:
                pixmap = QPixmap(profile["logo_path"])
                self.logo_label.setPixmap(pixmap)
                self.logo_path = profile["logo_path"]
                
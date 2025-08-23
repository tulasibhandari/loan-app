from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox,
    QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from models.witness_model import save_witness
from context import current_session
from styles.app_styles import AppStyles

class WitnessForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("साक्षी विवरण")
        self.setWindowIcon(QIcon("icons/logo.ico"))

        self.resize(600, 700)
        self.setMinimumSize(QSize(450, 300))

        self.setup_ui()
    
    def setup_ui(self):
        # Apply global styles
        self.setStyleSheet(AppStyles.get_main_stylesheet())

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            AppStyles.PADDING_LARGE,
            AppStyles.PADDING_LARGE,
            AppStyles.PADDING_LARGE,
            AppStyles.PADDING_LARGE
        )
        main_layout.setSpacing(AppStyles.SPACING_MEDIUM)

        # Title Section
        title = QLabel("Member's Witness Info")
        title.setStyleSheet(f"""
            font-size: {AppStyles.FONT_LARGE};
            font-weight: bold;
            color: {AppStyles.TEXT_PRIMARY};
            margin-bottom: 5px;
        """)

        subtitle = QLabel("साक्षीको विवरणः")
        subtitle.setStyleSheet(f"""
            font-size: {AppStyles.FONT_MEDIUM};
            color: {AppStyles.TEXT_SECONDARY};
            margin-bottom: {AppStyles.SPACING_MEDIUM}px;
        """)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setHorizontalSpacing(AppStyles.SPACING_MEDIUM)
        form_layout.setVerticalSpacing(AppStyles.SPACING_SMALL)

        # Add form fields
        self.member_input = self.add_form_field(form_layout, "Member Number: ", "सदस्य नं: ")
        self.member_input.setText(current_session.get("member_number", ""))
        self.member_input.setReadOnly(True)
        self.name_input = self.add_form_field(form_layout, "Witness Name: ", "साक्षीको नामः")
        self.relation_input = self.add_form_field(form_layout, "Relation:", "ऋणीसँगको नाताः")
        self.address_input = self.add_form_field(form_layout, "Address:", "ठेगाना (न.पा. / गा.पा)")
        self.tole_input = self.add_form_field(form_layout, "Tole:", "टोलः")
        self.ward_input = self.add_form_field(form_layout, "Ward No:", "वार्ड नं")
        self.age_input = self.add_form_field(form_layout, "Age:", "उमेरः")


        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push button to the right
        
        save_button = QPushButton("Save")
        save_button.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        save_button.setMinimumWidth(120)
        save_button.clicked.connect(self.save_data)
        button_layout.addWidget(save_button)

        # Add Widgets to main layout
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
    
    def add_form_field(self, layout, label, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"min-width:{150}px;")

        layout.addRow(label_widget, field)
        return field
    
    def save_data(self):
        member_number = current_session.get("member_number")
        if not member_number:
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.warning(self, "Member Missing", "Please select a member first")
            return
        
        data = {
            "member": member_number,
            "name": self.name_input.text().strip(),
            "relation": self.relation_input.text().strip(),
            "address_mun": self.address_input.text().strip(),
            "ward_no": self.ward_input.text().strip(),
            "address_tole": self.tole_input.text().strip(),
            "age": self.age_input.text().strip()
        }

        try:
            save_witness(member_number, data)
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.information(self, "Saved", "साक्षी विवरण सुरक्षित भयो!")
            self.accept()
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.critical(self, "Error", f"Failed to save witness:\n{e}")

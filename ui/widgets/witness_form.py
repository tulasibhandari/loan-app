from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
QPushButton, QMessageBox, QLabel, QHBoxLayout, QWidget)
from PyQt5.QtCore import Qt
from models.witness_model import save_witness
from context import current_session


class WitnessForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("साक्षी विवरण")
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Title Section
        title = QLabel("Member's Witness Info")
        subtitle = QLabel("साक्षीको विवरणः")

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(10)

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
        save_button.setFixedWidth(100)
        save_button.clicked.connect(self.save_data)
        
        button_layout.addWidget(save_button)

        # form_widget = QWidget()
        # form_widget.setLayout(form_layout)
        # Add Widgets to main layout
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        # Apply styles
        self.apply_styles(title, subtitle)

        self.setLayout(main_layout)
    
    def add_form_field(self, layout, label, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        layout.addRow(QLabel(label), field)
        return field
    
    def apply_styles(self, title, subtitle):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }

            QLabel {
                color:#333;
                font-size:14px
            }
                           
            QLabel {
                color: #333;
                font-size: 14px;
            }
            
            QLabel[title] {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            QLabel[subtitle] {
                font-size: 16px;
                color: #7f8c8d;
                margin-bottom: 15px;
            }
            
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                min-width: 250px;
                background-color: white;
            }
            
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
            
            QLabel[required]::after {
                content: " *";
                color: #e74c3c;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #1d6fa5;
            }
        """)
        
        title.setProperty("class", "title")
        subtitle.setProperty("class", "subtitle")

    def save_data(self):
        member_number = current_session.get("member_number")
        if not member_number:
            QMessageBox.warning(self, "Member Missing", "Please select a member first")
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

        save_witness(member_number, data)
        QMessageBox.information(self, "Saved", "साक्षी विवरण सुरक्षित भयो!")
        self.accept()

if __name__ == "__main__":
    app = QApplication([])
    form = WitnessForm()
    form.show()
    app.exec_()

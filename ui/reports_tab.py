# ui/reports_tab.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QCheckBox, QVBoxLayout, QFormLayout, QScrollArea, QPushButton)

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
      
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        form_layout = QFormLayout(content)
        scroll.setWidget(content)


        # Create Checkboxes
        self.checkbox_loan_app = QCheckBox("Generate Loan Application Report")
        self.checkbox_tamasuk = QCheckBox("Generate Tamasuk Report")

        # Add checkboxes to layout
        form_layout.addWidget(self.checkbox_loan_app)
        form_layout.addWidget(self.checkbox_tamasuk)

        # Select template for Loan Application
        self.loan_template_button = QPushButton("Choose Loan Application Template")
        # self.loan_template_button.clicked.connect(self.select_loan_template)
        form_layout.addWidget(self.loan_template_button)

        self.loan_template_label = QLabel("No file selected")
        form_layout.addWidget(self.loan_template_label)

        # Select template for Tamasuk
        self.tamasuk_template_button = QPushButton("Choose Tamasuk Template")
        # self.tamasuk_template_button.clicked.connect(self.select_tamasuk_template)
        form_layout.addWidget(self.tamasuk_template_button)

        self.tamasuk_template_label = QLabel("No file selected")
        form_layout.addWidget(self.tamasuk_template_label)


        # Add Preview Button
        preview_button = QPushButton("Preview")
        # preview_button.clicked.connect(self.show_preview)
        form_layout.addWidget(preview_button)

        # Add Generate Reports button
        generate_button = QPushButton("Generate Reports")
        # generate_button.clicked.connect(self.handle_generate_reports)
        form_layout.addWidget(generate_button)

        



        # --Setting layout --
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
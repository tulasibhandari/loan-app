# ui/reports_tab.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QCheckBox, QVBoxLayout, QFormLayout,
    QScrollArea, QPushButton, QFileDialog, QMessageBox)

import os
from docxtpl import DocxTemplate
from nepali_datetime import date as nepali_date

from context import current_session
from services.prepare_report_contexts import prepare_report_context

class ReportsTab(QWidget):
    def __init__(self):

        super().__init__()
      
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        form_layout = QFormLayout(content)
        scroll.setWidget(content)

        # Template selection
        self.template_label = QLabel("📄 No template selected")
        form_layout.addWidget(self.template_label)

        # Create Checkboxes
        self.checkbox_loan_app = QCheckBox("Generate Loan Application Report")
        self.checkbox_tamasuk = QCheckBox("Generate Tamasuk Report")

        # Add checkboxes to layout
        form_layout.addWidget(self.checkbox_loan_app)
        form_layout.addWidget(self.checkbox_tamasuk)

        # Select template for Loan Application
        self.loan_template_button = QPushButton("Choose Loan Application Template")
        self.loan_template_button.clicked.connect(self.choose_loan_template)
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
        self.btn_generate_report = QPushButton("Generate Report")
        self.btn_generate_report.clicked.connect(self.generate_report)
        form_layout.addWidget(self.btn_generate_report)

              # --Setting layout --
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    
    def choose_loan_template(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Word Template", "", "Word Documents (*.docx)")
        if path:
            self.template_path = path
            self.template_label.setText(f"📄 Selected: {os.path.basename(path)}")

    def generate_report(self):
        if not self.template_path:
            QMessageBox.warning(self, "No Template", "Please select a Word Template first.")
            return
        
        member_number = current_session.get("member_number")

        if not member_number:
            QMessageBox.warning(self, "No Member selected", "Please search/select a member first.")
            return
        
        data = prepare_report_context(member_number)
        if not data:
            QMessageBox.warning(self, "Data Error", "No Data found for the selected member.")
            return
        nepali_today = nepali_date.today()
        nepali_date_str = nepali_today.strftime('%Y%m%d')  # e.g., '20821101'
      
        try:
            tpl = DocxTemplate(self.template_path)
            tpl.render(data)
            output_name = f"generated_reports/ऋण आवेदन_{member_number}_{nepali_date_str}.docx"
            os.makedirs(os.path.dirname(output_name), exist_ok=True)
            tpl.save(output_name)

            QMessageBox.information(self, "Success", f"Report generated and saved to:\n{output_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report:\n{e}")

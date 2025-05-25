# ui/approval_tab.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QGroupBox, QScrollArea,
    QFormLayout, QLineEdit, QComboBox, QPushButton
)
from PyQt5.QtCore import Qt

class ApprovalTab(QWidget):
    def __init__(self):
        super().__init__()

        # --- Scrollable Content ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)

        main_form_layout = QVBoxLayout(content)

        # --- Summary GroupBox ---
        summary_group = QGroupBox("Summary of Entered Information")
        summary_layout = QFormLayout()

        self.member_number_summary = QLabel()
        summary_layout.addRow("Member Number:", self.member_number_summary)

        self.member_name_summary = QLabel()
        summary_layout.addRow("Member Name:", self.member_name_summary)

        self.address_summary = QLabel()
        summary_layout.addRow("Address:", self.address_summary)

        self.ward_no_summary = QLabel()
        summary_layout.addRow("Ward No:", self.ward_no_summary)

        self.phone_summary = QLabel()
        summary_layout.addRow("Phone:", self.phone_summary)

        self.citizenship_summary = QLabel()
        summary_layout.addRow("Citizenship No:", self.citizenship_summary)

        self.father_name_summary = QLabel()
        summary_layout.addRow("Father Name:", self.father_name_summary)

        self.loan_amount_summary = QLabel()
        summary_layout.addRow("Applied Loan Amount:", self.loan_amount_summary)

        self.loan_type_summary = QLabel()
        summary_layout.addRow("Loan Type:", self.loan_type_summary)

        self.loan_duration_summary = QLabel()
        summary_layout.addRow("Loan Duration:", self.loan_duration_summary)

        self.monthly_saving_summary = QLabel()
        summary_layout.addRow("Monthly Saving (Rs.):", self.monthly_saving_summary)

        self.pension_saving_summary = QLabel()
        summary_layout.addRow("Pension Saving (Rs.):", self.pension_saving_summary)

        self.child_saving_summary = QLabel()
        summary_layout.addRow("Child Saving (Rs.):", self.child_saving_summary)

        summary_group.setLayout(summary_layout)
        main_form_layout.addWidget(summary_group)

        # --- Approval Section GroupBox ---
        approval_group = QGroupBox("Approval Section")
        approval_layout = QFormLayout()

        self.approval_date = QLineEdit()
        approval_layout.addRow("Approval Date (BS):", self.approval_date)

        self.entered_by = QComboBox()
        approval_layout.addRow("Entered By:", self.entered_by)

        self.entered_designation = QLineEdit()
        self.entered_designation.setReadOnly(True)
        approval_layout.addRow("Designation:", self.entered_designation)

        self.approved_by = QComboBox()
        approval_layout.addRow("Approved By:", self.approved_by)

        self.designation = QLineEdit()
        self.designation.setReadOnly(True)
        approval_layout.addRow("Designation:", self.designation)

        approval_group.setLayout(approval_layout)
        main_form_layout.addWidget(approval_group)

        # --- Navigation Button ---
        self.next_button = QPushButton("Next")
        # self.next_button.clicked.connect(self.go_to_reports_tab)
        main_form_layout.addWidget(self.next_button)

        # --- Final Main Layout with Scroll ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)


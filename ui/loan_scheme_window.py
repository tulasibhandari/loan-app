from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
                             QDoubleSpinBox, QGroupBox, QTableWidget,  QTableWidgetItem,
                             QHeaderView)
from PyQt5.QtGui import QIcon
from models.loan_scheme_model import add_or_update_loan_scheme, fetch_all_loan_schemes
from styles.app_styles import AppStyles

class LoanSchemeManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Scheme Manager")
        self.setWindowIcon(QIcon("icons/logo.ico"))
        self.setMinimumSize(1000, 800)

        # Apply the comprehensive stylesheet from AppStyles
        self.setStyleSheet(AppStyles.get_main_stylesheet())

        layout = QVBoxLayout()
        layout.setSpacing(AppStyles.SPACING_SMALL)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)

        # Create form group
        group = QGroupBox("📋 Loan Scheme Settings")
        form_layout = QFormLayout()
        form_layout.setSpacing(AppStyles.SPACING_SMALL)

        # Input Fields
        self.loan_type_input = QLineEdit()
        self.loan_type_input.setPlaceholderText("Enter loan type (e.g. घरायसी, कृषि)")
        self.interest_rate_input = QDoubleSpinBox()
        self.interest_rate_input.setSuffix(" %")
        self.interest_rate_input.setRange(0.0, 100.0)
        self.interest_rate_input.setSingleStep(0.1)
        self.interest_rate_input.setMinimumHeight(20)

        form_layout.addRow("Loan Type:", self.loan_type_input)
        form_layout.addRow("Interest Rate:", self.interest_rate_input)

        self.add_button = QPushButton("Add / Update")
        self.add_button.clicked.connect(self.save_scheme)
        self.add_button.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        form_layout.addRow(self.add_button)

        group.setLayout(form_layout)
        layout.addWidget(group)

        # self.scheme_table = QTableWidget()
        # self.scheme_table.setColumnCount(2)
        # self.scheme_table.setHorizontalHeaderLabels(["Loan Type", "Interest Rate (%)"])
        self.scheme_table = QTableWidget(5, 3)
        self.scheme_table.setHorizontalHeaderLabels(["Loan Type", "Interest Rate", "Actions"])

        # Basic table configuration
        self.scheme_table.setShowGrid(True)
        self.scheme_table.setAlternatingRowColors(True)
        self.scheme_table.setMinimumHeight(200)

        # Set fixed row height
        self.scheme_table.verticalHeader().setDefaultSectionSize(40)
        self.scheme_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # Configure horizontal header with fixed widths
        header = self.scheme_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)  # Prevent column resizing

        # Set specific column widths
        header.setDefaultSectionSize(150)  # Default width if not specified
        header.resizeSection(0, 200)  # Loan Type column - wider
        header.resizeSection(1, 150)  # Interest Rate column
        header.resizeSection(2, 120)  # Actions column

        # Optional: Prevent user resizing
        header.setCascadingSectionResizes(False)
        header.setStretchLastSection(False)

        # Optional: Style the headers
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #f0f2f5;
                padding: 8px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)

        self.scheme_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #444;
                gridline-color: #aaa;
                alternate-background-color: #f0f0f0;
                background-color: #ffffff;
            }
            QTableWidget::item {
                padding: 8px;
                border: 1px solid #bbb;
            }
            QHeaderView::section {
                padding: 10px;
                background-color: #ccc;
                border-bottom: 2px solid #dee2e6;
            }
            QTableWidget::item:selected {
                background-color: #a8d8ea;
                color: black;
            }
        # """)
       

        layout.addWidget(self.scheme_table)
        
        self.setLayout(layout)
        self.load_data()

    def save_scheme(self):
        loan_type = self.loan_type_input.text().strip()
        interest_rate = self.interest_rate_input.value()
        if loan_type:
            add_or_update_loan_scheme(loan_type, interest_rate)
            self.load_data()
        # 🎯 Clear the input fields
        self.loan_type_input.clear()
        self.interest_rate_input.setValue(0.0)
        self.loan_type_input.setFocus()
        
    def load_data(self):
        self.scheme_table.setRowCount(0)
        for row_idx, (loan_type, rate) in enumerate(fetch_all_loan_schemes()):
            self.scheme_table.insertRow(row_idx)
            self.scheme_table.setItem(row_idx, 0, QTableWidgetItem(loan_type))
            self.scheme_table.setItem(row_idx, 1, QTableWidgetItem(str(rate)))
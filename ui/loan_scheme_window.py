from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QDoubleSpinBox, QGroupBox, QTableWidget,  QTableWidgetItem
from PyQt5.QtGui import QIcon
from models.loan_scheme_model import add_or_update_loan_scheme, fetch_all_loan_schemes

class LoanSchemeManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Scheme Manager")
        self.setWindowIcon(QIcon("icons/logo.ico"))
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        group = QGroupBox("📋 Loan Scheme Settings")
        form_layout = QFormLayout()

        self.loan_type_input = QLineEdit()
        self.interest_rate_input = QDoubleSpinBox()
        self.interest_rate_input.setSuffix(" %")
        self.interest_rate_input.setRange(0.0, 100.0)
        self.interest_rate_input.setSingleStep(0.1)

        form_layout.addRow("Loan Type:", self.loan_type_input)
        form_layout.addRow("Interest Rate:", self.interest_rate_input)

        self.add_button = QPushButton("Add / Update")
        self.add_button.clicked.connect(self.save_scheme)
        form_layout.addRow(self.add_button)

        group.setLayout(form_layout)
        layout.addWidget(group)

        # self.scheme_table = QTableWidget()
        # self.scheme_table.setColumnCount(2)
        # self.scheme_table.setHorizontalHeaderLabels(["Loan Type", "Interest Rate (%)"])
        self.scheme_table = QTableWidget(5, 3)
        self.scheme_table.setHorizontalHeaderLabels(["Loan Type", "Interest Rate", "Actions"])
        self.scheme_table.setShowGrid(True)
        self.scheme_table.setAlternatingRowColors(True)
        self.scheme_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #444;
                gridline-color: #aaa;
                alternate-background-color: #f0f0f0;
                background-color: #ffffff;
            }
            QTableWidget::item {
                border: 1px solid #bbb;
            }
            QHeaderView::section {
                background-color: #ccc;
                border: 1px solid #888;
            }
            QTableWidget::item:selected {
                background-color: #a8d8ea;
                color: black;
            }
        """)

        layout.addWidget(self.scheme_table)
        
        self.setLayout(layout)
        self.load_data()

    def save_scheme(self):
        loan_type = self.loan_type_input.text().strip()
        interest_rate = self.interest_rate_input.value()
        if loan_type:
            add_or_update_loan_scheme(loan_type, interest_rate)
            self.load_data()
    
    def load_data(self):
        self.scheme_table.setRowCount(0)
        for row_idx, (loan_type, rate) in enumerate(fetch_all_loan_schemes()):
            self.scheme_table.insertRow(row_idx)
            self.scheme_table.setItem(row_idx, 0, QTableWidgetItem(loan_type))
            self.scheme_table.setItem(row_idx, 1, QTableWidgetItem(str(rate)))
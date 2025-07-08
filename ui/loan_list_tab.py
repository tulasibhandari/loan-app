# ui/loan_list_tab.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QHeaderView
)
from PyQt5.QtCore import Qt
from models.loan_model import fetch_all_loans
from styles.app_styles import AppStyles

class LoanListTab(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Loan List Viewer")
        # Apply the comprehensive stylesheet from AppStyles
        self.setStyleSheet(AppStyles.get_main_stylesheet())

        layout = QVBoxLayout()

        # Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search Member No, Name, Loan Type, Status...")
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(QLabel("Filter:"))
        search_layout.addWidget(self.search_input)

        layout.addLayout(search_layout)

        # Loan Table(
        self.loan_table = QTableWidget()
        self.loan_table.setColumnCount(7)
        self.loan_table.setHorizontalHeaderLabels([
            "Member No.", "Name", "Loan_type", "Applied Amount", 
            "Approved Amount", "Status", "Approved Date"
        ])
        self.loan_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.loan_table.setSelectionBehavior(self.loan_table.SelectRows)
        self.loan_table.setEditTriggers(self.loan_table.NoEditTriggers)

        layout.addWidget(self.loan_table)
        self.setLayout(layout)
        self.load_data()
    
    def load_data(self):
        """ Load loan data from DB"""
        self.all_loans = fetch_all_loans()
        self.populate_table(self.all_loans)
    
    def populate_table(self, loans):
        self.loan_table.setRowCount(len(loans))

        for row_idx, loan in enumerate(loans):
            for col_idx, value in enumerate(loan):
                item = QTableWidgetItem(str(value))

                # apply color  for status column
                if col_idx == 5: # Status Column
                    if value == "Approved":
                        item.setForeground(Qt.green)
                    elif value == "Pending":
                        item.setForeground(Qt.darkYellow)
                    elif value == "Cleared":
                        item.setForeground(Qt.darkCyan)
                    else:
                        item.setForeground(Qt.red)
                self.loan_table.setItem(row_idx, col_idx, item)
    
    def filter_table(self):
        """ Filter  table rows based on search input"""
        keyword = self.search_input.text().lower()
        filtered_loans = [
            loan for loan in self.all_loans
            if any(keyword in str(field).lower() for field in loan)
        ]
        self.populate_table(filtered_loans)

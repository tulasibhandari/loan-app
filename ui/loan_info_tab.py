# ui/loan_info_tab.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea, QFormLayout, QComboBox, QLineEdit, QPushButton)

class LoanInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        form_layout = QFormLayout(content)
        scroll.setWidget(content)


        self.loan_type = QComboBox()
        self.loan_type.addItems(["खरखाँचो", "घरजग्गा", "घरायसी"])
        form_layout.addRow("Type of Loan:", self.loan_type)
        
        self.interest_rate = QLineEdit()
        # self.interest_rate.setValidator(QDoubleValidator(0.0, 1e9, 2))
        form_layout.addRow("Current Interest Rate:", self.interest_rate)

        self.loan_duration = QComboBox()
        self.loan_duration.addItems(["अर्धवार्षिक", "वार्षिक", "२ वर्ष", "३ वर्ष", "४ वर्ष", "५ वर्ष"])
        form_layout.addRow("Loan Duration:", self.loan_duration)

        self.repayment_duration = QComboBox()
        self.repayment_duration.addItems(["मासिक", "त्रैमासिक", "अर्धवार्षिक"])
        form_layout.addRow("Repayment Duration:", self.repayment_duration)

        # validator = QDoubleValidator(0.0, 1000000.0, 2)
        # validator.setNotation(QDoubleValidator.StandardNotation)
        self.loan_amount = QLineEdit()
        # self.loan_amount.setValidator(validator)
        # self.loan_amount.editingFinished.connect(self.convert_amount_to_words)
        form_layout.addRow("Loan Amount:", self.loan_amount)

        self.loan_amount_in_words = QLineEdit()
        self.loan_amount_in_words.setReadOnly(True)
        form_layout.addRow("Loan Amount in words (रू.):", self.loan_amount_in_words)

        self.loan_completion_year = QLineEdit()
        # year_validator = QIntValidator(2000,2100)
        # self.loan_completion_year.setValidator(year_validator)
        form_layout.addRow("Loan Completion Year (BS):", self.loan_completion_year)

        self.loan_completion_month = QLineEdit()
        # month_validator = QIntValidator(1, 12)
        # self.loan_completion_month.setValidator(month_validator)
        form_layout.addRow("Loan Completion Month (BS):", self.loan_completion_month)

        self.loan_completion_day = QLineEdit()
        # day_validator = QIntValidator(1, 32)
        # self.loan_completion_day.setValidator(day_validator)
        form_layout.addRow("Loan Completion Day (BS):", self.loan_completion_day)


        
        
        next_button = QPushButton("Next")
        # next_button.clicked.connect(self.go_to_collateral_tab) # -- link to main.py later --
        form_layout.addRow(next_button)

        # --Setting layout --
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

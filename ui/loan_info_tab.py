# ui/loan_info_tab.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea, QFormLayout, QComboBox, QLineEdit, QPushButton)

from models.loan_model import save_loan_info
from utils.converter import convert_to_nepali_digits
from utils.amount_to_words import convert_number_to_nepali_words 

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
        self.loan_amount.editingFinished.connect(self.update_amount_in_words)
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


        
        
        self.next_button = QPushButton("Next")
        # next_button.clicked .connect(self.go_to_collateral_tab) # -- link to main.py later --
        self.next_button.clicked.connect(self.save_loan_data)
        form_layout.addRow(self.next_button)

        # --Setting layout --
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def update_amount_in_words(self):
        try:
            amount = int(self.loan_amount.text().strip())
            nepali_text = convert_number_to_nepali_words(amount)
            self.loan_amount_in_words.setText(nepali_text)
        except ValueError:
            self.amount_in_words.setText("गलत रकम")

    def save_loan_data(self):
        try:
            amount_text = self.loan_amount.text().strip()
            if not amount_text:
                raise ValueError("Loan amount is empty")

            loan_amount_nep = convert_to_nepali_digits(amount_text)
            amount_in_words = convert_number_to_nepali_words(int(amount_text))

            data = {
                'loan_type': self.loan_type.currentText(),
                'interest_rate': self.interest_rate.text().strip(),
                'loan_duration': self.loan_duration.currentText(),
                'repayment_duration': self.repayment_duration.currentText(),
                'loan_amount': loan_amount_nep,
                'loan_amount_in_words': amount_in_words,
                'loan_completion_year': convert_to_nepali_digits(self.loan_completion_year.text().strip()),
                'loan_completion_month': convert_to_nepali_digits(self.loan_completion_month.text().strip()),
                'loan_completion_day': convert_to_nepali_digits(self.loan_completion_day.text().strip())
            }

            save_loan_info(data)
            print("✅ Loan info saved successfully!")

        except Exception as e:
            print("❌ Failed to save loan info:", e)


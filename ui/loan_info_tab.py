# ui/loan_info_tab.py
from PyQt5.QtWidgets import (
    QWidget,QApplication, QLabel, QVBoxLayout, QGroupBox, QScrollArea, QFormLayout, QComboBox, QLineEdit, QPushButton)

from models.loan_model import save_loan_info
from utils.converter import convert_to_nepali_digits
from utils.amount_to_words import convert_number_to_nepali_words

from models.loan_scheme_model import fetch_all_loan_schemes
from context import current_session
from signal_bus import signal_bus

class LoanInfoTab(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ Define this first!
        main_layout = QVBoxLayout()

        # 📌 Member Header Group
        header_group = QGroupBox("📋 Associated Member Information")
        header_layout = QFormLayout()
        self.header_label = QLabel()
        self.header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green; padding: 4px;")
        header_layout.addRow(self.header_label)
        header_group.setLayout(header_layout)

        main_layout.addWidget(header_group)   # ✅ Now it's valid
        self.update_header()
      
      

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        form_layout = QFormLayout(content)
        scroll.setWidget(content)
       
       

        # Fetch loan schemes
        self.loan_schemes = fetch_all_loan_schemes()
        loan_types = [scheme[0] for scheme in self.loan_schemes]


        self.loan_type = QComboBox()
        self.loan_type.addItems(loan_types)
        self.loan_type.currentIndexChanged.connect(self.update_interest_rate)
        form_layout.addRow("Type of Loan:", self.loan_type)
        
        self.interest_rate = QLineEdit()
        self.interest_rate.setReadOnly(True)
        form_layout.addRow("Current Interest Rate:", self.interest_rate)

        self.update_interest_rate()

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
        # main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        signal_bus.session_updated.connect(self.update_header)

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

            self.clear_form() # Clears form for next entry
            QApplication.instance().activeWindow().statusBar().showMessage("✅ ऋण माग विवरण सफलतापूर्वक सुरक्षित गरियो", 5000)
        except Exception as e:
            print("❌ Failed to save loan info:", e)

    def update_interest_rate(self):
        index = self.loan_type.currentIndex()
        if index >= 0 and index < len(self.loan_schemes):
            rate = self.loan_schemes[index][1]
            self.interest_rate.setText(f"{rate:.2f}")


    def update_header(self):
        from context import current_session
        member = current_session.get("member_number")
        name = current_session.get("member_name")
        if member and name:
            self.header_label.setText(f"📌 Currently editing: {member} - {name}")
        else:
            self.header_label.setText("📌 No member selected")

    def clear_form(self):
        self.loan_type.setCurrentIndex(0)
        self.loan_duration.setCurrentIndex(0)
        self.repayment_duration.setCurrentIndex(0)
        self.loan_amount.clear()
        self.loan_amount_in_words.clear()
        self.loan_completion_year.clear()
        self.loan_completion_month.clear()
        self.loan_completion_day.clear()
        self.update_interest_rate()
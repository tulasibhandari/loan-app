# ui/loan_info_tab.py
from PyQt5.QtWidgets import (
    QWidget,QApplication, QLabel, QVBoxLayout, QGroupBox, QScrollArea, 
    QFormLayout, QComboBox, QLineEdit, QPushButton, QMessageBox, QCompleter)

from PyQt5.QtCore import Qt, QStringListModel



from models.loan_model import save_loan_info, has_existing_active_loan
from services.member_lookup import fetch_members_matching
from utils.converter import convert_to_nepali_digits
from utils.amount_to_words import convert_number_to_nepali_words

from models.loan_scheme_model import fetch_all_loan_schemes
from ui.widgets.witness_form import WitnessForm
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

        # ➕ New 
        self.new_button = QPushButton("➕ New ")
        self.new_button.clicked.connect(self.enable_form)
        main_layout.addWidget(self.new_button)

        # 🔎 Search Member
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search Member (name or number)")
        self.search_box.setEnabled(False)
        self.search_box.textChanged.connect(self.update_completer)
        self.search_box.returnPressed.connect(self.select_member)
        main_layout.addWidget(self.search_box)

        # Setup Completer
        self.completer_model = QStringListModel()
        self.completer = QCompleter(self.completer_model)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)  # Show even partial matches
        self.completer.setCompletionMode(QCompleter.PopupCompletion)  # Always show popup
        self.search_box.setCompleter(self.completer)

           

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.form_layout = QFormLayout()
        content.setLayout(self.form_layout)
        scroll.setWidget(content)


        # Apply styles
        self.setStyleSheet("""
            QWidget {
                    font-family: Arial;
                    font-size: 14px
           }
            
            QLabel {
                    color: #333;
                    min-width: 150px;
            }
            QLineEdit, QDateEdit {
                           border: 1px solid #ddd;
                           border-radius: 4px;
                           padding: 8px;
                           min-width:250px;
                           background-color: white;
            }
            QLineEdit:focus, QDateEdit:focus {
                        border: 1px solid #3498db;
            }
            QPushButton {
                           background-color: #4CAF50;
                           color: white;
                           border: none;
                           padding: 10px 15px;
                           border-radius: 4px;
                           min-width: 100px;
                           }
            QPushButton:hover {
                           background-color: #45a049;
                           }                        
        """)      
       

        # Fetch loan schemes
        self.loan_schemes = fetch_all_loan_schemes()
        loan_types = [scheme[0] for scheme in self.loan_schemes]

        
        

        self.loan_type = QComboBox()
        self.loan_type.addItems(loan_types)
        self.loan_type.currentIndexChanged.connect(self.update_interest_rate)
        self.loan_type.currentTextChanged.connect(self.on_loan_type_change)
        


        self.form_layout.addRow("Type of Loan:", self.loan_type)
        
        self.interest_rate = QLineEdit()
        self.interest_rate.setReadOnly(True)
        self.form_layout.addRow("Current Interest Rate:", self.interest_rate)

        if "खरखाँचो" in loan_types:
            index = loan_types.index("खरखाँचो")
            self.loan_type.setCurrentIndex(index)
        else:
            self.update_interest_rate()

        self.loan_duration = QComboBox()
        self.loan_duration.addItems(["अर्धवार्षिक", "वार्षिक", "२ वर्ष", "३ वर्ष", "४ वर्ष", "५ वर्ष"])
        self.form_layout.addRow("Loan Duration:", self.loan_duration)

        self.repayment_duration = QComboBox()
        self.repayment_duration.addItems(["मासिक", "त्रैमासिक", "अर्धवार्षिक"])
        self.form_layout.addRow("Repayment Duration:", self.repayment_duration)

        # validator = QDoubleValidator(0.0, 1000000.0, 2)
        # validator.setNotation(QDoubleValidator.StandardNotation)
        self.loan_amount = QLineEdit()
        # self.loan_amount.setValidator(validator)
        self.loan_amount.editingFinished.connect(self.update_amount_in_words)
        self.form_layout.addRow("Loan Amount:", self.loan_amount)

        self.loan_amount_in_words = QLineEdit()
        self.loan_amount_in_words.setReadOnly(True)
        self.form_layout.addRow("Loan Amount in words (रू.):", self.loan_amount_in_words)

        self.loan_completion_year = QLineEdit()
        # year_validator = QIntValidator(2000,2100)
        # self.loan_completion_year.setValidator(year_validator)
        self.form_layout.addRow("Loan Completion Year (BS):", self.loan_completion_year)

        self.loan_completion_month = QLineEdit()
        # month_validator = QIntValidator(1, 12)
        # self.loan_completion_month.setValidator(month_validator)
        self.form_layout.addRow("Loan Completion Month (BS):", self.loan_completion_month)

        self.loan_completion_day = QLineEdit()
        # day_validator = QIntValidator(1, 32)
        # self.loan_completion_day.setValidator(day_validator)
        self.form_layout.addRow("Loan Completion Day (BS):", self.loan_completion_day)


        
        
        self.next_button = QPushButton("Next")
        # next_button.clicked .connect(self.go_to_collateral_tab) # -- link to main.py later --
        self.next_button.clicked.connect(self.save_loan_data)
        self.form_layout.addRow(self.next_button)

        self.witness_button = QPushButton("➕ साक्षी विवरण थप्नुहोस्")
        self.witness_button.clicked.connect(self.open_witness_form)
        self.form_layout.addRow(self.witness_button)

        # --Setting layout --
        # main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
        # Initially disable form
        self.set_form_enabled(False)

        # Listen for session updates
        signal_bus.session_updated.connect(self.update_header)
    
    def enable_form(self):
        """ Enable form clicking ➕ New """
        self.set_form_enabled(True)
        self.search_box.setEnabled(True)
        self.search_box.setFocus()

    def set_form_enabled(self, enabled):
        """ Enable / disable form fields and buttons"""
        for i in range(self.form_layout.count()):
            widget = self.form_layout.itemAt(i).widget()
            if widget:
                widget.setEnabled(enabled)
        self.witness_button.setEnabled(enabled)
        self.next_button.setEnabled(enabled)

    def update_completer(self, text):
        """Update member search suggestions """
        results = fetch_members_matching(text)
        # print(f"🔍 Matching Members for '{text}':", results)  # Debug
        names = [
            f"{row['member_name']} ({row['member_number']})" if isinstance(row, dict)
            else f"{row[1]} ({row[0]})"
            for row in results    
        ]
        self.completer_model.setStringList(names)
        # Force popup to show updated suggestions
        if names:
            self.completer.complete()

    def select_member(self):
        """ Set selected member in session """
        selected = self.search_box.text()
        if "(" in selected and ")" in selected:
            # member_number = selected.split("(")[-1].rstrip(")") -> old code
            member_number = selected.split("(")[-1].strip(")").strip()
            member_name = selected.split("(")[0].strip()
            current_session["member_number"] = member_number
            current_session["member_name"] = member_name
            signal_bus.session_updated.emit()
        else:
            QMessageBox.warning(self, "Invalid", "Please select a valid member from suggestions!")
            
    def update_amount_in_words(self):
        try:
            amount = int(self.loan_amount.text().strip())
            nepali_text = convert_number_to_nepali_words(amount)
            self.loan_amount_in_words.setText(nepali_text)
        except ValueError:
            self.amount_in_words.setText("गलत रकम")

    def save_loan_data(self):
        try:
            member_number = current_session.get("member_number")
            if not member_number:
                QMessageBox.warning(self, "No Member Selected", "Please select a member first.")
                return
            
            # Check for existing active loan
            if has_existing_active_loan(member_number):
                QMessageBox.warning(self, "Loan Exists", f"This member ({member_number}) already has a pending or approved loan. Cannot apply again.")
            amount_text = self.loan_amount.text().strip()
            if not amount_text:
                raise ValueError("Loan amount is empty")

            loan_amount_nep = convert_to_nepali_digits(amount_text)
            amount_in_words = convert_number_to_nepali_words(int(amount_text))

            data = {
                'member_number':current_session.get("member_number"),
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
            QMessageBox.information(self, "Loan Saved", "Loan information saved successfully.")
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

    def on_loan_type_change(self):
        selected_type = self.loan_type.currentText()
        current_session["loan_type"] = selected_type


    def update_header(self):
        """Update header with current session"""
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
    
    def open_witness_form(self):
        dialog = WitnessForm()
        dialog.exec_()
from PyQt5.QtWidgets import (
    QWidget, QApplication, QLabel, QVBoxLayout, QGroupBox, QScrollArea, 
    QFormLayout, QComboBox, QLineEdit, QPushButton, QMessageBox, QCompleter, QHBoxLayout
)
from PyQt5.QtCore import Qt, QStringListModel
from models.loan_model import save_loan_info
from services.member_lookup import fetch_members_matching
from utils.converter import convert_to_nepali_digits
from utils.amount_to_words import convert_number_to_nepali_words
from models.loan_scheme_model import fetch_all_loan_schemes
from ui.widgets.witness_form import WitnessForm
from context import current_session
from signal_bus import signal_bus
from styles.app_styles import AppStyles

class LoanInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.loan_schemes = fetch_all_loan_schemes()
        self.setup_ui()

        # Listen for session updates
        signal_bus.session_updated.connect(self.update_header)
        # Signal for loan addition
        self.loan_added = signal_bus.loan_added

    def setup_ui(self):
        # Apply global styles
        self.setStyleSheet(AppStyles.get_main_stylesheet())

        # Define main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM
        )
        main_layout.setSpacing(AppStyles.SPACING_MEDIUM)

        # Member Header Group
        header_group = QGroupBox("📋 सदस्य विवरण")
        header_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {AppStyles.FONT_MEDIUM};
                font-weight: bold;
                color: {AppStyles.TEXT_PRIMARY};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }}
        """)
        header_layout = QFormLayout()
        self.member_number_label = QLabel()
        self.member_number_label.setStyleSheet(f"""
            font-size: {AppStyles.FONT_NORMAL};
            color: {AppStyles.TEXT_PRIMARY};
            padding: 4px;
        """)
        self.member_name_label = QLabel()
        self.member_name_label.setStyleSheet(f"""
            font-size: {AppStyles.FONT_NORMAL};
            color: {AppStyles.TEXT_PRIMARY};
            padding: 4px;
        """)
        header_layout.addRow("सदस्य नं:", self.member_number_label)
        header_layout.addRow("सदस्यको नाम:", self.member_name_label)
        header_group.setLayout(header_layout)
        main_layout.addWidget(header_group)
        self.update_header()

        # New Button 
        self.new_button = QPushButton("➕ New")
        self.new_button.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        self.new_button.clicked.connect(self.enable_form)
        main_layout.addWidget(self.new_button)

        # Search Member
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search Member (name or number)")
        self.search_box.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.search_box.setEnabled(False)
        self.search_box.textChanged.connect(self.update_completer)
        self.search_box.returnPressed.connect(self.select_member)
        main_layout.addWidget(self.search_box)

        # Setup Completer
        self.completer_model = QStringListModel()
        self.completer = QCompleter(self.completer_model)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.search_box.setCompleter(self.completer)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(AppStyles.SPACING_SMALL)
        self.form_layout.setHorizontalSpacing(AppStyles.SPACING_MEDIUM)
        content.setLayout(self.form_layout)
        scroll.setWidget(content)

        # Loan Type
        self.loan_type = QComboBox()
        self.loan_type.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        loan_types = [scheme[0] for scheme in self.loan_schemes]
        self.loan_type.addItems(loan_types)
        self.loan_type.currentIndexChanged.connect(self.update_interest_rate)
        self.loan_type.currentTextChanged.connect(self.on_loan_type_change)
        self.form_layout.addRow("ऋणको प्रकार:", self.loan_type)
        
        # Interest Rate
        self.interest_rate = QLineEdit()
        self.interest_rate.setReadOnly(True)
        self.interest_rate.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.form_layout.addRow("हालको ब्याजदर:", self.interest_rate)

        if "खरखाँचो" in loan_types:
            index = loan_types.index("खरखाँचो")
            self.loan_type.setCurrentIndex(index)
        else:
            self.update_interest_rate()

        # Loan Duration
        self.loan_duration = QComboBox()
        self.loan_duration.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.loan_duration.addItems(["अर्धवार्षिक", "वार्षिक", "२ वर्ष", "३ वर्ष", "४ वर्ष", "५ वर्ष"])
        self.form_layout.addRow("ऋण अवधि:", self.loan_duration)

        # Repayment Duration
        self.repayment_duration = QComboBox()
        self.repayment_duration.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.repayment_duration.addItems(["मासिक", "त्रैमासिक", "अर्धवार्षिक"])
        self.form_layout.addRow("भुक्तानी अवधि:", self.repayment_duration)

        # Loan Amount
        self.loan_amount = QLineEdit()
        self.loan_amount.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.loan_amount.editingFinished.connect(self.update_amount_in_words)
        self.form_layout.addRow("ऋण रकम:", self.loan_amount)

        self.loan_amount_in_words = QLineEdit()
        self.loan_amount_in_words.setReadOnly(True)
        self.loan_amount_in_words.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.form_layout.addRow("ऋण रकम (शब्दमा):", self.loan_amount_in_words)

        # Loan Completion Date
        self.loan_completion_year = QLineEdit()
        self.loan_completion_year.setMinimumHeight(AppStyles.INPUT_HEIGHT)       
        self.form_layout.addRow("ऋण समापन वर्ष (BS):", self.loan_completion_year)

        self.loan_completion_month = QLineEdit()
        self.loan_completion_month.setMinimumHeight(AppStyles.INPUT_HEIGHT)        
        self.form_layout.addRow("ऋण समापन महिना (BS):", self.loan_completion_month)

        self.loan_completion_day = QLineEdit()
        self.loan_completion_day.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.form_layout.addRow("ऋण समापन दिन (BS):", self.loan_completion_day)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(AppStyles.SPACING_MEDIUM)
               
        self.next_button = QPushButton("💾 Save")
        self.next_button.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        self.next_button.clicked.connect(self.save_loan_data)
        button_layout.addWidget(self.next_button)

        self.witness_button = QPushButton("➕ साक्षी विवरण थप्नुहोस्")
        self.witness_button.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        self.witness_button.clicked.connect(self.open_witness_form)
        button_layout.addWidget(self.witness_button)

        self.form_layout.addRow(button_layout)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
        # Initially disable form
        self.set_form_enabled(False)

    def enable_form(self):
        """Enable form clicking ➕ New"""
        self.set_form_enabled(True)
        self.search_box.setEnabled(True)
        self.search_box.setFocus()

    def set_form_enabled(self, enabled):
        """Enable/disable form fields and buttons"""
        for i in range(self.form_layout.count()):
            widget = self.form_layout.itemAt(i).widget()
            if widget:
                widget.setEnabled(enabled)
        self.witness_button.setEnabled(enabled)
        self.next_button.setEnabled(enabled)

    def update_completer(self, text):
        """Update member search suggestions"""
        results = fetch_members_matching(text)
        names = [
            f"{row['member_name']} ({row['member_number']})" if isinstance(row, dict)
            else f"{row[1]} ({row[0]})"
            for row in results    
        ]
        self.completer_model.setStringList(names)
        if names:
            self.completer.complete()

    def select_member(self):
        """Set selected member in session"""
        selected = self.search_box.text()
        if "(" in selected and ")" in selected:
            member_number = selected.split("(")[-1].strip(")").strip()
            member_name = selected.split("(")[0].strip()
            current_session["member_number"] = member_number
            current_session["member_name"] = member_name
            signal_bus.session_updated.emit()
        else:
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.warning(self, "अमान्य", "कृपया सुझावहरूबाट मान्य सदस्य छान्नुहोस्!")

    def update_amount_in_words(self):
        try:
            amount = self.loan_amount.text().strip()
            if not amount:
                self.loan_amount_in_words.setText("")
                return
            amount_int = int(amount.replace(",", ""))
            nepali_text = convert_number_to_nepali_words(amount_int)
            self.loan_amount_in_words.setText(nepali_text)
        except ValueError:
            self.loan_amount_in_words.setText("गलत रकम")

    def save_loan_data(self):
        try:
            member_number = current_session.get("member_number")
            if not member_number:
                msg = QMessageBox()
                msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
                msg.warning(self, "कुनै सदस्य चयन गरिएको छैन", "कृपया पहिले सदस्य छान्नुहोस्।")
                return

            data = {
                'member_number': member_number,
                'loan_type': self.loan_type.currentText(),
                'interest_rate': self.interest_rate.text().strip(),
                'loan_duration': self.loan_duration.currentText(),
                'repayment_duration': self.repayment_duration.currentText(),
                'loan_amount': convert_to_nepali_digits(self.loan_amount.text().strip()),
                'loan_amount_in_words': self.loan_amount_in_words.text().strip(),
                'loan_completion_year': convert_to_nepali_digits(self.loan_completion_year.text().strip()),
                'loan_completion_month': convert_to_nepali_digits(self.loan_completion_month.text().strip()),
                'loan_completion_day': convert_to_nepali_digits(self.loan_completion_day.text().strip())
            }

            # Validate inputs
            if not data["loan_amount"]:
                raise ValueError("ऋण रकम खाली छ।")
            if not all(data[field] for field in ["loan_completion_year", "loan_completion_month", "loan_completion_day"]):
                raise ValueError("ऋण समापन मिति (वर्ष, महिना, दिन) खाली छ।")

            save_loan_info(data)
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.information(self, "ऋण सुरक्षित", "✅ ऋण विवरण सफलतापूर्वक सुरक्षित भयो।")
            QApplication.instance().activeWindow().statusBar().showMessage("✅ ऋण माग विवरण सफलतापूर्वक सुरक्षित गरियो", 5000)
            self.clear_form()
            self.loan_added.emit()  # Notify ApprovalTab

        except ValueError as e:
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.warning(self, "प्रतिबन्धित", str(e))
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.critical(self, "त्रुटि", f"❌ ऋण विवरण सुरक्षित गर्न असफल:\n{e}")

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
        member_number = current_session.get("member_number", "")
        member_name = current_session.get("member_name", "")
        self.member_number_label.setText(member_number if member_number else "कुनै सदस्य चयन गरिएको छैन")
        self.member_name_label.setText(member_name if member_name else "कुनै सदस्य चयन गरिएको छैन")

    def clear_form(self):
        self.loan_type.setCurrentIndex(0)
        self.loan_duration.setCurrentIndex(0)
        self.repayment_duration.setCurrentIndex(0)
        self.loan_amount.clear()
        self.loan_amount_in_words.clear()
        self.loan_completion_year.clear()
        self.loan_completion_month.clear()
        self.loan_completion_day.clear()
        self.search_box.clear()
        self.update_interest_rate()
        self.set_form_enabled(False)
    
    def open_witness_form(self):
        dialog = WitnessForm()
        dialog.exec_()

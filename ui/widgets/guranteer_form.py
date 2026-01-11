from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QFormLayout, QPushButton, QMessageBox, QComboBox,
    QHBoxLayout  
)
from PyQt5.QtCore import Qt
from models.database import get_connection
from models.guarantor_model import save_guranteer_details  # Assuming this is the correct file
from context import current_session
from styles.app_styles import AppStyles
from nepali_datetime import date as nepali_date
from utils.converter import convert_to_nepali_digits

class GuranteerFormDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("व्यक्तिगत जमानी विवरण")
        self.setMinimumSize(500, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                 AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)

        # Applicant Member data from session (Readonly)
        self.applicant_member_number = QLineEdit()
        self.applicant_member_number.setReadOnly(True)
        self.applicant_member_number.setText(current_session.get("member_number", ""))
        layout.addRow("ऋण आवेदक सदस्य नंः", self.applicant_member_number)

        # Guarantor member number (Searchable QComboBox)
        self.guranteer_member_number = QComboBox()
        self.guranteer_member_number.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.guranteer_member_number.setEditable(True)
        self.guranteer_member_number.currentTextChanged.connect(self.autofill_guranteer_info)
        self.load_member_numbers()
        layout.addRow("जमानी सदस्य नंः", self.guranteer_member_number)

        # Autofilled Fields
        self.guranteer_name = QLineEdit()
        self.guranteer_name.setReadOnly(True)
        layout.addRow("जमानीको नामः", self.guranteer_name)

        self.address = QLineEdit()
        self.address.setReadOnly(True)
        layout.addRow("ठेगानाः", self.address)

        self.ward_no = QLineEdit()
        self.ward_no.setReadOnly(True)
        layout.addRow("वार्ड नंः", self.ward_no)

        self.grandfather_name = QLineEdit()
        self.grandfather_name.setReadOnly(True)
        layout.addRow("बाजेको नामः", self.grandfather_name)
         
        self.father_name = QLineEdit()
        self.father_name.setReadOnly(True)
        layout.addRow("बाबुको नामः", self.father_name)

        self.age = QLineEdit()
        self.age.setReadOnly(True)
        layout.addRow("जमानीको उमेरः", self.age)

        self.phone = QLineEdit()
        self.phone.setReadOnly(True)
        layout.addRow("मोबाइल नंः", self.phone)

        self.citizenship_no = QLineEdit()
        self.citizenship_no.setReadOnly(True)
        layout.addRow("नागरिकता नंः", self.citizenship_no)

        self.issue_district = QLineEdit()
        layout.addRow("नागरिकता जारी जिल्लाः", self.issue_district)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(AppStyles.SPACING_SMALL)

        self.save_button = QPushButton("Save Guarantor Info")
        self.save_button.setMinimumHeight(int(AppStyles.BUTTON_HEIGHT // 1.5))
        self.save_button.clicked.connect(self.save_guarantor)
        button_layout.addWidget(self.save_button)

        self.clear_btn = QPushButton("Clear Form")
        self.clear_btn.setMinimumHeight(int(AppStyles.BUTTON_HEIGHT // 1.5))
        self.clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumHeight(int(AppStyles.BUTTON_HEIGHT // 1.5))
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addRow(button_layout)
        self.setLayout(layout)

    def load_member_numbers(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT member_number FROM member_info")
            member_numbers = [row[0] for row in cursor.fetchall()]
            self.guranteer_member_number.addItems(member_numbers)
            conn.close()
        except Exception as e:
            print(f"Error loading member numbers: {e}")
    
    def autofill_guranteer_info(self):
        guranteer_member = self.guranteer_member_number.currentText()
        if not guranteer_member:
            self.clear_autofill_fields()
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT member_name, address, ward_no, phone, citizenship_no, grandfather_name, father_name, dob_bs
                FROM member_info
                WHERE member_number = ?
            """, (guranteer_member,))
            result = cursor.fetchone()
            conn.close()

            if result:
                member_name, address, ward_no, phone, citizenship_no, grandfather_name, father_name, dob_bs = result
                self.guranteer_name.setText(member_name or "")
                self.address.setText(address or "")
                self.ward_no.setText(ward_no or "")
                self.phone.setText(phone or "")
                self.citizenship_no.setText(citizenship_no or "")
                self.grandfather_name.setText(grandfather_name or "")
                self.father_name.setText(father_name or "")

                # Calculate age from DOB
                if dob_bs:
                    try:
                        year = int(dob_bs.split('-')[0])
                        current_year = nepali_date.today().year
                        age = current_year - year
                        self.age.setText(str(age) if age > 0 else "")
                    except (ValueError, IndexError):
                        self.age.setText("")
                else:
                    self.age.setText("")
            else:
                self.clear_autofill_fields()
        except Exception as e:
            print(f"Error auto-filling guarantor info: {e}")

    def clear_autofill_fields(self):
        for field in [self.guranteer_name, self.address, self.ward_no, self.phone, 
                     self.citizenship_no, self.grandfather_name, self.father_name, 
                     self.age, self.issue_district]:
            field.clear()
    
    def save_guarantor(self):
        member_number = current_session.get("member_number")
        guranteer_member = self.guranteer_member_number.currentText().strip()

        if not member_number or not guranteer_member:
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.warning(self, "Error", "आवेदक वा जमानीको सदस्य नं आवश्यक छ")
            return
        
        data = {
            'member_number': convert_to_nepali_digits(member_number),
            'guarantor_member_number':convert_to_nepali_digits(guranteer_member),  # Corrected to string value
            'guarantor_name': self.guranteer_name.text().strip(),
            'guarantor_address': self.address.text().strip(),
            'guarantor_ward': convert_to_nepali_digits(self.ward_no.text().strip()),
            'guarantor_phone': convert_to_nepali_digits(self.phone.text().strip()),
            'guarantor_citizenship': convert_to_nepali_digits(self.citizenship_no.text().strip()),
            'guarantor_grandfather': self.grandfather_name.text().strip(),
            'guarantor_father': self.father_name.text().strip(),
            'guarantor_issue_dist': self.issue_district.text().strip(),
            'guarantor_age': convert_to_nepali_digits(self.age.text().strip())
        }
        if not data['guarantor_name'] or not data['guarantor_phone']:
            QMessageBox.warning(self, "त्रुटि", "जमानीको नाम र सम्पर्क नं आवश्यक छ।")
            return

        try:
            print(f"Saving data: {data}")  # Debug output
            success = save_guranteer_details(data)
            if success:
                QMessageBox.information(self, "सफलता", "व्यक्तिगत जमानी विवरण सुरक्षित भयो।")
                self.accept()
            else:
                QMessageBox.warning(self, "त्रुटि", "डाटा सुरक्षित गर्न असफल भयो।")
        except Exception as e:
            QMessageBox.critical(self, "त्रुटि", f"जमानी विवरण सुरक्षित गर्न असफल:\n{e}")

    def clear_form(self):
        self.guranteer_member_number.setCurrentIndex(-1)
        self.clear_autofill_fields()
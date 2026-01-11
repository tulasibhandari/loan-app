from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from models.manjurinama_model import save_manjurinama_details
from context import current_session
from styles.app_styles import AppStyles
from utils.converter import convert_to_nepali_digits

class ManjurinamaForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("मञ्जुरीनामा विवरण")
        self.setMinimumSize(500,400)
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

        
        self.consenting_person = QLineEdit()
        self.consenting_person.setPlaceholderText("मञ्जुरीनामा दिने व्यक्तिको नामथर")
        layout.addRow("मञ्जुरीनामा दिने व्यक्तिः", self.consenting_person)

        self.consenting_grandfather = QLineEdit()
        self.consenting_grandfather.setPlaceholderText("मञ्जुरीनामा दिने व्यक्तिको हजुरबुवाको नामथर")
        layout.addRow("मञ्जुरीनामा दिने व्यक्तिको हजुरबुवा:", self.consenting_grandfather)

        self.consenting_father = QLineEdit()
        self.consenting_father.setPlaceholderText("मञ्जुरीनामा दिने व्यक्तिको बुवाको नामथर:")
        layout.addRow("मञ्जुरीनामा दिने व्यक्तिको बुवा:", self.consenting_father)

        self.district = QLineEdit()
        self.district.setPlaceholderText("मञ्जुरीनामा दिने व्यक्तिको ठेगाना (जिल्ला)")
        layout.addRow("ठेगानाः (जिल्ला)", self.district)

        self.municipality =  QLineEdit()
        self.municipality.setPlaceholderText("मञ्जुरीनामा दिने व्यक्तिको ठेगाना (गा.पा. / न.पा.)")
        layout.addRow("ठेगानाः (गा.पा. / न.पा.)", self.municipality)

        self.ward_no =  QLineEdit()
        self.ward_no.setPlaceholderText("मञ्जुरीनामा दिने व्यक्तिको ठेगाना (वार्ड नं)")
        layout.addRow("ठेगानाः (वार्ड नं)", self.ward_no)

        self.tole =  QLineEdit()
        self.tole.setPlaceholderText("मञ्जुरीनामा दिने व्यक्तिको ठेगाना (टोल)")
        layout.addRow("ठेगानाः (टोल)", self.tole)

        self.consenting_age = QLineEdit()
        self.consenting_age.setPlaceholderText("मञ्जुरीनामा दिने व्यक्तिको ठेगाना उमेर")
        layout.addRow("उमेर:", self.consenting_age)

        save_btn = QPushButton("Save Manjurinama Info")
        save_btn.setMinimumHeight(int(AppStyles.BUTTON_HEIGHT // 1.5))
        save_btn.clicked.connect(self.save_manjurinama)
        layout.addRow(save_btn)

        clear_btn = QPushButton("Clear Form")
        clear_btn.setMinimumHeight(int(AppStyles.BUTTON_HEIGHT))
        clear_btn.clicked.connect(self.clear_form)
        layout.addRow(clear_btn)

        self.setLayout(layout)
    
    def save_manjurinama(self):
        member_number = current_session.get("member_number")
        if not member_number:
            QMessageBox.warning(self, "Error", "कृपया पहिले सदस्य छान्नुहोस्।")
            return
        data = {
            'member_number': member_number,
            'person_name': self.consenting_person.text().strip(),
            'grandfather_name': self.consenting_grandfather.text().strip(),
            'father_name':self.consenting_father.text().strip(),
            'age': convert_to_nepali_digits(self.consenting_age.text().strip()),
            'district': self.district.text().strip(),
            'muncipality': self.municipality.text().strip(),
            'wada_no':convert_to_nepali_digits(self.ward_no.text().strip()),
            'tole': self.tole.text().strip()
        }

        if not data["member_number"] or not data["person_name"]:
            QMessageBox.warning(self, "Error", "Applicant member number or Consenting person name is missing.")
            return

        try:
            save_manjurinama_details(data)
            QMessageBox.information(self, "Success", "Manjurinama Details have been saved successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"मञ्जुरीनामा विवरण सुरक्षित गर्न असफल:\n{e}")


    def clear_form(self):
        self.consenting_person.clear()
        self.consenting_grandfather.clear()
        self.consenting_father.clear()
        self.consenting_age.clear()
        self.district.clear()
        self.municipality.clear()
        self.ward_no.clear()
        self.tole.clear()

        

        



        
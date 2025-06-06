# ui/personal_info_tab.py
from PyQt5.QtWidgets import (
    QWidget, QApplication, QFormLayout, QLineEdit, QDateEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QScrollArea, QMessageBox)

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from nepali_datetime import date as nepali_date

from models.loan_model import save_or_update_member_info
from utils.converter import convert_to_nepali_digits
from services.member_lookup import fetch_member_data
from context import current_session
from signal_bus import signal_bus


class PersonalInfoTab(QWidget):
    def __init__(self):
        super().__init__()

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        form_layout = QFormLayout(content)
        scroll.setWidget(content)

        # --Form Fields --
        self.date_field = QLineEdit()
        self.date_field.setReadOnly(True)
        current_bs_date = nepali_date.today().strftime("%Y-%m-%d")
        # --Debug print --
        print("Nepali Date:", current_bs_date)
        # -- End of debug print --
        self.date_field.setText(current_bs_date)
        form_layout.addRow(QLabel("मितिः"), self.date_field)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by Member ID or Name")
        self.search_btn = QPushButton("Search Member")
        self.search_btn.clicked.connect(self.search_member)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        form_layout.addRow(search_layout)

        self.member_number = QLineEdit()
        form_layout.addRow(QLabel("सदस्य नं"), self.member_number)

        self.member_name = QLineEdit()
        form_layout.addRow(QLabel("सदस्यको नामथरः"), self.member_name)

        self.member_address = QLineEdit()
        form_layout.addRow(QLabel("ठेगानाः"),self.member_address)
        
        self.member_address_wardno = QLineEdit()
        form_layout.addRow(QLabel("वार्ड नं"), self.member_address_wardno)

        self.member_phone = QLineEdit()
        form_layout.addRow(QLabel("सम्पर्क नं"), self.member_phone)

        self.bs_dob = QDateEdit()
        self.bs_dob.setDisplayFormat("yyyy-MM-dd")
        self.bs_dob.setDate(QDate(2055,1,1))
        form_layout.addRow("Date of Birth (BS):", self.bs_dob)

        self.member_citizenship_no = QLineEdit()
        form_layout.addRow("Citizenship No:", self.member_citizenship_no)

        self.member_father_name = QLineEdit()
        form_layout.addRow("Father's Name:", self.member_father_name)

        self.member_grandfather_name = QLineEdit()
        form_layout.addRow("Grandfather's Name:", self.member_grandfather_name)

        self.member_spouse = QLineEdit()
        form_layout.addRow("Spouse Name:", self.member_spouse)

        self.member_spouse_number = QLineEdit()
        form_layout.addRow("Spouse Phone No:", self.member_spouse_number)

        self.member_business = QLineEdit()
        form_layout.addRow("Business Name:", self.member_business)

        self.member_business_address = QLineEdit()
        form_layout.addRow("Business Address:", self.member_business_address)

        self.member_job = QLineEdit()
        form_layout.addRow("Job Name:", self.member_job)

        self.member_job_address = QLineEdit()
        form_layout.addRow("Job Address:", self.member_job_address)

        # --- Next Button Placeholder ---
        self.next_button = QPushButton("Save")
        # self.next_button.clicked.connect(...) ← Will be connected in MainWindow
        self.next_button.clicked.connect(self.save_data)
        self.next_button.setIcon(QIcon('icon/icon_btn.png'))
        form_layout.addRow(self.next_button)

        self.clear_btn = QPushButton("Clear Form")
        self.clear_btn.clicked.connect(self.clear_form)
        form_layout.addRow(self.clear_btn)



        # --Setting layout --
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def save_data(self):
        dob = self.bs_dob.date().toString('yyyy-MM-dd')
        dob_nepali = convert_to_nepali_digits(dob)

        data = {
            'date': self.date_field.text(),
            'member_number': self.member_number.text(),
            'member_name': self.member_name.text(),
            'address': self.member_address.text(),
            'ward_no': self.member_address_wardno.text(),
            'phone': self.member_phone.text(), 
            'dob_bs': dob_nepali, 
            'citizenship_no': self.member_citizenship_no.text(), 
            'father_name': self.member_father_name.text(), 
            'grandfather_name': self.member_grandfather_name.text(),
            'spouse_name': self.member_spouse.text(), 
            'spouse_phone': self.member_spouse_number.text(), 
            'business_name': self.member_business.text(), 
            'business_address': self.member_business_address.text(),
            'job_name': self.member_job.text(), 
            'job_address': self.member_job_address.text(),
        }

        save_or_update_member_info(data)
        print("✅ Member info saved successfully!")
        self.clear_form()
        QApplication.instance().activeWindow().statusBar().showMessage("✅ सदस्य विवरण सफलतापूर्वक सुरक्षित गरियो", 5000)

       
    def search_member(self):
        keyword = self.search_input.text().strip()

        if not keyword:
            QMessageBox.warning(self, "Empty Input", "Please enter Member ID or Name to Search | कृपया सदस्य नं अथवा सदस्यको नाम प्रविष्ट गर्नुहोस")
            return # Don't proceed if input is empty
        
        result = fetch_member_data(keyword)
        
        if result:
            self.fill_form(result)            
            # Update session
            current_session["member_number"] = result["member_number"]
            current_session["member_name"] = result["member_name"]
        else:
            QMessageBox.warning(self, " Not Found", "No member found with that ID or name")

        # Notify MainWindow to update tab headers
        main_window = self.window()
        if hasattr(main_window, 'refresh_member_header_in_all_tabs'):
            main_window.refresh_member_header_in_all_tabs()

    def fill_form(self, data):

        dob_str = data.get('dob_bs', '2055-01-01')
        year, month, day = map(int, dob_str.split('-'))


        print("🧪 Keys available in data:", data.keys())
        self.member_number.setText(data['member_number'])
        self.member_name.setText(data['member_name']),
        self.member_address.setText(data['address']),
        self.member_address_wardno.setText(data['ward_no']),
        self.member_phone.setText(data['phone']), 
        self.bs_dob.setDate(QDate(year, month, day)),
        self.member_citizenship_no.setText(data['citizenship_no']), 
        self.member_father_name.setText(data['father_name']), 
        self.member_grandfather_name.setText(data['grandfather_name']),
        self.member_spouse.setText(data['spouse_name']), 
        self.member_spouse_number.setText(data.get('spouse_phone', ''))
        self.member_business.setText(data.get('business_name', ''))
        self.member_business_address.setText(data.get('business_address', ''))
        self.member_job.setText(data.get('job_name', ''))
        self.member_job_address.setText(data.get('job_address', ''))

        # current_session['member_number'] = data['member_number']
        # current_session['member_name'] = data['member_name']


    def clear_form(self):
        # Clear form
        self.search_input.clear()
        self.member_number.clear()
        self.member_name.clear()
        self.member_address.clear()
        self.member_address_wardno.clear()
        self.member_phone.clear()
        self.bs_dob.setDate(QDate(2055, 1, 1))
        self.member_citizenship_no.clear()
        self.member_father_name.clear()
        self.member_grandfather_name.clear()
        self.member_spouse.clear()
        self.member_spouse_number.clear()
        self.member_business.clear()
        self.member_business_address.clear()
        self.member_job.clear()
        self.member_job_address.clear()

        # Clear global session
        current_session['member_number'] = ""
        current_session['member_name'] = ""

        signal_bus.session_updated.emit()
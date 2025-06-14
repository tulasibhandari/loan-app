# ui/approval_tab.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QGroupBox, QScrollArea,
    QFormLayout, QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from nepali_datetime import date as nepali_date

from models.database import get_connection
from context import current_session
from services.fetch_full_member_data import fetch_all_member_related_data
from models.user_model import get_all_users, get_user_details

class ApprovalTab(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username

        # --- Scrollable Content ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)

        main_form_layout = QVBoxLayout(content)

        # --- Summary Table ---
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(3)
        self.summary_table.setHorizontalHeaderLabels(['Field', "Value", 'Action'])
        self.summary_table.setRowCount(0)  # Start empty
        self.summary_table.setAlternatingRowColors(True)
        self.summary_table.verticalHeader().setDefaultSectionSize(40)
        self.summary_table.setColumnWidth(0, 220)  # Field column
        self.summary_table.setColumnWidth(1, 300)  # Value column
        self.summary_table.setColumnWidth(2, 120)  # Action (Update Button)

        self.summary_table.setStyleSheet("""
            QTableWidget {
                background-color:#f8f9fa;
                alternate-background-color: #e9ecef;
                gridline-color: #dee2e6;
                font-size: 14px;
            }
                                         
            QHeaderView::section {
                background-color: #343a40;
                color: white;
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ced4da;
            }
                                         
            QTableWidget::item {
                padding: 6px;
            }
                                         
            QPushButton {
                paddind: 4px 10px;
                background-color: #17a2b8
                color: white;
                border-radius: 4px
            }
                                         
            QPushButton::hover {
            background-color: #138496
            }                                         
        """)
        main_form_layout.addWidget(QLabel("📋 Member Data Summary:"))
        main_form_layout.addWidget(self.summary_table)

       

        # --- Approval Section GroupBox ---
        approval_group = QGroupBox("✅ Approval Section")
        approval_layout = QFormLayout()

        self.approval_date = QLineEdit()
        current_bs_date = nepali_date.today().strftime("%Y-%m-%d")
        self.approval_date.setText(current_bs_date)
        approval_layout.addRow("Approval Date (BS):", self.approval_date)

        self.entered_by = QComboBox()
        self.entered_by.setEnabled(False)
        approval_layout.addRow("Entered By:", self.entered_by)

        self.entered_designation = QLineEdit()
        self.entered_designation.setReadOnly(True)
        approval_layout.addRow("Designation:", self.entered_designation)

        self.approved_by = QComboBox()
        approval_layout.addRow("Approved By:", self.approved_by)
        self.approved_by.currentTextChanged.connect(self.update_approver_post)

        self.designation = QLineEdit()
        self.designation.setReadOnly(True)
        approval_layout.addRow("Designation:", self.designation)

        approval_group.setLayout(approval_layout)
        main_form_layout.addWidget(approval_group)

        # --- Navigation Button ---
        self.next_button = QPushButton("Next")
        # self.next_button.clicked.connect(self.go_to_reports_tab)
        main_form_layout.addWidget(self.next_button)

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        self.populate_users()

    
    def populate_users(self):
        user_details = get_user_details(self.username)
        print("Print Current User Info:", user_details)
        if user_details:
            self.entered_by.addItem(user_details['full_name_nepali'])
            self.entered_designation.setText(user_details['post'])
        
        # Populate approver combobox
        self.user_map = {} # map Nepali name - post
        users = get_all_users()
        for user in users:
            name = user['full_name_nepali']
            print (name)
            # self.approved_by.addItem(user['full_name_nepali'])
            self.approved_by.addItem(name)
            # self.user_map[user['username']] = user['post']
            self.user_map[name] = user['post']
        
        self.approved_by.currentTextChanged.connect(self.update_approver_post)

    def update_approver_post(self):
        selected = self.approved_by.currentText()
        post = self.user_map.get(selected, "")
        self.designation.setText(post)            

        # Load Member data from database
        self.load_summary_data()

    def update_field(self, field):
        row_count = self.summary_table.rowCount()
        for row in range(row_count):
            if self.summary_table.item(row, 0).text() == field:
                new_value = self.summary_table.item(row, 1).text()
                self._update_field_in_db(field, new_value)
                QMessageBox.information(self, "Updated", f"{field} updated.")
                break

    def _update_field_in_db(self, field, value):
        member_number = current_session.get("member_number", "")
        if not member_number:
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE member_info SET {field} = ? WHERE member_number = ?", (value, member_number))
        conn.commit()
        conn.close()

    def load_summary_data(self):    
        member_number = current_session.get("member_number", "")
        print(f"🔎 Loading summary for member: {member_number}")  # Add this
        if not member_number:
            print("⚠ No member selected")
            return

        data = fetch_all_member_related_data(member_number)
        if not data:
            print("⚠ No data found for member:", member_number)
            return

        # Map of database field names to user-friendly labels
        field_name_map = {
            "member_info.id": "ID",
            "member_info.member_number": "सदस्य नंः",
            "member_info.member_name": "सदस्यको नामथरः",
            "member_info.address": "ठेगानाः (न.पा./गा.पा.)",
            "member_info.ward_no": "वार्ड नंः",
            "member_info.phone": "फोन नंः",
            "member_info.dob_bs": "जन्ममितिः (वि.सं.)",
            "member_info.citizenship_no": "ना.प्र.नंः",
            "member_info.father_name": "बाबुको नामः",
            "member_info.grandfather_name": "बाजेको नामः",
            "member_info.spouse_name": "पति / पत्नीको नामः",
            "member_info.spouse_phone": "पति / पत्नीको फोन",
            "member_info.business_name": "व्यवसायको नामः",
            "member_info.business_address": "व्यवसायको ठेगानाः",
            "member_info.job_name": "रोजगार / नोकरीः",
            "member_info.job_address": "रोजगार / नोकरीको ठेगानाः",
            "loan_info.loan_type": "ऋणको  किसिमः",
            "loan_info.interest_rate": "हालको व्याजदरः",
            "loan_info.loan_duration": "ऋण अवधि",
            "loan_info.repayment_duration": "सांवा भुक्तानीः",
            "loan_info.loan_amount": "ऋण माग रकमः",
            "loan_info.loan_amount_in_words": "ऋण माग रकमः (अक्षरमा)",
            "loan_info.loan_completion_year": "ऋण सकिने अवधिः (साल)",
            "loan_info.loan_completion_month": "ऋण सकिने अवधिः (महिना)",
            "loan_info.loan_completion_day": "ऋण सकिने अवधिः (गते)",
            "collateral_basic.monthly_saving": "जम्मा मासिक बचतः",
            "collateral_basic.child_saving": "जम्मा बाल बचतः",
            "collateral_basic.total_saving": "जम्मा बचत रकमः",
            "collateral_properties.owner_name": "जग्गा धनीको नामः",
            "collateral_properties.father_or_spouse": "जग्गा धनीको बाबु / पतिको नामः",
            "collateral_properties.grandfather_or_father_inlaw": "जग्गा धनीको बाजे / ससुराको नामः",
            "collateral_properties.district": "जिल्लाः",
            "collateral_properties.municipality_vdc": "नगरपालिका / गाउँपालिकाः",
            "collateral_properties.sheet_no": "सिट नंः",
            "collateral_properties.ward_no": "वार्ड नंः",
            "collateral_properties.plot_no": "कित्ता नंः",
            "collateral_properties.area": "क्षेत्रफलः",
            "collateral_properties.land_type": "जग्गाको किसिमः"
        }

        self.summary_table.setRowCount(0)
        print("🧪 Summary data keys:", list(data.keys()))

        for row_idx, (key, value) in enumerate(data.items()):
            label = field_name_map.get(key, key) 
            self.summary_table.insertRow(row_idx)
            self.summary_table.setItem(row_idx, 0, QTableWidgetItem(str(label)))
            self.summary_table.setItem(row_idx, 1, QTableWidgetItem(str(value)))

            update_button = QPushButton("Update Data")
            update_button.clicked.connect(lambda _, k=key: self.update_field(k))
            self.summary_table.setCellWidget(row_idx, 2, update_button)

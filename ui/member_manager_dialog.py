# ui/member_manager_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QWidget,
    QAbstractScrollArea
)
from PyQt5.QtCore import Qt
from models.member_model import fetch_all_members, delete_member
from ui.personal_info_tab import PersonalInfoTab

PAGE_SIZE = 50  # 🔥 Change this if you want more/less per page

class MemberManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("👥 Member Manager")
        self.resize(1200, 700)
        # self.showMaximized()

        self.current_page = 1
        self.total_pages = 1
        self.filtered_members = []

        self.init_ui()
        self.load_members()

    def init_ui(self):
        layout = QVBoxLayout()

        # 🔍 Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name or Member Number.")
        search_btn = QPushButton("🔍 Search")
        search_btn.clicked.connect(self.search_member)
        clear_btn = QPushButton("❌ Clear")
        clear_btn.clicked.connect(self.clear_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(clear_btn)
        layout.addLayout(search_layout)

        # 📋 Member Table
        self.table = QTableWidget()
        self.table.setColumnCount(19)
        self.table.setHorizontalHeaderLabels([
            "सदस्य नं", "सदस्यको नाम", "फोन", "जन्ममिति (वि.सं.)", "ना.प्र. न.",
            "ठेगाना", "वार्ड नं", "बाबुको नाम", "बाजेको नाम",
            "पति/पत्नीको नाम", "ईमेल", "पेशा", "फेसबुक", "Whatsapp/Viber", "व्यवसाय", "व्यवसाय ठेगाना",
            "रोजगारदाता", "ठेगाना (रोजगारदाता)", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addWidget(self.table)

        # ⏮️ Pagination Controls
        pagination_layout = QHBoxLayout()
        self.prev_btn = QPushButton("⏮️ Previous")
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn = QPushButton("Next ⏭️")
        self.next_btn.clicked.connect(self.next_page)
        self.page_info = QLabel("Page 1 of 1")

        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_info)
        pagination_layout.addWidget(self.next_btn)
        layout.addLayout(pagination_layout)

        self.setLayout(layout)

    def clear_search(self):
        """Clear search input and reload all members"""
        self.search_input.clear()
        self.load_members()

    def search_member(self):
        """Search/filter members based on text"""
        keyword = self.search_input.text().strip().lower()
        all_members = fetch_all_members()
        self.filtered_members = [
            m for m in all_members
            if keyword in m['member_name'].lower() or keyword in m['member_number'].lower()
        ]
        self.current_page = 1
        self.update_pagination()

    def load_members(self):
        """Load all members into memory and setup pagination"""
        self.filtered_members = fetch_all_members()
        self.current_page = 1
        self.update_pagination()

    def update_pagination(self):
        """Update table data and pagination info"""
        total_records = len(self.filtered_members)
        self.total_pages = max(1, (total_records + PAGE_SIZE - 1) // PAGE_SIZE)

        start_index = (self.current_page - 1) * PAGE_SIZE
        end_index = start_index + PAGE_SIZE
        page_members = self.filtered_members[start_index:end_index]

        self.populate_table(page_members)
        self.page_info.setText(f"Page {self.current_page} of {self.total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_pagination()

    def populate_table(self, members):
        """Populate table with member data"""
        self.table.setRowCount(0)
        for row_num, m in enumerate(members):
            self.table.insertRow(row_num)
            
            col_values = [
                m['member_number'], m['member_name'], m['phone'], m['dob_bs'], m['citizenship_no'],
                m['address'], m['ward_no'], m['father_name'], m['grandfather_name'],
                m['spouse_name'], m['spouse_phone'], m['email'], m['profession'],
                m['facebook_detail'], m['whatsapp_detail'], m['business_name'],
                m['business_address'], m['job_name']
            ]

            for col, value in enumerate(col_values):
                item = QTableWidgetItem(value if value else "—")
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_num, col, item)

            # 🛠️ Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 30)
            edit_btn.clicked.connect(lambda _, mem=m: self.edit_member_dialog(mem))
            del_btn = QPushButton("🗑️")
            del_btn.setFixedSize(30, 30)
            del_btn.clicked.connect(lambda _, mem=m: self.delete_member(mem))
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(del_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row_num, 18, action_widget)

    def edit_member_dialog(self, member):
        """Load member details into PersonalInfoTab"""
        info_tab = PersonalInfoTab()
        info_tab.fill_form(member)
        info_tab.exec_()

    def delete_member(self, member):
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete member {member['member_number']} ({member['member_name']})?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_member(member['member_number'])
            QMessageBox.information(self, "Deleted", f"Member {member['member_number']} deleted.")
            self.load_members()

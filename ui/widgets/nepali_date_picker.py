from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLayout, QLabel, QPushButton, QGridLayout, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from nepali_datetime import date as nepali_date

class NepaliDatePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_date = None
        self.setWindowTitle("Select Nepali Date")
        self.current_nep_date = nepali_date.today()
        self.init_ui()
    
    def init_ui(self):
        self.main_layout = QVBoxLayout()

        # Header
        self.header = QLabel()
        self.header.setAlignment(Qt.AlignCenter)
        self.update_header()

        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("<<")
        self.prev_btn.clicked.connect(self.prev_month)
        self.next_btn = QPushButton(">>")
        self.next_btn.clicked.connect(self.next_month)

        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.header)
        nav_layout.addWidget(self.next_btn)

        self.main_layout.addLayout(nav_layout)

        # Calender Grid
        self.grid = QGridLayout()
        self.main_layout.addLayout(self.grid)
        self.create_calendar_grid()

        self.setLayout(self.main_layout)
    
    def create_calendar_grid(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().deleteLater()

        days = ["आइत", "सोम", "मंगल", "बुध", "बिही", "शुक्र", "शनि"]
        for col, day in enumerate(days):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont("Arial", 10))
            self.grid.addWidget(lbl, 0, col)
        
        year = self.current_nep_date.year
        month = self.current_nep_date.month
        start_day = nepali_date(year, month, 1).weekday()
        num_days = nepali_date.days_in_month(year, month)

        row, col = 1, start_day
        for day in range(1, num_days + 1):
            btn = QPushButton(str(day))
            btn.setFixedSize(36,36)
            btn.clicked.connect(lambda _, d=day: self.selected_date(d))
            self.grid.addWidget(btn, row, col)

            col += 1
            if col > 6:
                col = 0
                row += 1
    
    def date_selected(self, day):
        self.selected_date = nepali_date(self.current_nep_date.year, self.current_nep_date.month, day)
        self.accept()
    
    def update_header(self):
        month_names = [
            "बैशाख", "जेठ", "असार", "साउन", "भदौ", "असोज",
            "कार्तिक", "मंसिर", "पुस", "माघ", "फागुन", "चैत"            
        ]
        self.header.setText(f"{month_names[self.current_nep_date.month - 1]} {self.current_nep_date.year}")
        self.header.setFont(QFont("Arial", 14))
    
    def prev_month(self):
        if self.current_nep_date.month == 1:
            self.current_nep_date = nepali_date(self.current_nep_date.year -1, 12, 1)
        else:
            self.current_nep_date = nepali_date(self.current_nep_date.year, self.current_nep_date.month -1, 1)
        self.create_calendar_grid()
        self.update_header()

    def next_month(self):
        if self.current_nep_date.month == 12:
            self.current_nep_date = nepali_date(self.current_nep_date +1, 1, 1)
        else:
            self.current_nep_date = nepali_date(self.current_nep_date.year, self.current_nep_date.month + 1, 1)
            self.create_calendar_grid()
            self.update_header()
        
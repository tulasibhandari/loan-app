from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QGroupBox, QScrollArea,
    QFormLayout, QLineEdit, QComboBox, QPushButton, QTableView,
    QMessageBox, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from nepali_datetime import date as nepali_date
from models.database import get_connection, get_database_path
from context import current_session
from services.fetch_full_member_data import fetch_all_member_related_data
from models.user_model import get_all_users, get_user_details
from models.approval_model import save_approval_info
from utils.converter import convert_to_nepali_digits
from utils.amount_to_words import convert_number_to_nepali_words
from styles.app_styles import AppStyles
from signal_bus import signal_bus
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ApprovalTab(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.selected_member_number = None
        self.selected_loan_id = None
        self.model = None
        self.setup_ui()
        self.populate_users()
        self.load_pending_loans()
        self.setup_timer()
        signal_bus.loan_added.connect(self.on_loan_added)

    def setup_ui(self):
        self.setStyleSheet(AppStyles.get_main_stylesheet())
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)

        self.main_layout = QVBoxLayout(content)
        self.main_layout.setContentsMargins(
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM
        )
        self.main_layout.setSpacing(AppStyles.SPACING_MEDIUM)

        self.main_layout.addWidget(QLabel("📋 बाँकी ऋणहरू:"))
        self.loan_table = QTableView()
        self.loan_table.setSelectionMode(QTableView.SingleSelection)
        self.loan_table.setSelectionBehavior(QTableView.SelectRows)
        self.loan_table.setStyleSheet(f"""
            QTableView {{
                background-color: white;
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 6px;
                gridline-color: {AppStyles.BORDER_COLOR};
            }}
            QTableView::item:selected {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
            }}
        """)
        self.loan_table.setSortingEnabled(True)
        self.main_layout.addWidget(self.loan_table)
    
        approval_group = QGroupBox("✅ स्वीकृति खण्ड")
        approval_group.setStyleSheet(f"""
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
        approval_layout = QFormLayout()
        approval_layout.setVerticalSpacing(AppStyles.SPACING_SMALL)
        approval_layout.setHorizontalSpacing(AppStyles.SPACING_MEDIUM)

        self.approval_date = QLineEdit()
        self.approval_date.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        current_bs_date = nepali_date.today().strftime("%Y-%m-%d")
        self.approval_date.setText(current_bs_date)
        approval_layout.addRow("स्वीकृत मिति (BS):", self.approval_date)
        
        self.approved_loan_amount = QLineEdit()
        self.approved_loan_amount.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.approved_loan_amount.textChanged.connect(self.update_approved_loan_amount_in_words)
        approval_layout.addRow("स्वीकृत ऋण रकम (रू.):", self.approved_loan_amount)

        self.approved_loan_amount_words = QLineEdit()
        self.approved_loan_amount_words.setReadOnly(True)
        self.approved_loan_amount_words.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        approval_layout.addRow("ऋण रकम (अक्षरमा):", self.approved_loan_amount_words)

        self.entered_by = QComboBox()
        self.entered_by.setEnabled(False)
        self.entered_by.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        approval_layout.addRow("प्रविष्ट गर्ने:", self.entered_by)

        self.entered_designation = QLineEdit()
        self.entered_designation.setReadOnly(True)
        self.entered_designation.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        approval_layout.addRow("पद:", self.entered_designation)

        self.approved_by = QComboBox()
        self.approved_by.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        approval_layout.addRow("स्वीकृत गर्ने:", self.approved_by)
        self.approved_by.currentTextChanged.connect(self.update_approver_post)

        self.designation = QLineEdit()
        self.designation.setReadOnly(True)
        self.designation.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        approval_layout.addRow("पद:", self.designation)

        approval_group.setLayout(approval_layout)
        self.main_layout.addWidget(approval_group)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(AppStyles.SPACING_MEDIUM)

        self.refresh_button = QPushButton("रिफ्रेश")
        self.refresh_button.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        self.refresh_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: {AppStyles.FONT_NORMAL};
                font-weight: bold;
                min-height: {AppStyles.BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: #375a7f;
            }}
            QPushButton:pressed {{
                background-color: #2e4a66;
            }}
        """)
        self.refresh_button.clicked.connect(self.load_pending_loans)
        button_layout.addWidget(self.refresh_button)

        self.save_button = QPushButton("स्वीकृति जानकारी सुरक्षित गर्नुहोस्")
        self.save_button.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.SUCCESS_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: {AppStyles.FONT_NORMAL};
                font-weight: bold;
                min-height: {AppStyles.BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: #17a673;
            }}
            QPushButton:pressed {{
                background-color: #138f64;
            }}
        """)
        self.save_button.clicked.connect(self.save_approval_info)
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()

        self.main_layout.addLayout(button_layout)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(scroll)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_pending_loans)
        self.timer.start(5000)

    def on_loan_added(self):
        logging.debug("Received loan_added signal")
        self.load_pending_loans()

    def load_pending_loans(self):
        for i in range(self.main_layout.count()):
            widget = self.main_layout.itemAt(i).widget()
            if isinstance(widget, QLabel) and widget.text().startswith("कुनै बाँकी ऋणहरू"):
                self.main_layout.removeWidget(widget)
                widget.deleteLater()

        db = QSqlDatabase.addDatabase("QSQLITE", "approval_tab_conn")
        db.setDatabaseName(get_database_path())
        logging.debug(f"Database path: {get_database_path()}")
        if not db.open():
            QApplication.instance().activeWindow().statusBar().showMessage("त्रुटि: डाटाबेसमा जडान गर्न असफल", 3000)
            logging.error("Failed to connect to database")
            return

        self.model = QSqlTableModel(self, db)
        query = QSqlQuery(db)
        query_str = """
            SELECT l.id, l.member_number, m.member_name, l.loan_type, l.loan_amount, l.loan_amount_in_words, l.status
            FROM loan_info l
            LEFT JOIN member_info m ON l.member_number = m.member_number
            WHERE l.status = 'pending'
        """
        logging.debug(f"Executing query: {query_str}")
        if not query.exec_(query_str):
            QApplication.instance().activeWindow().statusBar().showMessage(f"त्रुटि: क्वेरी असफल: {query.lastError().text()}", 3000)
            logging.error(f"Query failed: {query.lastError().text()}")
            db.close()
            return

        self.model.setQuery(query)
        headers = ["ID", "सदस्य नं", "सदस्यको नाम", "ऋणको प्रकार", "ऋण रकम", "ऋण रकम (शब्दमा)", "स्थिति"]
        for col, header in enumerate(headers):
            self.model.setHeaderData(col, Qt.Horizontal, header)
        
        self.loan_table.setModel(self.model)
        self.loan_table.hideColumn(0)
        self.loan_table.resizeColumnsToContents()
        self.loan_table.selectionModel().selectionChanged.connect(self.on_row_selected)

        logging.debug(f"Rows fetched: {self.model.rowCount()}")
        db.close()

    def on_row_selected(self):
        selected = self.loan_table.selectionModel().selectedRows()
        if not selected:
            self.clear_form()
            return
        
        row = selected[0].row()
        self.selected_loan_id = self.model.data(self.model.index(row, 0))
        self.selected_member_number = self.model.data(self.model.index(row, 1))
        loan_amount = self.model.data(self.model.index(row, 4))
        self.approved_loan_amount.setText(loan_amount)
        current_bs_date = nepali_date.today().strftime("%Y-%m-%d")
        self.approval_date.setText(current_bs_date)
        self.update_approved_loan_amount_in_words()

    def clear_form(self):
        self.selected_member_number = None
        self.selected_loan_id = None
        self.approval_date.setText(nepali_date.today().strftime("%Y-%m-%d"))
        self.approved_loan_amount.clear()
        self.approved_loan_amount_words.clear()

    def update_approved_loan_amount_in_words(self):
        try:
            amount = self.approved_loan_amount.text().strip()
            if not amount:
                self.approved_loan_amount_words.setText("")
                return
            amount_int = int(amount.replace(",", ""))
            nepali_digits = convert_to_nepali_digits(amount_int)
            nepali_words = convert_number_to_nepali_words(amount_int)
            self.approved_loan_amount.setText(nepali_digits)
            self.approved_loan_amount_words.setText(nepali_words)
        except ValueError:
            self.approved_loan_amount_words.setText("अमान्य रकम!")

    def populate_users(self):
        user_details = get_user_details(self.username)
        if user_details:
            self.entered_by.addItem(user_details['full_name_nepali'])
            self.entered_designation.setText(user_details['post'])
        
        self.user_map = {}
        users = get_all_users()
        for user in users:
            name = user['full_name_nepali']
            self.approved_by.addItem(name)
            self.user_map[name] = user['post']

    def update_approver_post(self):
        selected = self.approved_by.currentText()
        post = self.user_map.get(selected, "")
        self.designation.setText(post)
        current_session["entered_by"] = self.entered_by.currentText()
        current_session["entered_by_post"] = self.entered_designation.text()
        current_session["approved_by"] = self.approved_by.currentText()
        current_session["approved_by_post"] = post

    def save_approval_info(self):
        if not self.selected_member_number or not self.selected_loan_id:
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.warning(self, "डाटा हराइरहेको", "कृपया तालिकाबाट ऋण छान्नुहोस्।")
            return
        try:
            # Validate amount
            amount_raw = self.approved_loan_amount.text().strip()
            if not amount_raw or not amount_raw.replace(",", "").isdigit():
                msg = QMessageBox()
                msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
                msg.warning(self, "अमान्य रकम", "कृपया मान्य संख्यात्मक रकम प्रविष्ट गर्नुहोस्।")
                return

            # Get loan_type for the selected loan
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT loan_type FROM loan_info
                WHERE id = ? AND member_number = ? AND status = 'pending'
            """, (self.selected_loan_id, self.selected_member_number))
            result = cursor.fetchone()
            if not result:
                conn.close()
                raise ValueError("चयन गरिएको ऋण फेला परेन वा पहिले नै स्वीकृत/रद्द गरिएको छ।")
            loan_type = result[0].strip()
            logging.debug(f"Saving approval for loan_id {self.selected_loan_id}, member_number {self.selected_member_number}, type: '{loan_type}'")

            # Proceed with approval (validation removed)
            approved_nep = convert_to_nepali_digits(amount_raw)
            approved_words = convert_number_to_nepali_words(int(amount_raw.replace(",", "")))

            data = {
                "member_number": self.selected_member_number,
                "approval_date": self.approval_date.text().strip(),
                "entered_by": self.entered_by.currentText(),
                "entered_designation": self.entered_designation.text(),
                "approved_by": self.approved_by.currentText(),
                "approved_designation": self.designation.text(),
                "approved_loan_amount": approved_nep,
                "approved_loan_amount_words": approved_words
            }

            logging.debug(f"Saving approval data: {data}")
            save_approval_info(data)
            cursor.execute("""
                UPDATE loan_info
                SET status = 'approved'
                WHERE id = ? AND member_number = ? AND status = 'pending'
            """, (self.selected_loan_id, self.selected_member_number))
            conn.commit()
            conn.close()

            current_session["approved_loan_amount"] = approved_nep
            current_session["approved_loan_amount_words"] = approved_words

            self.load_pending_loans()
            self.clear_form()

            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.information(self, "✅ सुरक्षित", "स्वीकृति जानकारी सुरक्षित भयो र ऋण स्थिति अद्यावधिक गरियो।")
        except ValueError as e:
            conn.close()
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.warning(self, "प्रतिबन्धित", str(e))
            logging.warning(f"Approval failed: {e}")
        except Exception as e:
            conn.close()
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.critical(self, "ERROR", f"स्वीकृति सुरक्षित गर्न असफल: {str(e)}")
            logging.error(f"Unexpected error during approval: {e}")

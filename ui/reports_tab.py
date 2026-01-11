from PyQt5.QtWidgets import (
    QWidget, QLabel, QCheckBox, QVBoxLayout, QHBoxLayout, QFormLayout,
    QScrollArea, QPushButton, QFileDialog, QFrame, QComboBox, QGroupBox,
    QApplication, QRadioButton, QMessageBox, QCompleter
)
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QFont
import os
from docxtpl import DocxTemplate
from nepali_datetime import date as nepali_date
from os.path import abspath
from models.loan_scheme_model import fetch_all_loan_schemes
from models.report_tracking_model import save_report_log
from models.loan_model import fetch_loan_info_members
from context import current_session
from services.prepare_report_contexts import prepare_report_context
from styles.app_styles import AppStyles
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ReportsTab(QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.template_path = None
        self.tamasuk_template_path = None
        self.loan_approval_template_path = None
        self.authority_template_path = None
        self.manjurinaama_template_path = None  # New for मञ्जुरीनामा
        self.guarantor_template_path = None     # New for व्यक्तिगत जमानी
        self.approved_members = []  # Store approved members for completer
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(AppStyles.get_main_stylesheet())
        main_layout = QVBoxLayout()
        main_layout.setSpacing(AppStyles.SPACING_MEDIUM)
        main_layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                       AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(AppStyles.SPACING_MEDIUM)
        content_layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                         AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)

        # Header Section (with member dropdown)
        header_frame = self.create_header_section()
        content_layout.addWidget(header_frame)

        # Loan Configuration Section
        loan_config_group = self.create_loan_config_section()
        content_layout.addWidget(loan_config_group)

        # Template Selection Section
        template_group = self.create_template_section()
        content_layout.addWidget(template_group)

        # Additional Documents Section
        additional_docs_group = self.create_additional_docs_section()
        content_layout.addWidget(additional_docs_group)

        # Action Buttons Section
        action_frame = self.create_action_section()
        content_layout.addWidget(action_frame)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        # Ensure btn_generate_report is initialized before validation
        if hasattr(self, 'btn_generate_report'):
            self.validate_inputs()
        # Update session label after all widgets are created
        self.update_session_label()
        # Populate approved members for completer
        self.populate_approved_members()

    def create_header_section(self):
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppStyles.INFO_COLOR};
                border-radius: 8px;
                padding: {AppStyles.PADDING_MEDIUM}px;
            }}
            QLabel {{
                color: white;
                font-size: {AppStyles.FONT_MEDIUM};
            }}
        """)
        layout = QVBoxLayout(header_frame)
        layout.setSpacing(AppStyles.SPACING_SMALL)

        title_label = QLabel("Report Generation Center")
        title_label.setAlignment(Qt.AlignCenter)
        try:
            font_size = int(AppStyles.FONT_LARGE.replace("px", "")) if isinstance(AppStyles.FONT_LARGE, str) else AppStyles.FONT_LARGE
        except ValueError:
            font_size = 16
            logging.error(f"Invalid AppStyles.FONT_LARGE: {AppStyles.FONT_LARGE}, using default 16")
        title_label.setFont(QFont("Arial", font_size, QFont.Bold))

        self.session_label = QLabel("No member selected for report generation")
        self.session_label.setAlignment(Qt.AlignCenter)
        self.session_label.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL}; background-color: rgba(255, 255, 255, 0.1); padding: 5px; border-radius: 4px;")
        self.session_label.setToolTip("Select a member from the dropdown below to generate reports")

        # Member Selection Dropdown with QCompleter
        self.member_dropdown = QComboBox()
        self.member_dropdown.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.member_dropdown.setEditable(True)  # Enable search/filter
        self.member_dropdown.lineEdit().setPlaceholderText("Search by member number")
        # Use a font that supports Nepali script
        self.member_dropdown.setFont(QFont("Noto Sans Devanagari", 16))  # Install Noto Sans Devanagari if needed
        self.member_dropdown.setStyleSheet(f"""
            QComboBox {{
                font-weight: bold;
                background-color: #f0f4f8;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: url(icons/down-arrow.png);
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #f0f4f8;
                selection-background-color: #3498db;
                color: #2c3e50;
                font: 16px "Noto Sans Devanagari";
            }}
        """)
        self.member_dropdown.setToolTip("Search or select an approved member by member number")
        self.member_dropdown.addItem("Select Member")
        self.member_dropdown.currentIndexChanged.connect(self.on_member_selected_dropdown)

        layout.addWidget(title_label)
        layout.addWidget(self.session_label)
        layout.addWidget(self.member_dropdown)
        return header_frame

    # def populate_approved_members(self):
    #     try:
    #         members = fetch_loan_info_members()
    #         logging.debug(f"Raw members data from fetch_loan_info_members: {members}")
    #         if not members:
    #             logging.warning("No members data returned from fetch_loan_info_members")
    #             self.show_status_message("No member data available")
    #             return

    #         self.approved_members = []
    #         for m in members:
    #             if len(m) > 3:
    #                 member_number, member_name, loan_type, loan_status = m[0], m[1], m[2], m[3]
    #                 if loan_status and loan_status.lower() == 'approved':
    #                     display_text = f"{member_number} - {member_name or 'N/A'} ({loan_type or 'N/A'})"
    #                     self.approved_members.append(display_text)
    #                     logging.debug(f"Added to completer: {display_text}")

    #         # Set up QCompleter
    #         completer = QCompleter(self.approved_members, self)
    #         completer.setCaseSensitivity(Qt.CaseInsensitive)
    #         completer.setFilterMode(Qt.MatchContains)  # Match anywhere in the string
    #         self.member_dropdown.setCompleter(completer)
    #         logging.debug(f"Populated completer with {len(self.approved_members)} approved members")
    #     except Exception as e:
    #         logging.error(f"Error populating approved members for completer: {e}")
    #         self.show_status_message("Failed to load approved member suggestions")

    # Updated populate_approved_members
    def populate_approved_members(self):
        try:
            members = fetch_loan_info_members()
            logging.debug(f"Raw members data from fetch_loan_info_members: {members}")
            if not members:
                logging.warning("No members data returned from fetch_loan_info_members")
                self.show_status_message("No member data available")
                return

            self.approved_members = []
            self.member_dropdown.clear()  # Clear existing items
            self.member_dropdown.addItem("Select Member")  # First item with no data
            
            for m in members:
                if len(m) > 3:
                    member_number, member_name, loan_type, loan_status = m[0], m[1], m[2], m[3]
                    if loan_status and loan_status.lower() == 'approved':
                        display_text = f"{member_number} - {member_name or 'N/A'} ({loan_type or 'N/A'})"
                        self.approved_members.append(display_text)
                        # **ADD THIS LINE** - Set the member_number as itemData
                        self.member_dropdown.addItem(display_text, member_number)
                        logging.debug(f"Added to dropdown: {display_text} with data: {member_number}")

            # Set up QCompleter
            completer = QCompleter(self.approved_members, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            self.member_dropdown.setCompleter(completer)
            logging.debug(f"Populated dropdown with {len(self.approved_members)} approved members")
        except Exception as e:
            logging.error(f"Error populating approved members: {e}")
            self.show_status_message("Failed to load approved member suggestions")


    def on_member_selected_dropdown(self, index):
        if index > 0:
            member_number = self.member_dropdown.itemData(index)
            display_text = self.member_dropdown.currentText()
            # Handle selection from completer or manual entry
            try:
                if display_text in self.approved_members:
                    parts = display_text.split(" - ")
                    if len(parts) > 1:
                        member_name = parts[1].split(" (")[0].strip()
                    else:
                        member_name = "Unknown"
                else:
                    # Fallback for partial matches or manual entry
                    for item in self.approved_members:
                        if item.startswith(display_text.split(" - ")[0]):
                            member_name = item.split(" - ")[1].split(" (")[0].strip()
                            break
                    else:
                        member_name = "Unknown"
            except (IndexError, ValueError, AttributeError):
                logging.warning(f"Invalid display text format: {display_text}, falling back to default")
                member_name = "Unknown"

            # ✅ ADD THIS - Ensure consistent padding
            raw_member_number = member_number if member_number else display_text.split(" - ")[0].strip()
            current_session["member_number"] = str(raw_member_number).strip().zfill(9)
            current_session["member_name"] = member_name
            logging.debug(f"Selected member: {current_session.get('member_number')} - {member_name}")
            self.update_session_label()
        else:
            current_session.pop("member_number", None)
            current_session.pop("member_name", None)
            self.update_session_label()

    def create_loan_config_section(self):
        group = QGroupBox("Loan Configuration")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {AppStyles.FONT_MEDIUM};
                font-weight: bold;
                color: {AppStyles.PRIMARY_COLOR};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 6px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        layout = QFormLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                 AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)

        loan_type_label = QLabel("Loan Type:")
        loan_type_label.setStyleSheet(f"font-weight: bold; color: {AppStyles.TEXT_PRIMARY};")
        self.loan_type_input = QComboBox()
        self.loan_type_input.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.loan_type_input.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL}; padding: 5px;")
        self.loan_type_input.setToolTip("Select the type of loan for the report")
        self.loan_type_input.addItem("Select Loan Type")
        loan_schemes = fetch_all_loan_schemes()
        loan_types = [scheme[0] for scheme in loan_schemes]
        self.loan_type_input.addItems(loan_types)
        self.loan_type_input.currentTextChanged.connect(self.validate_inputs)

        layout.addRow(loan_type_label, self.loan_type_input)
        group.setLayout(layout)
        return group

    def create_template_section(self):
        group = QGroupBox("Primary Template Selection")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {AppStyles.FONT_MEDIUM};
                font-weight: bold;
                color: {AppStyles.SUCCESS_COLOR};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 6px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        layout = QHBoxLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)

        self.template_label = QLabel("No template selected")
        self.template_label.setStyleSheet(f"""
            font-size: {AppStyles.FONT_NORMAL};
            color: {AppStyles.TEXT_PRIMARY};
            padding: {AppStyles.PADDING_SMALL}px;
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 4px;
        """)
        self.template_label.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.template_label.setToolTip("Selected loan application template")

        self.loan_template_button = QPushButton("Choose Template")
        self.loan_template_button.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.loan_template_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.INFO_COLOR};
                color: white;
                font-size: {AppStyles.FONT_NORMAL};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #2c9faf;
            }}
        """)
        self.loan_template_button.clicked.connect(self.choose_loan_template)
        self.loan_template_button.setToolTip("Select a Word document template for the loan application")

        layout.addWidget(self.template_label, 1)
        layout.addWidget(self.loan_template_button, 1)
        group.setLayout(layout)
        return group

    def create_additional_docs_section(self):
        group = QGroupBox("Additional Documents")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {AppStyles.FONT_MEDIUM};
                font-weight: bold;
                color: {AppStyles.PRIMARY_COLOR};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 6px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        layout = QFormLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                 AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)

        self.radio_select_all = QRadioButton("Select All Documents")
        self.radio_select_all.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL}; color: {AppStyles.PRIMARY_COLOR};")
        self.radio_select_all.toggled.connect(self.toggle_all_documents)
        layout.addRow(self.radio_select_all)

        documents = [
            ("Tamasuk | तमासुक", "checkbox_tamasuk", "tamasuk_template_button", self.select_tamasuk_template),
            ("Loan Approval | ऋण स्वीकृत", "checkbox_loan_approval", "btn_loan_approval_template", self.choose_loan_approval_template),
            ("Debit Authority | खाता अख्तियारी", "checkbox_debit_authority", "btn_debit_authority", self.choose_debit_authority_template),
            (" Consent | मञ्जुरीनामा", "checkbox_manjurinaama", "btn_manjurinaama_template", self.choose_manjurinaama_template),  # New
            ("Personal Gurantee | व्यक्तिगत जमानी", "checkbox_guarantor", "btn_guarantor_template", self.choose_guarantor_template)       # New
        ]

        for doc_name, checkbox_attr, button_attr, handler in documents:
            checkbox = QCheckBox(doc_name)
            checkbox.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL};")
            checkbox.setToolTip(f"Generate {doc_name} document")
            setattr(self, checkbox_attr, checkbox)

            button = QPushButton("Choose Template")
            button.setMinimumHeight(AppStyles.INPUT_HEIGHT)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppStyles.INFO_COLOR};
                    color: white;
                    font-size: {AppStyles.FONT_NORMAL};
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: #2c9faf;
                }}
            """)
            button.clicked.connect(handler)
            button.setToolTip(f"Select a Word document template for {doc_name}")
            setattr(self, button_attr, button)

            button_row = QHBoxLayout()
            button_row.addWidget(button)
            button_row.addStretch()
            layout.addRow(checkbox, button_row)

        group.setLayout(layout)
        return group

    def create_action_section(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppStyles.CARD_BACKGROUND};
                border: 1px solid {AppStyles.SUCCESS_COLOR};
                border-radius: 6px;
                padding: {AppStyles.PADDING_MEDIUM}px;
            }}
        """)
        layout = QHBoxLayout(frame)
        layout.setSpacing(AppStyles.SPACING_MEDIUM)

        self.btn_generate_report = QPushButton("Generate Reports")
        self.btn_generate_report.setMinimumHeight(AppStyles.INPUT_HEIGHT + 10)
        self.btn_generate_report.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.SUCCESS_COLOR};
                color: white;
                font-size: {AppStyles.FONT_MEDIUM};
                font-weight: bold;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #17a673;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)
        self.btn_generate_report.clicked.connect(self.generate_report)
        self.btn_generate_report.setToolTip("Generate selected reports")
        self.btn_generate_report.setEnabled(False)

        clear_button = QPushButton("Clear Selection")
        clear_button.setMinimumHeight(AppStyles.INPUT_HEIGHT + 10)
        clear_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.DANGER_COLOR};
                color: white;
                font-size: {AppStyles.FONT_MEDIUM};
                font-weight: bold;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
        """)
        clear_button.clicked.connect(self.clear_selection)
        clear_button.setToolTip("Clear all template and document selections")

        layout.addStretch()
        layout.addWidget(self.btn_generate_report)
        layout.addWidget(clear_button)
        layout.addStretch()
        return frame

    def update_session_label(self):
        member = current_session.get("member_number", "")
        name = current_session.get("member_name", "")
        if member and name:
            self.session_label.setText(f"Preparing report for: {member} - {name}")
            self.session_label.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL}; background-color: rgba(0, 128, 0, 0.2); padding: 5px; border-radius: 4px;")
        else:
            self.session_label.setText("No member selected for report generation")
            self.session_label.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL}; background-color: rgba(255, 0, 0, 0.2); padding: 5px; border-radius: 4px;")
        self.validate_inputs()

    def choose_loan_template(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Loan Application Template", "", "Word Documents (*.docx)")
        if path:
            self.template_path = path
            filename = os.path.basename(path)
            self.template_label.setText(filename)
            self.template_label.setStyleSheet(f"""
                font-size: {AppStyles.FONT_NORMAL};
                color: white;
                background-color: {AppStyles.SUCCESS_COLOR};
                padding: {AppStyles.PADDING_SMALL}px;
                border-radius: 4px;
            """)
            self.validate_inputs()

    def select_tamasuk_template(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Tamasuk Template", "", "Word Documents (*.docx)")
        if path:
            self.tamasuk_template_path = path
            filename = os.path.basename(path)
            self.tamasuk_template_button.setText(filename)
            self.validate_inputs()

    def choose_loan_approval_template(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Loan Approval Template", "", "Word Documents (*.docx)")
        if path:
            self.loan_approval_template_path = path
            filename = os.path.basename(path)
            self.btn_loan_approval_template.setText(filename)
            self.validate_inputs()

    def choose_debit_authority_template(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Debit Authority Template", "", "Word Documents (*.docx)")
        if path:
            self.authority_template_path = path
            filename = os.path.basename(path)
            self.btn_debit_authority.setText(filename)
            self.validate_inputs()

    def choose_manjurinaama_template(self):  # New
        path, _ = QFileDialog.getOpenFileName(self, "Select मञ्जुरीनामा Template", "", "Word Documents (*.docx)")
        if path:
            self.manjurinaama_template_path = path
            filename = os.path.basename(path)
            self.btn_manjurinaama_template.setText(filename)
            self.validate_inputs()

    def choose_guarantor_template(self):     # New
        path, _ = QFileDialog.getOpenFileName(self, "Select व्यक्तिगत जमानी Template", "", "Word Documents (*.docx)")
        if path:
            self.guarantor_template_path = path
            filename = os.path.basename(path)
            self.btn_guarantor_template.setText(filename)
            self.validate_inputs()

    def toggle_all_documents(self, checked):
        self.checkbox_tamasuk.setChecked(checked)
        self.checkbox_loan_approval.setChecked(checked)
        self.checkbox_debit_authority.setChecked(checked)
        self.checkbox_manjurinaama.setChecked(checked)    # New
        self.checkbox_guarantor.setChecked(checked)       # New

    def clear_selection(self):
        self.member_dropdown.setCurrentIndex(0)
        current_session.pop("member_number", None)
        current_session.pop("member_name", None)
        self.loan_type_input.setCurrentIndex(0)
        self.template_path = None
        self.template_label.setText("Select Member")
        self.template_label.setStyleSheet(f"""
            font-size: {AppStyles.FONT_NORMAL};
            color: {AppStyles.TEXT_PRIMARY};
            padding: {AppStyles.PADDING_SMALL}px;
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 4px;
        """)
        self.tamasuk_template_path = None
        self.tamasuk_template_button.setText("Choose Template")
        self.loan_approval_template_path = None
        self.btn_loan_approval_template.setText("Choose Template")
        self.authority_template_path = None
        self.btn_debit_authority.setText("Choose Template")
        self.manjurinaama_template_path = None             # New
        self.btn_manjurinaama_template.setText("Choose Template")  # New
        self.guarantor_template_path = None                # New
        self.btn_guarantor_template.setText("Choose Template")     # New
        self.checkbox_tamasuk.setChecked(False)
        self.checkbox_loan_approval.setChecked(False)
        self.checkbox_debit_authority.setChecked(False)
        self.checkbox_manjurinaama.setChecked(False)       # New
        self.checkbox_guarantor.setChecked(False)          # New
        self.radio_select_all.setChecked(False)
        self.show_status_message("All selections cleared")
        self.update_session_label()

    def validate_inputs(self):
        is_valid = False
        try:
            is_valid = (
                bool(self.template_path) and
                hasattr(self, 'loan_type_input') and
                self.loan_type_input.currentText() != "Select Loan Type" and
                bool(current_session.get("member_number")) and
                bool(current_session.get("entered_by")) and
                bool(current_session.get("approved_by"))
            )
        except AttributeError as e:
            logging.error(f"Error in validate_inputs: {e}")
            is_valid = False
        if hasattr(self, 'btn_generate_report'):
            self.btn_generate_report.setEnabled(is_valid)
        else:
            logging.warning("btn_generate_report not initialized in validate_inputs")

    def generate_report(self):
        logging.debug(f"Selected member_number: {current_session.get('member_number')}")
        entered_by_name = current_session.get("entered_by", "")
        entered_by_post = current_session.get("entered_by_post", "")
        approved_by_name = current_session.get("approved_by", "")
        approved_by_post = current_session.get("approved_by_post", "")
        member_number = current_session.get("member_number")
        loan_type = self.loan_type_input.currentText().strip()
        nepali_today = nepali_date.today()
        nepali_date_str = nepali_today.strftime('%Y%m%d')

        logging.debug(f"About to call prepare_report_context with member_number: {member_number}")

        # Prepare base context
        data = prepare_report_context(
            member_number, entered_by_name, entered_by_post, approved_by_name, approved_by_post
        )
        if not data:
            self.show_status_message("No data found for the selected member")
            return

        # Generate Primary Report
        try:
            tpl = DocxTemplate(self.template_path)
            tpl.render(data)
            base_dir = 'generated reports'
            loan_type_folder = os.path.join(base_dir, loan_type)
            os.makedirs(loan_type_folder, exist_ok=True)
            filename = f"{loan_type}_{member_number}_{nepali_date_str}.docx"
            output_path = os.path.join(loan_type_folder, filename)
            absolute_output_path = abspath(output_path)
            tpl.save(absolute_output_path)
            save_report_log({
                "member_number": member_number,
                "report_type": "Loan Application",
                "generated_by": self.username,
                "file_path": absolute_output_path,
                "date": nepali_date.today().strftime('%Y-%m-%d')
            })
            self.show_status_message(f"Loan Application saved to: {output_path}")
        except Exception as e:
            self.show_status_message(f"Failed to generate Loan Application: {e}")
            logging.error(f"Error generating Loan Application: {e}")
            return

        # Generate Additional Documents
        extra_docs = [
            ("Tamasuk", self.checkbox_tamasuk, self.tamasuk_template_path, prepare_report_context),
            ("Loan Approval", self.checkbox_loan_approval, self.loan_approval_template_path, prepare_report_context),
            ("Debit Authority", self.checkbox_debit_authority, self.authority_template_path, prepare_report_context),
            ("मञ्जुरीनामा", self.checkbox_manjurinaama, self.manjurinaama_template_path, prepare_report_context),
            ("व्यक्तिगत जमानी", self.checkbox_guarantor, self.guarantor_template_path, prepare_report_context)
        ]
        for doc_name, checkbox, template_path, context_func in extra_docs:
            if checkbox.isChecked() and template_path:
                try:
                    data = context_func(member_number) if context_func != prepare_report_context else context_func(
                        member_number, entered_by_name, entered_by_post, approved_by_name, approved_by_post
                    )
                    if not data:
                        self.show_status_message(f"No data found for {doc_name}")
                        continue
                    tpl = DocxTemplate(template_path)
                    tpl.render(data)
                    folder_path = os.path.join("generated reports", doc_name)
                    os.makedirs(folder_path, exist_ok=True)
                    filename = f"{doc_name}_{member_number}_{nepali_date_str}.docx"
                    output_path = os.path.join(folder_path, filename)
                    tpl.save(output_path)
                    save_report_log({
                        "member_number": member_number,
                        "report_type": doc_name,
                        "generated_by": self.username,
                        "file_path": output_path,
                        "date": nepali_date.today().strftime('%Y-%m-%d')
                    })
                    self.show_status_message(f"{doc_name} saved to: {output_path}")
                except Exception as e:
                    self.show_status_message(f"Failed to generate {doc_name}: {e}")
                    logging.error(f"Error generating {doc_name}: {e}")

    def show_status_message(self, message):
        window = QApplication.instance().activeWindow()
        logging.debug(f"Active window: {window}")
        if window and hasattr(window, 'statusBar') and window.statusBar():
            status_bar = window.statusBar()
            status_bar.showMessage(message, 5000)
            logging.debug(f"Status bar message set: {message}")
        else:
            logging.warning(f"Status bar unavailable for window {window}, showing QMessageBox: {message}")
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Report Status")
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()  # Modal dialog to ensure visibility
            logging.debug(f"QMessageBox displayed: {message}")
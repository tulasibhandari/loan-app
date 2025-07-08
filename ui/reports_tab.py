# ui/reports_tab.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QCheckBox, QVBoxLayout, QHBoxLayout, QFormLayout,
    QScrollArea, QPushButton, QFileDialog, QMessageBox, QFrame,
    QComboBox, QGroupBox, QRadioButton, QApplication, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os
from docxtpl import DocxTemplate
from nepali_datetime import date as nepali_date
from os.path import abspath

from models.loan_scheme_model import fetch_all_loan_schemes
from models.report_tracking_model import save_report_log
from context import current_session, clear_session
from services.prepare_report_contexts import prepare_report_context

from styles.app_styles import AppStyles

class ReportsTab(QWidget):
    def __init__(self, username=None):

        super().__init__()
        self.username = username

        # Initialize Template path
        self.template_path = None
        self.tamasuk_template_path = None
        self.loan_approval_template_path = None
        self.authority_template_path = None

        self.setup_ui()
     
    def setup_ui(self):
        self.setStyleSheet(AppStyles.get_main_stylesheet())

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(AppStyles.SPACING_MEDIUM)
        main_layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                       AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)
              
        # Create Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Content Widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(AppStyles.SPACING_LARGE)
        content_layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                          AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)
        
        # Header section
        header_frame = self.create_header_section()
        content_layout.addWidget(header_frame)

        # Loan configuration section
        loan_config_group = self.create_loan_config_section()
        content_layout.addWidget(loan_config_group)

        # Main Template Section
        main_template_group = self.create_main_template_section()
        content_layout.addWidget(main_template_group)

        # Additional Documents section
        additional_docs_group = self.create_additional_docs_section()
        content_layout.addWidget(additional_docs_group)
        
        # Action buttons section
        action_frame = self.create_action_section()
        content_layout.addWidget(action_frame)
        
        # Add stretch to push everything to top
        content_layout.addStretch()

        # Set scroll widget
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def create_header_section(self):
        """ Create header section with session info """
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color:{AppStyles.INFO_COLOR};
                border-radius: 8px;
                padding: {AppStyles.PADDING_MEDIUM}px;
            }}
            QLabel {{
                color: white;
                font-weight: bold;
                font-style: {AppStyles.FONT_MEDIUM};
            }}
        """)

        layout = QVBoxLayout(header_frame)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                  AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,)
        
        title_label = QLabel("📋 Report Generation Center")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size:{AppStyles.FONT_LARGE}; font-weight:bold;")

        self.session_label = QLabel("⚠ No member selected for report generation")
        self.session_label.setAlignment(Qt.AlignCenter)
        self.session_label.setStyleSheet(f"font-size:{AppStyles.FONT_NORMAL};")

        layout.addWidget(title_label)
        layout.addWidget(self.session_label)
        
        # Update Session info
        self.update_session_label()

        return header_frame
      
    def create_loan_config_section(self):
        """ Create loan configuration section """
        group = QGroupBox("🏦 Loan Configuration")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size:{AppStyles.FONT_MEDIUM};
                font-weight:bold;
                color: {AppStyles.PRIMARY_COLOR};
                border: 2px solid {AppStyles.BORDER_COLOR};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-orgin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: {AppStyles.BACKGROUND_COLOR}
            }}
        """)

        layout = QFormLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                  AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)

        # --- Loan Type Selection ---
        loan_type_label = QLabel("Loan Type:")
        loan_type_label.setStyleSheet(f"font-weight: bold; color: {AppStyles.TEXT_PRIMARY};")

        self.loan_type_input = QComboBox()
        self.loan_type_input.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.loan_type_input.setStyleSheet(f"font-size: {AppStyles.FONT_NORMAL};")

        # Populate loan types from database
        loan_schemes = fetch_all_loan_schemes()  # Returns list of (loan_type, interest_rate)
        loan_types = [scheme[0] for scheme in loan_schemes]
        self.loan_type_input.addItems(loan_types)
        
        layout.addRow(loan_type_label, self.loan_type_input)
        group.setLayout(layout)

        return group
        
    def create_main_template_section(self):
        """ Create main template selection section """
        group = QGroupBox("📄 Primary Template Selection")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {AppStyles.FONT_MEDIUM};
                font-weight: bold;
                color: {AppStyles.SUCCESS_COLOR};
                border: 2px solid {AppStyles.BORDER_COLOR};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: {AppStyles.BACKGROUND_COLOR};
            }}
        """)

        layout = QVBoxLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                  AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,)
        
        # Template Selection Row
        template_row = QHBoxLayout()
        template_row.setSpacing(AppStyles.SPACING_MEDIUM)

        # Template Label
        self.template_label = QLabel("📄 No Loan Application Template Selected")
        self.template_label.setStyleSheet(f"""
            QLabel {{
                background-color: {AppStyles.WARNING_COLOR};
                color: {AppStyles.TEXT_PRIMARY};
                padding: {AppStyles.PADDING_SMALL}px;
                border-radius: 4px;
                font-weight: bold;
            }}        
        """)
        self.template_label.setMinimumHeight(AppStyles.INPUT_HEIGHT)
        self.template_label.setAlignment(Qt.AlignCenter)

        # Template Button
        self.loan_template_button = QPushButton("📝 Choose Loan Application Template")
        self.loan_template_button.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        self.loan_template_button.setMinimumWidth(250)
        self.loan_template_button.clicked.connect(self.choose_loan_template)

        template_row.addWidget(self.template_label, 2)
        template_row.addWidget(self.loan_template_button, 1)
        
        layout.addLayout(template_row)
        group.setLayout(layout)

        return group

    def create_additional_docs_section(self):
        """Create additional documents section"""
        group = QGroupBox("📋 Additional Documents Generation")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {AppStyles.FONT_MEDIUM};
                font-weight: bold;
                color: {AppStyles.DANGER_COLOR};
                border: 2px solid {AppStyles.BORDER_COLOR};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: {AppStyles.BACKGROUND_COLOR};
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(AppStyles.SPACING_MEDIUM)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_LARGE,
                                 AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)
        
        # Select All option
        select_all_row = QHBoxLayout()
        self.radio_select_all = QRadioButton("🔄 Select All Documents")
        self.radio_select_all.setStyleSheet(f"""
            QRadioButton {{
                font-weight: bold;
                color: {AppStyles.PRIMARY_COLOR};
                font-size: {AppStyles.FONT_NORMAL};
            }}
        """)
        self.radio_select_all.toggled.connect(self.toggle_all_documents)
        select_all_row.addWidget(self.radio_select_all)
        select_all_row.addStretch()
        layout.addLayout(select_all_row)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Document sections
        documents = [
            ("📋 Tamasuk", "checkbox_tamasuk", "tamasuk_template_button", "📝 Choose Tamasuk Template", self.select_tamasuk_template),
            ("✅ Loan Approval (ऋण स्वीकृत)", "checkbox_loan_approval", "btn_loan_approval_template", "📄 Choose ऋण स्वीकृत Template", self.choose_loan_approval_template),
            ("🔐 Debit Authority (खाता अख्तियारी)", "checkbox_debit_authority", "btn_debit_authority", "📄 Choose खाता अख्तियारी Template", self.choose_debit_authority_template)
        ]
        
        for doc_name, checkbox_attr, button_attr, button_text, button_handler in documents:
            doc_frame = self.create_document_section(doc_name, checkbox_attr, button_attr, button_text, button_handler)
            layout.addWidget(doc_frame)
        
        group.setLayout(layout)
        return group

    def create_document_section(self, doc_name, checkbox_attr, button_attr, button_text, button_handler):
        """Create individual document section"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppStyles.CARD_BACKGROUND};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 6px;
                padding: {AppStyles.PADDING_SMALL}px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(AppStyles.SPACING_SMALL)
        layout.setContentsMargins(AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM,
                                 AppStyles.PADDING_MEDIUM, AppStyles.PADDING_MEDIUM)
        
        # Checkbox
        checkbox = QCheckBox(doc_name)
        checkbox.setStyleSheet(f"""
            QCheckBox {{
                font-weight: bold;
                color: {AppStyles.TEXT_PRIMARY};
                font-size: {AppStyles.FONT_NORMAL};
            }}
        """)
        setattr(self, checkbox_attr, checkbox)
        
        # Button row
        button_row = QHBoxLayout()
        button = QPushButton(button_text)
        button.setMinimumHeight(AppStyles.BUTTON_HEIGHT)
        button.clicked.connect(button_handler)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.INFO_COLOR};
                color: white;
                font-size: {AppStyles.FONT_SMALL};
            }}
            QPushButton:hover {{
                background-color: #2c9faf;
            }}
        """)
        setattr(self, button_attr, button)
        
        button_row.addWidget(button)
        button_row.addStretch()
        
        layout.addWidget(checkbox)
        layout.addLayout(button_row)
        
        return frame

    def create_action_section(self):
        """Create action buttons section"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppStyles.CARD_BACKGROUND};
                border: 2px solid {AppStyles.SUCCESS_COLOR};
                border-radius: 8px;
                padding: {AppStyles.PADDING_MEDIUM}px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(AppStyles.SPACING_LARGE)
        layout.setContentsMargins(AppStyles.PADDING_LARGE, AppStyles.PADDING_LARGE,
                                 AppStyles.PADDING_LARGE, AppStyles.PADDING_LARGE)
        
        # Generate button
        self.btn_generate_report = QPushButton("🚀 Generate Reports")
        self.btn_generate_report.setMinimumHeight(AppStyles.BUTTON_HEIGHT + 10)
        self.btn_generate_report.setMinimumWidth(200)
        self.btn_generate_report.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.SUCCESS_COLOR};
                color: white;
                font-size: {AppStyles.FONT_MEDIUM};
                font-weight: bold;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: #17a673;
            }}
        """)
        self.btn_generate_report.clicked.connect(self.generate_report)
        
        layout.addStretch()
        layout.addWidget(self.btn_generate_report)
        layout.addStretch()
        
        return frame



        # -- Old UI codes ---
        # # CheckBoxes to control tamasuk generation
        # self.checkbox_tamasuk = QCheckBox("📋Generate Tamasuk")
        # additional_layout.addWidget(self.checkbox_tamasuk)
        # # Select template for Tamasuk
        # self.tamasuk_template_button = QPushButton("📝 Choose Tamasuk Template")
        # self.tamasuk_template_button.clicked.connect(self.select_tamasuk_template)
        # additional_layout.addWidget(self.tamasuk_template_button)
        
        # # Loan Approval letter CheckBox + Button
        # self.checkbox_loan_approval = QCheckBox("ऋण स्वीकृत")
        # self.btn_loan_approval_template = QPushButton("Choose ऋण स्वीकृत Template")
        # self.btn_loan_approval_template.clicked.connect(self.choose_loan_approval_template)
        # additional_layout.addWidget(self.checkbox_loan_approval)
        # additional_layout.addWidget(self.btn_loan_approval_template)

        # # Debit Authority CheckBox + Button
        # self.checkbox_debit_authority = QCheckBox("खाता खर्च गर्न सक्ने अख्तियारी पत्र")
        # self.btn_debit_authority = QPushButton("Choose खाता अख्तियारी Template")
        # self.btn_debit_authority.clicked.connect(self.choose_debit_authority_template)
        # additional_layout.addWidget(self.checkbox_debit_authority)
        # additional_layout.addWidget(self.btn_debit_authority)
        
        # self.additional_docs_group.setLayout(additional_layout)
        # form_layout.addRow(self.additional_docs_group)


        # # Add Generate Reports button
        # self.btn_generate_report = QPushButton("Generate Report")
        # self.btn_generate_report.clicked.connect(self.generate_report)
        # form_layout.addWidget(self.btn_generate_report)

        # # --- Path Tracking ---
        # self.selected_template_path = None
        # self.loan_approval_template_path = None
        # self.authority_template_path = None

        # -- End of Old UI codes

        # --Setting layout --
        # main_layout = QVBoxLayout()
        # main_layout.addWidget(scroll)
        # self.setLayout(main_layout)
    

    def update_session_label(self):
        """Update session label with current member info"""
        member = current_session.get("member_number", "")
        name = current_session.get("member_name", "")
        if member and name:
            self.session_label.setText(f"📌 Preparing report for: {member} - {name}")
            self.session_label.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    font-size: {AppStyles.FONT_NORMAL};
                    background-color: #ffffff;
                    padding: {AppStyles.PADDING_SMALL}px;
                    border-radius: 4px;
                }}
            """)
        else:
            self.session_label.setText("⚠ No member selected for report generation")
            self.session_label.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    font-size: {AppStyles.FONT_NORMAL};
                    background-color: {AppStyles.SUCCESS_COLOR};
                    padding: {AppStyles.PADDING_SMALL}px;
                    border-radius: 4px;
                }}
            """)
        
    
    
    def choose_loan_template(self):
        """Choose loan application template"""
        path, _ = QFileDialog.getOpenFileName(self, "Select Loan Application Template", "", "Word Documents (*.docx)")
        if path:
            self.template_path = path
            filename = os.path.basename(path)
            self.template_label.setText(f"📄 {filename}")
            self.template_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {AppStyles.SUCCESS_COLOR};
                    color: white;
                    padding: {AppStyles.PADDING_SMALL}px;
                    border-radius: 4px;
                    font-weight: bold;
                }}
            """)
    def select_tamasuk_template(self):        
        """Select Tamasuk template"""
        path, _ = QFileDialog.getOpenFileName(self, "📝 Select Tamasuk Template", "", "Word Documents (*.docx)")
        if path:
            self.tamasuk_template_path = path
            filename = os.path.basename(path)
            self.tamasuk_template_button.setText(f"📄 {filename}")
            self.tamasuk_template_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppStyles.SUCCESS_COLOR};
                    color: white;
                    font-size: {AppStyles.FONT_SMALL};
                }}
            """)

    def choose_loan_approval_template(self):
        """Choose loan approval template"""
        path, _ = QFileDialog.getOpenFileName(self, "Choose ऋण स्वीकृत Template", "", "Word Files (*.docx)")
        if path:
            self.loan_approval_template_path = path
            filename = os.path.basename(path)
            self.btn_loan_approval_template.setText(f"📄 {filename}")
            self.btn_loan_approval_template.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppStyles.SUCCESS_COLOR};
                    color: white;
                    font-size: {AppStyles.FONT_SMALL};
                }}
            """)
    
    def choose_debit_authority_template(self):
        """Choose debit authority template"""
        path, _ = QFileDialog.getOpenFileName(self, "Choose खाता अख्तियारी Template", "", "Word Files (*.docx)")
        if path:
            self.authority_template_path = path
            filename = os.path.basename(path)
            self.btn_debit_authority.setText(f"📄 {filename}")
            self.btn_debit_authority.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppStyles.SUCCESS_COLOR};
                    color: white;
                    font-size: {AppStyles.FONT_SMALL};
                }}
            """)

    def toggle_all_documents(self, checked):
        self.checkbox_loan_approval.setChecked(checked)
        self.checkbox_debit_authority.setChecked(checked)
        if hasattr(self, "checkbox_tamasuk"):
            self.checkbox_tamasuk.setChecked(checked)
    
    def generate_report(self):
        entered_by_name = current_session.get("entered_by", "")
        entered_by_post = current_session.get("entered_by_post", "")
        approved_by_name = current_session.get("approved_by", "")
        approved_by_post = current_session.get("approved_by_post", "")


        if not self.template_path:
            QMessageBox.warning(self, "No Template", "Please select a Word Template first.")
            return
        
        member_number = current_session.get("member_number")

        if not member_number:
            QMessageBox.warning(self, "No Member selected", "Please search/select a member first.")
            return
        
        data = prepare_report_context(
            member_number,
            entered_by_name,
            entered_by_post,
            approved_by_name,
            approved_by_post
        )

        if not data:
            QMessageBox.warning(self, "Data Error", "No Data found for the selected member.")
            return
        nepali_today = nepali_date.today()
        nepali_date_str = nepali_today.strftime('%Y%m%d')  # e.g., '20821101'

        loan_type = self.loan_type_input.currentText().strip()
        if not loan_type:
            QMessageBox.warning(self, "Loan Type Missing.", "Please select a loan type.")
            return
        
        if not entered_by_name or not approved_by_name:
            QMessageBox.warning(self, "Missing Approval Info", "Please go to Approval Tab and select approvers before generating the report.")
            return

      
        try:
            tpl = DocxTemplate(self.template_path)
            tpl.render(data)

            # Prepare folders and file name
            base_dir = 'generated reports'
            loan_type_folder = os.path.join(base_dir, loan_type)
            os.makedirs(loan_type_folder, exist_ok=True)
            
            filename = f"{loan_type}_{member_number}_{nepali_date_str}.docx"
            output_path = os.path.join(loan_type_folder, filename)
            absolute_output_path = abspath(output_path) 
            
            tpl.save(absolute_output_path)
            

            # ✅ Save tracking info
            save_report_log({
                "member_number": member_number,
                "report_type": "Loan Application",
                "generated_by": self.username,
                "file_path": absolute_output_path,
                "date": nepali_date.today().strftime('%Y-%m-%d')
            })

            QMessageBox.information(self, "Report Saved", f"Report saved to: {output_path}")
            # output_name = f"generated_reports/ऋण आवेदन_{member_number}_{nepali_date_str}.docx"
            # os.makedirs(os.path.dirname(output_name), exist_ok=True)
            # tpl.save(output_name)
            # QMessageBox.information(self, "Success", f"Report generated and saved to:\n{output_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report:\n{e}")
        

        # Trigger refresh in history tab (if it exists)
            main_window = self.window()
            if hasattr(main_window, 'history_tab') and hasattr(main_window.history_tab, 'refresh_table'):
                main_window.history_tab.refresh_table()
       
        if self.checkbox_tamasuk.isChecked():
            if not hasattr(self, 'tamasuk_template_path') or not self.tamasuk_template_path:
                QMessageBox.warning(self, "No Tamasuk Template", "Please select a tamasuk template first!")
                return
            try:
                tpl_tamasuk = DocxTemplate(self.tamasuk_template_path)
                tpl_tamasuk.render(data)
                
                # Save Tamasuk
                tamasuk_folder = os.path.join("generated reports", "तमसुक")
                os.makedirs(tamasuk_folder,exist_ok=True)
                tamasuk_filename = f"तमसुक_{member_number}_{nepali_date_str}.docx"
                tamasuk_path = os.path.join(tamasuk_folder, tamasuk_filename)
                tpl_tamasuk.save(tamasuk_path)

                # Log to report tracking
                save_report_log({
                    "member_number": member_number,
                    "report_type": "Tamasuk",
                    "generated_by": self.username,
                    "file_path": tamasuk_path,
                    "date": nepali_date_str
                })
                QMessageBox.information(self, "Tamasuk Saved", f"Tamasuk report saved to:\n{tamasuk_path}")
            except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to generate Tamasuk:\n{e}")
        
        # 🔁 Generate selected documents
        extra_docs = [
            ("ऋण स्वीकृत", self.checkbox_loan_approval, self.loan_approval_template_path),
            ("अख्तियारी पत्र", self.checkbox_debit_authority, self.authority_template_path)
        ]


        for doc_name, checkbox, template_path in extra_docs:
            if checkbox.isChecked():
                if not template_path:
                    QMessageBox.warning(self, "Missing Template", f"Please select template for: {doc_name}")
                    continue
                try:
                    tpl = DocxTemplate(template_path)
                    tpl.render(data)
                    filename = f"{doc_name}_{member_number}_{nepali_date_str}.docx"
                    folder_path = os.path.join("generated reports", doc_name)
                    os.makedirs(folder_path, exist_ok=True)
                    output_path = os.path.join(folder_path, filename)
                    tpl.save(output_path)

                    # Save report log
                    save_report_log({
                        "member_number": member_number,
                        "report_type": doc_name,
                        "generated_by": self.username,
                        "file_path":  output_path,
                        "date": nepali_date_str
                    })
                    QMessageBox.information(self, "Document Saved", f"{doc_name} report saved to:\n{output_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"failed to generate {doc_name}:\n{e}")

        # clear_session()
        # QApplication.instance().activeWindow().statusBar().showMessage("✅ Session cleared after report generation", 5000)

        # Optional: Refresh headers
        if hasattr(self.parentWidget(), 'refresh_member_header_in_all_tabs'):
            self.parentWidget().refresh_member_header_in_all_tabs()    
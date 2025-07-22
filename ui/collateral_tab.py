# ui/collateral_tab.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea, QFormLayout, QLineEdit, 
    QPushButton, QStackedLayout, QGroupBox, QHBoxLayout, QMessageBox, 
    QSizePolicy, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from context import current_session
from signal_bus import signal_bus
from models.collateral_model import (save_collateral_info,
                                save_affiliated_institutions, 
                                save_property_info,
                                save_family_info,
                                save_income_expense )
from utils.converter import convert_to_nepali_digits
from styles.app_styles import AppStyles

# class CollateralTab(QWidget):
#     def __init__(self):
#         super().__init__()
  

#         self.main_layout = QVBoxLayout()
       

#         # 📌 Header Group
#         header_group = QGroupBox("📋 Associated Member Information")
#         header_layout = QFormLayout()
#         self.header_label = QLabel("📌 No member selected")
#         self.header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green; padding: 4px;")
#         header_layout.addRow(self.header_label)
#         header_group.setLayout(header_layout)
#         self.main_layout.addWidget(header_group)

#         # Apply styles
#         self.setStyleSheet("""
#             QWidget {
#                     font-family: Arial;
#                     font-size: 14px
#            }
            
#             QLabel {
#                     color: #333;
#                     min-width: 150px;
#             }
#             QLineEdit, QDateEdit {
#                            border: 1px solid #ddd;
#                            border-radius: 4px;
#                            padding: 8px;
#                            min-width:250px;
#                            background-color: white;
#             }
#             QLineEdit:focus, QDateEdit:focus {
#                         border: 1px solid #3498db;
#             }
#             QPushButton {
#                            background-color: #4CAF50;
#                            color: white;
#                            border: none;
#                            padding: 10px 15px;
#                            border-radius: 4px;
#                            min-width: 100px;
#                            }
#             QPushButton:hover {
#                            background-color: #45a049;
#                            }                        
#         """)
      

#         self.stack = QStackedLayout()
#         self.main_layout.addLayout(self.stack)    

#         # Basic form "खरखाँचो"
#         self.basic_widget = QWidget()
#         self.basic_form_layout = QFormLayout(self.basic_widget)
#         self.basic_form_layout.addRow(QLabel("खरखाँचो ऋण बचत रोक्का विवरण:"))
        
#         self.monthly_saving = QLineEdit()
#         self.basic_form_layout.addRow("मासिक बचतः", self.monthly_saving)
#         self.child_saving = QLineEdit()
#         self.basic_form_layout.addRow("बाल बचतः", self.child_saving)

#         for field in [self.monthly_saving, self.child_saving]:
#             field.editingFinished.connect(self.update_total_saving)

#         self.total_saving = QLineEdit()
#         self.basic_form_layout.addRow("कुल बचत:", self.total_saving)

#         self.next_button = QPushButton("Save")
#         self.next_button.setIcon(QIcon('icons/icon_btn.png'))
#         self.next_button.setFixedWidth(220)
#         # self.next_button.setIconSize(QSize(25, 25))
#         # self.next_button.setStyleSheet("QPushButton::menu-indicator { padding-left: 6px; }"
#         #                        "QPushButton { text-align: center; padding-left: 10px; }")
#         # self.next_button.setStyleSheet("QPushButton { padding-left: 10px; }")
#         self.next_button.clicked.connect(self.save_basic_collateral_data)
#         # self.basic_form_layout.addRow(self.next_button)
       
        
#         next_button_layout = QHBoxLayout()        
#         next_button_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)
#         self.basic_form_layout.addRow(next_button_layout)
        
       

#         # Extended Form

#         self.extended_widget = QWidget()
#         self.extended_layout = QVBoxLayout(self.extended_widget)

#         # Section 1: सम्बद्ध संस्थाको विवरण
#         self.affiliated_group = self.create_dynamic_group(
#             title = "📌 सम्बद्ध संस्थाको विवरण",
#             fields = [
#                 "संस्था / व्यवसायको नाम", 
#                 "ठेगाना", 
#                 "पद", 
#                 "अनुमानित वार्षिक आम्दानी",
#                 "कैफियत"
#             ]
#         )
#         self.extended_layout.addWidget(self.affiliated_group["groupbox"])

#         # Section 2: घर जग्गाको धितोको विवरण
#         self.property_collateral_group = self.create_dynamic_group(
#             title = "🏚️ घर जग्गाको धितो विवरण",
#             fields = [
#                 "जग्गा धनीको नाम",
#                 "बाबु / पति",
#                 "बाजे / ससुरा",
#                 "जिल्ला",
#                 "न.पा./ गा.पा. ",
#                 "सिट नं",
#                 "वडा नं",
#                 "कित्ता नं",
#                 "क्षेत्रफल",
#                 "किसिम"
#             ]
#         )
#         self.extended_layout.addWidget(self.property_collateral_group["groupbox"])

#         # Section 3: पारिवारीक विवरण
#         self.family_group = self.create_dynamic_group(
#             title = "👩‍👩‍👧 पारिवारीक विवरण",
#             fields = [
#                 "नाम",
#                 "उमेर",
#                 "ऋण मागकर्ता सँगको नाता",
#                 "संस्थामा सदस्य भए नभएको",
#                 "पेशा",
#                 "मासिक आय"
#             ]
#         )
#         self.extended_layout.addWidget(self.family_group["groupbox"])

#         # Section 4: मासिक आम्दानी र खर्च विवरण
#         self.income_expense_group = self.create_dynamic_group(
#             title = "💰 ऋणीको मासिक आम्दानी र खर्चको विवरण",
#             fields = [
#                 "घरभाडा आम्दानी",
#                 "तलब / ज्याला आम्दानी",
#                 "व्यवसायको आम्दानी",
#                 "कृषिबाट आम्दानी",
#                 "वैदेशिक रोजगार आम्दानी",
#                 "कमिसन आम्दानी",
#                 "पारिवारीक आम्दानी",
#                 "अन्य आम्दानी",
#                 "घरभाडा / विजुली / पानी, केवल खर्च",
#                 "सञ्चार खर्च",
#                 "रासन / लत्ताकपडा",
#                 "शिक्षा/औषधी उपचार खर्च",
#                 "अन्य वित्तिय संस्थाको  किस्ता",
#                 "यातायात इन्धन खर्च",
#                 "अन्य अनिवार्य खर्च",
#                 "जम्मा खर्च",
#                 "मासिक बचत रकम"
#             ]
#         )
#         self.extended_layout.addWidget(self.income_expense_group["groupbox"])

#         # Save button for extended form
#         self.extended_save_button = QPushButton("Save")
#         self.extended_save_button.setIcon(QIcon('icons/icon_btn.png'))
#         self.extended_save_button.setFixedWidth(220)

#         save_btn_layout = QHBoxLayout()
#         save_btn_layout.addWidget(self.extended_save_button, alignment=Qt.AlignCenter)
#         self.extended_layout.addLayout(save_btn_layout)

#         self.extended_save_button.clicked.connect(self.save_extended_collateral_data)

#         # --- End of extended form
        
#         # Add both to stacked layout
#         self.main_layout.addWidget(header_group)
#         self.stack.addWidget(self.basic_widget)
#         self.stack.addWidget(self.extended_widget)

#         self.setLayout(self.main_layout)

#         # Initially disable form
#         # self.set_form_enabled(False)

#         # Listen for session updates
#         signal_bus.session_updated.connect(self.update_header)

#     # def set_form_enabled(self, enabled):
#     #     """Enable/disable form fields and buttons"""
#     #     for i in range(self.form_layout.count()):
#     #         widget = self.form_layout.itemAt(i).widget()
#     #         if widget:
#     #             widget.setEnabled(enabled)
#     #     self.save_button.setEnabled(enabled)

#     def update_header(self):
#         """Update header with current session"""
#         member = current_session.get("member_number")
#         name = current_session.get("member_name")
#         if member and name:
#             self.header_label.setText(f"📌 Currently editing: {member} - {name}")
#             # self.set_form_enabled(True)
#         else:
#             self.header_label.setText("📌 No member selected")
#             # self.set_form_enabled(False)
        
#     def showEvent(self, event):
#         loan_type = current_session.get("loan_type", "")
#         if loan_type == "खरखाँचो":
#             self.stack.setCurrentWidget(self.basic_widget)
#         else:
#             self.stack.setCurrentWidget(self.extended_widget)
#         super().showEvent(event)
       
#     #     # Scroll area
#     #     scroll = QScrollArea()
#     #     scroll.setWidgetResizable(True)
#     #     content = QWidget()
#     #     form_layout = QFormLayout(content)
#     #     scroll.setWidget(content)


#     #     self.monthly_saving = QLineEdit()
#     #     self.child_saving = QLineEdit()
        
#     #     # Validate float input
#     #     # validator = QDoubleValidator(0.0, 1000000.0, 2)

#     #     for field in [self.monthly_saving, self.child_saving]:
#     #         # field.setValidator(validator)
#     #         field.editingFinished.connect(self.update_total_saving)

#     #     form_layout.addRow("Monthly Saving:", self.monthly_saving)
#     #     form_layout.addRow("Child Saving:", self.child_saving)
        
        
#     #     self.total_saving = QLineEdit()
#     #     self.total_saving.setReadOnly(True)
#     #     form_layout.addRow("Total Saving:", self.total_saving)

    

#     #     # --Setting layout --
#     #     main_layout = QVBoxLayout()
#     #     main_layout.addWidget(scroll)
#     #     self.setLayout(main_layout)
#     def create_dynamic_group(self, title, fields):
#         groupbox = QGroupBox(title)
#         layout = QVBoxLayout()
#         rows = []

#         add_button = QPushButton("➕ थप्नुहोस्")
#         layout.addWidget(add_button)

#         def add_row():
#             row_layout = QHBoxLayout()
#             inputs = []
#             for field in fields:
#                 line = QLineEdit()
#                 line.setPlaceholderText(field)
#                 inputs.append(line)
#                 row_layout.addWidget(line)
#             rows.append(inputs)
#             layout.insertLayout(layout.count() - 1, row_layout)

#         add_button.clicked.connect(add_row)
#         # Initial row on load
#         add_row()        
#         groupbox.setLayout(layout)

#         return {
#             "groupbox": groupbox,
#             "rows": rows,
#             "add_row": add_row
#         }

#     def update_total_saving(self):
#         m = float(self.monthly_saving.text() or 0)
#         c = float(self.child_saving.text() or 0)
#         total = m + c
#         self.total_saving.setText(f"{total:.2f}")
    

#     def save_extended_collateral_data(self):
#         # try:
#         #     monthly = float(self.monthly_saving.text())
#         #     child = float(self.child_saving.text())
#         #     total = monthly + child

#         #     data = {
#         #         'monthly_saving': convert_to_nepali_digits(monthly),
#         #         'child_saving': convert_to_nepali_digits(child),
#         #         'total_saving': convert_to_nepali_digits(total)
#         #     }

#         #     save_collateral_info(data)
#         #     print("✅ Collateral data saved successfully!")

#         # except Exception as e:
#         #     print("❌ Error saving collateral data:", e)

#         try:
#             # Get current member number
#             member_number = current_session.get("member_number", "").strip()
#             if not member_number:
#                 QMessageBox.warning(self, "No Member Selected", "Please select a member first.")
#                 print("❌ No Member Selected")
#                 return
           
#             # Save affiliated institutions
#             affiliated_entries = [[field.text().strip() for field in row] for row in self.affiliated_group["rows"]]
#             save_affiliated_institutions(member_number, affiliated_entries)

#             # Save properties info
#             property_entries = [[field.text().strip() for field in row] for row in self.property_collateral_group["rows"]]
#             save_property_info(member_number, property_entries)

#             # Save family info
#             family_entries =[[field.text().strip() for field in row] for row in self.family_group["rows"]]
#             save_family_info(member_number, family_entries)

#             # Save Income and expense info
#             income_expense_entries = []
#             for field in self.income_expense_group["rows"][0]: # Only one
#                 label =  field.placeholderText()
#                 value = field.text().strip()
#                 typ = "income" if "आम्दानी" in label else "expense"
#                 income_expense_entries.append([label, value, typ])
#             save_income_expense(member_number, income_expense_entries)

#             QMessageBox.information(self, "Collateral", "Collateral information is saved successfully." )

#             print("✅ All Colleteral data saved successfully!")
            
#         except Exception as e:
#             print("❌ Error saving collateral data:", e)

#     def save_basic_collateral_data(self):
#         try:
#             # Get current member number
#             member_number = current_session.get("member_number", "").strip()
#             if not member_number:
#                 print("❌ No Member Selected")
#                 return
            
#             # Save basic saving info
#             monthly = float(self.monthly_saving.text())
#             child = float(self.child_saving.text())
#             total = monthly + child
                    
#             data = {
#                 'monthly_saving': convert_to_nepali_digits(monthly),
#                 'child_saving': convert_to_nepali_digits(child),
#                 'total_saving': convert_to_nepali_digits(total)
#             }

#             save_collateral_info(data, member_number)
#             QMessageBox.information(self, "Basic Collateral" "Basic Collateral info saved successfully.")
#             self.clear_basic_form()
#             print("✅ Basic Collateral data saved successfully!")

#         except Exception as e:
#             print("❌ Error saving basic collateral data:", e)

#     def save_basic_form(self):
#         self.monthly_saving.clear()
#         self.child_saving.clear()
#         self.total_saving.clear()

# -- New updated UI layout
class CollateralTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """ Initialize and setup the user interface """
        # Main layout with proper margins and spacing
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM)
        self.main_layout.setSpacing(AppStyles.PADDING_MEDIUM)

        # Create Header
        self.create_header()

        # Create main content with scroll area
        self.create_main_content()

        # Apply responsive stylesheet
        self.apply_responsive_styles()

    def create_header(self):
        """ Create responsive header section"""
        header_group = QGroupBox("📋 Associated Member Information")
        header_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        header_layout = QVBoxLayout(header_group)
        header_layout.setContentsMargins(
            AppStyles.PADDING_SMALL,
            AppStyles.PADDING_SMALL,
            AppStyles.PADDING_SMALL,
            AppStyles.PADDING_SMALL
        )

        self.header_label = QLabel("📌 No member selected")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setWordWrap(True) # Allow text wrapping
        self.header_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        header_layout.addWidget(self.header_label)
        self.main_layout.addWidget(header_group)
    
    def create_main_content(self):
        """ Create main content area with scroll support """
        # Create scroll area for main content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Content widget for scroll area
        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Stack layout for different forms
        self.stack = QStackedLayout(content_widget)

        # Create forms
        self.create_basic_form()
        self.create_extended_form()

        scroll_area.setWidget(content_widget)
        self.main_layout.addWidget(scroll_area)

    def create_basic_form(self):
        """ Create basic collateral form with responsive layout"""
        self.basic_widget = QWidget()
        main_layout = QVBoxLayout(self.basic_widget)
        main_layout.setContentsMargins(
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM
        )
        main_layout.setSpacing(AppStyles.SPACING_MEDIUM)

        # Form section
        form_group = QGroupBox("खरखाँचो ऋण बचत रोक्का विवरण")
        form_layout = QFormLayout(form_group)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        form_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)

        # Create input fields with proper size policies
        self.monthly_saving = self.create_responsive_line_edit()
        self.child_saving = self.create_responsive_line_edit()
        self.total_saving = self.create_responsive_line_edit()
        self.total_saving.setReadOnly(True)

        # Connect Signals for auto-calculation
        self.monthly_saving.editingFinished.connect(self.update_total_saving)
        self.child_saving.editingFinished.connect(self.update_total_saving)

        # Add fields to form
        form_layout.addRow("मासिक बचत:", self.monthly_saving)
        form_layout.addRow("बाल बचत:", self.child_saving)
        form_layout.addRow("कुल बचत:", self.total_saving)

        main_layout.addWidget(form_group)

        # Save button with proper layout
        self.create_save_button_layout(
            main_layout,
            self.save_basic_collateral_data, 
            "Save Basic Info"
        )

        # Add stretch to push content up
        main_layout.addStretch()

        self.stack.addWidget(self.basic_widget)
    
    def create_extended_form(self):
        """Create extended collateral form with responsive layout"""
        self.extended_widget = QWidget()
        main_layout = QVBoxLayout(self.extended_widget)
        main_layout.setContentsMargins(
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM
        )
        main_layout.setSpacing(AppStyles.SPACING_MEDIUM)

        # Section 1: सम्बद्ध संस्थाको विवरण
        self.affiliated_group = self.create_responsive_dynamic_group(
            title = "सम्बद्ध संस्थाको विवरण",
            fields = [
                "संस्था/व्यवसायको नाम",
                "ठेगाना",
                "पद",
                "अनुमानित वार्षिक आम्दानी",
                "कैफियत"
            ]
        )
        main_layout.addWidget(self.affiliated_group["groupbox"])

        # Section 2: घर जग्गा धितोको विवरण
        self.property_collateral_group = self.create_responsive_dynamic_group(
            title = "घर जग्गाको धितो विवरण",
            fields = [
                "जग्गा धनीको नाम",
                "बाबु/पति",
                "बाजे/ससुरा",
                "जिल्ला",
                "न.पा./गा.पा",
                "सिट नं",
                "वडा नं",
                "कित्ता नं",
                "क्षेत्रफल",
                "किसिम"
            ]
        )
        main_layout.addWidget(self.property_collateral_group["groupbox"])
        
        # Section 3: पारिवारिक विवरण
        self.family_group = self.create_responsive_dynamic_group(
            title = "पारिवारीक विवरण",
            fields = [
                "नाम",
                "उमेर",
                "ऋण मागकर्ता सँगको नाता",
                "संस्थामा सदस्य भए नभएको", 
                "पेशा", 
                "मासिक आय"
            ]
        )
        main_layout.addWidget(self.family_group["groupbox"])

        # Section 4: मासिक आम्दानी
        self.income_expense_group = self.create_responsive_dynamic_group(
            title = "ऋणीको मासिक आम्दानी र खर्चको विवरण",
            fields = [
                "घरभाडा आम्दानी", 
                "तलब / ज्याला आम्दानी", 
                "व्यवसायको आम्दानी",
                "कृषिबाट आम्दानी", 
                "वैदेशिक रोजगार आम्दानी", 
                "कमिसन आम्दानी",
                "पारिवारीक आम्दानी", 
                "अन्य आम्दानी", 
                "घरभाडा/विजुली/पानी केवल खर्च",
                "सञ्चार खर्च", 
                "रासन / लत्ताकपडा", 
                "शिक्षा/औषधी उपचार खर्च",
                "अन्य वित्तिय संस्थाको किस्ता", 
                "यातायात इन्धन खर्च",
                "अन्य अनिवार्य खर्च", 
                "जम्मा खर्च", 
                "मासिक बचत रकम"
            ]
        )
        main_layout.addWidget(self.income_expense_group["groupbox"])

        # Save Button
        self.create_save_button_layout(
            main_layout,
            self.save_extended_collateral_data,
            "Save Extended Info"
        )

        # Add stretch
        main_layout.addStretch()

        self.stack.addWidget(self.extended_widget)

    def create_responsive_line_edit(self):
        """ Create a responsive QLineEdit with proper size policies"""
        line_edit = QLineEdit()
        line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line_edit.setMinimumWidth(200) # Minimum width instead of fixed
        line_edit.setMaximumWidth(400) # Maximum width to prevent over-stretching
        return line_edit

    def create_save_button_layout(self, parent_layout, callback, text):
        """ Create a centered save button with responsive layout"""
        button_frame = QFrame()
        button_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, AppStyles.SPACING_MEDIUM, 0, AppStyles.SPACING_MEDIUM)

        save_button = QPushButton(text)
        save_button.setIcon(QIcon('icons/icon_btn.png'))
        save_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        save_button.setMinimumWidth(150)
        save_button.setMaximumWidth(250)
        save_button.clicked.connect(callback)

        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addStretch()

        parent_layout.addWidget(button_frame)

    def create_responsive_dynamic_group(self, title, fields):
        """ Create a responsive dynamic group with proper layout management"""
        groupbox = QGroupBox(title)
        groupbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        main_layout = QVBoxLayout(groupbox)
        main_layout.setContentsMargins(
            AppStyles.PADDING_SMALL,
            AppStyles.PADDING_SMALL,
            AppStyles.PADDING_SMALL,
            AppStyles.PADDING_SMALL
        )
        main_layout.setSpacing(AppStyles.SPACING_SMALL)

        rows = []
        rows_container = QWidget()
        rows_layout = QVBoxLayout(rows_container)
        rows_layout.setSpacing(AppStyles.SPACING_SMALL)

        # Add button
        add_button = QPushButton("➕ थप्नुहोस्")
        add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_button.setMaximumWidth(150)

        def add_row():
            row_widget = QWidget()
            row_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            inputs = []
            
            # Determine layout type based on number of fields
            if len(fields) > 6:
                # Use grid layout for many fields (3 columns)
                row_layout = self.create_grid_row_layout(fields, 3)
                inputs = row_layout.inputs
            elif len(fields) > 3:
                # Use grid layout for medium number of fields (2 columns)
                row_layout = self.create_grid_row_layout(fields, 2)
                inputs = row_layout.inputs
            else:
                # Single row layout for few fields
                row_layout = QHBoxLayout()
                row_layout.setSpacing(AppStyles.SPACING_SMALL)
                
                for field in fields:
                    line_edit = self.create_responsive_line_edit()
                    line_edit.setPlaceholderText(field)
                    inputs.append(line_edit)
                    row_layout.addWidget(line_edit)
            
            row_widget.setLayout(row_layout)
            rows.append(inputs)
            rows_layout.addWidget(row_widget)

        add_button.clicked.connect(add_row)

        # Initial row
        add_row()

        # Add components to main layout
        main_layout.addWidget(add_button)
        main_layout.addWidget(rows_container)

        return {
            "groupbox": groupbox,
            "rows": rows,
            "add_row": add_row
        }
    
    def create_grid_row_layout(self, fields, columns):
        """Create a grid layout for fields with specified number of columns"""
        grid_layout = QGridLayout()
        grid_layout.setSpacing(AppStyles.SPACING_SMALL)

        inputs = []
        for i, field in enumerate(fields):
            row = i // columns
            col = i % columns

            line_edit = self.create_responsive_line_edit()
            line_edit.setPlaceholderText(field)
            inputs.append(line_edit)
            grid_layout.addWidget(line_edit, row, col)
        
        # Store inputs in layout for access
        grid_layout.inputs = inputs
        return grid_layout
    
    def apply_responsive_styles(self):
        """ Apply responsive stylesheet that adapts to different screen sizes"""
        self.setStyleSheet(f"""
                QWidget {{
                           font-family: 'Segoe UI', Arial, sans-serif;
                           font-size: {AppStyles.FONT_NORMAL}px;
                }}

                QGroupBox {{
                            font-weight: bold;
                            border: 2px solid {AppStyles.BORDER_COLOR};
                            border-radius: 8px;
                            margin-top: 10px;
                            padding-top: 10px;
                            background-color: {AppStyles.CARD_BACKGROUND};
                }}

                QGroupBox::title {{
                            subcontrol-origin: margin;
                            left: 15px;
                            padding: 0 8px 0 8px;
                            color: {AppStyles.PRIMARY_COLOR};
                            font-size: {AppStyles.FONT_MEDIUM}px;
                }}

                QLabel {{
                            color: {AppStyles.TEXT_PRIMARY};
                            font-size: {AppStyles.FONT_NORMAL}px;
                            padding: 2px;
                }}

                QLineEdit {{
                            border: 1px solid {AppStyles.BORDER_COLOR};
                            border-radius: 4px;
                            padding: 8px 12px;
                            font-size: {AppStyles.FONT_NORMAL}px;
                            background-color: white;
                            min-height: {AppStyles.INPUT_HEIGHT}px;
                }}

                QLineEdit:focus {{
                            border: 2px solid {AppStyles.PRIMARY_COLOR};
                }}

                QLineEdit:read-only {{
                            background-color: {AppStyles.BACKGROUND_COLOR};
                            color: {AppStyles.TEXT_SECONDARY};
                }}

                QPushButton {{
                            background-color: {AppStyles.SUCCESS_COLOR};
                            color: white;
                            border: none;
                            padding: 12px 20px;
                            border-radius: 6px;
                            font-size: {AppStyles.FONT_NORMAL}px;
                            font-weight: bold;
                            min-height: {AppStyles.BUTTON_HEIGHT}px;
                }}

                QPushButton:hover {{
                            background-color: #17a673;
                }}

                QPushButton:pressed {{
                            background-color: #138f64;
                }}

                QScrollArea {{
                            border: none;
                            background-color: transparent;
                }}

                QScrollBar:vertical {{
                            border: none;
                            background-color: {AppStyles.BACKGROUND_COLOR};
                            width: 12px;
                            border-radius: 6px;
                }}

                QScrollBar::handle:vertical {{
                            background-color: {AppStyles.BORDER_COLOR};
                            border-radius: 6px;
                            min-height: 20px;
                }}

                QScrollBar::handle:vertical:hover {{
                            background-color: {AppStyles.TEXT_SECONDARY};
                }}
        """)
    
    def connect_signals(self):
        """Connect all signals"""
        signal_bus.session_updated.connect(self.update_header)
    
    def showEvent(self, event):
        """ Handle show event to switch forms based on loan type"""
        loan_type = current_session.get("loan_type", "")
        if loan_type == "खरखाँचो":
            self.stack.setCurrentWidget(self.basic_widget)
        else:
            self.stack.setCurrentWidget(self.extended_widget)
        super().showEvent(event)
    
    def update_header(self):
        """ update header with current session"""
        member = current_session.get("member_number")
        name = current_session.get("member_name")
        if member and name:
            self.header_label.setText(f"📌 Currently editing: {member} - {name}")
            self.header_label.setStyleSheet(f"""
                font-size: {AppStyles.FONT_MEDIUM}px;
                font-weight: bold;
                color: {AppStyles.SUCCESS_COLOR};
                padding: 8px;
                background-color: {AppStyles.CARD_BACKGROUND};
                border-radius: 4px;
            """)
        else:
            self.header_label.setText("📌 No member selected")
            self.header_label.setStyleSheet(f"""
                font-size: {AppStyles.FONT_MEDIUM}px;
                font-weight: bold;
                color: {AppStyles.TEXT_SECONDARY};
                padding: 8px;
            """)
    
    def update_total_saving(self):
        """Update total saving calculation"""
        try:
            monthly = float(self.monthly_saving.text() or 0)
            child = float(self.child_saving.text() or 0)
            total = monthly + child
            self.total_saving.setText(f"{total:.2f}")
        except ValueError:
            self.total_saving.setText("0.00")
        
    def save_basic_collateral_data(self):
        """ Save basic collateral data with proper error handling"""
        try:
            member_number = current_session.get("member_number", "").strip()
            if not member_number:
                QMessageBox.warning(self, "No Member Selected", 
                                    "Please select a member first")
                return
            
            monthly = float(self.monthly_saving.text() or 0)
            child = float(self.child_saving.text() or 0)
            total = monthly + child

            data = {
                'monthly_saving': convert_to_nepali_digits(monthly),
                'child_saving': convert_to_nepali_digits(child),
                'total_saving': convert_to_nepali_digits(total)
            }
            save_collateral_info(data, member_number)
            QMessageBox.information(self, "Success",
                                    "Basic Collateral info saved successfully.")
            self.clear_basic_form()
            print("✅ Basic Collateral data saved.")

        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                                "Please enter valid numbers for saving amounts.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving data: {str(e)}")
            print(f"❌ Error saving basic collateral data: {e}")
    
    def save_extended_collateral_data(self):
        """Save extended collateral data with proper error handling"""
        try:
            member_number = current_session.get("member_number", "").strip()
            if not member_number:
                QMessageBox.warning(self, "No Member Selected", 
                                    "Please select a member first")
                return
            
            # Save all sections
            self.save_section_data(member_number)

            QMessageBox.information(self, "Success", 
                                    "All Collateral information saved successfully.")
            print("✅ All Collateral data saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 f"Error saving collateral data: {str(e)}")
            print(f"❌ Error saving collateral data: {e}")
    
    def save_section_data(self, member_number):
        """ Save data from all sections"""
        # Save affiliated institutions
        affiliated_entries = [
            [field.text().strip() for field in row]
            for row in self.affiliated_group["rows"]
        ]
        save_affiliated_institutions(member_number, affiliated_entries)

        # Save properties info
        property_entries = [
            [field.text().strip() for field in row]
            for row in self.property_collateral_group["rows"]
        ]
        save_property_info(member_number, property_entries)

        # Save family info
        family_entries = [
            [field.text().strip() for field in row]
            for row in self.family_group["rows"]
        ]
        save_family_info(member_number, family_entries)

        # Save Income and expense info
        income_expense_entries = []
        for field in self.income_expense_group["rows"][0]:
            label = field.placeholderText()
            value = field.text().strip()
            entry_type = "income" if "आम्दानी" in label else "expense"
            income_expense_entries.append([label, value, entry_type])
        save_income_expense(member_number, income_expense_entries)
    
    def clear_basic_form(self):
        """Clear basic form fields"""
        self.monthly_saving.clear()
        self.child_saving.clear()
        self.total_saving.clear()

            
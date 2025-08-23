# ui/member_manager_dialog.py

import os

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QWidget,
    QAbstractScrollArea, QFrame, QSpacerItem, QSizePolicy, QDialogButtonBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon
from models.member_model import fetch_all_members, delete_member
from ui.personal_info_tab import PersonalInfoTab
from styles.app_styles import AppStyles


PAGE_SIZE = 50

class MemberManagerDialog(QDialog):
    """Member Manager Dialog with global styling and enhanced UX"""
    
    member_updated = pyqtSignal()  # Signal to refresh parent views
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("👥 सदस्य व्यवस्थापन")
        self.setModal(True)
        self.resize(1400, 800)
        
        # Data management
        self.current_page = 1
        self.total_pages = 1
        self.filtered_members = []
        self.all_members = []
        
        # Apply global stylesheet
        self.setStyleSheet(self._get_dialog_stylesheet())
        
        self.init_ui()
        self.load_members()

    def _get_dialog_stylesheet(self):
        """Get comprehensive stylesheet for the dialog"""
        return f"""
        /* Dialog Base Styling */
        QDialog {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        /* Header Section */
        QFrame[frameRole="header"] {{
            background-color: {AppStyles.CARD_BACKGROUND};
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 8px;
            padding: {AppStyles.PADDING_LARGE}px;
            margin-bottom: {AppStyles.SPACING_MEDIUM}px;
        }}
        
        /* Search Section */
        QFrame[frameRole="search"] {{
            background-color: {AppStyles.CARD_BACKGROUND};
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 6px;
            padding: {AppStyles.PADDING_MEDIUM}px;
            margin-bottom: {AppStyles.SPACING_MEDIUM}px;
        }}
        
        /* Search Input */
        QLineEdit[inputRole="search"] {{
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 6px;
            padding: {AppStyles.PADDING_MEDIUM}px;
            font-size: {AppStyles.FONT_MEDIUM};
            min-height: 40px;
            background-color: white;
        }}
        
        QLineEdit[inputRole="search"]:focus {{
            border: 2px solid {AppStyles.PRIMARY_COLOR};
            background-color: #fcfcff;
        }}
        
        /* Action Buttons */
        QPushButton[buttonRole="search"] {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
            border: none;
            border-radius: 6px;
            padding: {AppStyles.PADDING_MEDIUM}px 24px;
            font-size: {AppStyles.FONT_NORMAL};
            font-weight: 600;
            min-height: 40px;
            min-width: 120px;
        }}
        
        QPushButton[buttonRole="search"]:hover {{
            background-color: #375a7f;
            transform: translateY(-1px);
        }}
        
        QPushButton[buttonRole="clear"] {{
            background-color: {AppStyles.WARNING_COLOR};
            color: {AppStyles.TEXT_PRIMARY};
            border: none;
            border-radius: 6px;
            padding: {AppStyles.PADDING_MEDIUM}px 24px;
            font-size: {AppStyles.FONT_NORMAL};
            font-weight: 600;
            min-height: 40px;
            min-width: 120px;
        }}
        
        QPushButton[buttonRole="clear"]:hover {{
            background-color: #f4b942;
        }}
        
        /* Table Styling */
        QTableWidget {{
            background-color: white;
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 8px;
            gridline-color: {AppStyles.BORDER_COLOR};
            font-size: {AppStyles.FONT_NORMAL};
            selection-background-color: {AppStyles.PRIMARY_COLOR};
            alternate-background-color: #f8f9fc;
        }}
        
        QTableWidget::item {{
            padding: 12px 8px;
            border-bottom: 1px solid {AppStyles.BORDER_COLOR};
        }}
        
        QTableWidget::item:selected {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
        }}
        
        QTableWidget::item:hover {{
            background-color: #f1f3f4;
        }}
        
        QHeaderView::section {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
            padding: 12px 8px;
            border: none;
            font-weight: bold;
            font-size: {AppStyles.FONT_NORMAL};
        }}
        
        /* Pagination Section */
        QFrame[frameRole="pagination"] {{
            background-color: {AppStyles.CARD_BACKGROUND};
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 6px;
            padding: {AppStyles.PADDING_MEDIUM}px;
            margin-top: {AppStyles.SPACING_MEDIUM}px;
        }}
        
        QPushButton[buttonRole="pagination"] {{
            background-color: {AppStyles.INFO_COLOR};
            color: white;
            border: none;
            border-radius: 6px;
            padding: {AppStyles.PADDING_SMALL}px 20px;
            font-size: {AppStyles.FONT_NORMAL};
            font-weight: 600;
            min-height: 36px;
            min-width: 100px;
        }}
        
        QPushButton[buttonRole="pagination"]:hover:enabled {{
            background-color: #2c9faf;
        }}
        
        QPushButton[buttonRole="pagination"]:disabled {{
            background-color: #6c757d;
            color: #adb5bd;
        }}
        
        /* Page Info Label */
        QLabel[labelRole="pageInfo"] {{
            color: {AppStyles.TEXT_PRIMARY};
            font-size: {AppStyles.FONT_MEDIUM};
            font-weight: 600;
            padding: 0 20px;
        }}

         /* Action Container Widget */
        QWidget[widgetRole="actionContainer"] {{
            background-color: transparent;
            border: none;
        }}
        
        /* Action Buttons in Table */
        QPushButton[actionRole="edit"] {{
            background-color: {AppStyles.SUCCESS_COLOR};
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            padding: 0px;
            min-width: 36px;
            max-width: 36px;
            min-height: 30px;
            max-height: 30px;

        }}
        
        QPushButton[actionRole="edit"]:hover {{
            background-color: #17a673;
            transform: scale(1.05);
        }}
        
        QPushButton[actionRole="delete"] {{
            background-color: {AppStyles.DANGER_COLOR};
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            padding: 0px;
            min-width: 30px;
            max-width: 30px;
            min-height: 30px;
            max-height: 30px;
        }}
        
        QPushButton[actionRole="delete"]:hover {{
            background-color: #c0392b;
            transform: scale(1.05);
        }}
        
        /* Statistics Labels */
        QLabel[labelRole="stats"] {{
            background-color: {AppStyles.INFO_COLOR};
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: {AppStyles.FONT_MEDIUM};
        }}
        """

    def init_ui(self):
        """Initialize the user interface with proper styling"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(AppStyles.SPACING_MEDIUM)
        main_layout.setContentsMargins(
            AppStyles.PADDING_LARGE, AppStyles.PADDING_LARGE,
            AppStyles.PADDING_LARGE, AppStyles.PADDING_LARGE
        )
        
        # Header Section
        header_frame = self._create_header_section()
        main_layout.addWidget(header_frame)
        
        # Search Section
        search_frame = self._create_search_section()
        main_layout.addWidget(search_frame)
        
        # Table Section
        self._create_table_section()
        main_layout.addWidget(self.table)
        
        # Pagination Section
        pagination_frame = self._create_pagination_section()
        main_layout.addWidget(pagination_frame)
        
        self.setLayout(main_layout)

    def _create_header_section(self):
        """Create header with title and statistics"""
        header_frame = QFrame()
        header_frame.setProperty("frameRole", "header")
        layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("👥 सदस्य व्यवस्थापन केन्द्र")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {AppStyles.PRIMARY_COLOR}; border: none; padding: 0;")
        
        # Statistics
        self.stats_label = QLabel("कुल सदस्यहरू: 0")
        self.stats_label.setProperty("labelRole", "stats")
        
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(self.stats_label)
        
        header_frame.setLayout(layout)
        return header_frame

    def _create_search_section(self):
        """Create search section with input and buttons"""
        search_frame = QFrame()
        search_frame.setProperty("frameRole", "search")
        layout = QHBoxLayout()
        
        # Search label
        search_label = QLabel("🔍 खोज्नुहोस्:")
        search_label.setStyleSheet(f"""
            color: {AppStyles.TEXT_PRIMARY};
            font-weight: 600;
            font-size: {AppStyles.FONT_MEDIUM};
            border: none;
            padding: 0;
        """)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setProperty("inputRole", "search")
        self.search_input.setPlaceholderText("सदस्यको नाम वा सदस्य नम्बरले खोज्नुहोस्...")
        self.search_input.returnPressed.connect(self.search_member)
        
        # Search button
        search_btn = QPushButton("🔍 Search Member")
        search_btn.setProperty("buttonRole", "search")
        search_btn.clicked.connect(self.search_member)
        
        # Clear button
        clear_btn = QPushButton("❌ Clear Search")
        clear_btn.setProperty("buttonRole", "clear")
        clear_btn.clicked.connect(self.clear_search)
        
        layout.addWidget(search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(search_btn)
        layout.addWidget(clear_btn)
        
        search_frame.setLayout(layout)
        return search_frame

    def _create_table_section(self):
        """Create and configure the member table"""
        self.table = QTableWidget()
        self.table.setColumnCount(19)
        
        headers = [
            "सदस्य नं", "सदस्यको नाम", "फोन", "जन्ममिति (वि.सं.)", "ना.प्र. नं.",
            "ठेगाना", "वार्ड नं", "बाबुको नाम", "बाजेको नाम",
            "पति/पत्नीको नाम", "ईमेल", "पेशा", "फेसबुक", "Whatsapp/Viber", 
            "व्यवसाय", "व्यवसाय ठेगाना", "रोजगारदाता", "ठेगाना (रोजगारदाता)", "Actions"
        ]
        
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(18, QHeaderView.Fixed)
        self.table.setColumnWidth(18, 120)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)

        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 44)

    def _create_pagination_section(self):
        """Create pagination controls"""
        pagination_frame = QFrame()
        pagination_frame.setProperty("frameRole", "pagination")
        layout = QHBoxLayout()
        
        # Previous button
        self.prev_btn = QPushButton("⏮️ अघिल्लो")
        self.prev_btn.setProperty("buttonRole", "pagination")
        self.prev_btn.clicked.connect(self.prev_page)
        
        # Page info
        self.page_info = QLabel("पृष्ठ 1 of 1")
        self.page_info.setProperty("labelRole", "pageInfo")
        self.page_info.setAlignment(Qt.AlignCenter)
        
        # Next button
        self.next_btn = QPushButton("अर्को ⏭️")
        self.next_btn.setProperty("buttonRole", "pagination")
        self.next_btn.clicked.connect(self.next_page)
        
        # Results info
        self.results_info = QLabel("")
        self.results_info.setStyleSheet(f"""
            color: {AppStyles.TEXT_SECONDARY};
            font-size: {AppStyles.FONT_SMALL};
            padding: 0;
            border: none;
        """)
        
        layout.addWidget(self.prev_btn)
        layout.addStretch()
        layout.addWidget(self.results_info)
        layout.addStretch()
        layout.addWidget(self.page_info)
        layout.addStretch()
        layout.addWidget(self.next_btn)
        
        pagination_frame.setLayout(layout)
        return pagination_frame

    def clear_search(self):
        """Clear search input and reload all members"""
        self.search_input.clear()
        self.load_members()

    def search_member(self):
        """Search/filter members based on text input"""
        keyword = self.search_input.text().strip().lower()
        if not keyword:
            self.load_members()
            return
            
        def safe_search(value, keyword):
            """Safely search in a value that might be None"""
            if value is None:
                return False
            return keyword in str(value).lower()
            
        self.filtered_members = [
            m for m in self.all_members
            if (safe_search(m.get('member_name'), keyword) or 
                safe_search(m.get('member_number'), keyword) or
                safe_search(m.get('phone'), keyword) or
                safe_search(m.get('citizenship_no'), keyword) or
                safe_search(m.get('address'), keyword) or
                safe_search(m.get('father_name'), keyword) or
                safe_search(m.get('grandfather_name'), keyword))
        ]

        self.current_page = 1
        self.update_pagination()

    def load_members(self):
        """Load all members into memory and setup pagination"""
        try:
            self.all_members = fetch_all_members()
            self.filtered_members = self.all_members.copy()
            self.current_page = 1
            self.update_pagination()
            self.update_statistics()
        except Exception as e:
            QMessageBox.critical(self, "त्रुटि", f"सदस्यहरू लोड गर्न सकिएन: {str(e)}")

    def update_statistics(self):
        """Update statistics label"""
        total_count = len(self.all_members)
        filtered_count = len(self.filtered_members)
        
        if total_count == filtered_count:
            self.stats_label.setText(f"कुल सदस्यहरू: {total_count}")
        else:
            self.stats_label.setText(f"खोज परिणाम: {filtered_count} / {total_count}")

    def update_pagination(self):
        """Update table data and pagination controls"""
        total_records = len(self.filtered_members)
        self.total_pages = max(1, (total_records + PAGE_SIZE - 1) // PAGE_SIZE)
        
        start_index = (self.current_page - 1) * PAGE_SIZE
        end_index = min(start_index + PAGE_SIZE, total_records)
        page_members = self.filtered_members[start_index:end_index]
        
        self.populate_table(page_members)
        
        # Update pagination info
        self.page_info.setText(f"पृष्ठ {self.current_page} of {self.total_pages}")
        self.results_info.setText(f"देखाइएको: {start_index + 1}-{end_index} of {total_records}")
        
        # Enable/disable pagination buttons
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)
        
        # Update statistics
        self.update_statistics()

    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_pagination()

    def populate_table(self, members):
        """Populate table with member data"""
        self.table.setRowCount(0)
        self.table.setSortingEnabled(False)  # Disable sorting during population
        
        for row_num, member in enumerate(members):
            self.table.insertRow(row_num)
            
            # Member data columns
            columns_data = [
                member.get('member_number', ''),
                member.get('member_name', ''),
                member.get('phone', ''),
                member.get('dob_bs', ''),
                member.get('citizenship_no', ''),
                member.get('address', ''),
                member.get('ward_no', ''),
                member.get('father_name', ''),
                member.get('grandfather_name', ''),
                member.get('spouse_name', ''),
                member.get('email', ''),
                member.get('profession', ''),
                member.get('facebook_detail', ''),
                member.get('whatsapp_detail', ''),
                member.get('business_name', ''),
                member.get('business_address', ''),
                member.get('job_name', ''),
                member.get('job_address', '')
            ]
            
            # Populate data columns
            for col, value in enumerate(columns_data):
                item = QTableWidgetItem(str(value) if value else "—")
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_num, col, item)
            
            # Create action buttons
            action_widget = self._create_action_buttons(member)
            self.table.setCellWidget(row_num, 18, action_widget)
        
        self.table.setSortingEnabled(True)  # Re-enable sorting

    def _create_action_buttons(self, member):
        """Create action buttons for each row with proper layout"""
        # Create container widget
        container = QWidget()
        container.setProperty("widgetRole", "actionContainer")
        container.setFixedHeight(36)

        # Create horizontal layout
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(2)
        # layout.setAlignment(Qt.AlignCenter)
        # Add stretch before buttons to push them to center
        layout.addStretch()

        # Get icon path with proper path handling
        icon_path = os.path.join(os.path.dirname(__file__), "..", "icons")

        # Create edit button
        edit_btn = QPushButton()
        edit_btn.setProperty("actionRole", "edit")
        edit_btn.setToolTip("सम्पादन गर्नुहोस्")
        edit_btn.setFixedSize(26, 26)
        edit_btn.setCursor(Qt.PointingHandCursor)

        # Try to load icon, fallback to test if not found
        edit_icon_path = os.path.join(icon_path, "edit.png")
        if os.path.exists(edit_icon_path):
            edit_icon = QIcon(edit_icon_path)
            edit_btn.setIcon(edit_icon)
            edit_btn.setIconSize(QSize(16, 16))
        else:
            edit_btn.setText("✏️") # Fallback to emoji/text
            edit_btn.setStyleSheet("font-size: 12px;")
        
        edit_btn.clicked.connect(lambda: self.edit_member_dialog(member))

        # Create delete button
        delete_btn = QPushButton()
        delete_btn.setProperty("actionRole", "delete")
        delete_btn.setToolTip("हटाउनुहोस")
        delete_btn.setFixedSize(26, 26)
        delete_btn.setCursor(Qt.PointingHandCursor)

        # Try to load icon, fallback to text if not found
        delete_icon_path = os.path.join(icon_path, "delete.png")
        if os.path.exists(delete_icon_path):
            delete_icon = QIcon(delete_icon_path)
            delete_btn.setIcon(delete_icon)
            delete_btn.setIconSize(QSize(16, 16))
        else: 
            delete_btn.setText("🗑️")
            delete_btn.setStyleSheet("font_size: 12px;")
        
        delete_btn.clicked.connect(lambda: self.delete_member(member))

        # Add buttons to layout
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)

        # Add stretch after buttons to center them perfectly
        layout.addStretch()

        return container


    def edit_member_dialog(self, member):
        """Open edit dialog for member"""
        # try:
        #     info_tab = PersonalInfoTab()
        #     info_tab.fill_form(member)
        #     info_tab.show()

        #     # Connect to a signal if availabe or just refresh after showing
        #     self.member_updated.emit()
        #     # self.load_members()  # Refresh the table
        # except Exception as e:
        #     QMessageBox.critical(self, "त्रुटि", f"सम्पादन संवाद खोल्न सकिएन: {str(e)}")

        try:
            # Create a proper dialog for editing
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Edit {member.get('member_name', '')}")
            dialog.setModal(True)
            dialog.resize(800, 600)

            layout = QVBoxLayout()

            # Create and fill the info tab
            info_tab = PersonalInfoTab()
            info_tab.fill_form(member)

            # Add save button
            btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

            btn_box.accepted.connect(dialog.accept)
            btn_box.rejected.connect(dialog.reject)

            layout.addWidget(info_tab)
            layout.addWidget(btn_box)
            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                self.member_updated.emit()
                self.load_members()
        except Exception as e:
            QMessageBox.critical(self, "त्रुटि", f"सम्पादन संवाद खोल्न सकिएन: {str(e)}")


    def delete_member(self, member):
        """Delete member with confirmation"""
        # Create custom message box with proper styling
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("पुष्टि गर्नुहोस्")
        msg_box.setText("के तपाईं निश्चित हुनुहुन्छ?")
        msg_box.setInformativeText(
            f"सदस्य {member.get('member_number', '')} ({member.get('member_name', '')}) "
            "लाई मेटाउन चाहनुहुन्छ? यो कार्य फिर्ता गर्न सकिँदैन।"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.setStyleSheet(AppStyles.get_messagebox_stylesheet())
        
        # Customize button text
        msg_box.button(QMessageBox.Yes).setText("हो, मेटाउनुहोस्")
        msg_box.button(QMessageBox.No).setText("रद्द गर्नुहोस्")
        
        if msg_box.exec_() == QMessageBox.Yes:
            try:
                delete_member(member.get('member_number'))
                
                # Success message
                success_msg = QMessageBox(self)
                success_msg.setWindowTitle("सफल")
                success_msg.setText("सदस्य सफलतापूर्वक मेटाइयो!")
                success_msg.setInformativeText(f"सदस्य {member.get('member_number')} मेटाइएको छ।")
                success_msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
                success_msg.exec_()
                
                self.member_updated.emit()
                self.load_members()  # Refresh the table
                
            except Exception as e:
                QMessageBox.critical(self, "त्रुटि", f"सदस्य मेट्न सकिएन: {str(e)}")

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_F5:
            self.load_members()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.search_input.hasFocus():
                self.search_member()
        super().keyPressEvent(event)

    def closeEvent(self, event):
        """Handle dialog close event"""
        self.member_updated.emit()  # Notify parent to refresh
        event.accept()
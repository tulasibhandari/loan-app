from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QTableView, QHBoxLayout, QMessageBox, QGroupBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from context import current_session
from models.project_model import save_project, fetch_projects_by_member
from models.database import get_connection, get_database_path
from styles.app_styles import AppStyles
from signal_bus import signal_bus

class ProjectTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("परियोजना विवरण")
        self.selected_project_id = None  # Track selected project
        self.model = None  # Initialize model to avoid None issues
        self.setup_ui()

        signal_bus.session_updated.connect(self.update_header)
        

    def setup_ui(self):
        # Apply global styles
        self.setStyleSheet(AppStyles.get_main_stylesheet())

        self.layout = QVBoxLayout()  # Store layout for adding placeholders
        self.layout.setContentsMargins(
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM,
            AppStyles.PADDING_MEDIUM
        )
        self.layout.setSpacing(AppStyles.SPACING_MEDIUM)

        # Member Header Group
        header_group = QGroupBox("📋 सदस्य विवरण")
        header_group.setStyleSheet(f"""
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
        header_layout = QFormLayout()
        header_layout.setVerticalSpacing(AppStyles.SPACING_SMALL)
        header_layout.setHorizontalSpacing(AppStyles.SPACING_MEDIUM)

        self.member_number_label = QLabel()
        self.member_number_label.setStyleSheet(f"""
            font-size: {AppStyles.FONT_NORMAL};
            color: {AppStyles.TEXT_PRIMARY};
            padding: 4px;
        """)
        self.member_name_label = QLabel()
        self.member_name_label.setStyleSheet(f"""
            font-size: {AppStyles.FONT_NORMAL};
            color: {AppStyles.TEXT_PRIMARY};
            padding: 4px;
        """)
        header_layout.addRow("सदस्य नं:", self.member_number_label)
        header_layout.addRow("सदस्यको नाम:", self.member_name_label)
        header_group.setLayout(header_layout)
        self.layout.addWidget(header_group)
        self.update_header()

        # Form Group
        form_group = QGroupBox("🛠 परियोजनाको विवरण भर्नुहोस्")
        form_group.setStyleSheet(f"""
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

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(AppStyles.SPACING_SMALL)
        form_layout.setHorizontalSpacing(AppStyles.SPACING_MEDIUM)

        # Input fields
        self.project_name = QLineEdit()
        self.self_investment = QLineEdit()
        self.requested_loan_amount = QLineEdit()
        self.total_cost = QLineEdit()
        self.remarks = QLineEdit()

        # Set consistent heights
        for field in [self.project_name, self.self_investment,
                      self.requested_loan_amount, self.total_cost,
                      self.remarks]:
            field.setMinimumHeight(AppStyles.INPUT_HEIGHT)

        form_layout.addRow("परियोजनाको नाम:", self.project_name)
        form_layout.addRow("आफूले लगानी गर्ने रकम:", self.self_investment)
        form_layout.addRow("ऋण माग रकम:", self.requested_loan_amount)
        form_layout.addRow("कुल लागत:", self.total_cost)
        form_layout.addRow("कैफियत:", self.remarks)

        # Save button
        self.save_button = QPushButton("💾 Save Project Info")
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
        self.save_button.clicked.connect(self.save_data)

        # Button container for better alignment
        button_container = QHBoxLayout()
        button_container.addStretch()
        button_container.addWidget(self.save_button)
        button_container.addStretch()

        form_layout.addRow(button_container)
        form_group.setLayout(form_layout)
        self.layout.addWidget(form_group)

        # Project Table
        self.layout.addWidget(QLabel("📋 Projects:"))
        self.project_table = QTableView()
        self.project_table.setSelectionMode(QTableView.SingleSelection)
        self.project_table.setSelectionBehavior(QTableView.SelectRows)
        self.project_table.setStyleSheet(f"""
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
        self.project_table.setSortingEnabled(True)
        self.layout.addWidget(self.project_table)

        self.setLayout(self.layout)
        self.load_projects()

    def update_header(self):
        member_number = current_session.get("member_number", "")
        member_name = current_session.get("member_name", "")
        self.member_number_label.setText(member_number if member_number else "No member selected")
        self.member_name_label.setText(member_name if member_name else "No member selected")

    def load_projects(self):
        # Update header
        self.update_header()

        # Clear any existing placeholder labels
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QLabel) and widget.text().startswith("No projects found"):
                self.layout.removeWidget(widget)
                widget.deleteLater()

        # Get member_number from current_session
        member_number = current_session.get("member_number", "")
        if not member_number:
            self.layout.addWidget(QLabel("No member selected. Please select a member."))
            return

        # Initialize QSqlDatabase
        db = QSqlDatabase.addDatabase("QSQLITE", "project_tab_conn")
        db.setDatabaseName(get_database_path())
        if not db.open():
            QMessageBox.critical(self, "Error", "Failed to connect to database", QMessageBox.Ok)
            self.layout.addWidget(QLabel("No projects found or database error."))
            return

        # Initialize QSqlTableModel
        self.model = QSqlTableModel(self, db)

        # Set query for projects
        query = QSqlQuery(db)
        query_str = """
            SELECT p.id, p.member_number, m.member_name, p.project_name, p.self_investment,
                   p.requested_loan_amount, p.total_cost, p.remarks
            FROM collateral_projects p
            JOIN member_info m ON p.member_number = m.member_number
            WHERE p.member_number = ?
        """
        query.prepare(query_str)
        query.addBindValue(member_number)
        if not query.exec_():
            QMessageBox.critical(self, "Error", f"Query failed: {query.lastError().text()}", QMessageBox.Ok)
            self.layout.addWidget(QLabel("No projects found or query error."))
            db.close()
            return

        self.model.setQuery(query)

        # Set headers for table
        headers = ["ID", "सदस्य नं", "सदस्यको नाम", "परियोजना", "आफूले लगानी गर्ने रकम",
                   "ऋण माग", "कुल लागत", "कैफियत"]
        for col, header in enumerate(headers):
            self.model.setHeaderData(col, Qt.Horizontal, header)

        self.project_table.setModel(self.model)
        self.project_table.hideColumn(0)  # Hide id column
        self.project_table.resizeColumnsToContents()

        # Connect selection signal AFTER setting the model
        self.project_table.selectionModel().selectionChanged.connect(self.on_row_selected)

        # Show placeholder if no data
        if self.model.rowCount() == 0:
            self.layout.addWidget(QLabel("No projects found for this member."))

        db.close()

    def on_row_selected(self):
        # Get selected row
        selected = self.project_table.selectionModel().selectedRows()
        if not selected:
            self.clear_form()
            return

        row = selected[0].row()
        self.selected_project_id = self.model.data(self.model.index(row, 0))  # Project ID
        self.project_name.setText(self.model.data(self.model.index(row, 3)))  # project_name
        self.self_investment.setText(self.model.data(self.model.index(row, 4)))  # self_investment
        self.requested_loan_amount.setText(self.model.data(self.model.index(row, 5)))  # requested_loan_amount
        self.total_cost.setText(self.model.data(self.model.index(row, 6)))  # total_cost
        self.remarks.setText(self.model.data(self.model.index(row, 7)))  # remarks

    def save_data(self):
        member_number = current_session.get("member_number", "")
        if not member_number:
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.warning(self, "सदस्य चयन गर्नुहोस्", "कृपया सदस्य छान्नुहोस्।")
            return

        data = {
            "member_number": member_number,
            "project_name": self.project_name.text().strip(),
            "self_investment": self.self_investment.text().strip(),
            "requested_loan_amount": self.requested_loan_amount.text().strip(),
            "total_cost": self.total_cost.text().strip(),
            "remarks": self.remarks.text().strip(),
        }

        try:
            save_project(data)
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.information(self, "Saved", "✅ परियोजनाको विवरण सुरक्षित भयो।")
            self.clear_form()
            self.load_projects()
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet(AppStyles.get_messagebox_stylesheet())
            msg.critical(self, "Error", f"❌ Failed to save project data:\n{e}")

    def clear_form(self):
        self.selected_project_id = None
        self.project_name.clear()
        self.self_investment.clear()
        self.requested_loan_amount.clear()
        self.total_cost.clear()
        self.remarks.clear()
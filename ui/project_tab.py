from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QGroupBox
)
from context import current_session
from models.project_model import save_project, fetch_projects_by_member

class ProjectTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("परियोजना विवरण")

        layout = QVBoxLayout()
        # Apply styles
        self.setStyleSheet("""
            QWidget {
                    font-family: Arial;
                    font-size: 14px
           }
            
            QLabel {
                    color: #333;
                    min-width: 150px;
            }
            QLineEdit, QDateEdit {
                           border: 1px solid #ddd;
                           border-radius: 4px;
                           padding: 8px;
                           min-width:250px;
                           background-color: white;
            }
            QLineEdit:focus, QDateEdit:focus {
                        border: 1px solid #3498db;
            }
            QPushButton {
                           background-color: #4CAF50;
                           color: white;
                           border: none;
                           padding: 10px 15px;
                           border-radius: 4px;
                           min-width: 100px;
                           }
            QPushButton:hover {
                           background-color: #45a049;
                           }                        
        """)
        
        form_group = QGroupBox("🛠 परियोजनाको विवरण भर्नुहोस्")
        form_layout = QFormLayout()

        self.project_name = QLineEdit()
        self.self_investment = QLineEdit()
        self.requested_loan_amount = QLineEdit()
        self.total_cost = QLineEdit()
        self.remarks = QLineEdit()


        form_layout.addRow("परियोजनाको नाम:", self.project_name)
        form_layout.addRow("आफूले लगानी गर्ने रकम:", self.self_investment)
        form_layout.addRow("ऋण माग रकम:", self.requested_loan_amount)
        form_layout.addRow("कुल लागत:", self.total_cost)
        form_layout.addRow("कैफियत:", self.remarks)

        self.save_button = QPushButton("💾 Save Project Info")
        self.save_button.clicked.connect(self.save_data)

        form_layout.addRow(self.save_button)
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Table to display saved project data
        self.project_table = QTableWidget()
        self.project_table.setColumnCount(5)
        self.project_table.setHorizontalHeaderLabels(
            ["सदस्य नं", "परियोजना", "आफूले लगानी गर्ने रकम", "ऋण माग", "कुल लागत", "कैफियत"]
        )
        layout.addWidget(self.project_table)

        self.setLayout(layout)

        self.load_projects()

    def save_data(self):
        member_number = current_session.get("member_number", "")
        if not member_number:
            QMessageBox.warning(self, "सदस्य चयन गर्नुहोस्", "कृपया सदस्य छान्नुहोस्।")
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
            QMessageBox.information(self, "Saved", "✅ परियोजनाको विवरण सुरक्षित भयो।")
            self.clear_form()
            self.load_projects()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Failed to save project data:\n{e}")

    def clear_form(self):
        self.project_name.clear()
        self.self_investment.clear()
        self.requested_loan_amount.clear()
        self.total_cost.clear()
        self.remarks.clear()

    def load_projects(self):
        self.project_table.setRowCount(0)
        member_number = current_session.get("member_number", "")
        if not member_number:
            return
        projects = fetch_projects_by_member(member_number)
        for row_idx, project in enumerate(projects):
            self.project_table.insertRow(row_idx)
            self.project_table.setItem(row_idx, 0, QTableWidgetItem(project["member_number"]))
            self.project_table.setItem(row_idx, 1, QTableWidgetItem(project["project_name"]))
            self.project_table.setItem(row_idx, 2, QTableWidgetItem(project["self_investment"]))
            self.project_table.setItem(row_idx, 3, QTableWidgetItem(project["requested_loan_amount"]))
            self.project_table.setItem(row_idx, 4, QTableWidgetItem(project["total_cost"]))
            self.project_table.setItem(row_idx, 5, QTableWidgetItem(project["remarks"]))

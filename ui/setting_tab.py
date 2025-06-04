from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from ui.add_user_dialog import AddUserDialog

from services.import_service import import_members_from_excel

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        import_member_btn = QPushButton("📥 Import Members from Excel")
        import_member_btn.clicked.connect(self.import_members_from_excel)
        layout.addWidget(import_member_btn)


        add_user_btn = QPushButton("➕ Add New User")
        add_user_btn.clicked.connect(self.show_add_user_dialog)
        layout.addWidget(add_user_btn)

        self.setLayout(layout)

    def import_members_from_excel(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        
        if path:
            print(f"📁 Importing members from: {path}")
            try:
                count = import_members_from_excel(path)
                QMessageBox.information(self, "Import Complete", f"{count} सदस्यहरू सफलतापूर्वक इम्पोर्ट गरियो।")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"⚠ त्रुटि भयो:\n{str(e)}")


            

    def show_add_user_dialog(self):
        dialog = AddUserDialog()
        dialog.exec_()

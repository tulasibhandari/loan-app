# ui/collateral_tab.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea, QFormLayout, QLineEdit, QPushButton)

from models.collateral_model import save_collateral_info
from utils.converter import convert_to_nepali_digits

class CollateralTab(QWidget):
    def __init__(self):
        super().__init__()
        
       
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        form_layout = QFormLayout(content)
        scroll.setWidget(content)


        self.monthly_saving = QLineEdit()
        self.child_saving = QLineEdit()
        
        # Validate float input
        # validator = QDoubleValidator(0.0, 1000000.0, 2)

        for field in [self.monthly_saving, self.child_saving]:
            # field.setValidator(validator)
            field.editingFinished.connect(self.update_total_saving)

        form_layout.addRow("Monthly Saving:", self.monthly_saving)
        form_layout.addRow("Child Saving:", self.child_saving)
        
        
        self.total_saving = QLineEdit()
        self.total_saving.setReadOnly(True)
        form_layout.addRow("Total Saving:", self.total_saving)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.save_collateral_data)
        form_layout.addRow(next_button)

        # --Setting layout --
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def update_total_saving(self):
        m = float(self.monthly_saving.text() or 0)
        c = float(self.child_saving.text() or 0)
        total = m + c
        self.total_saving.setText(f"{total:.2f}")
    

    def save_collateral_data(self):
        try:
            monthly = float(self.monthly_saving.text())
            child = float(self.child_saving.text())
            total = monthly + child

            data = {
                'monthly_saving': convert_to_nepali_digits(monthly),
                'child_saving': convert_to_nepali_digits(child),
                'total_saving': convert_to_nepali_digits(total)
            }

            save_collateral_info(data)
            print("✅ Collateral data saved successfully!")

        except Exception as e:
            print("❌ Error saving collateral data:", e)


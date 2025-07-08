"""
Standardized message boxes with uniform styling
"""
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from styles.app_styles import AppStyles

class StandardMessageBox:
    """Factory class for creating standardized message boxes"""
    
    @staticmethod
    def _create_base_msgbox(parent, title, text, icon_type):
        """Create base message box with standard styling"""
        msgbox = QMessageBox(parent)
        msgbox.setWindowTitle(title)
        msgbox.setIcon(icon_type)
        
        # Apply styles
        msgbox.setStyleSheet(AppStyles.get_messagebox_stylesheet())
        
        # Set fixed size for consistency
        msgbox.setFixedSize(AppStyles.MSGBOX_WIDTH, AppStyles.MSGBOX_HEIGHT)
        
        # Center text with proper formatting
        msgbox.setTextFormat(Qt.RichText)
        msgbox.setText(f"<div style='text-align: center; padding: 10px; font-size: 14px;'>{text}</div>")
        
        return msgbox
    
    @staticmethod
    def information(parent, title, text):
        """Create standardized information message box"""
        msgbox = StandardMessageBox._create_base_msgbox(
            parent, title, text, QMessageBox.Information
        )
        msgbox.exec_()
    
    @staticmethod
    def warning(parent, title, text):
        """Create standardized warning message box"""
        msgbox = StandardMessageBox._create_base_msgbox(
            parent, title, text, QMessageBox.Warning
        )
        msgbox.exec_()
    
    @staticmethod
    def critical(parent, title, text):
        """Create standardized error message box"""
        msgbox = StandardMessageBox._create_base_msgbox(
            parent, title, text, QMessageBox.Critical
        )
        msgbox.exec_()
    
    @staticmethod
    def question(parent, title, text):
        """Create standardized question message box"""
        msgbox = StandardMessageBox._create_base_msgbox(
            parent, title, text, QMessageBox.Question
        )
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgbox.setDefaultButton(QMessageBox.No)
        return msgbox.exec_() == QMessageBox.Yes
"""
Centralized system for uniform PyQt5 application design
"""
class AppStyles:
    """Central styling class for consistent UI Design"""
    
    # Color Palette
    PRIMARY_COLOR = "#4e73df"
    SUCCESS_COLOR = "#1cc88a"
    WARNING_COLOR = "#f6c23e"
    DANGER_COLOR = "#e74a3b"
    INFO_COLOR = "#36b9cc"

    BACKGROUND_COLOR = "#f8f9fc"
    CARD_BACKGROUND = "#ffffff"
    TEXT_PRIMARY = "#5a5c69"
    TEXT_SECONDARY = "#858796"
    BORDER_COLOR = "#e3e6f0"
    HOVER_BORDER = "#bac8f3"

    # Status Bar colors
    STATUS_BG = "#ffffff"
    STATUS_TEXT = "#5a5c69"
    STATUS_BORDER = "#e3e6f0"

    # Font Sizes
    FONT_LARGE = "18px"
    FONT_MEDIUM = "16px"
    FONT_NORMAL = "14px"
    FONT_SMALL = "12px"

    # Spacing
    SPACING_LARGE = 30
    SPACING_MEDIUM = 20
    SPACING_SMALL = 10
    PADDING_LARGE = 20
    PADDING_MEDIUM = 15
    PADDING_SMALL = 10

    # Standard Sizes
    BUTTON_HEIGHT = 35
    INPUT_HEIGHT = 35
    CARD_MIN_WIDTH = 300
    CARD_MIN_HEIGHT = 200

    # Message Box Sizes
    MSGBOX_WIDTH = 450
    MSGBOX_HEIGHT = 200

    @staticmethod
    def get_main_stylesheet():
        """ Global Stylesheet for the entire application"""
        return f"""
        /* Main Application Style */
        QMainWindow {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: {AppStyles.FONT_NORMAL}
        }}

        QWidget {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            color: {AppStyles.TEXT_PRIMARY};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        /* Menu Bar Style */
        QMenuBar {{
            background-color: {AppStyles.CARD_BACKGROUND};
            color: {AppStyles.TEXT_PRIMARY};
            border-bottom: 1px solid {AppStyles.BORDER_COLOR};
            padding: 4px;
            font-size: {AppStyles.FONT_NORMAL};
        }}

        QMenuBar::item {{
            background-color: transparent;
            padding: 8px 12px;
            border-radius: 4px;
            font-weight: 500;
        }}

        QMenuBar::item:selected {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
        }}

        QMenuBar::item:pressed {{
            background-color: #375a7f;
        }}

        QMenu {{
            background-color: {AppStyles.CARD_BACKGROUND};
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 6px;
            padding: 4px;
            font-size: {AppStyles.FONT_NORMAL}
        }}

        QMenu::item {{
            padding: 8px 16px;
            border-radius: 4px;
            margin: 2px;
        }}

        QMenu::item:selected {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
        }}

        /* STATUS BAR Styles */
        QStatusBar {{
            background-color: {AppStyles.STATUS_BG};
            color: {AppStyles.STATUS_TEXT};
            border-top: 1px solid {AppStyles.STATUS_BORDER};
            font-size: {AppStyles.FONT_NORMAL};
            padding: 4px
        }}

        QStatusBar QLabel {{
            background-color: transparent;
            color: {AppStyles.STATUS_TEXT};
            padding: 6px 12px;
            margin: 2px;
            border-radius: 4px;
            font-weight: 500;
        }}
        
        QStatusBar QLabel[statusType="user"] {{
            background-color: {AppStyles.INFO_COLOR};
            color: white;
        }}

        QStatusBar QLabel[statusType="date"] {{
            background-color: {AppStyles.WARNING_COLOR};
            color: {AppStyles.TEXT_PRIMARY};
        }}

        /* Tab Widget Styles */
        QTabWidget::pane {{
            border: 1px solid {AppStyles.BORDER_COLOR};
            background-color: {AppStyles.CARD_BACKGROUND};
            border-radius: 6px;
            margin-top: -1px;
        }}

        QTabWidget::tab-bar {{
            alignment: left;
        }}

        QTabBar::tab {{
            background-color: {AppStyles.BACKGROUND_COLOR}; 
            color: {AppStyles.TEXT_SECONDARY};
            padding: 12px 20px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-bottom: none;
            font-size: {AppStyles.FONT_NORMAL};
            font-weight: 500;
            min-width: 120px;
        }}

        QTabBar::tab:selected {{
            background-color:{AppStyles.CARD_BACKGROUND};
            color: {AppStyles.TEXT_PRIMARY};
            border-bottom: 2px solid {AppStyles.PRIMARY_COLOR};
            font-weight: bold
        }}

        QTabBar::tab:hover:!selected {{
            background-color: #f1f3f4;
            color: {AppStyles.PRIMARY_COLOR};
        }}

        QTabBar::tab:first {{
            margin-left: 0;
        }}

        /* Standard Buttons */
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

        QPushButton:disabled {{
            background-color: #6c757d;
            color: #adb5bd; 
        }}
        
        /* Input Fields */
        QLineEdit, QTextEdit, QComboBox {{
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 4px;
            padding: 8px 12px;
            font-size: {AppStyles.FONT_NORMAL};
            min-height: {AppStyles.INPUT_HEIGHT}px;
            background-color: white;
        }}

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border: 2px solid {AppStyles.PRIMARY_COLOR};
            outline: none;
        }}

        /* Tables */
        QTableWidget {{
            background-color: white;
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 6px;
            gridline-color: {AppStyles.BORDER_COLOR};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {AppStyles.BORDER_COLOR};
        }}
        
        QTableWidget::item:selected {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
        }}
        
        QHeaderView::section {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
            padding: 10px;
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-bottom: 2px solid {AppStyles.BORDER_COLOR};
            font-weight: bold;
            font-size: {AppStyles.FONT_NORMAL};
            min-height: 30px;
        }}
        
        QTableWidget::corner {{
            background-color: {AppStyles.PRIMARY_COLOR};
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-right: none;
            border-bottom: none;
        }}
        """
    
    @staticmethod
    def get_messagebox_stylesheet():
        """Stylesheet specifically for message boxes"""
        return f"""
        QMessageBox {{
            background-color: {AppStyles.CARD_BACKGROUND};
            color: {AppStyles.TEXT_PRIMARY};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: {AppStyles.FONT_NORMAL};
        }}
        
        QMessageBox QLabel {{
            color: {AppStyles.TEXT_PRIMARY};
            font-size: {AppStyles.FONT_NORMAL};
            padding: 15px;
            text-align: center;
        }}
        
        QMessageBox QPushButton {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            font-size: {AppStyles.FONT_NORMAL};
            font-weight: bold;
            min-width: 100px;
            min-height: 35px;
        }}
        
        QMessageBox QPushButton:hover {{
            background-color: #375a7f;
        }}
        """
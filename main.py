#!/usr/bin/env python3
"""
Loan Desktop Application - Main Entry Point
Properly configured for PyInstaller bundling
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon

from models.database import initialize_db
from models.user_model import create_user_table


# Add current directory to Python path for bundled app
if getattr(sys, 'frozen', False):
    # Running as bundled executable
    application_path = Path(sys._MEIPASS)
    os.chdir(sys._MEIPASS)
else:
    # Running as script
    application_path = Path(__file__).parent

# Add project root to Python path
sys.path.insert(0, str(application_path))

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle
        base_path = Path(sys._MEIPASS)
    else:
        # Development
        base_path = Path(__file__).parent
    
    return str(base_path / relative_path)

def get_database_path():
    """Get database path for both development and bundled app"""
    return resource_path('data/loan_app_bundle.db')

def setup_application():
    """Setup application with proper icons and settings"""
    app = QApplication(sys.argv)
    app.setApplicationName("Loan Desktop App")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Manakamana Saving & Credit Cooperative Society Pvt. Ltd.")
    
    # Set application icon for taskbar
    app_icon_path = resource_path('assets/icons/app_icon.ico')
    if os.path.exists(app_icon_path):
        app.setWindowIcon(QIcon(app_icon_path))
    
    return app

def main():
    initialize_db()
    """Main application entry point"""
    try:
        # Create application
        app = setup_application()

        main_window = None
        create_user_table()
        
        # Import windows
        from ui.main_window import MainWindow
        from ui.login_window import LoginWindow

        # handle successful login
        def handle_login_success(username):
            nonlocal main_window
            main_window =  MainWindow(username=username)

            # Set window icon
            window_icon_path = resource_path('assets/icons/window_icon.png')
            if os.path.exists(window_icon_path):
                main_window.setWindowIcon(QIcon(window_icon_path))
            
            main_window.showMaximized()
            login_window.close()

        # Create and show login window with callback
        login_window = LoginWindow(on_login_success=handle_login_success)
        login_window.show()

        sys.exit(app.exec_())

    except Exception as e:
        print(f"Application startup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
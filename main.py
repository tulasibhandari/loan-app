# main.py
import sys
from PyQt5.QtWidgets import QApplication

from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from models.init_models import initialize_all
# from models.alter_user_table import alter_users_table_add_fullname



def main():
    app = QApplication(sys.argv)
    initialize_all()
    # alter_users_table_add_fullname()
    
    # Hold reference globally
    app_window = {}

    def launch_main_app(username):
        app_window['main'] = MainWindow(username)
        app_window['main'].show()

    login = LoginWindow(on_login_success=launch_main_app)
    login.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


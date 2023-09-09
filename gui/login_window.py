from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from gui.main_window import MainWindow
from modules.database_connection import connect_to_db  # Import the connect_to_db function
import json

class LoginWindow(QtWidgets.QWidget):
    
    def __init__(self, config_file_path='config.json'):
        super().__init__()
        
        self.config_file_path = config_file_path
        self.initUI()
        
    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Login')

        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()

        # Username
        self.user_label = QtWidgets.QLabel('Username:')
        self.user_line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_line_edit)

        # Password
        self.password_label = QtWidgets.QLabel('Password:')
        self.password_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_line_edit)

        # Hostname
        self.hostname_label = QtWidgets.QLabel('Hostname:')
        self.hostname_line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.hostname_label)
        layout.addWidget(self.hostname_line_edit)

        # Port
        self.port_label = QtWidgets.QLabel('Port:')
        self.port_line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_line_edit)

        # Service Name
        self.service_name_label = QtWidgets.QLabel('Service Name:')
        self.service_name_line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.service_name_label)
        layout.addWidget(self.service_name_line_edit)

        # Login button
        self.login_button = QtWidgets.QPushButton('Login')
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Load pre-filled values from the config file
        self.load_prefilled_values()

    def load_prefilled_values(self):
        try:
            with open(self.config_file_path, 'r') as file:
                config_data = json.load(file)
            
            db_config = config_data.get('databaseConnection', {})
            
            self.user_line_edit.setText(db_config.get('username', ''))
            self.password_line_edit.setText(db_config.get('password', ''))
            self.hostname_line_edit.setText(db_config.get('hostname', ''))
            self.port_line_edit.setText(str(db_config.get('port', '')))
            self.service_name_line_edit.setText(db_config.get('service_name', ''))
        except FileNotFoundError:
            QMessageBox.warning(self, 'Config File Not Found', f'The config file at {self.config_file_path} could not be found.')
        except json.JSONDecodeError:
            QMessageBox.warning(self, 'Config File Error', 'The config file contains invalid JSON.')

    def check_login(self):
        # Get the input values
        username = self.user_line_edit.text()
        password = self.password_line_edit.text()
        hostname = self.hostname_line_edit.text()
        port = self.port_line_edit.text()
        service_name = self.service_name_line_edit.text()

        # Validate the inputs (add more validation as needed)
        if not username or not password or not hostname or not port or not service_name:
            QMessageBox.warning(self, 'Input Error', 'All fields are required.')
            return

        # Attempt to connect to the database
        try:
            connection = connect_to_db(username, password, hostname, service_name, port)
            QMessageBox.information(self, 'Success', 'Connected to the database successfully.')
            # Here, you can pass the connection object to your main window or other parts of your application
            self.main_window = MainWindow(connection)
            self.main_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Could not connect to the database: {e}')

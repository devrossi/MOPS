from PyQt5 import QtWidgets
import json
from modules import dbutils
from modules import file_operations

class LoadTestTab(QtWidgets.QWidget):
    
    def __init__(self, database):
        super().__init__()
        
        self.database = database

        # Load default values from JSON file
        with open('config.json') as f:
            self.config = json.load(f)

        self.initUI()
        
    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Create a notebook for the subtabs
        notebook = QtWidgets.QTabWidget(self)
        
        # Create the "Configuration" subtab
        frame_configuration = QtWidgets.QWidget()
        frame_configuration_layout = QtWidgets.QVBoxLayout(frame_configuration)
        
        # Schema Details section
        schema_details_group = QtWidgets.QGroupBox("Schema Details")
        schema_details_layout = QtWidgets.QFormLayout()
        
        self.entry_schema_name = QtWidgets.QLineEdit(self.config['schemaCreation']['schema_name'])
        self.entry_password = QtWidgets.QLineEdit(self.config['schemaCreation']['password'])
        self.entry_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.entry_tablespace_name = QtWidgets.QLineEdit(self.config['schemaCreation']['tablespace'])
        self.entry_tablespace_size = QtWidgets.QLineEdit(str(self.config['schemaCreation'].get('tablespace_size', '')))
        self.entry_tablespace_quota = QtWidgets.QLineEdit(str(self.config['schemaCreation'].get('tablespace_quota', '')))

        schema_details_layout.addRow('Schema Name:', self.entry_schema_name)
        schema_details_layout.addRow('Password:', self.entry_password)
        schema_details_layout.addRow('Tablespace Name:', self.entry_tablespace_name)
        schema_details_layout.addRow('Size (GB):', self.entry_tablespace_size)
        schema_details_layout.addRow('Quota (GB):', self.entry_tablespace_quota)
        
        schema_details_group.setLayout(schema_details_layout)
        frame_configuration_layout.addWidget(schema_details_group)

        # Privileges section
        privileges_group = QtWidgets.QGroupBox("Privileges")
        privileges_layout = QtWidgets.QVBoxLayout()
        
        self.check_dba = QtWidgets.QCheckBox('DBA')
        self.check_connect = QtWidgets.QCheckBox('CONNECT')
        self.check_quota = QtWidgets.QCheckBox('Quota')
        
        privileges_layout.addWidget(self.check_dba)
        privileges_layout.addWidget(self.check_connect)
        privileges_layout.addWidget(self.check_quota)
        
        privileges_group.setLayout(privileges_layout)
        frame_configuration_layout.addWidget(privileges_group)

        # Console section
        console_group = QtWidgets.QGroupBox("Console")
        console_layout = QtWidgets.QVBoxLayout()
        
        self.console = QtWidgets.QTextEdit()
        self.console.setReadOnly(True)
        
        console_layout.addWidget(self.console)
        
        console_group.setLayout(console_layout)
        frame_configuration_layout.addWidget(console_group)

        # Create and Validate buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        self.create_button = QtWidgets.QPushButton('Create')
        self.validate_button = QtWidgets.QPushButton('Validate')
        
        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.validate_button)
        
        frame_configuration_layout.addLayout(buttons_layout)

        # Add frame_configuration as a tab to the notebook
        notebook.addTab(frame_configuration, "Configuration")

        # Create the "Data Load" subtab
        frame_data_load = QtWidgets.QWidget()
        frame_data_load_layout = QtWidgets.QVBoxLayout(frame_data_load)

        # Manual section
        manual_group = QtWidgets.QGroupBox("Manual")
        manual_layout = QtWidgets.QFormLayout()
        
        self.entry_script_sql = QtWidgets.QLineEdit()
        self.browse_sql_button = QtWidgets.QPushButton('Browse')
        self.entry_directory = QtWidgets.QLineEdit()
        self.browse_directory_button = QtWidgets.QPushButton('Browse')
        
        manual_layout.addRow('Script (SQL):', self.entry_script_sql)
        manual_layout.addWidget(self.browse_sql_button)
        manual_layout.addRow('Directory:', self.entry_directory)
        manual_layout.addWidget(self.browse_directory_button)
        
        manual_group.setLayout(manual_layout)
        frame_data_load_layout.addWidget(manual_group)

        # Auto section
        auto_group = QtWidgets.QGroupBox("Auto")
        auto_layout = QtWidgets.QFormLayout()
        
        self.entry_schema_name_auto = QtWidgets.QLineEdit(self.config['schemaCreation']['schema_name'])
        self.entry_num_rows = QtWidgets.QLineEdit(str(self.config['dataLoad']['num_rows']))
        self.entry_num_threads = QtWidgets.QLineEdit(str(self.config['dataLoad']['num_threads']))
        self.entry_parallel = QtWidgets.QLineEdit(str(self.config['dataLoad']['parallel']))
        self.start_stop_button = QtWidgets.QPushButton('Start')
        
        auto_layout.addRow('Schema:', self.entry_schema_name_auto)
        auto_layout.addRow('Number of rows:', self.entry_num_rows)
        auto_layout.addRow('Number of threads:', self.entry_num_threads)
        auto_layout.addRow('Parallel:', self.entry_parallel)
        auto_layout.addWidget(self.start_stop_button)
        
        auto_group.setLayout(auto_layout)
        frame_data_load_layout.addWidget(auto_group)

        # Add frame_data_load as a tab to the notebook
        notebook.addTab(frame_data_load, "Data Load")

        # Set the notebook as the main layout
        layout.addWidget(notebook)
        self.setLayout(layout)

        # Connect the buttons to their respective methods
        self.create_button.clicked.connect(self.create_schema)
        self.validate_button.clicked.connect(self.validate_schema)
        self.start_stop_button.clicked.connect(self.toggle_start_stop)
        self.browse_sql_button.clicked.connect(self.browse_sql_file)
        self.browse_directory_button.clicked.connect(self.browse_directory)

    def create_schema(self):
        schema_name = self.entry_schema_name.text()
        password = self.entry_password.text()
        tablespace_name = self.entry_tablespace_name.text()
        size_gb = self.entry_tablespace_size.text()
        quota_gb = self.entry_tablespace_quota.text()
        dba_privilege = self.check_dba_var.isChecked()
        connect_privilege = self.check_connect_var.isChecked()
        quota_privilege = self.check_quota_var.isChecked()

        dbutils.create_schema(self, self.database, schema_name, password, tablespace_name, size_gb, quota_gb, dba_privilege, connect_privilege, quota_privilege)

    def validate_schema(self):
        schema_name = self.entry_schema_name.text()
        tablespace_name = self.entry_tablespace_name.text()
        quota_gb = self.entry_tablespace_quota.text()
        dba_privilege = self.check_dba_var.isChecked()
        connect_privilege = self.check_connect_var.isChecked()
        quota_privilege = self.check_quota_var.isChecked()

        dbutils.validate_schema(self, self.database, schema_name, tablespace_name, quota_gb, dba_privilege, connect_privilege, quota_privilege)
        
    def toggle_start_stop(self):
        if self.start_stop_button.text() == "Start":
            self.start_stop_button.setText("Stop")
            # Add code to handle the "Start" action
        else:
            self.start_stop_button.setText("Start")
            # Add code to handle the "Stop" action

    def browse_sql_file(self):
        file_operations.browse_sql_file(self.entry_script_sql)

    def browse_directory(self):
        file_operations.browse_directory(self.entry_directory)
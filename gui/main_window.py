from PyQt5 import QtWidgets
from gui.load_test import LoadTestTab
from gui.performance_emulator import PerformanceEmulatorTab

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, db_connection):
        super().__init__()

        self.database = db_connection  # Use the db_connection passed from the LoginWindow
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('MOPS v0.2')

        # Create tabs
        self.tab_widget = QtWidgets.QTabWidget()
        
        # Load Test tab
        self.load_test_tab = LoadTestTab(self.database)
        self.tab_widget.addTab(self.load_test_tab, "Load Test")
        
        # Performance Emulator tab
        self.performance_emulator_tab = PerformanceEmulatorTab(self.database)
        self.tab_widget.addTab(self.performance_emulator_tab, "Performance Emulator")

        # Set tab widget as central widget
        self.setCentralWidget(self.tab_widget)

        # Bind the on_closing method to the window close event
        self.closeEvent = self.on_closing

    def on_closing(self, event):
        self.database.close()  # Close the database connection when the window is closed
        event.accept()

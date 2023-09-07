import tkinter as tk
from tkinter import ttk
from .load_test import LoadTestTab
from .performance_emulator import PerformanceEmulatorTab

class MainWindow(tk.Tk):
    def __init__(self, connection):
        print("MainWindow __init__ connection argument:", connection)  # Add this line
        super().__init__()
        self.title("Main Window")
        
        # Store the database connection
        self.connection = connection
        
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(self)
        
        # Create the main tabs
        load_test_tab = LoadTestTab(notebook, self.connection)
        performance_emulator_tab = PerformanceEmulatorTab(notebook)  # Assuming this doesn't need the connection
        
        # Add the tabs to the main notebook
        notebook.add(load_test_tab, text="Load Test")
        notebook.add(performance_emulator_tab, text="Performance Emulator")
        
        # Pack the main notebook in the main window
        notebook.pack(expand=True, fill="both")

    def on_closing(self):
        # Close the database connection
        self.connection.close()
        
        # Destroy the window
        self.destroy()


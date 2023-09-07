import tkinter as tk
from tkinter import messagebox, ttk
import json

class LoginWindow(tk.Tk):
    def __init__(self, db_connection_callback):
        super().__init__()
        self.db_connection_callback = db_connection_callback
        self.title("Database Connection")
        
        # Load config values
        with open('config.json') as f:
            self.config = json.load(f)['databaseConnection']

        # Create and place the labels and entry fields for the user inputs
        tk.Label(self, text="Username:").grid(row=0, column=0, padx=20, pady=5)
        self.entry_username = tk.Entry(self)
        self.entry_username.insert(0, self.config['username'])
        self.entry_username.grid(row=0, column=1, padx=20, pady=5)
        
        tk.Label(self, text="Password:").grid(row=1, column=0, padx=20, pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.insert(0, self.config['password'])
        self.entry_password.grid(row=1, column=1, padx=20, pady=5)
        
        tk.Label(self, text="Hostname:").grid(row=2, column=0, padx=20, pady=5)
        self.entry_hostname = tk.Entry(self)
        self.entry_hostname.insert(0, self.config['hostname'])
        self.entry_hostname.grid(row=2, column=1, padx=20, pady=5)
        
        tk.Label(self, text="Port:").grid(row=3, column=0, padx=20, pady=5)
        self.entry_port = tk.Entry(self)
        self.entry_port.insert(0, self.config['port'])
        self.entry_port.grid(row=3, column=1, padx=20, pady=5)
        
        tk.Label(self, text="Service Name:").grid(row=4, column=0, padx=20, pady=5)
        self.entry_service_name = tk.Entry(self)
        self.entry_service_name.insert(0, self.config['service_name'])
        self.entry_service_name.grid(row=4, column=1, padx=20, pady=5)
        
        # Create and place the connect button
        connect_button = tk.Button(self, text="Connect", command=self.connect_to_db)
        connect_button.grid(row=5, column=0, columnspan=2, pady=20)

    def connect_to_db(self):
        # Get the user inputs
        username = self.entry_username.get()
        password = self.entry_password.get()
        hostname = self.entry_hostname.get()
        port = self.entry_port.get()
        service_name = self.entry_service_name.get()
        
        # Call the callback function with the input values
        self.db_connection_callback(username, password, hostname, service_name, port)

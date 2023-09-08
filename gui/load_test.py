import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from modules.create_schema import create_schema
from modules.validate_schema import validate_schema
from modules.file_operations import browse_sql_file, browse_directory
import json

class LoadTestTab(ttk.Frame):
    def __init__(self, parent, connection):  # Add a second parameter for the connection
        super().__init__(parent)
        self.connection = connection  # Store the connection as an attribute

        # Load default values from JSON file
        with open('config.json') as f:
            self.config = json.load(f)

        # Create a notebook for the subtabs
        notebook = ttk.Notebook(self)
        
        # Create the "Configuration" subtab
        frame_configuration = ttk.Frame(notebook, padding="20 20 20 20")  # Add padding here
        frame_configuration.grid(row=0, column=0, padx=20, pady=20)  # Add padding when placing the frame in the grid

        # Create the "Data Load" subtab
        frame_data_load = ttk.Frame(notebook, padding="20 20 20 20")  
        frame_data_load.grid(row=0, column=0, padx=20, pady=20)  

        # Add frame_configuration as a tab to the notebook
        notebook.add(frame_configuration, text="Configuration")
        
        # Schema Details section
        schema_details_frame = ttk.Labelframe(frame_configuration, text="Schema Details", padding="20 20 20 20")
        schema_details_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        label_width = 18
        
        ttk.Label(schema_details_frame, text="Schema Name:", width=label_width).grid(row=0, column=0, padx=20, pady=5, sticky=tk.E)
        self.entry_schema_name = ttk.Entry(schema_details_frame)
        self.entry_schema_name.insert(0, self.config['schemaCreation']['schema_name'])
        self.entry_schema_name.grid(row=0, column=1, padx=(0, 10), pady=5)
        
        ttk.Label(schema_details_frame, text="Password:", width=label_width).grid(row=1, column=0, padx=20, pady=5, sticky=tk.E)
        self.entry_password = ttk.Entry(schema_details_frame, show="*")
        self.entry_password.insert(0, self.config['schemaCreation']['password'])
        self.entry_password.grid(row=1, column=1, padx=(0, 10), pady=5)
        
        ttk.Label(schema_details_frame, text="Tablespace Name:", width=label_width).grid(row=2, column=0, padx=20, pady=5, sticky=tk.E)
        self.entry_tablespace_name = ttk.Entry(schema_details_frame)
        self.entry_tablespace_name.insert(0, self.config['schemaCreation']['tablespace'])
        self.entry_tablespace_name.grid(row=2, column=1, padx=(0, 10), pady=5)
        
        ttk.Label(schema_details_frame, text="Size(GB):", width=label_width).grid(row=2, column=2, padx=20, pady=5, sticky=tk.E)
        self.entry_tablespace_size = ttk.Entry(schema_details_frame)
        self.entry_tablespace_size.insert(0, self.config['schemaCreation'].get('tablespace_size', ''))
        self.entry_tablespace_size.grid(row=2, column=3, padx=(0, 10), pady=5)
        
        ttk.Label(schema_details_frame, text="Quota(GB):", width=label_width).grid(row=2, column=4, padx=20, pady=5, sticky=tk.E)
        self.entry_tablespace_quota = ttk.Entry(schema_details_frame)
        self.entry_tablespace_quota.insert(0, self.config['schemaCreation'].get('tablespace_quota', ''))
        self.entry_tablespace_quota.grid(row=2, column=5, padx=(0, 10), pady=5)

        # Privileges section
        privileges_frame = ttk.Labelframe(frame_configuration, text="Privileges", padding="20 20 20 20")
        privileges_frame.grid(row=1, column=0, columnspan=2, pady=(20, 10), sticky=(tk.W, tk.E))
                
        self.check_dba_var = tk.BooleanVar(value=False)
        self.check_dba = ttk.Checkbutton(privileges_frame, text="DBA", variable=self.check_dba_var)
        self.check_dba.grid(row=0, column=0, padx=20, pady=5, sticky=tk.W)
                
        self.check_connect_var = tk.BooleanVar(value=False)
        self.check_connect = ttk.Checkbutton(privileges_frame, text="CONNECT", variable=self.check_connect_var)
        self.check_connect.grid(row=0, column=1, padx=20, pady=5)
                
        self.check_quota_var = tk.BooleanVar(value=False)
        self.check_quota = ttk.Checkbutton(privileges_frame, text="Quota", variable=self.check_quota_var)
        self.check_quota.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky=tk.W)

        # Console section configuration
        console_frame = ttk.Labelframe(frame_configuration, text="Console", padding="20 20 20 20")
        console_frame.grid(row=2, column=0, columnspan=2, pady=(20, 10), sticky=(tk.W, tk.E))

        
        self.console = tk.Text(console_frame, width=100, height=10, wrap='word')
        self.console.grid(row=0, column=0, padx=20, pady=5, sticky=(tk.W, tk.E))
        self.console.configure(state='disabled')  # Disable editing of the console

        # Create and Validate buttons

        ttk.Button(frame_configuration, text="Create", command=self.create_schema).grid(row=7, column=0, padx=20, pady=(20, 0), sticky=tk.E)
        ttk.Button(frame_configuration, text="Validate", command=self.validate_schema).grid(row=7, column=1, padx=20, pady=(20, 0), sticky=tk.W)
        
        # Add the frames to the subtab notebook
        notebook.add(frame_configuration, text="Configuration")
     
        # Pack the notebook in the tab frame
        notebook.pack(expand=True, fill="both", padx=20, pady=20)

        notebook.add(frame_data_load, text="Data Load")

        # Data Load

        # Manual section
        manual_frame = ttk.Labelframe(frame_data_load, text="Manual", padding="20 20 20 20")
        manual_frame.grid(row=0, column=0, pady=(0, 10), sticky=(tk.W, tk.E))

        # Script (SQL) label, entry, and button
        ttk.Label(manual_frame, text="Script (SQL):").grid(row=0, column=0, padx=20, pady=5, sticky=tk.E)
        self.entry_script_sql = ttk.Entry(manual_frame)
        self.entry_script_sql.grid(row=0, column=1, padx=(0, 10), pady=5, sticky=(tk.W, tk.E))
        ttk.Button(manual_frame, text="Browse", command=lambda: browse_sql_file(self.entry_script_sql)).grid(row=0, column=2, padx=20, pady=5)

        # Directory label, entry, and button
        ttk.Label(manual_frame, text="Directory:").grid(row=1, column=0, padx=20, pady=5, sticky=tk.E)
        self.entry_directory = ttk.Entry(manual_frame)
        self.entry_directory.grid(row=1, column=1, padx=(0, 10), pady=5, sticky=(tk.W, tk.E))
        ttk.Button(manual_frame, text="Browse", command=lambda: browse_directory(self.entry_directory)).grid(row=1, column=2, padx=20, pady=5)


        # Auto section
        auto_frame = ttk.Labelframe(frame_data_load, text="Auto", padding="20 20 20 20")
        auto_frame.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Schema label and entry
        ttk.Label(auto_frame, text="Schema:").grid(row=0, column=0, padx=20, pady=5, sticky=tk.E)
        self.entry_schema_name = ttk.Entry(auto_frame)
        self.entry_schema_name.insert(0, self.config['schemaCreation']['schema_name'])  # Adjust the key as per your JSON structure
        self.entry_schema_name.grid(row=0, column=1, padx=(0, 10), pady=5, sticky=(tk.W, tk.E))
        
        # Number of rows label and entry
        ttk.Label(auto_frame, text="Number of rows:").grid(row=1, column=0, padx=20, pady=5, sticky=tk.E)
        self.entry_num_rows = ttk.Entry(auto_frame)
        self.entry_num_rows.insert(0, self.config['dataLoad']['num_rows'])  # Adjust the key as per your JSON structure
        self.entry_num_rows.grid(row=1, column=1, padx=(0, 10), pady=5, sticky=(tk.W, tk.E))
        
        # Number of threads label and entry
        ttk.Label(auto_frame, text="Number of threads:").grid(row=2, column=0, padx=20, pady=5, sticky=tk.E)
        self.entry_num_threads = ttk.Entry(auto_frame)
        self.entry_num_threads.insert(0, self.config['dataLoad']['num_threads'])  # Adjust the key as per your JSON structure
        self.entry_num_threads.grid(row=2, column=1, padx=(0, 10), pady=5, sticky=(tk.W, tk.E))
        
        # Parallel label and entry
        ttk.Label(auto_frame, text="Parallel:").grid(row=3, column=0, padx=20, pady=5, sticky=tk.E)
        self.entry_parallel = ttk.Entry(auto_frame)
        self.entry_parallel.insert(0, self.config['dataLoad']['parallel'])  # Adjust the key as per your JSON structure
        self.entry_parallel.grid(row=3, column=1, padx=(0, 10), pady=5, sticky=(tk.W, tk.E))
        
        # Start/Stop toggle button
        self.start_stop_button = ttk.Button(auto_frame, text="Start", command=self.toggle_start_stop)
        self.start_stop_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # ... (remaining code)
        
    def toggle_start_stop(self):
            if self.start_stop_button['text'] == "Start":
                self.start_stop_button.config(text="Stop")
                # Add code to handle the "Start" action
            else:
                self.start_stop_button.config(text="Start")
                # Add code to handle the "Stop" action
        
        

    def create_schema(self):
            # Get the values from the entry fields
            schema_name = self.entry_schema_name.get()
            password = self.entry_password.get()
            tablespace_name = self.entry_tablespace_name.get()
            size_gb = self.entry_tablespace_size.get()
            quota_gb = self.entry_tablespace_quota.get()
            
            # Get the values from the check buttons
            dba_privilege = self.check_dba_var.get()
            connect_privilege = self.check_connect_var.get()
            quota_privilege = self.check_quota_var.get()
    
            # Call the create_schema function from schema_operations module
            create_schema(self,self.connection, schema_name, password, tablespace_name, size_gb, quota_gb, dba_privilege, connect_privilege, quota_privilege)

    def validate_schema(self):
            # Get the values from the entry fields
            schema_name = self.entry_schema_name.get()
            tablespace_name = self.entry_tablespace_name.get()
            quota_gb = self.entry_tablespace_quota.get()
            
            # Get the values from the check buttons
            dba_privilege = self.check_dba_var.get()
            connect_privilege = self.check_connect_var.get()
            quota_privilege = self.check_quota_var.get()
    
            # Call the create_schema function from schema_operations module
            validate_schema(self,self.connection, schema_name, tablespace_name, quota_gb, dba_privilege, connect_privilege, quota_privilege)
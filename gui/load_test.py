import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

        
        # Create and Validate buttons

        ttk.Button(frame_configuration, text="Create", command=self.create_schema).grid(row=7, column=0, padx=20, pady=(20, 0), sticky=tk.E)
        ttk.Button(frame_configuration, text="Validate").grid(row=7, column=1, padx=20, pady=(20, 0), sticky=tk.W)
        
        # Add the frames to the subtab notebook
        notebook.add(frame_configuration, text="Configuration")
        
        # Pack the notebook in the tab frame
        notebook.pack(expand=True, fill="both", padx=20, pady=20)

    def create_schema(self):
        # Get the values from the entry fields
        schema_name = self.entry_schema_name.get()
        password = self.entry_password.get()
        tablespace_name = self.entry_tablespace_name.get()
        size_gb = self.entry_tablespace_size.get()
        quota_gb = self.entry_tablespace_quota.get()
        
        # Get the values from the check buttons
        dba_privilege = self.check_dba.instate(['selected'])
        connect_privilege = self.check_connect.instate(['selected'])
        quota_privilege = self.check_quota.instate(['selected'])

        # Construct the DDL statements
        ddl_statements = []
        ddl_statements.append(f"CREATE TABLESPACE {tablespace_name} DATAFILE '+DATA' SIZE {size_gb}G")


        create_user_ddl = f'CREATE USER {schema_name} IDENTIFIED BY "{password}" DEFAULT TABLESPACE {tablespace_name}'

        if quota_privilege:
            create_user_ddl += f" QUOTA {quota_gb}G ON {tablespace_name}"
        ddl_statements.append(create_user_ddl)

        if dba_privilege:
            ddl_statements.append(f"GRANT DBA TO {schema_name}")

        if connect_privilege:
            ddl_statements.append(f"GRANT CONNECT TO {schema_name}")

        cursor = None
        try:
            cursor = self.connection.cursor()
            
            for ddl in ddl_statements:
                print(ddl)
                cursor.execute(ddl)

            
            # Commit the transaction
            self.connection.commit()
            
            # Show a success message
            messagebox.showinfo("Success", "Schema created successfully!")
        except Exception as e:
            # Show an error message
            messagebox.showerror("Error", str(e))
            import traceback
            traceback.print_exc()
        finally:
            # Close the cursor if it was created
            if cursor:
                cursor.close()
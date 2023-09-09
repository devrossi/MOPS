from tkinter import messagebox
import tkinter as tk
import cx_Oracle

def create_schema(self, connection, schema_name, password, tablespace_name, size_gb, quota_gb, dba_privilege, connect_privilege, quota_privilege):
    # Construct the DDL statements
    ddl_statements = [
        f"CREATE TABLESPACE {tablespace_name} DATAFILE '+DATA' SIZE {size_gb}G",
        f'CREATE USER {schema_name} IDENTIFIED BY "{password}" DEFAULT TABLESPACE {tablespace_name}'
    ]
    
    if quota_privilege:
        ddl_statements[1] += f" QUOTA {quota_gb}G ON {tablespace_name}"
    
    if dba_privilege:
        ddl_statements.append(f"GRANT DBA TO {schema_name}")

    if connect_privilege:
        ddl_statements.append(f"GRANT CONNECT TO {schema_name}")

    cursor = None
    try:
        cursor = connection.cursor()
        
        for ddl in ddl_statements:
            try:
                print(ddl)
                cursor.execute(ddl)
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                if error.code == 1543:  # Adjust the error code to match the ORA-01543
                    self.console.configure(state='normal')
                    self.console.insert(tk.END, "[WARNING] Tablespace exists. No need to create\n")
                    self.console.configure(state='disabled')
                    continue
                elif error.code == 1920:
                    self.console.configure(state='normal')
                    self.console.insert(tk.END, "[WARNING] User exists. No need to create\n")
                    self.console.configure(state='disabled')
                    continue                   
                else:
                    raise  # Re-raise the exception if it's a different error

        # Commit the transaction
        connection.commit()
        
        # Show a success message
        self.console.configure(state='normal')
        self.console.insert(tk.END, "[OK] Success.\n")
        self.console.configure(state='disabled')

    except Exception as e:
        # Show an error message
        self.console.configure(state='normal')
        self.console.insert(tk.END, str(e))
        self.console.configure(state='disabled')
        import traceback
        traceback.print_exc()
    finally:
        # Close the cursor if it was created
        if cursor:
            cursor.close()


def validate_schema(self, connection, schema_name, tablespace_name, quota_gb, dba_privilege, connect_privilege, quota_privilege):
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Validate the existence of the tablespace
        cursor.execute(f"SELECT COUNT(*) FROM dba_tablespaces WHERE tablespace_name = '{tablespace_name.upper()}'")
        tablespace_count, = cursor.fetchone()
        if tablespace_count == 0:
            self.console.configure(state='normal')
            self.console.insert(tk.END, "[ERROR] Tablespace does not exist\n")
            self.console.configure(state='disabled')
        else:
            self.console.configure(state='normal')
            self.console.insert(tk.END, "[OK] Tablespace exists.\n")
            self.console.configure(state='disabled')
        
        # Validate the existence of the user
        cursor.execute(f"SELECT COUNT(*) FROM dba_users WHERE username = '{schema_name.upper()}'")
        user_count, = cursor.fetchone()
        if user_count == 0:
            self.console.configure(state='normal')
            self.console.insert(tk.END, "[ERROR] The schema does not exist\n")
            self.console.configure(state='disabled')
        else:
            self.console.configure(state='normal')
            self.console.insert(tk.END, "[OK] The schema exists.\n")
            self.console.configure(state='disabled')
        
    except cx_Oracle.DatabaseError as e:
        # Handle any database errors
        error, = e.args
        messagebox.showerror("Database Error", error.message)
    except Exception as e:
        # Handle any other exceptions
        messagebox.showerror("Error", str(e))
    finally:
        # Close the cursor if it was created
        if cursor:
            cursor.close()

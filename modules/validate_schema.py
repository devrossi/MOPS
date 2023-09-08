from tkinter import messagebox
import tkinter as tk
import cx_Oracle

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

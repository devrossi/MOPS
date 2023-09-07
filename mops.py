import sys
from gui import LoginWindow, MainWindow
sys.path.append('./gui')
sys.path.append('./connection')

from gui import LoginWindow, MainWindow
from database import connect_to_db
from tkinter import messagebox
import json

def db_connection_callback(username, password, host, service_name, port):
    try:
        connection = connect_to_db(username, password, host, service_name, port)
        print("Connection object:", connection)
        # If connection is successful, show a success message and open the main window
        messagebox.showinfo("Success", "Connected to the database successfully!")
        
        # Close the login window
        login_window.destroy()
        
        # Open the main window with the database connection
        main_window = MainWindow(connection)
        main_window.mainloop()
    except Exception as e:
        # If connection fails, show the error message
        messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    login_window = LoginWindow(db_connection_callback)
    login_window.mainloop()

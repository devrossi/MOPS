from tkinter import filedialog

def browse_sql_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("SQL files", "*.sql"), ("All files", "*.*")])
    if file_path:
        entry.delete(0, 'end')
        entry.insert(0, file_path)

def browse_directory(entry):
    directory_path = filedialog.askdirectory()
    if directory_path:
        entry.delete(0, 'end')
        entry.insert(0, directory_path)

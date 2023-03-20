import platform
import os
from tkinter.filedialog import askdirectory, askopenfilename
import customtkinter
import tkinter.messagebox as messagebox
import threading

def check_platform():
    if platform.system() == "Windows":
        return main()
    else:
        return error()

def error():
    messagebox.showerror("Unsupported Platform", "Error: This program is not supported on your platform. Only works in Windows")

def export():
    # Create a new window
    export_window = customtkinter.CTkToplevel(root)
    export_window.title("Export Settings")
    x = root.winfo_x()
    y = root.winfo_y()

    # Center the window
    export_window.geometry(f"+{x+100}+{y+100}")

    export_window.resizable(False, False)
    
    # Create a label and entry for the file path
    path_label = customtkinter.CTkLabel(export_window, text="File Path:")
    path_entry = customtkinter.CTkEntry(export_window, width=300)
    path_button = customtkinter.CTkButton(export_window, text="Choose", command=lambda: choose_path(path_entry, export_window))

    # Create a label and entry for the file name
    name_label = customtkinter.CTkLabel(export_window, text="File Name:")
    name_entry = customtkinter.CTkEntry(export_window, width=300)

    # Create a button to save the file
    save_button = customtkinter.CTkButton(export_window, text="Save", command=lambda: save_file(path_entry.get(), name_entry.get(), export_window))

    # Pack the widgets into the window
    path_label.grid(row=0, column=0, padx=10, pady=10)
    path_entry.grid(row=0, column=1, padx=10, pady=10)
    path_button.grid(row=0, column=2, padx=10, pady=10)
    name_label.grid(row=1, column=0, padx=10, pady=10)
    name_entry.grid(row=1, column=1, padx=10, pady=10)
    save_button.grid(row=2, column=1, padx=10, pady=10)

    export_window.grab_set()

def choose_path(path_entry, window):
    window.lift()
    # Ask the user to choose a folder and update the path entry with the selected folder
    path = askdirectory(title="Select a folder to save the file to", parent=window)
    path_entry.delete(0, customtkinter.END)
    path_entry.insert(0, path)

def choose_file(path_entry, window):
    window.lift()
    # Ask the user to choose a folder and update the path entry with the selected folder
    filetypes = (("JSON files", "*.json"), ("All files", "*.*"))
    path = askopenfilename(filetypes=filetypes)
    path_entry.delete(0, customtkinter.END)
    path_entry.insert(0, path)

def import_file(path, window):
    # Show an error message if the path is empty
    if path == "":
        messagebox.showerror("Error", "Please enter a file path")
    else:
        # Define a function to run the command in a separate thread
        def run_command():
            os.system(f"winget import {path}")

            # Destroy the spinner window after the command has finished
            spinner_window.destroy()
            # Close the export settings window
            window.destroy()
            # Show a message box to tell user the programs have been imported
            messagebox.showinfo("Import Complete", "The programs have been imported")

        # Create a new window with a spinner animation
        spinner_window = customtkinter.CTkToplevel(window)
        spinner_window.title("Importing...")
        # Center the window
        x = window.winfo_x()
        y = window.winfo_y()
        spinner_window.geometry(f"+{x+100}+{y+100}")
        spinner_label = customtkinter.CTkLabel(spinner_window, text="Importing, please wait...")
        spinner_label.pack(padx=10, pady=10)
        spinner = customtkinter.CTkProgressBar(spinner_window)
        spinner.pack(padx=10, pady=10)

        spinner_window.resizable(False, False)

        # Start the spinner animation
        spinner.start()

        spinner_window.grab_set()

        # Start a new thread to run the command
        thread = threading.Thread(target=run_command)
        thread.start()

def save_file(path, name, window):
    # Show an error message if the path or name is empty
    if path == "" or name == "":
        messagebox.showerror("Error", "Please enter a file path and name")

    else:
        # Define a function to run the command in a separate thread
        def run_command():
            os.system(f"winget export -o {path}/{name}.json --accept-source-agreements")
            # Destroy the spinner window after the command has finished
            spinner_window.destroy()
            # Close the export settings window
            window.destroy()
            # Show a message box to tell the user the file has been saved
            messagebox.showinfo("File Saved", f"File saved to {path}/{name}.json")

        # Create a new window with a spinner animation
        spinner_window = customtkinter.CTkToplevel(window)
        spinner_window.title("Exporting...")
        # Center the window
        x = window.winfo_x()
        y = window.winfo_y()
        spinner_window.geometry(f"+{x+100}+{y+100}")
        spinner_label = customtkinter.CTkLabel(spinner_window, text="Exporting, please wait...")
        spinner_label.pack(padx=10, pady=10)
        spinner = customtkinter.CTkProgressBar(spinner_window)
        spinner.pack(padx=10, pady=10)

        spinner_window.resizable(False, False)

        # Start the spinner animation
        spinner.start()

        spinner_window.grab_set()

        # Start a new thread to run the command
        thread = threading.Thread(target=run_command)
        thread.start()

def import_data():

    # Create a new window
    import_window = customtkinter.CTkToplevel(root)
    import_window.title("Import Settings")

    import_window.resizable(False, False)

    # Center the window
    x = root.winfo_x()
    y = root.winfo_y()
    import_window.geometry(f"+{x+100}+{y+100}")

    # Create a label and entry for the file path
    path_label = customtkinter.CTkLabel(import_window, text="File Path:")
    path_entry = customtkinter.CTkEntry(import_window, width=300)
    path_button = customtkinter.CTkButton(import_window, text="Choose", command=lambda: choose_file(path_entry, import_window))
    import_button = customtkinter.CTkButton(import_window, text="Import", command=lambda: import_file(path_entry.get(), import_window))

    # Pack the widgets into the window
    path_label.grid(row=0, column=0, padx=10, pady=10)
    path_entry.grid(row=0, column=1, padx=10, pady=10)
    path_button.grid(row=0, column=2, padx=10, pady=10)
    import_button.grid(row=1, column=1, padx=10, pady=10)

    import_window.grab_set()

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.resizable(False, False)
window_width = 800
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

root.title("Winget Exporter/Importer")

title_label = customtkinter.CTkLabel(root, text="Winget Exporter/Importer", font=("Arial", 40))
title_label.pack(padx=10, pady=60)

# Create a frame to hold the buttons
button_frame = customtkinter.CTkFrame(root)

# Add the buttons to the frame
import_button = customtkinter.CTkButton(button_frame, text="IMPORT", command=import_data)
export_button = customtkinter.CTkButton(button_frame, text="EXPORT", command=export)

# Center the buttons inside the frame
import_button.pack(side="left", padx=10, pady=10)
export_button.pack(side="right", padx=10, pady=10)

# Center the frame inside the main window
button_frame.place(relx=0.5, rely=0.5, anchor="center")

def main():

    root.mainloop()

if __name__ == "__main__":
    check_platform()
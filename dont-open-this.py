import os
import sys
import ctypes
import subprocess
from tkinter import messagebox, Tk

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def find_and_open_exe_files(root_dir='C:\\'):
    exe_files = []
    
    # Walk through the directory tree
    for root, dirs, files in os.walk(root_dir):
        try:
            for file in files:
                if file.lower().endswith('.exe'):
                    exe_path = os.path.join(root, file)
                    exe_files.append(exe_path)
                    
                    # Try to open the EXE file
                    try:
                        subprocess.Popen(exe_path, shell=True)
                        print(f"Opened: {exe_path}")
                    except Exception as e:
                        print(f"Failed to open {exe_path}: {str(e)}")
        except PermissionError:
            continue  # Skip directories we can't access
        except Exception as e:
            print(f"Error processing {root}: {str(e)}")
    
    return exe_files

def main():
    # Hide the main tkinter window
    root = Tk()
    root.withdraw()
    
    if not is_admin():
        # Show UAC prompt if not admin
        messagebox.showwarning(
            "Admin Required",
            "This application requires administrative privileges to access all EXE files.\n"
            "Please grant permission when prompted."
        )
        run_as_admin()
    else:
        # Proceed with the operation
        messagebox.showinfo(
            "Starting",
            "The application will now search for and open all EXE files in the C drive.\n"
            "This may take some time and could impact system performance."
        )
        
        try:
            found_exes = find_and_open_exe_files()
            messagebox.showinfo(
                "Completed",
                f"Process completed.\nFound and attempted to open {len(found_exes)} EXE files."
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred during execution:\n{str(e)}"
            )

if __name__ == "__main__":
    main()
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

DEFAULT_SERVER_IP = "172.30.146.44"  

def refresh_exports():
    try:
        with open("/etc/exports", "r") as f:
            exports = [line.split()[0] for line in f if line.strip()]
        if not exports:
            exports_var.set(["No exports available."])
        else:
            exports_var.set(exports)
    except FileNotFoundError:
        exports_var.set(["/etc/exports file not found."])

def add_export():
    folder = simpledialog.askstring("Add Export", "Enter directory path to export:")
    if not folder:
        return
    if not os.path.exists(folder):
        messagebox.showerror("Error", "Directory does not exist.")
        return

    permissions_window = tk.Toplevel(root)
    permissions_window.title("Select Permissions")
    permissions_window.geometry("300x150")

    permissions_var = tk.StringVar(value="Select permissions")
    permissions_options = [
        "Select permissions", 
        "rw,sync,no_subtree_check",
        "ro,sync,no_subtree_check",
        "rw,sync",
        "ro,sync"
    ]
    permissions_menu = ttk.OptionMenu(permissions_window, permissions_var, *permissions_options)
    permissions_menu.pack(fill="x", padx=10, pady=10)

    def submit_permissions():
        permissions = permissions_var.get()
        if permissions == "Select permissions":
            messagebox.showerror("Error", "Please select permissions.")
            return

        
        ip_address = DEFAULT_SERVER_IP
        export_entry = f"{folder} {ip_address}({permissions})\n"

        try:
            with open("/etc/exports", "r+") as f:
                lines = f.readlines()
                if export_entry.strip() in [line.strip() for line in lines]:
                    messagebox.showinfo("Info", "Export already exists.")
                    return
                f.write(export_entry)
            subprocess.run(["sudo", "exportfs", "-r"], check=True)
            refresh_exports()
            messagebox.showinfo("Success", "Export added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        permissions_window.destroy()

    ttk.Button(permissions_window, text="Submit", command=submit_permissions).pack(pady=10)

def remove_export():
    selected = exports_list.curselection() 
    if not selected:
        messagebox.showerror("Error", "No export selected.")
        return
    
    selected_export = exports_list.get(selected[0])  

    try:
        with open("/etc/exports", "r") as f:
            lines = f.readlines()
        with open("/etc/exports", "w") as f:
            for line in lines:
                if not line.startswith(selected_export):
                    f.write(line)
        subprocess.run(["sudo", "exportfs", "-r"], check=True)
        refresh_exports()  # Refresh the export list
        messagebox.showinfo("Success", f"Export '{selected_export}' removed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def view_permissions():
    selected = exports_list.curselection()
    if not selected:
        messagebox.showerror("Error", "No export selected.")
        return

    selected_export = exports_list.get(selected[0])
    
    try:
        permissions = subprocess.check_output(["ls", "-ld", selected_export], text=True)
        messagebox.showinfo("Current Permissions", f"Permissions for {selected_export}:\n{permissions}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch permissions: {e}")

def manage_permissions():
    selected = exports_list.curselection()
    if not selected:
        messagebox.showerror("Error", "No export selected.")
        return

    selected_export = exports_list.get(selected[0])

    # Show the permissions dropdown after selecting the export
    chmod_window = tk.Toplevel(root)
    chmod_window.title("Manage Permissions")
    chmod_window.geometry("300x150")

    chmod_var = tk.StringVar(value="Select permission level")
    chmod_options = [
        "Select permission level",
        "chmod 777 (Full Access)",
        "chmod 775 (Owner & Group)",
        "chmod 773 (Owner & Group Read/Write)"
    ]
    chmod_menu = ttk.OptionMenu(chmod_window, chmod_var, *chmod_options)
    chmod_menu.pack(fill="x", padx=10, pady=10)

    def submit_chmod():
        permission = chmod_var.get()
        if permission == "Select permission level":
            messagebox.showerror("Error", "Please select a permission level.")
            return

        try:
            if permission == "chmod 777 (Full Access)":
                subprocess.run(["sudo", "chmod", "777", selected_export], check=True)
            elif permission == "chmod 775 (Owner & Group)":
                subprocess.run(["sudo", "chmod", "775", selected_export], check=True)
            elif permission == "chmod 773 (Owner & Group Read/Write)":
                subprocess.run(["sudo", "chmod", "773", selected_export], check=True)

            messagebox.showinfo("Success", f"Permissions updated to {permission} for {selected_export}")
            chmod_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Could not update permissions: {e}")

    ttk.Button(chmod_window, text="Apply", command=submit_chmod).pack(pady=10)

# GUI Setup
root = tk.Tk()
root.title("NFS Server Manager")
root.geometry("400x350")
root.resizable(False, False)

# Export List
exports_var = tk.StringVar(value=["Click 'Refresh' to load exports"])
exports_list = tk.Listbox(root, listvariable=exports_var, height=10)
exports_list.pack(fill="both", expand=True, padx=10, pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(fill="x", pady=5)

ttk.Button(button_frame, text="Refresh", command=refresh_exports).pack(side="left", padx=5)
ttk.Button(button_frame, text="Add Export", command=add_export).pack(side="left", padx=5)
ttk.Button(button_frame, text="Remove Export", command=remove_export).pack(side="left", padx=5)
ttk.Button(button_frame, text="View Permissions", command=view_permissions).pack(side="left", padx=5)
ttk.Button(button_frame, text="Manage Permissions", command=manage_permissions).pack(side="left", padx=5)

refresh_exports()
root.mainloop()

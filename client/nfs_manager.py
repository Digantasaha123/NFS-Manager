import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

DEFAULT_SERVER_IP = "172.30.146.44"  # Default server IP for the NFS server

def show_mounts():
    try:
        result = subprocess.run(["showmount", "-e", DEFAULT_SERVER_IP], capture_output=True, text=True)
        if result.returncode == 0:
            exports = result.stdout.splitlines()
            if len(exports) > 1:  
                available_exports.set(exports[1:])
            else:
                available_exports.set(["No exports available."])
        else:
            messagebox.showerror("Error", f"Could not retrieve available exports.\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def mount_nfs():
    selected_export = exports_list.curselection()
    if not selected_export:
        messagebox.showerror("Error", "Please select an export to mount.")
        return

    export = exports_list.get(selected_export[0]).split()[0]  # Extract the directory path
    mount_point = filedialog.askdirectory(title="Select Mount Point")
    if not mount_point:
        return

    try:
        subprocess.run(
            ["sudo", "mount", "-t", "nfs", f"{DEFAULT_SERVER_IP}:{export}", mount_point],
            check=True
        )
        messagebox.showinfo("Success", f"Mounted {export} to {mount_point}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to mount.\n{e.stderr or e}")

def unmount_nfs():
    mount_point = filedialog.askdirectory(title="Select Mounted Directory to Unmount")
    if not mount_point:
        return

    try:
        subprocess.run(["sudo", "umount", mount_point], check=True)
        messagebox.showinfo("Success", f"Unmounted {mount_point}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to unmount.\n{e.stderr or e}")

# GUI Setup
root = tk.Tk()
root.title("NFS Client Manager")
root.geometry("400x300")
root.resizable(False, False)

# Listbox for available exports
available_exports = tk.StringVar(value=["Click 'Show Mounts' to load exports"])
exports_list = tk.Listbox(root, listvariable=available_exports, height=10)
exports_list.pack(fill="both", expand=True, padx=10, pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(fill="x", pady=5)

ttk.Button(button_frame, text="Show Mounts", command=show_mounts).pack(side="left", padx=5)
ttk.Button(button_frame, text="Mount", command=mount_nfs).pack(side="left", padx=5)
ttk.Button(button_frame, text="Unmount", command=unmount_nfs).pack(side="left", padx=5)

root.mainloop()

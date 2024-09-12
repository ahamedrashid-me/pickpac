#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
import re
import os

# Function to run APT command and display output in the package_listbox
def run_apt_command(command, args, task_name, percentage):
    try:
        update_progress(task_name, percentage)
        result = subprocess.run([command] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Clear the listbox before showing new results
        package_listbox.delete(0, tk.END)

        # Display command output in the listbox
        if result.stdout:
            for line in result.stdout.splitlines():
                package_listbox.insert(tk.END, line)
        if result.stderr:
            package_listbox.insert(tk.END, "ERROR: " + result.stderr)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run the command: {e}")
    finally:
        progress_label.grid_forget()

# Function to update progress label
def update_progress(task_name, percentage):
    progress_label.config(text=f"{task_name} {percentage}%")
    progress_label.grid(row=0, column=2, padx=5)

# Function to check if GDebi is installed and install if not
def ensure_gdebi_installed():
    if is_program_installed('gdebi'):
        return True
    else:
        update_progress("Installing gdebi...", 50)
        try:
            subprocess.run(['sudo', 'apt', 'install', '-y', 'gdebi'], check=True)
            update_progress("GDebi installed.", 100)
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Failed to install gdebi: {e}")
            return False

def is_program_installed(program_name):
    result = subprocess.run(['which', program_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0

def search_packages():
    package_name = search_entry.get().strip()  # Get and trim the user input
    if not package_name:
        messagebox.showwarning("Input Error", "Please enter a package name to search.")
        return

    update_progress("Searching for package...", 30)
    root.after(100, lambda: run_apt_command('apt', ['search', package_name], "Searching for package", 30))

def install_package():
    package_name = search_entry.get().strip()
    if not package_name:
        messagebox.showwarning("Input Error", "Please enter a package name to install.")
        return
    update_progress("Installing package...", 30)
    run_apt_command('sudo', ['apt', 'install', '-y', package_name], "Installing package", 30)

def remove_package():
    package_name = search_entry.get().strip()
    if not package_name:
        messagebox.showwarning("Input Error", "Please enter a package name to remove.")
        return
    update_progress("Removing package...", 30)
    run_apt_command('sudo', ['apt', 'remove', '-y', package_name], "Removing package", 30)

def refresh_packages():
    try:
        update_progress("Refreshing packages...", 30)

        package_listbox.insert(tk.END, "Checking for broken packages...")

        # Check for broken packages
        result_broken = subprocess.run(['sudo', 'apt', '--fix-broken', 'install', '-y'], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)
        if result_broken.stdout:
            package_listbox.insert(tk.END, "Broken packages fixed:")
            for line in result_broken.stdout.splitlines():
                package_listbox.insert(tk.END, line)

        # Update package cache
        package_listbox.insert(tk.END, "\nRefreshing package cache and checking for missing keys...")
        result_update = subprocess.run(['sudo', 'apt', 'update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True)

        if result_update.stdout:
            package_listbox.insert(tk.END, "Package cache refreshed:")
            for line in result_update.stdout.splitlines():
                package_listbox.insert(tk.END, line)

        # Check for missing public keys (NO_PUBKEY)
        missing_keys = re.findall(r'NO_PUBKEY ([A-F0-9]{8,})', result_update.stdout)
        if missing_keys:
            package_listbox.insert(tk.END, "\nMissing public keys found. Installing missing keys...")
            for key in missing_keys:
                install_key(key)

        # automatically clean!

        else:
            package_listbox.insert(tk.END, "\nNo missing public keys detected.")

        # Fix missing packages
        package_listbox.insert(tk.END, "\nChecking for missing packages...")
        result_missing = subprocess.run(['sudo', 'apt', '--fix-missing', 'install', '-y'], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True)
        if result_missing.stdout:
            package_listbox.insert(tk.END, "Missing packages fixed:")
            for line in result_missing.stdout.splitlines():
                package_listbox.insert(tk.END, line)

        package_listbox.insert(tk.END, "\nRefresh complete. All issues fixed.")
        progress_label.grid_forget()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to refresh packages: {e}")
        progress_label.grid_forget()

def install_key(key):
    try:
        package_listbox.insert(tk.END, f"Installing missing key: {key}...")
        result = subprocess.run(['sudo', 'apt-key', 'adv', '--keyserver', 'keyserver.ubuntu.com', '--recv-keys', key],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            package_listbox.insert(tk.END, f"Public key {key} installed:")
            for line in result.stdout.splitlines():
                package_listbox.insert(tk.END, line)
        if result.stderr:
            package_listbox.insert(tk.END, "ERROR: " + result.stderr)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to install key: {e}")

#direct select deb file to install using gdebi!

def local():
    try:
        # Ask the user to select a .deb file
        deb_file = filedialog.askopenfilename(filetypes=[("Debian packages", "*.deb")])
        if deb_file:
            subprocess.run(['pkexec', 'gdebi', deb_file])
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")


def edit_repo():
    try:
        # Open the system's default terminal with nano to edit /etc/apt/sources.list
        if os.name == 'posix':
            subprocess.run(['x-terminal-emulator', '-e', 'sudo nano /etc/apt/sources.list'])
        else:
            messagebox.showerror("Error", "Unsupported OS. Please edit /etc/apt/sources.list manually.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Terminal not found. Ensure it's installed and try again.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open terminal: {e}")

# Create the main window
root = tk.Tk()
root.title(" [pickpac] V1.0 by @ahamedrashid.fb")
root.geometry("746x698")
root.resizable(False, False)  # Make the window non-resizable

# Search box and search button
search_frame = tk.Frame(root)
search_frame.grid(row=1, column=0, padx=30, pady=8, sticky="nw")

search_label = tk.Label(search_frame, text="Package Name:")
search_label.grid(row=0, column=0, padx=5)

search_entry = tk.Entry(search_frame, width=40)
search_entry.grid(row=0, column=1, padx=5)

# Progress label
progress_label = tk.Label(search_frame, text="")  # Start with an empty text

# Top buttons (SEARCH, INSTALL, REMOVE, INSTALLED, REFRESH, EDIT-REPO, LOCAL.DEB)
top_frame = tk.Frame(root)
top_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

buttons = [
    ("SEARCH", lambda: search_packages()),
    ("INSTALL", lambda: install_package()),
    ("REMOVE", lambda: remove_package()),
    ("INSTALLED", lambda: run_apt_command('apt', ['list', '--installed'], "Listing installed packages", 50)),
    ("REFRESH", lambda: refresh_packages()),
    ("EDIT-REPO", lambda: edit_repo()),
    ("LOCAL-PKG", lambda: local())
]

for i, (text, cmd) in enumerate(buttons):
    btn = tk.Button(top_frame, text=text, command=cmd)
    btn.grid(row=0, column=i, padx=5)

# Package List section
package_frame = tk.Frame(root)
package_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Create a listbox for the combined package name and details
package_listbox = tk.Listbox(package_frame, height=32, width=79)
package_listbox.grid(row=0, column=0, padx=5, pady=10)

# Scrollbar for the listbox
scrollbar = tk.Scrollbar(package_frame, orient="vertical", command=package_listbox.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
package_listbox.config(yscrollcommand=scrollbar.set)

# Start the Tkinter event loop
root.mainloop()

PickPac: Package Management GUI

PickPac is a user-friendly GUI application for managing packages on Debian-based Linux distributions. It allows users to search, install, remove, and refresh packages with a simple and intuitive interface. The application also supports installing .deb files locally and editing repository lists.
Features

Search Packages: Find packages in the repository.
Install Packages: Install new packages.
Remove Packages: Remove installed packages.
List Installed Packages: View a list of currently installed packages.
Refresh Packages: Update package lists, fix broken packages, and handle missing keys.
Local .deb Installation: Install .deb files using GDebi.
Edit Repositories: Open the repository list for manual editing.

Dependencies

Before running PickPac, ensure that the following packages are installed:

  python3-tk - Tkinter for Python 3
  gdebi-core - Tool for installing .deb packages
  apt-transport-https - Allows the use of HTTPS for APT

Installation

   Clone the Repository:

   bash

git clone https://github.com/ahamedrashid-me/pickpac.git

cd pickpac

Run the Setup Script:

The setup.sh script will handle the installation of required dependencies and set up the application:

bash

sudo ./setup.sh

This script will:

  Check and install missing dependencies.
   Copy the pickpac.py script to /usr/local/bin and make it executable.


Run PickPac:

After installation, you can run PickPac from the terminal:

bash

   pickpac

Usage

   Search for Packages: Enter the package name in the search box and click "SEARCH".
   Install/Remove Packages: Enter the package name and click "INSTALL" or "REMOVE".
   Refresh Packages: Click "REFRESH" to update package lists and fix issues.
   Install Local .deb File: Click "LOCAL-PKG" to select and install a .deb file.
   Edit Repositories: Click "EDIT-REPO" to open the repository list in the default terminal editor.

Contributing

Contributions are welcome! Please submit a pull request or open an issue if you find a bug or have suggestions for improvements.
License

This project is licensed under the MIT License. See the LICENSE file for details.

![pickpac3](https://github.com/user-attachments/assets/ab9a65e8-4455-442a-8b74-ef3cab575018)
![pickpac1](https://github.com/user-attachments/assets/06ae8973-a104-4939-ae6f-9dd0811e25b5)
![pickpac](https://github.com/user-attachments/assets/ff7a86c9-fa7c-49d4-92a4-3f228df502ea)

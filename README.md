
---

# Network File System (NFS) Project

This project showcases the setup, configuration, and usage of a **Network File System (NFS)** to facilitate efficient and secure file sharing over a network. The project demonstrates both server and client configurations, tested in a Linux-based environment using **Windows Subsystem for Linux (WSL)**, simulating real-world scenarios.

---

## 📋 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
  - [Server Setup](#server-setup)
  - [Client Setup](#client-setup)
- [Usage](#usage)
- [File Structure](#file-structure)
- [UI Screenshots](#ui-screenshots)
- [Future Enhancements](#future-enhancements)
- [Challenges Faced](#challenges-faced)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

---

## 📖 Introduction

The **Network File System (NFS)** allows files to be accessed and shared across multiple systems over a network as if they were local files. This project provides a comprehensive guide for configuring an NFS server and client, focusing on file synchronization, secure sharing, and scalability. The setup aims to demonstrate NFS concepts, enabling users to explore real-world networking challenges and solutions.

---

## ✨ Features

- **Server Configuration**:
  - Share directories with customizable permissions.
  - Support for read-only or read-write access for clients.
  - Compatibility with both local and remote clients.

- **Client Access**:
  - Seamless mounting of shared directories.
  - Efficient synchronization between server and client.

- **GUI Interface**:
  - **Tinker**-based graphical interface for managing NFS settings, viewing logs, and troubleshooting issues. The GUI provides an intuitive interface for both server and client-side interactions.

- **Logging and Monitoring**:
  - Maintain detailed logs for shared file access to assist with troubleshooting and system auditing.

---

## 🛠 System Requirements

- **Operating System**: Ubuntu 20.04 or higher, or any compatible Linux distribution.
- **Required Tools**:
  - `nfs-kernel-server` for the server-side configuration.
  - `nfs-common` for the client-side operations.
- **Networking**:
  - Server and client need network connectivity, either local or remote.
- **Testing Environment**:
  - Setup verified using **Windows Subsystem for Linux (WSL)**.

---

## ⚙️ Installation

### Server Setup

1. **Install NFS Kernel Server**:

   ```bash
   sudo apt update
   sudo apt install nfs-kernel-server
   ```

2. **Define Shared Directories**: Edit the `/etc/exports` file to specify the directories that will be shared:

   ```bash
   /exports/backup 127.0.0.1(rw,sync,no_root_squash)
   /exports/docs 127.0.0.1(rw,sync,no_root_squash)
   /exports/testfolder 127.0.0.1(rw,sync,no_root_squash)
   ```

3. **Export Configurations**:

   ```bash
   sudo exportfs -a
   ```

4. **Start and Enable NFS Service**:

   ```bash
   sudo systemctl start nfs-kernel-server
   sudo systemctl enable nfs-kernel-server
   ```

### Client Setup

1. **Install NFS Utilities**:

   ```bash
   sudo apt update
   sudo apt install nfs-common
   ```

2. **Mount the NFS Shares**:

   ```bash
   sudo mount -t nfs <server-ip>:/exports/backup /mnt/nfs/backup
   sudo mount -t nfs <server-ip>:/exports/docs /mnt/nfs/docs
   sudo mount -t nfs <server-ip>:/exports/testfolder /mnt/nfs/testfolder
   ```

---

## 🚀 Usage

1. **Start the NFS Server**: Ensure that the server is running:

   ```bash
   sudo systemctl start nfs-kernel-server
   ```

2. **Access Shared Files**: On the client, navigate to the mounted directories to access the shared files:

   ```bash
   cd /mnt/nfs/backup
   ```

3. **View Mounted Directories**:

   ```bash
   showmount -e <server-ip>
   ```

4. **Unmount Directories**: Once finished, unmount the directories:

   ```bash
   sudo umount /mnt/nfs/backup
   sudo umount /mnt/nfs/docs
   sudo umount /mnt/nfs/testfolder
   ```

5. **Logs and Troubleshooting**:
   - **Verify Exported Shares**:

     ```bash
     sudo exportfs
     ```

   - **Check Logs in `/var/log/syslog` for Debugging**:

     ```bash
     sudo tail -f /var/log/syslog
     grep nfs /var/log/syslog
     ```

---

## 📂 File Structure

```
NFS-Manager/
├── exports/                 # NFS server exports configuration
│   └── nfs_exports.conf     # NFS exports configuration file
├── setup_guide.txt          # Detailed terminal commands for NFS server and client setup
├── README.md                # Project documentation (this file)
├── logs/                    # Logs directory for NFS activities
│   └── server_log.txt       # Log file for tracking NFS server activities
├── server/                  # Python server-side script
│   └── nfs_export_manager.py # Python script for NFS server functionality
└── client/                  # Python client-side script
    └── nfs_manager.py       # Python script for NFS client functionality
└── ui_screenshots/          # Folder for UI screenshots
    └── screenshot1.png      # Example screenshot of the GUI interface
    └── screenshot2.png      # Another screenshot of the GUI
```

---

## 🖼️ UI Screenshots

The `ui_screenshots` folder contains visual representations of the **Graphical User Interface (GUI)** for NFS management. Screenshots include:

- **Main Dashboard**: A view of the NFS configuration and shared directory status.
- **Logs Viewer**: A screenshot showing logs of file access activities.
- **Configuration Panel**: A screenshot for managing server settings and shared directories.

---

## 🔮 Future Enhancements

### 1. **Additional Features for the GUI**
   - **Objective**: Enhance the existing GUI to provide more functionalities like configuring server-side permissions, managing multiple clients, and viewing detailed access logs.
   - **Benefit**: Further streamlines NFS management for users, making the system even more user-friendly.

### 2. **Support for Multiple Clients**
   - **Objective**: Improve the server to handle multiple clients with various access levels (e.g., read-only for some clients, read-write for others).
   - **Benefit**: Makes the NFS system scalable and adaptable to more complex network environments.

### 3. **Automated Backup and Synchronization**
   - **Objective**: Implement scripts that automatically back up shared directories and synchronize data between server and clients.
   - **Benefit**: Ensures data is consistently backed up, preventing data loss.

### 4. **Security Enhancements**
   - **Objective**: Add **Kerberos authentication** to ensure secure communication between server and client, along with additional firewall and encryption measures.
   - **Benefit**: Increases the security of the NFS system by protecting data and verifying identities.

### 5. **Cloud Integration**
   - **Objective**: Integrate cloud storage services (e.g., AWS S3, Google Cloud Storage) for off-site backups.
   - **Benefit**: Adds redundancy and ensures data protection in case of hardware failure.

---

## 🧩 Challenges Faced

- **Compatibility Issues with WSL**: One of the major challenges was ensuring that the NFS server and client configuration worked smoothly within **Windows Subsystem for Linux (WSL)**. NFS is primarily designed for Linux, so some tweaks and workarounds were required to get it to function correctly in a WSL environment.
- **File Permissions and Access Control**: Configuring granular file permissions and ensuring that clients could only access the appropriate directories was tricky. It involved editing the `/etc/exports` file multiple times to get the correct permissions.
- **Performance Issues**: There were some performance-related challenges when accessing files over the network. This was mainly related to the size and number of files being shared and required optimization for smooth synchronization between the server and clients.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository, make changes, and submit a pull request. All contributions will be reviewed for quality and compatibility with the project goals.

---

## 🙏 Acknowledgements

- Special thanks to the **Linux Foundation** for providing the documentation on NFS setup.
- Thanks to **WSL (Windows Subsystem for Linux)** for allowing the creation of this project in a Windows-based environment.
- All contributors and open-source communities who continuously improve network protocols like NFS.

---
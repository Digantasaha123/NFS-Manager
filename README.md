# Network File System (NFS) Project

This project showcases the setup, configuration, and usage of a **Network File System (NFS)** to facilitate efficient and secure file sharing over a network. The project demonstrates both server and client configurations, tested in a Linux-based environment with **Windows Subsystem for Linux (WSL)**, simulating real-world scenarios.

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
- [Future Enhancements](#future-enhancements)
- [Challenges Faced](#challenges-faced)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## 📖 Introduction

The **Network File System (NFS)**  allows files to be accessed and shared across multiple systems over a network as if they were local files. This project provides a guide to configure an NFS server and client, focusing on file synchronization, secure sharing, and scalability. The setup emphasizes educational purposes, enabling users to understand NFS concepts while exploring real-world networking challenges.

---

## ✨ Features

- **Server Configuration**:
  - Share directories with customizable permissions.
  - Support for read-only or read-write access.
  - Compatibility with local and remote clients.

- **Client Access**:
  - Mount shared directories seamlessly.
  - Ensure robust synchronization with the server.

- **Planned GUI Integration**:
  - A graphical interface using **Tinker** for easy NFS management.

- **Logging and Monitoring**:
  - Maintain logs of shared file access for troubleshooting and auditing.

---

## 🛠 System Requirements

- **Operating System**: Ubuntu 20.04 or higher, or compatible Linux distribution.
- **Tools Required**:
  - `nfs-kernel-server` (for the server configuration).
  - `nfs-common` (for client-side operations).
- **Networking**:
  - Both server and client require network connectivity (local or remote).
- **Testing Environment**:
  - Verified using **Windows Subsystem for Linux (WSL)** instances.

---

## ⚙️ Installation

### Server Setup

1. **Install NFS Kernel Server**:
   ```bash
   sudo apt update
   sudo apt install nfs-kernel-server

2. **Define Shared Directories:**  Edit the /etc/exports file to specify directories to be shared:
    ```bash
   /exports/backup 127.0.0.1(rw,sync,no_root_squash)
   /exports/docs 127.0.0.1(rw,sync,no_root_squash)
   /exports/testfolder 127.0.0.1(rw,sync,no_root_squash)

3. **Export Configurations:**
    ```bash
    sudo exportfs -a

4. **Start and Enable the NFS Service:**
     ```bash
    sudo systemctl start nfs-kernel-server
    sudo systemctl enable nfs-kernel-server

### Client Setup 

1.**Install NFS Utilities:**
    ```bash
    sudo apt update
    sudo apt install nfs-common

2.**Mount the NFS Share:**
    ```bash
    sudo mount -t nfs <17..30.146.44>:/exports/backup /mnt/nfs/backup
    sudo mount -t nfs <17..30.146.44>:/exports/docs /mnt/nfs/docs
    sudo mount -t nfs <17..30.146.44>:/exports/testfolder /mnt/nfs/testfolder

---

## 🚀 Usage

1. **Start the NFS Server:**  Ensure the server is running:
    ```bash
    sudo systemctl start nfs-kernel-server
    
2. **Access Shared Files:** On the client, navigate to the mounted directory to access shared files:
    cd /mnt/nfs/backup

3. **Show Mounted Directories**
     showmount -e 172.30.146.44

4. **Unmount When Done**: To unmount the directory:
    sudo umount /mnt/nfs/backup
    sudo umount /mnt/nfs/docs
    sudo umount /mnt/nfs/testfolder

5. **Logs and Troubleshooting:**
    5.1  *Verify Exported Shares with exportfs*
        exportfs

    5.2 *Check Logs in /var/log/syslog for Debugging*
        sudo tail -f /var/log/syslog
        grep nfs /var/log/syslog


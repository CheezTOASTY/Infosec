#    __                         __                                      
#  _/  |_  _________    _______/  |________   ____   ____  ____   ____  
#  \   __\/  _ \__  \  /  ___/\   __\_  __ \_/ __ \_/ ___\/  _ \ /    \ 
#   |  | (  <_> ) __ \_\___ \  |  |  |  | \/\  ___/\  \__(  <_> )   |  \
#   |__|  \____(____  /____  > |__|  |__|    \___  >\___  >____/|___|  /
#                   \/     \/                    \/     \/           \/ 
#  PacketChx v1.6                                                                     
                                                                     

import hashlib
import os
import time
import logging
import smtplib
from tkinter import Tk, filedialog, messagebox
from plyer import notification

# Setup logging
def setup_logging():
    logging.basicConfig(
        filename="file_integrity.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO
    )

# Generate the hash of a file
def hash_file(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None

# Monitor files for changes
def monitor_files(file_paths, interval, email_config):
    file_hashes = {}
    
    # Initialize file hashes
    for file in file_paths:
        file_hashes[file] = hash_file(file)
    
    print(f"Monitoring {len(file_paths)} files for changes every {interval} seconds...")
    
    while True:
        for file in file_paths:
            current_hash = hash_file(file)
            if current_hash is None:
                continue
            if file_hashes[file] != current_hash:
                message = f"[ALERT] Change detected in file: {file}"
                print(message)
                logging.warning(message)
                file_hashes[file] = current_hash
                send_email_alert(email_config, file)
                show_desktop_notification(file)
        time.sleep(interval)

# Send email alert
def send_email_alert(email_config, file):
    try:
        with smtplib.SMTP(email_config["smtp_server"], email_config["port"]) as server:
            server.starttls()
            server.login(email_config["sender_email"], email_config["password"])
            message = f"Subject: File Integrity Alert\n\nChange detected in file: {file}"
            server.sendmail(email_config["sender_email"], email_config["receiver_email"], message)
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

# Show desktop notification
def show_desktop_notification(file):
    notification.notify(
        title="File Integrity Alert",
        message=f"Change detected in file: {file}",
        timeout=10
    )

# GUI for file selection
def select_files():
    root = Tk()
    root.withdraw()  # Hide the root window
    files = filedialog.askopenfilenames(title="Select Files to Monitor")
    return list(files)

def main():
    setup_logging()
    print("=== Enhanced File Integrity Checker ===")
    
    # GUI for file selection
    files = select_files()
    if not files:
        messagebox.showerror("Error", "No files selected!")
        return
    
    # Monitoring interval
    interval = int(input("Enter the monitoring interval (in seconds): "))
    
    # Email configuration
    email_config = {
        "smtp_server": input("Enter SMTP server (e.g., smtp.gmail.com): "),
        "port": int(input("Enter SMTP port (e.g., 587): ")),
        "sender_email": input("Enter sender's email address: "),
        "password": input("Enter sender's email password: "),
        "receiver_email": input("Enter receiver's email address: ")
    }
    
    # Start monitoring
    monitor_files(files, interval, email_config)

if __name__ == "__main__":
    main()
#    __                         __                                      
#  _/  |_  _________    _______/  |________   ____   ____  ____   ____  
#  \   __\/  _ \__  \  /  ___/\   __\_  __ \_/ __ \_/ ___\/  _ \ /    \ 
#   |  | (  <_> ) __ \_\___ \  |  |  |  | \/\  ___/\  \__(  <_> )   |  \
#   |__|  \____(____  /____  > |__|  |__|    \___  >\___  >____/|___|  /
#                   \/     \/                    \/     \/           \/ 
#  GoPhish v1.0                                                                     
                                                                     

import smtplib
import random
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import csv

# Setup logging
def setup_logging():
    logging.basicConfig(
        filename="phishing_simulation.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO
    )

# Email templates for phishing
PHISHING_TEMPLATES = [
    {
        "subject": "Urgent: Account Verification Needed",
        "body": "Your account has been flagged for suspicious activity. Please verify your credentials here: http://localhost:8000/?user={user}."
    },
    {
        "subject": "Payroll Update Required",
        "body": "We couldn't process your recent payroll. Please update your information here: http://localhost:8000/?user={user}."
    },
    {
        "subject": "You've Won a Prize!",
        "body": "Congratulations! Click here to claim your prize: http://localhost:8000/?user={user}."
    }
]

# Response tracking
def start_tracking_server(tracking_data):
    class TrackingHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            user = self.path.split("user=")[-1]
            tracking_data.append({"user": user, "timestamp": self.log_date_time_string()})
            logging.info(f"Tracked interaction from user: {user}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Thank you for participating in the simulation.")

    server = HTTPServer(("0.0.0.0", 8000), TrackingHandler)
    print("Tracking server running on http://localhost:8000...")
    server.serve_forever()

# Send phishing email
def send_phishing_email(sender_email, sender_password, recipient_email, user_id):
    template = random.choice(PHISHING_TEMPLATES)
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = template["subject"]
    body = template["body"].format(user=user_id)
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logging.info(f"Phishing email sent to {recipient_email} with subject: {template['subject']}")
        print(f"Phishing email sent to {recipient_email}.")
    except Exception as e:
        logging.error(f"Error sending email to {recipient_email}: {e}")
        print(f"Error: {e}")

# Generate report
def generate_report(tracking_data):
    with open("phishing_report.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["user", "timestamp"])
        writer.writeheader()
        writer.writerows(tracking_data)
    print("Report generated: phishing_report.csv")
    logging.info("Phishing simulation report generated.")

def main():
    setup_logging()
    print("=== Phishing Email Simulation Tool ===")

    sender_email = input("Enter the sender's email address: ")
    sender_password = input("Enter the sender's email password: ")
    recipient_email = input("Enter the recipient's email address: ")
    user_id = input("Enter a unique ID for the recipient (e.g., employee ID): ")

    # Start tracking server in a separate thread
    tracking_data = []
    threading.Thread(target=start_tracking_server, args=(tracking_data,), daemon=True).start()

    # Send phishing email
    send_phishing_email(sender_email, sender_password, recipient_email, user_id)

    input("Press Enter to stop tracking and generate the report...")
    generate_report(tracking_data)

if __name__ == "__main__":
    main()
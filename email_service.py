import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "your_smtp_server"
SMTP_PORT = 587
SMTP_USERNAME = "your_email_address"
SMTP_PASSWORD = "your_email_password"

def send_email(subject, body, recipient, smtp_details):
    msg = MIMEMultipart()
    msg['From'] = smtp_details['username']
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_details['server'], smtp_details['port'])
    server.starttls()
    server.login(smtp_details['username'], smtp_details['password'])
    text = msg.as_string()
    server.sendmail(smtp_details['username'], recipient, text)
    server.quit()

def generate_verification_token():
    return secrets.token_urlsafe(16)

def generate_verification_link(username):
    token = generate_verification_token()
    # Store the token in the database for the user
    database_connection.add_verification_token(username, token)
    return f"http://yourdomain.com/verify?token={token}"

def send_verification_email(email, username):
    smtp_details = {
        "server": SMTP_SERVER,
        "port": SMTP_PORT,
        "username": SMTP_USERNAME,
        "password": SMTP_PASSWORD
    }
    verification_link = generate_verification_link(username)
    subject = "Verify Your Email"
    body = f"Please click on the link to verify your account: {verification_link}"
    send_email(subject, body, email, smtp_details)

def send_admin_creation_request(admin_email, new_admin_data):
    smtp_details = {
        "server": SMTP_SERVER,
        "port": SMTP_PORT,
        "username": SMTP_USERNAME,
        "password": SMTP_PASSWORD
    }
    subject = "Admin Account Creation Request"
    body = f"New Admin Data: Username - {new_admin_data['username']}, Email - {new_admin_data['email']}\nPlease create an admin account for this user."
    send_email(subject, body, admin_email, smtp_details)

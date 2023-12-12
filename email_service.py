def send_verification_email(email, username, smtp_details):
    verification_link = generate_verification_link(username)
    subject = "Verify Your Email"
    body = f"Please click on the link to verify your account: {verification_link}"
    # send_email(subject, body, email, **smtp_details)
    # For now, let's just print it (Replace with actual email sending in production)
    print(f"Verification email to {email}: {verification_link}")


def send_admin_creation_request(admin_email, new_admin_data):
    # Simulate sending an email to the admin
    print(f"Admin Creation Request to {admin_email}:")
    print(f"New Admin Data: Username - {new_admin_data['username']}, Email - {new_admin_data['email']}")
    print("Please create an admin account for this user.")

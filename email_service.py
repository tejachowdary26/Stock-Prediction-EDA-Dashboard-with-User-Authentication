def send_verification_email(email, username):
    verification_link = f"http://example.com/verify?user={username}"
    print(f"Send this verification link to {email}: {verification_link}")

def send_admin_creation_request(admin_email, new_admin_data):
    # Simulate sending an email to the admin
    print(f"Admin Creation Request to {admin_email}:")
    print(f"New Admin Data: Username - {new_admin_data['username']}, Email - {new_admin_data['email']}")
    print("Please create an admin account for this user.")

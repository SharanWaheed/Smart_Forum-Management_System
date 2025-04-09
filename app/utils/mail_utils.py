from app import mail
from flask_mail import Message

def send_email(subject, recipient, body):
    # Debugging - print the recipient email to check if it's valid
    print(f"Sending email to: {recipient}")

    # Check if the recipient is a valid email address
    if "@" not in recipient:
        raise ValueError(f"Invalid email address: {recipient}")

    # Create the email message
    msg = Message(subject=subject,
                  recipients=[recipient],
                  body=body)
    mail.send(msg)  # Send the email using the 'mail' object


#Look for Sockets 
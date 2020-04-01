#!/usr/bin/env python3

import email.message
import mimetypes
import os.path
import smtplib

server_address = ""

def generate(sender, recipient, subject, body, attachment_path):
    """Creates an email with an attachment."""
    # Basic Email formatting
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    if not attachment_path is None:
        # Process the attachment and add it to the email
        attachment_filename = os.path.basename(attachment_path)
        mime_type, _ = mimetypes.guess_type(attachment_path)
        mime_type, mime_subtype = mime_type.split('/', 1)

        with open(attachment_path, 'rb') as ap:
            message.add_attachment(ap.read(),
                                    maintype=mime_type,
                                    subtype=mime_subtype,
                                    filename=attachment_filename)
    
    return message

# This method does not use ssl, therefore no credentials are used and it is unsecure
def send(message):
    """Sends the message to the configured SMTP server."""
    mail_server = smtplib.SMTP(server_address)
    mail_server.send_message(message)
    mail_server.quit()
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"  # Your Gmail address
APP_PASSWORD = "your-16-digit-app-password"  # Your 16-digit app password

# Add delay between emails to avoid Gmail limits
DELAY_BETWEEN_EMAILS = 1  # seconds

# Email template
def create_email_template(recipient_email):
    subject = "Important: IAED Online Account Password Reset and Next Steps"
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #003366;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 5px 5px 0 0;
            }
            .content {
                background-color: #ffffff;
                padding: 20px;
                border: 1px solid #dddddd;
            }
            .section {
                margin-bottom: 20px;
                padding: 15px;
                background-color: #f9f9f9;
                border-left: 4px solid #003366;
            }
            .important-notes {
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
            }
            .help-section {
                background-color: #e8f4f8;
                border-left: 4px solid #17a2b8;
                padding: 15px;
                margin: 20px 0;
            }
            .footer {
                text-align: center;
                padding: 20px;
                color: #666666;
                font-size: 14px;
            }
            h2 {
                color: #003366;
                margin-top: 0;
            }
            ul {
                padding-left: 20px;
            }
            a {
                color: #0066cc;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>IAED Member Update</h1>
            </div>
            
            <div class="content">
                <p>Dear IAED Member,</p>
                
                <p>We hope this email finds you well. We're writing to inform you about important updates regarding your IAED online account.</p>
                
                <div class="section">
                    <h2>Password Reset Notice</h2>
                    <p>Your account on the new IAED website (<a href="https://www.iaedonline.com/">iaedonline.com</a>) will be receiving a password reset notification.</p>
                </div>

                <div class="section">
                    <h2>Required Steps After Reset</h2>
                    <ol>
                        <li>
                            <strong>Complete Your Profile:</strong>
                            <ul>
                                <li>Visit: <a href="https://www.iaedonline.com/membership-account/your-profile/">Your Profile Page</a></li>
                                <li>Update all your information to ensure your listing is current</li>
                            </ul>
                        </li>
                        <li>
                            <strong>Submit Your Certification Documents:</strong>
                            <ul>
                                <li>Submit your Continuing Education documents to maintain IAED Certification</li>
                                <li>This will ensure you're listed on our <a href="https://www.iaedonline.com/all-members/">Members and Find An Equine Dentist page</a></li>
                                <li>Review <a href="https://www.iaedonline.com/certification/">certification guidelines</a></li>
                            </ul>
                        </li>
                    </ol>
                </div>

                <div class="important-notes">
                    <h2>Important Notes</h2>
                    <ul>
                        <li>If your membership shows as expired, please purchase an annual or monthly subscription at: <a href="https://www.iaedonline.com/membership-account/membership-levels/">Membership Levels</a></li>
                        <li>If you believe you have an active subscription but it's not showing, please email: <a href="mailto:ucid@andrewsama.com">ucid@andrewsama.com</a></li>
                    </ul>
                </div>

                <div class="help-section">
                    <h2>Need Help?</h2>
                    <p>For any assistance with profile setup or membership issues, please contact: <a href="mailto:ucid@andrewsama.com">ucid@andrewsama.com</a></p>
                </div>

                <div class="footer">
                    <p>Thank you for your continued membership with IAED.</p>
                    <p><strong>Best regards,<br>IAED Team</strong></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Add both plain text and HTML versions
    text = """
    Dear IAED Member,

    We hope this email finds you well. We're writing to inform you about important updates regarding your IAED online account.

    Your account on the new IAED website (https://www.iaedonline.com/) will be receiving a password reset notification. Once you've reset your password, please complete these two important steps:

    1. Complete Your Profile:
       - Visit: https://www.iaedonline.com/membership-account/your-profile/
       - Update all your information to ensure your listing is current

    2. Submit Your Certification Documents:
       - Submit your Continuing Education documents to maintain IAED Certification
       - This will ensure you're listed on our Members and Find An Equine Dentist page: https://www.iaedonline.com/all-members/
       - Review certification guidelines at: https://www.iaedonline.com/certification/

    Important Notes:
    - If your membership shows as expired, please purchase an annual or monthly subscription at: https://www.iaedonline.com/membership-account/membership-levels/
    - If you believe you have an active subscription but it's not showing, please email: ucid@andrewsama.com

    Need Help?
    For any assistance with profile setup or membership issues, please contact: ucid@andrewsama.com

    Thank you for your continued membership with IAED.

    Best regards,
    IAED Team
    """

    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    
    return msg

def send_emails():
    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        
        # Read email list
        with open('mailing_list.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            total_emails = 0
            successful_sends = 0
            
            for row in csv_reader:
                recipient_email = row['email']
                try:
                    msg = create_email_template(recipient_email)
                    server.send_message(msg)
                    successful_sends += 1
                    print(f"Successfully sent email to: {recipient_email}")
                    
                    # Add delay between sends
                    time.sleep(DELAY_BETWEEN_EMAILS)
                    
                except Exception as e:
                    print(f"Failed to send email to {recipient_email}: {str(e)}")
                total_emails += 1

                # Gmail sending limits check
                if total_emails % 80 == 0:  # Gmail daily limit is ~500, so pause every 80 emails
                    print("Pausing for 1 minute to avoid Gmail limits...")
                    time.sleep(60)

        # Close the server connection
        server.quit()
        
        print(f"\nEmail sending complete!")
        print(f"Successfully sent: {successful_sends}/{total_emails} emails")
        
    except Exception as e:
        print(f"Error connecting to SMTP server: {str(e)}")

if __name__ == "__main__":
    send_emails() 
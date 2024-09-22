import firebase_admin
from firebase_admin import credentials, auth
import smtplib
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize Firebase Admin SDK
cred = credentials.Certificate("sch-relay-firebase-adminsdk-yvm46-58d9223eaa.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sch-relay-default-rtdb.firebaseio.com/'  # Replace with your database URL
})


# Function to generate a random password
def generate_password(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


# Function to send email with generated password
def send_password_email(client_email, password):
    sender_email = "your-email@gmail.com"
    sender_password = "your-email-password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = "Your Registration Password"

    body = f"Hello,\n\nYour password is: {password}\nPlease use this password to log in."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, client_email, text)
    server.quit()


# Function to create a new user in Firebase Authentication
def register_user_with_firebase(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f'Successfully created new user: {user.uid}')
    except Exception as e:
        print(f'Error creating new user: {str(e)}')


# Main function to handle client registration
def client_registration():
    client_email = input("Enter your email: ")
    password = generate_password()

    # Send password to the client via email
    send_password_email(client_email, password)

    # Register the user with Firebase Authentication
    register_user_with_firebase(client_email, password)

    print("Registration complete. Please check your email for the password.")
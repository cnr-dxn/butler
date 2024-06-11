import imaplib
import email
from email.header import decode_header
import webbrowser
import os

username = "connnorprojects28@gmail.com"
password = os.environ['MERCEDES']
print(password)

try:
	# Connect to the server
	mail = imaplib.IMAP4_SSL("imap.gmail.com")
	# Login to your account
	mail.login(username, password)
	print("no way")
except Exception as e:
	print(f"gah damn: {e}")


# Importing required packages

import smtplib
import ssl
from config import *
from email.message import EmailMessage

# Welcome function UI


def welcome():
    print('=' * 50)
    print('Mass Mailer by Ali Baig\n')

    email_type = (input(f"""1. Plain-Text Email
2. HTML Email
{'=' * 50}
Enter email type: """))

    return email_type

# Function to get mail list from text file


def get_mail_list():
    mail_list = input('Enter mail list: ')
    mail_list_ = list()

    try:
        with open(mail_list, 'r') as contacts:
            for each_contact in contacts:
                if '\n' in each_contact:
                    mail_list_.append(each_contact[:-1])
                else:
                    mail_list_.append(each_contact)
        return mail_list_

    except Exception as error:
        print('Error:', error)
        exit(0)

# Function to send email in plain-text format


def text_email(message):
    file_name = input('Enter txt file with email body: ')
    try:
        with open(file_name, 'r') as email_body:
            message.set_content(email_body.read())

    except Exception as error:
        print('Error:', error)
        exit(0)

# Function to send email in HTML format


def html_email(message):
    body = input('Enter html file with email body: ')
    try:
        with open(body, 'r') as email_body:
            message.add_alternative(email_body.read(), subtype='html')
    except Exception as error:
        print('Error:', error)
        exit(0)

# Function to connect to the SMTP server


def smtp_connection(message):
    if smtp_server['smtp_port'] == 465:

        try:
            with smtplib.SMTP_SSL(smtp_server['smtp_host'], smtp_server['smtp_port']) as smtp:
                print('Logging in to the SMTP server ')
                smtp.login(smtp_server['smtp_username'], smtp_server['smtp_password'])
                print('Logged in Successfully')
                print('Sending messages! Please wait...')
                smtp.send_message(message)
        except Exception as e:
            print('Error:', e)

    elif smtp_server['smtp_port'] == 587:

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(smtp_server['smtp_host'], smtp_server['smtp_port']) as smtp:
                smtp.ehlo()
                smtp.starttls(context=context)
                smtp.ehlo()
                print('Logging in to the SMTP server ')
                smtp.login(smtp_server['smtp_username'], smtp_server['smtp_password'])
                print('Logged in Successfully')
                print('Sending messages! Please wait...')

                for each_email in temp:
                    smtp.sendmail(message['From'], each_email, message)
        except Exception as e:
            print('Error:', e)


welcome = welcome()

# Email related information collection
msg = EmailMessage()
temp = get_mail_list()
msg['To'] = temp
msg['From'] = input('Enter sender\'s email: ')
msg['Subject'] = input('Enter subject: ')

if welcome == '1':
    text_email(msg)

elif welcome == '2':
    html_email(msg)

else:
    print('Not a valid choice!\nThe program will exit now')
    exit(0)

smtp_connection(msg)
print('Done!')
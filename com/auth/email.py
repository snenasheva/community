import base64
import json
import os.path

from flask import current_app, render_template
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_service():
    creds = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            print('Loaded credentials from file')
        except json.JSONDecodeError as e:
            print(f'Error decoding {token_path}. Deleting the file and re-authenticating. Details: {e}')
            os.remove(token_path)
        except Exception as e:
            print(f'Unexpected error loading credentials: {e}')
            os.remove(token_path)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print('Refreshed credentials.')
            except Exception as e:
                print(f'Error refreshing credentials {e}')
                creds = None

        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=8000)
                print('OAuth flow completed successfully.')
                print(f'Credentials after OAuth flow: {creds}')
            except Exception as e:
                print(f'Error during OAuth flow: {e}')
                return None
        if creds:
            try:
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                print('Credentials saved to the file')
            except Exception as e:
                print(f'Error saving credentials to the file: {e}')

    try:
        if creds is None:
            raise ValueError('Credentials are not properly initialized.')
        service = build('gmail', 'v1', credentials=creds)
        return service
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(f'Error: "credentials.json" or "token.json" not found. Please, ensure these files exists')
        print(f'Details: {e}')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
    except Exception as e:
        print(f'Unexpected error occurred: {type:(e).__name__}: {e}')

    return None


def send_email_gmail(subject, sender, to, message_text):
    service = get_gmail_service()
    if service:
        message = {
            "raw": base64.urlsafe_b64encode(f"From: {sender}\r\n"
                                            f"To: {to}\r\n"
                                            f"Subject: {subject}\r\n\r\n"
                                            f"{message_text}".encode('utf-8')
                                            ).decode('utf-8')
        }
        try:
            # sending the email
            message = service.users().messages().send(userId='me', body=message).execute()
            print(f'Message sent! ID: {message["id"]}')
            return message
        except HttpError as error:
            print(f'An error occurred {error}')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')

        return None


def send_verification_email(user):
    token = user.get_reset_psw_token()
    text_body = render_template('email/email_verification.txt', user=user, username=user.username, token=token)
    send_email_gmail(
        subject='Confirm your registration',
        message_text=text_body,
        sender=current_app.config['ADMINS'][0],
        to=user.email
    )


def send_psw_reset_email(user):
    token = user.get_reset_psw_token()
    text_body = render_template('email/reset_password.txt', user=user, username=user.username, token=token)
    send_email_gmail(
        subject='Reset your password',
        sender=current_app.config['ADMINS'][0],
        to=user.email, message_text=text_body,
    )
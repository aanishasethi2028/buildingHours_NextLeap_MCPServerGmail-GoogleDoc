import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from auth import get_credentials


def create_email_draft(to: str, subject: str, body: str):
    """
    Creates a new draft email in the user's Gmail account.
    """
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    message = EmailMessage()
    message.set_content(body)
    message["To"] = to
    message["From"] = "me"  # 'me' refers to the authenticated user
    message["Subject"] = subject

    # Encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"message": {"raw": encoded_message}}

    draft = (
        service.users()  # pylint: disable=no-member
        .drafts()
        .create(userId="me", body=create_message)
        .execute()
    )

    return draft

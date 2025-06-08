from typing import Any
import os
from mcp.server.fastmcp import FastMCP

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

import base64
from email.mime.text import MIMEText

import asyncio

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.insert",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/gmail.settings.sharing"
]

mcp = FastMCP("gmail_tools")

def get_gmail_service():
    creds = None
    token_file = "token.json"

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000, access_type='offline', prompt='consent')
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

import json
from email.utils import parsedate_to_datetime

@mcp.tool()
async def read_inbox(count: int = 5) -> str:
    service = get_gmail_service()
    messages = service.users().messages().list(userId='me', maxResults=count).execute().get('messages', [])
    output = []

    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_detail.get("payload", {}).get("headers", [])
        
        def get_header(name):
            return next((h["value"] for h in headers if h["name"].lower() == name.lower()), None)

        subject = get_header("Subject") or "(No Subject)"
        sender = get_header("From") or "(Unknown Sender)"
        recipient = get_header("To") or "(Unknown Recipient)"
        date_str = get_header("Date")
        
        try:
            date = parsedate_to_datetime(date_str).isoformat() if date_str else None
        except Exception:
            date = date_str
        
        snippet = msg_detail.get('snippet', '')
        thread_id = msg_detail.get('threadId', '')
        message_id = msg_detail.get('id', '')
        labels = msg_detail.get('labelIds', [])
        
        output.append({
            "subject": subject,
            "snippet": snippet,
            "from": sender,
            "to": recipient,
            "date": date,
            "threadId": thread_id,
            "messageId": message_id,
            "labels": labels
        })

    print(output)
    return json.dumps(output, indent=2)

@mcp.tool()
async def send_mail(to: str, subject: str, body: str) -> str:
    service = get_gmail_service()
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    try:
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        return f"Email sent to {to}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def list_labels() -> str:
    service = get_gmail_service()
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    return "\n".join([label['name'] for label in labels])

@mcp.tool()
async def mark_as_read(message_id: str) -> str:
    service = get_gmail_service()
    service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
    return f"Marked {message_id} as read."

@mcp.tool()
async def delete_email(message_id: str) -> str:
    service = get_gmail_service()
    service.users().messages().delete(userId='me', id=message_id).execute()
    return f"Deleted email with ID {message_id}."

@mcp.tool()
async def create_label(name: str) -> str:
    service = get_gmail_service()
    body = {"name": name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
    service.users().labels().create(userId='me', body=body).execute()
    return f"Label '{name}' created."

@mcp.tool()
async def list_drafts() -> str:
    service = get_gmail_service()
    drafts = service.users().drafts().list(userId='me').execute().get('drafts', [])
    return f"Draft count: {len(drafts)}"

@mcp.tool()
async def create_draft(to: str, subject: str, body: str) -> str:
    service = get_gmail_service()
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft = {'message': {'raw': raw}}
    service.users().drafts().create(userId='me', body=draft).execute()
    return "Draft created."

@mcp.tool()
async def get_signature() -> str:
    service = get_gmail_service()
    settings = service.users().settings().sendAs().list(userId='me').execute()
    primary = next((s for s in settings.get("sendAs", []) if s.get("isPrimary")), None)
    return primary.get("signature", "No signature found") if primary else "Primary account not found"

@mcp.tool()
async def set_signature(signature: str) -> str:
    service = get_gmail_service()
    settings = service.users().settings().sendAs().list(userId='me').execute()
    primary = next((s for s in settings.get("sendAs", []) if s.get("isPrimary")), None)
    if primary:
        service.users().settings().sendAs().patch(
            userId='me', sendAsEmail=primary['sendAsEmail'], body={'signature': signature}
        ).execute()
        return "Signature updated."
    return "Primary account not found"

if __name__ == "__main__":
    print("[INFO] Gmail MCP server starting...", flush=True)
    # asyncio.run(create_label('CodeBreaker'))
    # asyncio.run(read_inbox(20))
    mcp.run(transport="streamable-http")
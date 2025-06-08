import json
from typing import ClassVar
from langchain.tools import BaseTool

from mcp_client import (
    read_inbox_sync,
    send_mail_sync,
    create_label_sync,
    delete_email_sync,
    create_draft_sync,
    get_signature_sync,
    set_signature_sync,
)


class GmailInboxTool(BaseTool):
    name: ClassVar[str] = "read_inbox"
    description: ClassVar[str] = "Reads the latest emails. Input is the number of emails to read."

    def _run(self, query: str) -> str:
        try:
            count = int(query)
        except Exception:
            count = 5
        return read_inbox_sync(count)

    async def _arun(self, query: str) -> str:
        return self._run(query)


class GmailSendTool(BaseTool):
    name: ClassVar[str] = "send_mail"
    description: ClassVar[str] = "Send an email. Input should be a JSON string with 'to', 'subject', and 'body'."

    def _run(self, query: str) -> str:
        try:
            data = json.loads(query)
            return send_mail_sync(data['to'], data['subject'], data['body'])
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, query: str) -> str:
        return self._run(query)


class GmailCreateLabelTool(BaseTool):
    name: ClassVar[str] = "create_label"
    description: ClassVar[str] = "Creates a Gmail label. Input is a string label name."

    def _run(self, query: str) -> str:
        return create_label_sync(query)

    async def _arun(self, query: str) -> str:
        return self._run(query)


class GmailDeleteEmailTool(BaseTool):
    name: ClassVar[str] = "delete_email"
    description: ClassVar[str] = "Deletes an email by ID. Input is a string email ID."

    def _run(self, query: str) -> str:
        return delete_email_sync(query)

    async def _arun(self, query: str) -> str:
        return self._run(query)


class GmailCreateDraftTool(BaseTool):
    name: ClassVar[str] = "create_draft"
    description: ClassVar[str] = "Creates a draft email. Input should be a JSON with 'to', 'subject', and 'body'."

    def _run(self, query: str) -> str:
        try:
            data = json.loads(query)
            return create_draft_sync(data['to'], data['subject'], data['body'])
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, query: str) -> str:
        return self._run(query)


class GmailGetSignatureTool(BaseTool):
    name: ClassVar[str] = "get_signature"
    description: ClassVar[str] = "Gets the current Gmail signature. No input required."

    def _run(self, query: str) -> str:
        return get_signature_sync()

    async def _arun(self, query: str) -> str:
        return self._run(query)


class GmailSetSignatureTool(BaseTool):
    name: ClassVar[str] = "set_signature"
    description: ClassVar[str] = "Sets the Gmail signature. Input is the new signature text."

    def _run(self, query: str) -> str:
        return set_signature_sync(query)

    async def _arun(self, query: str) -> str:
        return self._run(query)

gmail_tools = [
    GmailInboxTool(),
    GmailSendTool(),
    GmailCreateLabelTool(),
    GmailDeleteEmailTool(),
    GmailCreateDraftTool(),
    GmailGetSignatureTool(),
    GmailSetSignatureTool(),
]

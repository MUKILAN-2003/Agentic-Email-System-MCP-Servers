import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

MCP_URL = "http://127.0.0.1:8000/mcp"

async def call_mcp_read_inbox_tool(count: int) -> str:
    async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("read_inbox", {"count": count})
            return result

def read_inbox_sync(count: int) -> str:
    return asyncio.run(call_mcp_read_inbox_tool(count))

async def call_mcp_send_mail_tool(to: str, subject: str, body: str) -> str:
    async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("send_mail", {"to": to, "subject": subject, "body": body})
            return result

def send_mail_sync(to: str, subject: str, body: str) -> str:
    return asyncio.run(call_mcp_send_mail_tool(to, subject, body))

async def call_mcp_create_label_tool(label_name: str) -> str:
    async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("create_label", {"name": label_name})
            return result

def create_label_sync(label_name: str) -> str:
    return asyncio.run(call_mcp_create_label_tool(label_name))

async def call_mcp_delete_email_tool(email_id: str) -> str:
    async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("delete_email", {"email_id": email_id})
            return result

def delete_email_sync(email_id: str) -> str:
    return asyncio.run(call_mcp_delete_email_tool(email_id))

async def call_mcp_create_draft_tool(to: str, subject: str, body: str) -> str:
    async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("create_draft", {"to": to, "subject": subject, "body": body})
            return result

def create_draft_sync(to: str, subject: str, body: str) -> str:
    return asyncio.run(call_mcp_create_draft_tool(to, subject, body))

async def call_mcp_get_signature_tool() -> str:
    async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("get_signature", {})
            return result

def get_signature_sync() -> str:
    return asyncio.run(call_mcp_get_signature_tool())

async def call_mcp_set_signature_tool(signature: str) -> str:
    async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("set_signature", {"signature": signature})
            return result

def set_signature_sync(signature: str) -> str:
    return asyncio.run(call_mcp_set_signature_tool(signature))

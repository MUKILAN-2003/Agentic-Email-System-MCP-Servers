import streamlit as st
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from typing import ClassVar
import asyncio
import json

from mcp_client import read_inbox_sync, send_mail_sync, create_label_sync

class GmailInboxTool(BaseTool):
    name: ClassVar[str] = "read_inbox"
    description: ClassVar[str] = "Reads the latest emails from Gmail inbox. Input is the number of emails to read."

    def _run(self, query: str) -> str:
        try:
            count = int(query)
        except:
            count = 5
        return read_inbox_sync(count)

    async def _arun(self, query: str) -> str:
        return await asyncio.to_thread(self._run, query)

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
        return await asyncio.to_thread(self._run, query)
    
class GmailLabelTool(BaseTool):
    name: ClassVar[str] = "create_label"
    description: ClassVar[str] = "Create the lable. Input should be a JSON string with 'label_name'."

    def _run(self, query: str) -> str:
        try:
            data = json.loads(query)
            return create_label_sync(data['label_name'])
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, query: str) -> str:
        return await asyncio.to_thread(self._run, query)


def main():
    st.set_page_config(page_title="Gmail Chat Agent", layout="wide")
    st.title("📧 Gmail Assistant (LLM-Powered)")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        tools = [GmailInboxTool(), GmailSendTool(), GmailLabelTool()]
        llm = OpenAI(openai_api_key="OPENAI_API_KEY", temperature=0.5, model="gpt-4o-mini")
        st.session_state.agent = initialize_agent(
            tools, llm, agent="zero-shot-react-description", verbose=True
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask me to check or send emails...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = asyncio.run(asyncio.to_thread(st.session_state.agent.run, prompt))
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()

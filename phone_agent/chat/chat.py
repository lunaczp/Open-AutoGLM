"""Helper for fetching reply messages from an external chat service."""

import json
import os
from typing import Any

import requests


DEFAULT_CHAT_URL = "http://localhost:3000/customer-chat"


def getReplyMessage(
    messages: list[dict[str, Any]],
    *,
    url: str | None = None,
    agent_token: str | None = None,
    timeout: float = 15.0,
) -> str:
    """
    Send messages to the external chat service and return the reply text.

    Args:
        messages: Conversation history in OpenAI-style {"role", "content"} dicts.
        url: Optional override for the chat endpoint; defaults to env CHAT_API_URL or localhost.
        agent_token: Optional agent token for Cookie header; defaults to env CHAT_AGENT_TOKEN.
        timeout: Request timeout in seconds.

    Returns:
        Reply text from the service.
    """
    if not messages:
        raise ValueError("messages must not be empty")

    endpoint = url or os.getenv("CHAT_API_URL", DEFAULT_CHAT_URL)
    token = agent_token or os.getenv("CHAT_AGENT_TOKEN")

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Cookie"] = f"agenttoken={token}"

    response = requests.post(
        endpoint, headers=headers, json={"messages": messages}, timeout=timeout
    )
    response.raise_for_status()

    try:
        data = response.json()
    except ValueError:
        return response.text

    if isinstance(data, dict):
        for key in ("message", "reply"):
            value = data.get(key)
            if isinstance(value, str):
                return value
        return json.dumps(data, ensure_ascii=False)

    if isinstance(data, str):
        return data

    return json.dumps(data, ensure_ascii=False)

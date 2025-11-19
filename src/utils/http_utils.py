"""Utilities for sending HTTP requests."""

import json

import urllib3

# Initialize HTTP client
http = urllib3.PoolManager()


def format_message(card: dict) -> dict:
    """Format the Adaptive Card as a Teams message."""
    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": card,
            }
        ],
    }


def send_to_teams(  # noqa: ANN201
    card: dict, webhook_url: str
):
    """Send the populated card to Microsoft Teams.

    Parameters
    ----------
    card : dict
        The populated card template as a dictionary.
    webhook_url : str
        The webhook URL for the Microsoft Teams channel.

    Returns
    -------
    urllib3.BaseHTTPResponse
        The response from the Teams webhook.

    Raises
    ------
    ConnectionError
        If the Teams webhook fails to send the notification.

    """
    message = format_message(card)
    response = http.request(
        method="POST",
        url=webhook_url,
        headers={"Content-Type": "application/json"},
        body=json.dumps(message).encode("utf-8"),
    )
    if response.status not in [200, 202]:
        error_message = f"Failed to send notification to Teams: {response.status} - {response.data.decode('utf-8')}"
        raise ConnectionError(error_message)
    return response

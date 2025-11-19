"""Base handler for all lambda functions."""

import json
from abc import ABC, abstractmethod
from os import getenv

from utils.error_handling import raise_error
from utils.http_utils import send_to_teams
from utils.logging import setup_logger
from utils.template_utils import fetch_card_template, populate_card_template

logger = setup_logger()


class BaseHandler(ABC):
    """Base handler class for all lambdas."""

    def __init__(self, bucket_name: str, template_key: str):
        """Initialise the class."""
        self.bucket_name = bucket_name
        self.template_key = template_key

    @staticmethod
    def get_message_content(event: dict) -> dict:
        """Get sns content from event."""
        return json.loads(event["Records"][0]["Sns"]["Message"])

    def get_card_template(self) -> dict:
        """Get the template card as dictionary."""
        return fetch_card_template(bucket_name=self.bucket_name, template_key=self.template_key)

    @abstractmethod
    def fill_placeholders(self) -> dict:
        """Fill the placeholders."""

    def get_populated_card(self) -> dict:
        """Return the card filled with placeholders."""
        return populate_card_template(
            template=self.get_card_template(), placeholders=self.fill_placeholders()
        )

    def send_card_to_teams(self, populated_card: dict):
        """Send card to Microsoft Teams."""
        webhook_url = getenv("WORKFLOW_TEAMS")
        if not webhook_url:
            logger.error("Missing WORKFLOW_TEAMS environment variable.")
            error_msg = "Missing WORKFLOW_TEAMS environment variable."
            raise_error(exception_type=OSError, message=error_msg)
        return send_to_teams(card=populated_card, webhook_url=webhook_url)

    def lambda_handler(self, event, context) -> dict:
        """Perform the whole workflow."""
        try:
            self.get_message_content(event=event)
            populated_card = self.get_populated_card()
            webhook_resp = self.send_card_to_teams(populated_card=populated_card)

            return {"statusCode": webhook_resp.status, "body": webhook_resp.data.decode("utf-8")}

        except Exception as e:
            return {"statusCode": 500, "body": f"Error: {e!s}"}

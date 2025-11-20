"""Base handler for all lambda functions."""

import json
from abc import ABC, abstractmethod
from os import getenv

from src.utils.error_handling import raise_error
from src.utils.http_utils import send_to_teams
from src.utils.logging_config import setup_logger
from src.utils.template_utils import fetch_card_template, populate_card_template

logger = setup_logger()


class BaseHandler(ABC):
    """Base handler class for all lambdas."""

    def __init__(self, bucket_name: str, template_key: str | None):
        """
        Initialise the class.

        Parameters
        ----------
        bucket_name : str
            S3 bucket containing templates.
        template_key : str, optional
            Default template key. Can be None if handler overrides get_card_template.

        """
        self.bucket_name = bucket_name
        self.template_key = template_key

    @staticmethod
    def get_message_content(event: dict) -> dict:
        """Get sns content from event."""
        return json.loads(event["Records"][0]["Sns"]["Message"])

    def get_card_template(self, sns_msg: dict | None = None) -> dict:
        """Get the template card as dictionary."""
        if not self.template_key:
            raise NotImplementedError("template_key not set and get_card_template not overridden")
        return fetch_card_template(bucket_name=self.bucket_name, template_key=self.template_key)

    @abstractmethod
    def fill_placeholders(self, sns_msg: dict) -> dict:
        """Fill the placeholders."""

    def get_populated_card(self, sns_msg: dict) -> dict:
        """Return the card filled with placeholders."""
        return populate_card_template(
            template=self.get_card_template(sns_msg), placeholders=self.fill_placeholders(sns_msg)
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
            sns_msg = self.get_message_content(event=event)
            populated_card = self.get_populated_card(sns_msg=sns_msg)
            webhook_resp = self.send_card_to_teams(populated_card=populated_card)

            return {"statusCode": webhook_resp.status, "body": webhook_resp.data.decode("utf-8")}

        except Exception as e:
            return {"statusCode": 500, "body": f"Error: {e!s}"}

from datetime import UTC, datetime
from os import getenv

from src.handlers.base_handler import BaseHandler
from src.utils.error_handling import raise_error
from src.utils.logging_config import setup_logger
from src.utils.template_utils import fetch_card_template

TEMPLATE_PATHS = {
    "SUCCEEDED": "notifications/teams/cicd/success-card.json",
    "FAILED": "notifications/teams/cicd/failure-card.json",
    "STARTED": "notifications/teams/cicd/manual-approval-card.json",
}

logger = setup_logger()


class CiCdNotificationHandler(BaseHandler):
    """CICD notification handler class."""

    def __init__(self):
        """Initialise"""
        super().__init__(bucket_name=getenv("BUCKET_NAME"), template_key=None)

    def get_card_template(self, sns_msg: dict | None = None) -> dict:
        """Get the template card based on pipeline state."""
        if not sns_msg:
            raise ValueError("sns_msg required for CI/CD handler")

        state = sns_msg["detail"]["state"]
        template_key = TEMPLATE_PATHS.get(state)
        if template_key is None:
            error_msg = f"Unsupported pipeline state: {state}"
            raise_error(exception_type=ValueError, message=error_msg)
        return fetch_card_template(bucket_name=self.bucket_name, template_key=template_key)

    def fill_placeholders(self, sns_msg: dict) -> dict:
        """Fill placeholders for the cicd notification."""
        state = sns_msg["detail"]["state"]

        placeholders = {
            "pipeline_name": sns_msg["detail"]["pipeline"],
            "execution_id": sns_msg["detail"]["execution-id"],
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S %Z"),
            "pipeline_url": f"https://eu-central-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/{sns_msg['detail']['pipeline']}/view?region=eu-central-1",
            "execution_url": f"https://eu-central-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/{sns_msg['detail']['pipeline']}/executions/{sns_msg['detail']['execution-id']}/timeline?region=eu-central-1",
        }

        # Add failed stage if state is FAILED
        if state == "FAILED":
            placeholders["failed_stage"] = sns_msg["detail"].get("stage", "Unknown")
        return placeholders

"""CICD notification handler."""

from datetime import UTC, datetime
from os import getenv

from src.aws_console_url_builders.codepipeline import CodePipelineURLBuilder
from src.handlers.base_handler import BaseHandler
from src.utils.error_handling import raise_error
from src.utils.template_utils import fetch_card_template

TEMPLATE_PATHS = {
    "SUCCEEDED": "notifications/teams/cicd/success-card.json",
    "FAILED": "notifications/teams/cicd/failure-card.json",
    "STARTED": "notifications/teams/cicd/manual-approval-card.json",
}


class CiCdNotificationHandler(BaseHandler):
    """CICD notification handler class."""

    def __init__(self):
        """Initialise"""
        super().__init__(bucket_name=getenv("BUCKET_NAME"), template_key=None)

    def get_card_template(self, sns_msg: dict | None = None) -> dict:
        """Get the template card based on pipeline state."""
        if not sns_msg:
            error_msg = "sns_msg required for CI/CD handler"
            raise_error(exception_type=ValueError, message=error_msg)

        state = sns_msg["detail"]["state"]
        template_key = TEMPLATE_PATHS.get(state)
        if template_key is None:
            error_msg = f"Unsupported pipeline state: {state}"
            raise_error(exception_type=ValueError, message=error_msg)
        return fetch_card_template(bucket_name=self.bucket_name, template_key=template_key)

    def fill_placeholders(self, sns_msg: dict) -> dict:
        """Fill placeholders for the cicd notification."""
        state = sns_msg["detail"]["state"]
        region = sns_msg["region"]

        placeholders = {
            "pipeline_name": sns_msg["detail"]["pipeline"],
            "execution_id": sns_msg["detail"]["execution-id"],
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S %Z"),
            "pipeline_url": CodePipelineURLBuilder.codepipeline_url(
                region=region, pipeline_name=sns_msg["detail"]["pipeline"]
            ),
            "execution_url": CodePipelineURLBuilder.codepipeline_execution_url(
                region=region,
                pipeline_name=sns_msg["detail"]["pipeline"],
                execution_id=sns_msg["detail"]["execution-id"],
            ),
        }

        # Add failed stage if state is FAILED
        if state == "FAILED":
            placeholders["failed_stage"] = sns_msg["detail"].get("stage", "Unknown")
        return placeholders

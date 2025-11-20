"""Notification handler for step functions."""

from datetime import UTC, datetime
from os import getenv

from src.aws_console_url_builders.step_function import StepFunctionURLBuilder
from src.handlers.base_handler import BaseHandler
from src.utils.error_handling import raise_error
from src.utils.template_utils import fetch_card_template

TEMPLATE_PATHS = {
    "SUCCESS": "notifications/teams/step-function/success-card.json",
    "FAILURE": "notifications/teams/step-function/failure-card.json",
}


class StepFunctionNotificationHandler(BaseHandler):
    """A class for step function notification handler."""

    def __init(self):
        """Initialise the class."""
        super().__init__(bucket_name=getenv("BUCKET_NAME"), template_key=None)

    @staticmethod
    def get_region_and_account_id(sns_msg: dict):
        """Get the region and account ID from the SNS message."""
        region = sns_msg["region"] or getenv("AWS_REGION")
        account_id = sns_msg["account_id"] or getenv("AWS_ACCOUNT_ID")
        return region, account_id

    def get_card_template(self, sns_msg: dict | None = None) -> dict:
        """Get the template card based on the lambda status."""
        if not sns_msg:
            error_msg = "sns_msg required for Step Function handler"
            raise_error(exception_type=ValueError, message=error_msg)

        status = sns_msg["status"]
        template_key = TEMPLATE_PATHS.get(status)
        if not template_key:
            error_msg = f"Unsupported workflow status: {status}"
            raise_error(exception_type=ValueError, message=error_msg)
        return fetch_card_template(self.bucket_name, template_key)

    def fill_placeholders(self, sns_msg: dict) -> dict:
        """Fill placeholders for the step function notification."""
        region, account_id = self.get_region_and_account_id(sns_msg)
        return {
            "status": sns_msg["status"],
            "workflow_name": sns_msg["workflow_name"],
            "execution_id": sns_msg["execution_id"].split(":")[-1],
            "details": sns_msg["details"],
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S %Z"),
            "workflow_url": StepFunctionURLBuilder.step_functions_url(
                region=region, account_id=account_id, step_function_name=sns_msg["workflow_name"]
            ),
            "execution_url": StepFunctionURLBuilder.step_functions_execution_url(
                region=region,
                account_id=account_id,
                step_function_name=sns_msg["workflow_name"],
                execution_id=sns_msg["execution_id"],
            ),
        }

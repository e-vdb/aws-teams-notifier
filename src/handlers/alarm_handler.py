"""Alarm Notification Handler."""

from datetime import UTC, datetime
from os import getenv

from src.aws_console_url_builders.cloudwatch import CloudWatchURLBuilder
from src.handlers.base_handler import BaseHandler
from src.utils.arn_utils import get_region_from_arn


class AlarmNotificationHandler(BaseHandler):
    """Alarm Notification Handler."""

    def __init__(self):
        """Initialise the class."""
        super().__init__(
            bucket_name=getenv("BUCKET_NAME"),
            template_key="notifications/teams/alarms/alarm-triggered-card.json",
        )

    def fill_placeholders(self, sns_msg: dict) -> dict:
        """Fill placeholders for the alarm notification."""
        region = get_region_from_arn(sns_msg["AlarmArn"])

        return {
            "alarm_name": sns_msg["AlarmName"],
            "alarm_description": sns_msg["AlarmDescription"],
            "alarm_state": sns_msg["NewStateValue"],
            "alarm_state_reason": sns_msg["NewStateReason"],
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S %Z"),
            "alarm_url": CloudWatchURLBuilder.alarm_url(
                region=region, alarm_name=sns_msg["AlarmName"], account_id=sns_msg["AWSAccountId"]
            ),
        }

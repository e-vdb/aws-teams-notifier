"""Alarm Notification Handler."""

from datetime import UTC, datetime
from os import getenv

from src.handlers.base_handler import BaseHandler
from src.utils.error_handling import raise_error


def get_region_from_arn(arn: str) -> str:
    """Extract the AWS region from an ARN.

    Parameters
    ----------
    arn: str
        The ARN of the resource.

    Returns
    -------
    str
        The region extracted from the ARN.

    Raises
    ------
    ValueError
        If the ARN format is invalid.

    """
    try:
        return arn.split(":")[3]
    except IndexError:
        error_msg = f"Invalid ARN format: {arn}"
        raise_error(exception_type=ValueError, message=error_msg)


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
            "alarm_url": f"https://{region}.console.aws.amazon.com/cloudwatch/home?region={region}#alarmsV2:alarm/{sns_msg['AlarmName']}?accountId={sns_msg['AWSAccountId']}&region={region}",
        }

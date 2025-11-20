"""Builder for AWS CloudWatch Console URLs."""

from urllib.parse import quote

from src.aws_console_url_builders.base import AWSConsoleURLBuilder


class CloudWatchURLBuilder(AWSConsoleURLBuilder):
    """Builder for AWS CloudWatch Console URLs."""

    @classmethod
    def logs_url(cls, region: str, log_group: str) -> str:
        """Build CloudWatch Logs URL.

        Parameters
        ----------
        region : str
            AWS region
        log_group : str
            Log group name (will be URL-encoded)
        """
        # Double encode for CloudWatch Logs V2
        encoded_log_group = quote(quote(log_group, safe=""))

        return cls.build_url(
            service="cloudwatch",
            region=region,
            path=f"/home#logsV2:log-groups/log-group/{encoded_log_group}",
        )

    @classmethod
    def alarm_url(cls, region: str, alarm_name: str, account_id: str) -> str:
        """Build CloudWatch alarm URL."""
        return cls.build_url(
            service="cloudwatch",
            region=region,
            path=f"/home#alarmsV2:alarm/{alarm_name}",
            query_params={"region": region, "accountId": account_id},
        )

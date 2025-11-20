"""Builder for AWS Lambda Console URLs."""

from src.aws_console_url_builders.base import AWSConsoleURLBuilder


class LambdaURLBuilder(AWSConsoleURLBuilder):
    """Builder for AWS Lambda Console URLs."""

    @classmethod
    def lambda_function_url(cls, region: str, function_name: str, tab: str = "monitoring") -> str:
        """Build Lambda function URL."""
        return cls.build_url(
            service="lambda",
            region=region,
            path=f"/home#/functions/{function_name}",
            query_params={"region": region, "tab": tab},
        )

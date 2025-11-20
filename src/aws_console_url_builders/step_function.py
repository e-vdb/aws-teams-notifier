"""Builder for AWS Step Function Console URLs."""

from urllib.parse import quote

from src.aws_console_url_builders.base import AWSConsoleURLBuilder


class StepFunctionURLBuilder(AWSConsoleURLBuilder):
    """Builder for AWS Step Function Console URLs."""

    @classmethod
    def step_functions_execution_url(cls, region: str, execution_arn: str) -> str:
        """Build Step Functions execution URL.

        Parameters
        ----------
        region : str
            AWS region
        execution_arn : str
            Execution ARN (will be URL-encoded)
        """
        encoded_arn = quote(execution_arn, safe="")

        return cls.build_url(
            service="states", region=region, path=f"/home#/v2/executions/details/{encoded_arn}"
        )

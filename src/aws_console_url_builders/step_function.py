"""Builder for AWS Step Function Console URLs."""

from urllib.parse import quote

from src.aws_console_url_builders.base import AWSConsoleURLBuilder


class StepFunctionURLBuilder(AWSConsoleURLBuilder):
    """Builder for AWS Step Function Console URLs."""

    @classmethod
    def step_functions_url(cls, region: str, step_function_name: str, account_id: str) -> str:
        """Build Step Functions URL.

        Parameters
        ----------
        region : str
            AWS region
        step_function_name : str
            Name of the step function
        account_id: str
            AWS Account ID
        """
        arn = f"arn:aws:states:{region}:{account_id}:stateMachine:{step_function_name}"
        encoded_arn = quote(arn, safe="")

        return cls.build_url(
            service="states",
            region=region,
            path=f"/home#/statemachines/view/{encoded_arn}",
            query_params={"type": "standard"},
        )

    @classmethod
    def step_functions_execution_url(
        cls, region: str, step_function_name: str, account_id: str, execution_id: str
    ) -> str:
        """Build Step Functions execution URL.

        Parameters
        ----------
        region : str
            AWS region
        step_function_name : str
            Name of the step function
        account_id: str
            AWS Account ID
        execution_id : str
            Execution ID
        """
        execution_arn = (
            f"arn:aws:states:{region}:{account_id}:execution:{step_function_name}:{execution_id}"
        )
        encoded_arn = quote(execution_arn, safe="")

        return cls.build_url(
            service="states", region=region, path=f"/home#/v2/executions/details/{encoded_arn}"
        )

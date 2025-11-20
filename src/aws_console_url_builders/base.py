"""Utilities for building AWS Console URLs."""

from urllib.parse import urlencode


class AWSConsoleURLBuilder:
    """Base builder for AWS Console URLs."""

    BASE_CONSOLE = "console.aws.amazon.com"

    @classmethod
    def build_url(
        cls, service: str, region: str, path: str, query_params: dict | None = None
    ) -> str:
        """Build an AWS Console URL.

        Parameters
        ----------
        service : str
            AWS service name (e.g., 'cloudwatch', 'lambda', 'codesuite')
        region : str
            AWS region (e.g., 'eu-central-1', 'us-east-1')
        path : str
            Path portion of the URL (e.g., '/home', '/functions/my-function')
        query_params : dict, optional
            Additional query parameters

        Returns
        -------
        str
            Complete AWS Console URL
        """
        # Ensure region is in query params
        if query_params is None:
            query_params = {}
        query_params.setdefault("region", region)

        # Build URL
        query_string = urlencode(query_params)
        return f"https://{region}.{cls.BASE_CONSOLE}/{service}{path}?{query_string}"

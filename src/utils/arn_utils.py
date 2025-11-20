"""Utility function to retrieve region name from aws arn resource."""

from src.utils.error_handling import raise_error
from src.utils.logging_config import setup_logger

# Set up logger from the utilities module
logger = setup_logger()


def get_region_from_arn(arn: str, default_region: str = "eu-central-1") -> str:
    """Extract the AWS region from an ARN.

    Parameters
    ----------
    arn : str
        The ARN of the resource.
    default_region : str, optional
        Default region to return for global services. Default is "us-east-1".

    Returns
    -------
    str
        The region extracted from the ARN, or default_region for global services.

    Raises
    ------
    ValueError
        If the ARN format is invalid.
    """
    try:
        parts = arn.split(":")
        if len(parts) < 6:
            raise ValueError(f"Invalid ARN format: {arn}")

        region = parts[3]

        # Global services have empty region field
        if not region:
            logger.debug(
                "ARN %s is for a global service, using default region %s", arn, default_region
            )
            return default_region

        return region

    except (IndexError, AttributeError):
        error_msg = f"Invalid ARN format: {arn}"
        raise_error(exception_type=ValueError, message=error_msg)

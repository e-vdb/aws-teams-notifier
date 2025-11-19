"""Helper functions for working with S3."""

import json

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from .error_handling import raise_error

s3 = boto3.client("s3")


def fetch_s3_object(bucket: str, key: str) -> dict:
    """Fetch and parse a JSON object from S3.

    Parameters
    ----------
    bucket: str
        Name of the S3 bucket.
    key: str
        Key of the object in the bucket.

    Returns
    -------
    dict:
        Parsed JSON content of the S3 object.

    Raises
    ------
        RuntimeError: If fetching the object fails.

    """
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return json.loads(response["Body"].read())
    except (BotoCoreError, ClientError) as e:
        error_msg = f"Failed to fetch object from S3: {e}"
        raise_error(exception_type=RuntimeError, message=error_msg)

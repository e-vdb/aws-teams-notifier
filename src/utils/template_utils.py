"""Utility functions for working with card templates."""

import json

from .s3_helpers import fetch_s3_object


def populate_card_template(template: dict, placeholders: dict) -> dict:
    """Replace placeholders in the template with actual values.

    Parameters
    ----------
    template : dict
        The card template as a dictionary.
    placeholders : dict
        A dictionary of placeholders and their corresponding values.

    Returns
    -------
    dict
        The populated card template as a dictionary.

    """
    template_str = json.dumps(template)
    for key, value in placeholders.items():
        placeholder = f"{{{{{key}}}}}"

        # Convert to string and escape for JSON insertion
        if isinstance(value, str):
            escaped_value = (
                value.replace("\\", "\\\\")  # escape backslashes
                .replace('"', '\\"')  # escape double quotes
                .replace("\n", "\\n")  # escape newlines
            )
        else:
            escaped_value = str(value)

        template_str = template_str.replace(placeholder, escaped_value)
    return json.loads(template_str)


def fetch_card_template(bucket_name: str, template_key: str) -> dict:
    """Fetch the card template from S3.

    Parameters
    ----------
    bucket_name : str
        The name of the S3 bucket containing the card template.
    template_key : str
        The key of the card template in the S3 bucket.

    Returns
    -------
    dict
        The card template as a dictionary.

    """
    return fetch_s3_object(bucket=bucket_name, key=template_key)

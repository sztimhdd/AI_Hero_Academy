import os


def get_user_email() -> str:
    """
    Returns the authenticated user's email address.
    In Databricks Apps, injected as DATABRICKS_USER_EMAIL env var.
    Falls back to DEV_USER_EMAIL for local development.
    """
    email = os.environ.get("DATABRICKS_USER_EMAIL")
    if not email:
        email = os.environ.get("DEV_USER_EMAIL", "dev@example.com")
    return email

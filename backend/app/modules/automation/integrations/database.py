from app.modules.automation.integrations import ConnectorNotConfiguredError


def require_registered_database_alias(alias: str, registered_aliases: set[str]) -> str:
    if alias not in registered_aliases:
        raise ValueError("Database actions must reference a registered tenant connector.")
    raise ConnectorNotConfiguredError(
        "Database execution adapter is not configured; no connection string was accepted."
    )

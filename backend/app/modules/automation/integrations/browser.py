from urllib.parse import urlsplit

from app.modules.automation.integrations.api import IntegrationTargetError


def validate_browser_target(url: str, approved_hosts: list[str]) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise IntegrationTargetError("Browser integrations require an HTTPS target.")
    hostname = parsed.hostname.rstrip(".").lower()
    if hostname not in {host.rstrip(".").lower() for host in approved_hosts}:
        raise IntegrationTargetError("Browser target is not in the integration's approved host list.")
    return hostname

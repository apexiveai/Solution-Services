from urllib.parse import urlsplit


class IntegrationTargetError(ValueError):
    pass


def validate_api_target(url: str, approved_hosts: list[str]) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise IntegrationTargetError("API integrations require an HTTPS URL without embedded credentials.")
    hostname = parsed.hostname.rstrip(".").lower()
    if hostname not in {host.rstrip(".").lower() for host in approved_hosts}:
        raise IntegrationTargetError("API target is not in the integration's approved host list.")
    return hostname

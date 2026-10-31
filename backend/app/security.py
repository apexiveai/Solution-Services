from functools import lru_cache
from typing import Any
import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from app.config import settings

bearer_scheme = HTTPBearer(auto_error=False)


class CurrentPrincipal(BaseModel):
    subject: str
    username: str | None = None
    email: str | None = None
    tenant_id: str
    roles: list[str] = []
    claims: dict[str, Any] = {}


@lru_cache
def get_jwks_client() -> PyJWKClient:
    return PyJWKClient(settings.oidc_jwks_url, cache_keys=True)


def _extract_roles(claims: dict[str, Any]) -> list[str]:
    roles: set[str] = set()
    realm_access = claims.get("realm_access") or {}
    roles.update(realm_access.get("roles") or [])
    resource_access = claims.get("resource_access") or {}
    for client in resource_access.values():
        roles.update((client or {}).get("roles") or [])
    roles.update(claims.get("roles") or [])
    return sorted(roles)


def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentPrincipal:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer access token required")

    token = credentials.credentials
    try:
        signing_key = get_jwks_client().get_signing_key_from_jwt(token).key
        claims = jwt.decode(
            token,
            signing_key,
            algorithms=settings.allowed_algorithms,
            issuer=settings.oidc_issuer,
            audience=settings.oidc_audience,
            options={"require": ["exp", "iat", "iss", "sub"]},
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token")

    tenant_id = claims.get("tenant_id") or claims.get("tenantId")
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is missing tenant_id claim")

    return CurrentPrincipal(
        subject=claims["sub"],
        username=claims.get("preferred_username"),
        email=claims.get("email"),
        tenant_id=str(tenant_id),
        roles=_extract_roles(claims),
        claims=claims,
    )


def require_roles(*allowed_roles: str):
    def dependency(principal: CurrentPrincipal = Depends(get_current_principal)) -> CurrentPrincipal:
        if not set(principal.roles).intersection(allowed_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role permissions")
        return principal
    return dependency

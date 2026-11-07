
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --------------------------------------------------
    # APPLICATION
    # --------------------------------------------------
    app_name: str = "ApexiveAI Enterprise Operations Platform"
    app_env: str = "development"
    app_debug: bool = True
    app_version: str = "0.1.0"

    # --------------------------------------------------
    # DATABASE
    # --------------------------------------------------
    database_url: str = Field(
        default="postgresql+psycopg://aeop:aeop_password@127.0.0.1:5433/aeop"
    )

    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Development only. Production should use Alembic.
    dev_create_tables: bool = True

    # --------------------------------------------------
    # KEYCLOAK / JWT
    # --------------------------------------------------
    aeop_jwks_url: str = ""
    aeop_jwt_issuer: str = ""
    aeop_jwt_audience: str = ""

    jwt_algorithms: list[str] = ["RS256"]

    # --------------------------------------------------
    # CORS
    # --------------------------------------------------
    cors_origins: str = (
        "http://localhost:3000,"
        "http://127.0.0.1:3000"
    )

    # --------------------------------------------------
    # TELECOM PLATFORM
    # --------------------------------------------------
    telecom_enabled: bool = True

    telecom_mno_enabled: bool = True
    telecom_isp_enabled: bool = True
    telecom_infrastructure_enabled: bool = True

    # Hybrid deployment foundation
    telecom_deployment_mode: str = "hybrid"

    # Monitoring integration capabilities
    telecom_snmp_enabled: bool = True
    telecom_snmp_traps_enabled: bool = True
    telecom_syslog_enabled: bool = True
    telecom_rest_api_enabled: bool = True
    telecom_netconf_enabled: bool = True
    telecom_restconf_enabled: bool = True
    telecom_streaming_telemetry_enabled: bool = True

    # --------------------------------------------------
    # NETWORK MONITORING
    # --------------------------------------------------
    telemetry_retention_days: int = 90
    alarm_auto_resolution: bool = False

    # --------------------------------------------------
    # SECURITY
    # --------------------------------------------------
    secret_key: str = "CHANGE_THIS_DEVELOPMENT_SECRET"
    access_token_expire_minutes: int = 30
    automation_credential_key: str = Field(
        default="",
        validation_alias="AEOP_AUTOMATION_CREDENTIAL_KEY",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

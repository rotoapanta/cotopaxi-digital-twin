# backend/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    influx_url: str = "http://influxdb:8086"
    influx_user: str = "admin"
    influx_pass: str = "admin123"
    influx_org:  str = "cotopaxi"
    influx_bucket: str = "sensors"
    influx_token: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()

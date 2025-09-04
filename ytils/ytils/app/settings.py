import os

from typing import Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # app configuration
    project_name: str = Field(..., env="PROJECT_NAME")
    api_host: str = Field(..., env="API_HOST")
    api_port: str = Field(..., env="API_PORT")
    api_url: Optional[str] = None
    logging_level: str = Field(..., env="LOGGING_LEVEL")
    static_files: Optional[str] = None

    # mongo configuration
    mongo_user: str = Field(..., env="MONGO_USER")
    mongo_password: str = Field(..., env="MONGO_PASSWORD")
    mongo_port: str = Field(..., env="MONGO_PORT")
    mongo_host: str = Field(..., env="MONGO_HOST")
    mongo_url: Optional[str] = None
    default_db: str = Field(..., env="DEFAULT_DB")
    default_collection: str = Field(..., env="DEFAULT_COLLECTION")

    # MinIO configuration
    minio_server_url: str = Field(..., env="MINIO_SERVER_URL")  # AKA endpoint
    minio_access_key: str = Field(..., env="MINIO_ACCESS_KEY")  # AKA username
    minio_secret_key: str = Field(..., env="MINIO_SECRET_KEY")  # AKA password
    minio_secure: bool = Field(..., env="MINIO_SECURE")  # use HTTPS
    minio_video_bucket: str = Field(..., env="MINIO_VIDEO_BUCKET")

    # Download configuration
    thumbnail_preferred_resolution: str = Field(..., env="THUMBNAIL_PREFERRED_RESOLUTION")
    thumbnail_backup_resolution: str = Field(..., env="THUMBNAIL_BACKUP_RESOLUTION")
    download_dir: str = Field(..., env="DOWNLOAD_DIR")
    download_opts: dict = None

    # Conversion configuration
    conversion_output_format: str = Field(..., env="CONVERSION_OUTPUT_FORMAT")

    @model_validator(mode="before")
    def set_other_props(cls, values):
        values["static_files"] = os.path.join(os.path.dirname(__file__), 'static')

        api_host = values.get("api_host")
        api_port = values.get("api_port")
        api_url = f"http://{api_host}:{api_port}"
        values["api_url"] = api_url

        mongo_user = values.get("mongo_user")
        mongo_password = values.get("mongo_password")
        mongo_host = values.get("mongo_host")
        mongo_port = values.get("mongo_port")
        default_db = values.get("default_db")
        values["mongo_url"] = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{default_db}?retryWrites=true&w=majority"

        if not os.path.exists(values["download_dir"]):
            print(f"Making directory: {values['download_dir']}")
            os.makedirs(values["download_dir"])

        download_opts = {
            "format": "bestaudio/best",
            "ffmpeg_location": "/usr/bin/ffmpeg",
            "outtmpl": "/app/downloads/%(id)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": values.get("conversion_output_format"),
                    "preferredquality": "192",
                }
            ],
        }

        values["download_opts"] = download_opts

        return values

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

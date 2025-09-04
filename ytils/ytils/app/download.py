import json
import os

from yt_dlp import YoutubeDL
from typing import List
from json import JSONEncoder

from app.settings import settings
from app.logger import logger


class DownloadObject:
    """
    Class is designed to hold the data for download objects.
    """
    # Data gotten from youtube
    id: str
    title: str
    description: str
    tags: List[str]
    chapters: List[str]
    thumbnail_url: str
    thumbnail_path: str

    # Server/FS specific items
    abs_path: str

    def __init__(self, info_dict: dict):
        self.id = info_dict.get("id", None)
        self.title = info_dict.get("title", None)
        self.description = info_dict.get("description", None)
        self.tags = info_dict.get("tags", None)
        self.chapters = info_dict.get("chapters", None)
        self.abs_path = f"{os.path.join(settings.download_dir, self.id)}.{settings.conversion_output_format}"

        # Thumbnail url logic
        thumbnails = info_dict.get("thumbnails")

        thumbnail_url = next(t.get("url") for t in thumbnails if t.get("resolution") == settings.thumbnail_preferred_resolution)
        if not thumbnail_url:
            thumbnail_url = next(t.get("url") for t in thumbnails if t.get("resolution") == settings.thumbnail_backup_resolution)

        # TODO: download and store
        thumbnail_url = info_dict.get("thumbnail")
        self.thumbnail_url = os.path.join(thumbnail_url)

    def __str__(self):
        return f"id:{self.id}, title:{self.title}, path:{self.abs_path}"


class DownloadManager:
    """
    Class is designed to handle the logic of downloads. Primarily a wrapper for download manifest management.
    """
    download_opts: dict

    def __init__(self) -> None:
        self.download_opts = settings.download_opts

    def download_file(self, video_id: str) -> DownloadObject:
        url = f"http://youtu.be/{video_id}"
        logger.debug(f"Downloading {video_id=}, opts: {self.download_opts}")

        try:
            with YoutubeDL(self.download_opts) as ydl:
                ydl.cache.remove()
                info_dict = ydl.extract_info(url, download=True)
                logger.info(info_dict)
                ydl.download([url])
                download_object = DownloadObject(info_dict)
                write_metadata_file(download_object)
                return download_object
        except Exception as e:
            logger.warning(e)
            return e


class DownloadObjectEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def write_metadata_file(download_object: DownloadObject) -> None:
    write_path = f"{download_object.abs_path}.json"
    logger.debug(f"writing {write_path}")

    with open(write_path, "w", encoding="UTF-8") as fobj:
        download_as_json = json.dumps(download_object, indent=2, cls=DownloadObjectEncoder)
        fobj.writelines(download_as_json)

    logger.debug(f"Wrote metadata file for {write_path}")

from fastapi import APIRouter, Request, HTTPException, Path, Form
from typing import Optional
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse, Response

from app.depends import templates
from app.logger import logger
import app.utils as utils

import io
from minio.error import S3Error
from app.crud import video
from app.download import DownloadManager

PREFIX = "/videos"


router = APIRouter(prefix=PREFIX)

download_manager = DownloadManager()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):

    videos = await video.find()
    context = {
        "request": request,
        "videos": videos
    }

    return templates.TemplateResponse("videos.html.j2", context=context)


@router.post('/download')
async def download_video(v: Optional[str] = Form(None)):
    logger.debug(f"Received youtube video download string of {v=}")
    
    video_id = utils.extract_video_id(v)

    video_obj = await video.find_one(**{"video_id": video_id})
    if video_obj:
        return RedirectResponse("/videos/")
    
    download = download_manager.download_file(video_id)

    video_dict = {"video_id": video_id}
    video_obj = await video.create(**video_dict)

    video_obj.store_in_minio(download.abs_path)
    return {"msg": "Success"}


@router.get("/download_from_minio/{id}")
async def download_video(id: str):
    video_obj = await video.get(id)
    object_name = video_obj.title if video_obj.title else video_obj.video_id
    object_name += ".wav"

    try:
        # Get object from MinIO (returns a response-like object)
        response = video_obj.get_from_minio()

        file_content = response.read()
        return Response(
            content=file_content,
            media_type="audio/wav",
            headers={
                "Content-Disposition": f'attachment; filename="{object_name}"'
            }
        )
    except S3Error as e:
        raise HTTPException(status_code=404, detail=f"Video not found: {e}")


@router.post("/update/{id}")
async def update_video(
    id: str = Path(...),
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    tags: str = Form(...)
):
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    video_obj = await video.get(id)
    kwargs = {
        "title": title,
        "artist": artist,
        "album": album,
        "tags": tag_list
    }
    await video_obj.update(**kwargs)

    return RedirectResponse(f"/videos/", status_code=303)


@router.get('/purge')
async def purge_videos():
    """
    TODO: Delete this, only here for easy testing
    """
    await video.purge_db_objects()

    return RedirectResponse("/videos/")


@router.get("/{id}", response_class=HTMLResponse)
async def get_model(request: Request, id: str):

    vid = await video.find_one(**{"video_id": id})
    context = {
        "request": request,
        "video": vid
    }

    return templates.TemplateResponse("video.html.j2", context=context)

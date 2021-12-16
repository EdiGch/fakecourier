from fastapi import APIRouter

from app.conf import settings

router = APIRouter()


@router.get("", tags=["version"])
def version():
    return settings.VERSION

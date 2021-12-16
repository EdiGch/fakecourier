import logging
import uuid
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from app.deps import get_db
from app.fake_courier.models.sample import SampleModel
from app.fake_courier.schemas.sample import SampleModelSchema

router = APIRouter(dependencies=[])
logger = logging.getLogger(__name__)

samples_v1_templates = Jinja2Templates(directory="app/templates/samples")


@router.get(
    "/{sample_id}",
    status_code=HTTPStatus.OK,
    response_model=SampleModelSchema,
)
async def sample_get(
    *,
    db=Depends(get_db),
    sample_id: uuid.UUID,
):
    sample = await SampleModel.get_by_id(db=db, entity_id=sample_id)
    return sample


@router.put(
    "/{sample_id}",
    status_code=HTTPStatus.OK,
    response_model=SampleModelSchema,
)
async def sample_put(
    *,
    db=Depends(get_db),
    sample_id: uuid.UUID,
    payload: SampleModelSchema,
):
    sample = await SampleModel.update(
        sample_id=sample_id,
        db=db,
        entity=payload.dict(exclude_unset=True),
    )

    return sample


@router.delete(
    "/{sample_id}",
    status_code=HTTPStatus.OK,
)
async def sample_delete(
    *,
    db=Depends(get_db),
    sample_id: uuid.UUID,
):
    await SampleModel.delete(db=db, entity_id=sample_id)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)


@router.post(
    "",
    status_code=HTTPStatus.OK,
    response_model=SampleModelSchema,
)
async def samples_post(
    *,
    db=Depends(get_db),
    payload: SampleModelSchema,
):
    sample = await SampleModel.add(
        db=db,
        entity=payload.dict(exclude_unset=True),
    )

    return sample


@router.get(
    "",
    status_code=HTTPStatus.OK,
    response_model=List[SampleModelSchema],
)
async def samples_get(
    *,
    db=Depends(get_db),
):
    samples = await SampleModel.get_all(db=db)
    return samples

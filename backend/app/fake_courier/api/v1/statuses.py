import logging
from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.fake_courier.statuses.courierStatuses import CourierStatuses

router = APIRouter(dependencies=[])
logger = logging.getLogger(__name__)

statuses_v1_templates = Jinja2Templates(directory="app/templates/statuses")


@router.get(
    "",
    status_code=HTTPStatus.OK
)
async def statuses_get():
    courier_statuses = CourierStatuses()
    statuses = courier_statuses.get_all_statuses_list()
    return statuses


@router.get(
    "/{status_id}",
    status_code=HTTPStatus.OK
)
async def status_get(
    *,
    status_id: int,
):
    courier_statuses = CourierStatuses()
    status = courier_statuses.get_by_value_from_dict(status_id)
    if bool(status):
        return status

    return JSONResponse(
        status_code=404,
        content={"message": f"Not found status"},
    )

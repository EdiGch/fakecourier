import logging
from fastapi import APIRouter
from http import HTTPStatus
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .fake_courier.api import version
from .fake_courier.api.v1.sample import router as sample_router
from .fake_courier.api.v1.shipment import router as shipment_router
from .fake_courier.api.v1.statuses import router as statuses_router

from .patches import fastapi_patched_setup
from .utils.cache import Cache

FastAPI.setup = fastapi_patched_setup

logger = logging.getLogger(__name__)


def setup_routing(router: APIRouter):
    router.include_router(version.router, prefix="/version", tags=["version"])
    router.include_router(sample_router, prefix="/v1/samples", tags=["samples"])
    router.include_router(shipment_router, prefix="/v1/shipments", tags=["shipments"])
    router.include_router(statuses_router, prefix="/v1/statuses", tags=["statuses"])


def setup_exceptions(app: FastAPI) -> FastAPI:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST, content={"detail": jsonable_encoder(exc.errors())}
        )

    @app.exception_handler(Exception)
    async def unhandled_exceptions_handler(request: Request, exc: Exception):
        logger.exception(exc)
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"error": str(exc)})

    return app


def create_app() -> FastAPI:
    api_router = APIRouter()
    setup_routing(api_router)

    app = FastAPI(
        title="Fake Courier",
        description="This is a very provocative and fancy app which makes fake courier even better :)",
        version="1.0.0",
        docs_url="/swagger",
        root_path="/",
    )
    app.include_router(api_router)
    app = setup_exceptions(app)

    @app.on_event("startup")
    def startup():
        app.state.short_cache = Cache(ttl=60 * 60)
        app.state.long_cache = Cache(ttl=5 * 60 * 60)

    @app.on_event("shutdown")
    def shutdown():
        logger.info("ON SHUTDOWN")

    return app

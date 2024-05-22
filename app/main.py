import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi_pagination import add_pagination
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from app.admin import AdminAuth, ItemAdmin, UserAdmin
from app.api.main import api_router
from app.core.config import settings
from app.core.db import engine


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
# pagination
add_pagination(app)

# sqladmin configuration
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(ItemAdmin)

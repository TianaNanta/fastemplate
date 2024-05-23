from datetime import timedelta

from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from sqlmodel import Session

from app import crud
from app.api.deps import get_current_user
from app.core import security
from app.core.config import settings
from app.core.db import engine


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        with Session(engine) as session:
            user = crud.authenticate(
                session=session, email=username, password=password)
            if not user:
                return False
            elif not user.is_active:
                return False
            elif not user.is_superuser:
                return False
            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

            token = security.create_access_token(
                user.id, expires_delta=access_token_expires
            )

            # Validate username/password credentials
            # And update session
            request.session.update({"token": token})

            return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        with Session(engine) as session:
            user = get_current_user(session, token)

            if not user:
                return False
            if not user.is_active:
                return False
            if not user.is_superuser:
                return False

            # Check the token in depth
            return True

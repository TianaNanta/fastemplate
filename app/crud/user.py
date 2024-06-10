from typing import Any

import requests
from fastapi import HTTPException
from fastapi import status
from sqlmodel import select
from sqlmodel import Session

from app.core.security import get_password_hash
from app.core.security import verify_password
from app.models import User
from app.models import UserCreate
from app.models import UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    """

    :param *:
    :param session: Session:
    :param user_create: UserCreate:

    """
    db_obj = User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)})

    validate_email = requests.get(
        f"https://api.mailcheck.ai/email/{db_obj.email}")
    data = validate_email.json()

    if validate_email.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=validate_email.status_code,
            detail=data["error"],
        )
    if data["disposable"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Disposable email is not authorized, use a real one !",
        )

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User,
                user_in: UserUpdate) -> Any:
    """

    :param *:
    :param session: Session:
    :param db_user: User:
    :param user_in: UserUpdate:

    """
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)

    validate_email = requests.get(
        f"https://api.mailcheck.ai/email/{db_user.email}")
    data = validate_email.json()

    if validate_email.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=validate_email.status_code,
            detail=data["error"],
        )
    if data["disposable"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Disposable email is not authorized, use a real one !",
        )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """

    :param *:
    :param session: Session:
    :param email: str:

    """
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str,
                 password: str) -> User | None:
    """

    :param *:
    :param session: Session:
    :param email: str:
    :param password: str:

    """
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

# app\api\endpoints\donation.py
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (CreateDonationBase, DonationBaseDB,
                                  DonationUserDB)
from app.services.investment import charges

router = APIRouter()


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: CreateDonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Содает донат"""
    new_donation = await donation_crud.create(donation, session, user)
    await charges(
        undivided=new_donation,
        crud_class=charity_project_crud,
        session=session
    )
    return new_donation


@router.get(
    '/',
    response_model=List[DonationBaseDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def gef_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.get(
    '/my', response_model=list[DonationUserDB],
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех донатов для текущего пользователя."""
    reservations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return reservations


@router.delete(
    '/{donat_id}',
    tags=('donation'),
    deprecated=True
)
async def del_donat(donat_id: int):
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Удаление донатов запрещено!"
    )


@router.patch(
    '/{donat_id}',
    tags=('donation'),
    deprecated=True
)
def patch_donat(donat_id: str):
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Изменение донатов запрещено!"
    )

# app\api\endpoints\donation.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.schemas.donation import CreateDonationBase, DonationBaseDB
from app.services.investment import charges


router = APIRouter()


@router.post(
    '/',
    response_model=DonationBaseDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: CreateDonationBase,
    session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create(donation, session)
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
)
async def gef_donations(
    session: AsyncSession = Depends(get_async_session)
):
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.delete(
    '/{donat_id}',
    tags=['donation'],
    deprecated=True
)
async def del_donat(donat_id: int):
    raise HTTPException(
        status_code=405,
        detail="Изменение донатов запрещено!"
    )


@router.patch(
    '/{donat_id}',
    tags=['donation'],
    deprecated=True
)
def patch_donat(donat_id: str):
    raise HTTPException(
        status_code=405,
        detail="Изменение донатов запрещено!"
    )

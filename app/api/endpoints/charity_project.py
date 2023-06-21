# app\api\endpoints\charity_project.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_fully_invested,
                                check_invested_amount_is_null,
                                check_name_duplicate, check_project_exists,
                                check_update_fully_invested,
                                check_update_project)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectDB,
                                         CharityProjectUpdate,
                                         CreateCharityProject)
from app.services.investment import charges

router = APIRouter()


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=List[CharityProjectDB]
)
async def get_project(
    session: AsyncSession = Depends(get_async_session),
):
    """GET-запрос на вывод всех проектов"""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
    project: CreateCharityProject,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await charges(
        undivided=new_project,
        crud_class=donation_crud,
        session=session
    )
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )
    await check_update_fully_invested(project_id, session)
    if obj_in.full_amount is not None:
        project = await check_update_project(project_id, obj_in.full_amount, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    await check_invested_amount_is_null(project_id, session)
    await check_fully_invested(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project

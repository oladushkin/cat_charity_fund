# app/api/meeting_room.py
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CreateCharityProject, CharityProjectDB, CharityProjectUpdate
)
from app.api.validators import check_name_duplicate, check_project_exists


router = APIRouter()


@router.get(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
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
)
async def create_new_project(
    project: CreateCharityProject,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = charity_project_crud.create(project, session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(
        project_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def remove_meeting_room(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    if project.invested_amount != 0:
        project.fully_invested = True
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project
    project = await charity_project_crud.remove(project, session)
    return project

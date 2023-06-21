# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_update_project(
        project_id: int,
        full_amount: int,
        session: AsyncSession,
):
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount is not None:
        if project.invested_amount > full_amount:
            raise HTTPException(
                status_code=400,
                detail="""Сумма для закрытия проекта не может
                    быть меньше чем сумма которую внесли в проект"""
            )
        if project.invested_amount == full_amount:
            project.fully_invested = True
    return project


async def check_invested_amount_is_null(
        project_id: int,
        session: AsyncSession
):
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!"
        )


async def check_fully_invested(project_id: int, session: AsyncSession):
    project = await charity_project_crud.get(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалять закрытые проекты"
        )


async def check_update_fully_invested(project_id: int, session: AsyncSession):
    project = await charity_project_crud.get(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="Закрытый проект нельзя редактировать!"
        )
    return project

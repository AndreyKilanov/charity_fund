from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_number_objects,
    check_charity_project_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charityproject import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investment import investment

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для администраторов. \n
    Создает благотворительный проект.
    """
    await check_name_duplicate(charity_project.name, session)
    donations = await donation_crud.get_unfinished(session)
    new_project = await charity_project_crud.create(charity_project, session)
    session.add_all(investment(new_project, donations))
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=List[CharityProjectDB]
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Любой пользователь. \n
    Получает список всех проектов.
    """
    return await check_number_objects(session, charity_project_crud)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для администраторов. \n
    Закрытый проект нельзя редактировать, также нельзя установить требуемую
    сумму меньше уже вложенной.
    """
    project = await check_charity_project_exists(project_id, session, obj_in)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    return await charity_project_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для администраторов. \n
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
    средства, его можно только закрыть.
    """
    project = await check_charity_project_exists(project_id, session)
    return await charity_project_crud.remove(project, session)

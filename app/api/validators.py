from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User, Donation, CharityProject
from app.schemas.charityproject import CharityProjectUpdate

PROJECT_ID_EXCEPTION = 'Проект с таким именем уже существует!'
OBJECTS_NOT_FOUND = 'Объекты не найдены!'
PROJECT_NOT_FOUND = 'Проект не найден!'
CLOSED_PROJECT_ERROR = 'Закрытый проект нельзя редактировать!'
FULL_AMOUNT_ERROR = 'Нельзя установить требуемую сумму меньше уже вложенной.'
INVEST_AMOUNT_ERROR = 'В проект были внесены средства, не подлежит удалению!'
MY_DONATION_ERROR = 'У вас еще нет пожертвований'


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """
    Проверяет есть ли проект с таким именем в базе.
    Если нет возвращает True.
    """
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(status_code=400, detail=PROJECT_ID_EXCEPTION)


async def check_number_objects(
        session: AsyncSession,
        crud,
) -> List:
    """
    Проверяет есть ли объекты в базе. Если есть возвращает список обьектов.
    """
    objects = await crud.get_multi(session)
    if not objects:
        raise HTTPException(status_code=404, detail=OBJECTS_NOT_FOUND)
    return objects


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
        obj_in: Optional[CharityProjectUpdate] = None,
) -> CharityProject:
    """
    Имеет 2 режима работы для обновления и удаления проекта.\n
    Для обоих режимов проверяет есть ли такой проект в базе. \n
    Для обновления дополнительно нужно передать `obj_in: CharityProjectUpdate`:
        1. Проверяет закрыт ли проект,
        2. Проверяет чтобы требуемая сумма была меньше вложенной.
    Для удаления нужны только `project_id: int, session: AsyncSession`:
        1. Проверяет инвестированы ли средства в проект.
    """
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=404, detail=PROJECT_NOT_FOUND)
    if obj_in:
        if project.fully_invested:
            raise HTTPException(status_code=400, detail=CLOSED_PROJECT_ERROR)
        if project.invested_amount and obj_in.full_amount is not None:
            if obj_in.full_amount < project.invested_amount:
                raise HTTPException(status_code=400, detail=FULL_AMOUNT_ERROR)
    else:
        if project.invested_amount:
            raise HTTPException(status_code=400, detail=INVEST_AMOUNT_ERROR)
    return project


async def check_my_donations(
        user: User,
        session: AsyncSession,
) -> List[Donation]:
    """
    Проверяет пожертвования пользователя, если есть возвращает список.
    """
    all_donations = await donation_crud.get_by_user(user, session)
    if not all_donations:
        raise HTTPException(status_code=404, detail=MY_DONATION_ERROR)
    return all_donations

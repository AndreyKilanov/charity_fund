from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_number_objects,
    check_my_donations
)
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationDB, DonationCreate, DonationResponse
from app.services.investment import investment

router = APIRouter()


@router.post(
    '/',
    response_model=DonationResponse,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Для зарегистрированных пользователей. \n
    Создание пожертвования.
    """
    projects = await charity_project_crud.get_unfinished(session)
    new_donat = await donation_crud.create(donation, session, user)
    session.add_all(investment(new_donat, projects))
    await session.commit()
    await session.refresh(new_donat)
    return new_donat


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для администраторов. \n
    Получает список всех пожертвований.
    """
    return await check_number_objects(session, donation_crud)


@router.get(
    '/my',
    response_model=List[DonationResponse],
    response_model_exclude_none=True,
)
async def get_my_all_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """
    Для зарегистрированных пользователей. \n
    Получает список пожертвований пользователя.
    """
    return await check_my_donations(user, session)

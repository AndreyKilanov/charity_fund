from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.services.google_api import (
    spreadsheets_create,
    set_user_permissions,
    spreadsheets_update_value,
    VALUE_ERROR_MESSAGE
)

router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],
)
async def get_projects(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """
    Только для администраторов. \n
    Выгружает только закрытые проекты отсортированные по скорости закрытия
    из бд в гугл таблицу.
    """
    projects = (
        await charity_project_crud.get_projects_by_completion_rate(session)
    )
    try:
        spreadsheet_id, spreadsheet_url, count_rows, count_columns = (
            await spreadsheets_create(projects, wrapper_services)
        )
    except ValueError:
        raise HTTPException(status_code=500, detail=VALUE_ERROR_MESSAGE)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(
        spreadsheet_id, projects, count_rows, count_columns, wrapper_services
    )
    return spreadsheet_url

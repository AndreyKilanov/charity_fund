from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get_project_id_by_name(
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    @staticmethod
    async def get_projects_by_completion_rate(
            session: AsyncSession,
    ) -> List[dict]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 1
            ).order_by(
                func.strftime('%s', CharityProject.close_date) -
                func.strftime('%s', CharityProject.create_date)
            )
        )
        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)

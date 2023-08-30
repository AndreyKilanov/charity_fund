import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
TABLE_VALUES = [
    ['Отчет от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
COLUMN = max(map(len, TABLE_VALUES))
SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет от ',
        locale='ru_RU',
    ),
    sheets=[
        dict(
            properties=dict(
                sheetType='GRID',
                sheetId=0,
                title='Лист1',
                gridProperties=dict(
                    rowCount=0,
                    columnCount=COLUMN
                )
            )
        )
    ]
)


async def spreadsheets_create(
        projects: list,
        wrapper_services: Aiogoogle
) -> tuple[str, str, int]:
    row = len(projects) + len(TABLE_VALUES)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = copy.deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] += datetime.now().strftime(FORMAT)
    spreadsheet_body['sheets'][0]['properties']['gridProperties'][
        'rowCount'] = row
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl'], row


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = dict(
        type='user',
        role='writer',
        emailAddress=settings.email
    )
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        row: int,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_value = [
        *copy.deepcopy(TABLE_VALUES),
        *[list(map(
            str,
            [res.name, (res.close_date - res.create_date), res.description])
        )for res in projects]
    ]
    table_value[0].append(datetime.now().__format__(FORMAT))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{row}C{COLUMN}',
            valueInputOption='USER_ENTERED',
            json=dict(majorDimension='ROWS', values=table_value)
        )
    )

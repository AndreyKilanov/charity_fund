import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
MAX_CELLS = 26000
VALUE_ERROR_MESSAGE = (f'Превышено допустимое кол-во ячеек!'
                       f' Максимум: {MAX_CELLS}')
TABLE_VALUES = [
    ['Отчет от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
SPREADSHEET_PROPERTIES = dict(
    title='Отчет от ',
    locale='ru_RU'
)
SHEET_PROPERTIES = dict(
    sheetType='GRID',
    sheetId=0,
    title='Лист1',
    gridProperties=dict(
        rowCount=0,
        columnCount=0
    )
)
SPREADSHEET_BODY = dict(
    properties=SPREADSHEET_PROPERTIES,
    sheets=[dict(properties=SHEET_PROPERTIES)]
)


async def spreadsheets_create(
        projects: list,
        wrapper_services: Aiogoogle
) -> list[str | int]:
    count_rows = len(projects) + len(TABLE_VALUES)
    count_columns = max(map(len, TABLE_VALUES))
    if (count_rows * count_columns) > MAX_CELLS:
        raise ValueError(VALUE_ERROR_MESSAGE)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = copy.deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] += datetime.now().strftime(FORMAT)
    spreadsheet_body['sheets'][0]['properties']['gridProperties'].update(
        dict(rowCount=count_rows, columnCount=count_columns)
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return [
        response['spreadsheetId'],
        response['spreadsheetUrl'],
        count_rows,
        count_columns
    ]


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
        count_rows: int,
        count_columns: int,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *copy.deepcopy(TABLE_VALUES),
        *[list(map(
            str,
            [res.name, (res.close_date - res.create_date), res.description])
        )for res in projects]
    ]
    table_values[0].append(datetime.now().strftime(FORMAT))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{count_rows}C{count_columns}',
            valueInputOption='USER_ENTERED',
            json=dict(majorDimension='ROWS', values=table_values)
        )
    )

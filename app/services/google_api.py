from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = '%Y/%m/%d %H:%M:%S'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    return (await wrapper_services.as_service_account(
        (
            await wrapper_services.discover('sheets', 'v4')
        ).spreadsheets.create(json={
            'properties': {
                'title': 'Отчёт закрытых проектов на {}'.format(
                    datetime.now().strftime(FORMAT)
                ),
                'locale': 'ru_RU'
            },
            'sheets': [
                {
                    'properties': {
                        'sheetType': 'GRID',
                        'title': 'Отчёт закрытых проектов',
                        'gridProperties': {
                            'rowCount': 100,
                            'columnCount': 3
                        }
                    }
                }
            ]
        })
    ))['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    await wrapper_services.as_service_account(
        (
            await wrapper_services.discover('drive', 'v3')
        ).permissions.create(
            fileId=spreadsheetid,
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': settings.email
            },
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    await wrapper_services.as_service_account(
        (
            await wrapper_services.discover('sheets', 'v4')
        ).spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:C100',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': [
                    ['Отчёт от', datetime.now().strftime(FORMAT)],
                    ['Топ проектов по скорости закрытия'],
                    ['Названия проекта', 'Время сбора', 'Описание'],
                    *[[
                        str(project['name']),
                        '{}day(s)'.format(project['days']),
                        str(project['description'])
                    ] for project in projects]
                ]
            }
        )
    )

from aiohttp import web
from datetime import datetime

from DataStorage import DataStorage


routes = web.RouteTableDef()


def _to_ms_date(date: str) -> int:
    zero = datetime(1899, 12, 30, 0, 0, 0)

    try:
        return (datetime.fromisoformat(date) - zero).days
    except ValueError:
        return 0


@routes.get('/api/roads/')
async def get_roads(request: web.Request) -> web.Response:
    storage: DataStorage = request.app['storage']
    return web.json_response(await storage.get_roads())


@routes.get('/api/locations/')
async def get_locations(request: web.Request) -> web.Response:
    storage: DataStorage = request.app['storage']
    return web.json_response(await storage.get_locations())


@routes.post('/api/repairs/')
async def check_repairs(request: web.Request) -> web.Response:
    storage: DataStorage = request.app['storage']

    data = await request.json()
    road = data['road']
    begin = _to_ms_date(data.get('begin', str()))
    end = _to_ms_date(data.get('end', str()))

    return web.json_response(await storage.get_repairs(road, begin, end))


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)

    settings = {
        'database': 'test',
    }

    app['storage'] = DataStorage(settings['database'])

    web.run_app(app)

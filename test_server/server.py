from aiohttp import web
import settings

routes = web.RouteTableDef()


@routes.get('/')
def home(request):
    return web.json_response('Test Server Alive')


@routes.post('/student')
async def verifyStudent(request):
    webData = await request.json()
    verified_students = ['STD-01', 'STD-02', 'STD-03']
    success = {'status': 1}
    failed = {'status': 0}
    if webData:
        data = {'isStaff': False}
        std_number = webData.get('std_number')
        if not std_number:
            return web.json_response({**failed, 'message': 'Student Number is required'}, status=400)
        if std_number in verified_students:
            data['isValid'] = True
            return web.json_response({**success, **data}, status=200)
        data['isValid'] = False
        return web.json_response({**failed, **data}, status=200)


@routes.post('/staff')
async def verifyStaff(request):
    webData = await request.json()
    verified_staff = ['REG-02', 'STF-01', 'STF-02', 'REG-01']
    success = {'status': 1}
    failed = {'status': 0}
    if webData:
        data = {}
        std_number = webData.get('std_number')
        if not std_number:
            return web.json_response({**failed, 'message': 'Staff Number is required'}, status=400)
        if std_number in verified_staff:
            data['isValid'] = True
            data['isStaff'] = True
            return web.json_response({**success, **data}, status=200)
        data['isValid'] = False
        data['isStaff'] = False
        return web.json_response({**failed, **data}, status=200)

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=settings.PORT)

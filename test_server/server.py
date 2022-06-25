from aiohttp import web
import settings

routes = web.RouteTableDef()


@routes.get('/')
def home(request):
    return web.json_response('Test Server Alive')


@routes.post('/student')
async def verifyStudent(request):
    webData = await request.json()
    verified_students = ['STD-01', 'STD-02', 'STD_03']
    success = {'status': 1}
    failed = {'status': 0}
    if webData:
        data = {}
        std_number = webData.get('std_number')
        if not std_number:
            return web.json_response({**failed, 'message': 'Student Number is required'}, status=400)
        if std_number in verified_students:
            data['isValid'] = True
            return web.json_response({**success, **data}, status=200)
        data['isValid'] = False
        return web.json_response({**failed, **data}, status=200)


@routes.post('/staff')
def verifyStaff(request):
    staff_no = request.POST.get('regNo')
    registered_staff_nos = []

    if staff_no not in registered_staff_nos:
        return web.json_response({'status': 'failed', 'message': 'Invalid Reg No'}, status=400)
    return web.json_response({'status': 'success', 'message': 'Valid Reg Number'}, status=404)


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=settings.PORT)

from aiohttp import web
import aiohttp_cors

async def handle_request(request):
    data = await request.json()
    context = data.get('context')
    user = data.get('user')
    message = data.get('message')
    print(message)

    return web.json_response({'status': 'success', 'message': 'Command received!'})

app = web.Application()

# CORS config
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

route = app.router.add_post('/', handle_request)
cors.add(route)
web.run_app(app, port=5000)

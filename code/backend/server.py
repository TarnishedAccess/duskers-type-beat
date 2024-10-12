from aiohttp import web
import aiohttp_cors
import asyncio

IGNORED_COMPONENTS = ['keyboard', 'filesystem', 'modem', 'gpu', 'screen', 'internet', 'eeprom', 'robot']
class Drone:
    def __init__(self, name, components, writer):
        self.name = name
        self.components = components
        self.writer = writer

connected_clients = []

# HTTP handler for JS calls
async def handle_request(request):
    data = await request.json()
    targetDrone = data.get('user')
    message = data.get('message')
    print(f"Received API request: {targetDrone}:{message}")

    await broadcast_message_target(targetDrone, message)
    return web.json_response({'status': 'success', 'message': 'Command broadcasted to Lua clients!'})

async def get_connected_drones(request):
    drones = [{'name': drone.name, 'components': drone.components} for drone in connected_clients]
    return web.json_response({'connected_drones': drones})

# TCP handler for Lua clients
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New Lua client connected from {addr}")

    handshake = await reader.read(1024)
    name, components = handshake.decode().split('|')
    components_list = [component.strip() for component in components.split(',')]

    # Filter out ignored components without modifying the list while iterating
    components_list = [component for component in components_list if component not in IGNORED_COMPONENTS]

    #==============================================#
    #ignored components:
    #keyboard, filesystem, modem, gpu, screen, internet, eeprom

    #ignore for now:
    #robot

    #potential uses:
    #computer: energy, shutdown, reboot, uptime
    #camera: distance front/up/down
    #radar: getplayers, getmobs, getitems
    #generator: refuel
    #navigation: get position, get facing
    #inventory controller: general inv management
    #==============================================#


    #======TESTS=======
    print(name)
    print(components_list)
    #==================

    connected_clients.append(Drone(name, components_list, writer))

    try:
        while True:
            data = await reader.read(100)
            if not data:
                print(f"Lua client {addr} disconnected.")
                break

            message = data.decode().strip()
            print(f"Received from {addr}: {message}")

    except ConnectionResetError:
        print(f"Lua client {addr} disconnected.")
    finally:
        for connected_client in connected_clients:
            if connected_client.writer == writer:
                connected_clients.remove(connected_client)
        writer.close()
        await writer.wait_closed()

# Broadcast messages to all Lua clients
async def broadcast_message(message):
    print(f"Broadcasting message to all Lua clients: {message}")
    for connected_client in connected_clients:
        connected_client.writer.write(f"{message}\n".encode())
        await connected_client.writer.drain()

# Broadcast message to specific client
async def broadcast_message_target(target, message):
    print(f"Broadcasting message to targetted Lua client: {message}")
    connected_clients[target].writer.write(f"{message}\n".encode())
    await connected_clients[target].writer.drain()

# Main server function
async def main():
    # TCP server for Lua clients
    tcp_server = await asyncio.start_server(handle_client, '127.0.0.1', 5000)

    # HTTP server for JavaScript API calls
    app = web.Application()
    
    # CORS config
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # HTTP route for JS calls
    route = app.router.add_post('/', handle_request)
    cors.add(route)

    get_route = app.router.add_get('/connected_drones', get_connected_drones)
    cors.add(get_route)

    print("Servers started: TCP port 5000, HTTP port 5001.")

    # Start servers
    async with tcp_server:
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '127.0.0.1', 5001)
        await site.start()

        # Keep servers running
        await tcp_server.serve_forever()

# Run the servers
asyncio.run(main())

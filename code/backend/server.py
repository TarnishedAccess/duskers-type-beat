from aiohttp import web
import aiohttp_cors
import asyncio

IGNORED_COMPONENTS = ['keyboard', 'filesystem', 'modem', 'gpu', 'screen', 'internet', 'eeprom', 'robot']
class Drone:
    def __init__(self, name, components, writer, reader):
        self.name = name
        self.components = components
        self.writer = writer
        self.reader = reader

connected_clients = []
queryReply = ""
queryReplyUpdate = asyncio.Event()
#This works for now? but If you need drones to work alongside each other just make a list and dynamically add these in instead of using one.

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

async def get_drone_info(request):
    global queryReply

    selected_drone = request.query.get('param1')
    context = "reply:queryReply=" + request.query.get('param2').strip()
    print("context: ", context)
    await broadcast_message_target(selected_drone, context)

    # Make sure the reply variable is updated before sending
    # Sloppy, but it works
    await queryReplyUpdate.wait()
    queryReplyUpdate.clear()

    return web.json_response({'drone_power': queryReply})


# TCP handler for Lua clients
async def handle_client(reader, writer):
    global queryReply

    addr = writer.get_extra_info('peername')
    print(f"New Lua client connected from {addr}")
    handshake = await reader.read(1024)
    name, components = handshake.decode().split('|')
    components_list = [component.strip() for component in components.split(',')]

    # Filter out ignored components
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

    connected_clients.append(Drone(name, components_list, writer, reader))

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"Lua client {addr} disconnected.")
                break
            
            message = data.decode().strip()

            if "reply:" in message:
                queryReply = message.split('reply:')[1]
                print("query reply:")
                print(queryReply)
                queryReplyUpdate.set()


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
    connected_clients[int(target)-1].writer.write(f"{message}\n".encode())
    await connected_clients[int(target)-1].writer.drain()

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

    get_route = app.router.add_get('/drone_info', get_drone_info)
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

#TODO: THE HANDLE CLIENT FUNCTION STEALS ALL THE READER ACTIVITY FROM GETTING DRONE INFO. FIX IT.
#TODO: THE SYSTEM HANGS UP, PROBABLY BECAUSE OF LOCKS. UNFUCK THE FIRST ONE AND YOU PROBABLY UNFUCK THE SECOND.
from aiohttp import web
import aiohttp_cors
import asyncio

connected_clients = []

# HTTP handler for JS calls
async def handle_request(request):
    data = await request.json()
    message = data.get('message')
    print(f"Received API request: {message}")

    # Eventually want to broadcast message to selected drone rather than all
    await broadcast_message(message)
    return web.json_response({'status': 'success', 'message': 'Command broadcasted to Lua clients!'})

# TCP handler for Lua clients
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New Lua client connected from {addr}")
    connected_clients.append(writer)

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
        connected_clients.remove(writer)
        writer.close()
        await writer.wait_closed()

# Broadcast messages to all Lua clients
# Change this to be broadcasted to a specific drone later
async def broadcast_message(message):
    print(f"Broadcasting message to all Lua clients: {message}")
    for client in connected_clients:
        client.write(f"{message}\n".encode())
        await client.drain()

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

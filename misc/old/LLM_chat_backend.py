#connected to module: LLM_chat.lua

import g4f
import asyncio

server_address = ('127.0.0.1', 6667)

memory = []
#model = g4f.models.solar_1_mini
model = g4f.models.gpt_3

def update_memory(self, user, user_message, bot_message):
    self.memory.extend(
        [
            {"role": "user", "content": f"{user}: {user_message}"},
            {"role": "assistant", "content": bot_message},
        ]
    )

async def get_response(context, user, user_message):

    global memory
    global model

    messages = []
    messages.append({"role": "system", "content": context})
    messages.extend(memory)
    messages.append({"role": "user", "content": f"{user}: {user_message}"})

    print("test here 2")

    response = g4f.ChatCompletion.create(
        model=model, messages=messages
    )

    print("test here 3")

    return response

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")
    print('waiting for data')

    while True:
        try:
            data = await reader.read(1024)
            if data:
                message = data.decode('utf-8')
                print(f"Received from {addr}: {message}")
                print("test here 0")
                split_message = message.split("|")
                context, user, message = split_message[0], split_message[1], split_message[2]
                print("test here 1")
                response = await get_response(context, user, message)
                print("test here 4")
                writer.write(response.encode())
                await writer.drain()

        except ConnectionResetError:
            print("Connection reset by peer {addr}")
            break

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, server_address[0], server_address[1])
    print(f"Server running on {server_address}")
    async with server:
        await server.serve_forever()

asyncio.run(main())
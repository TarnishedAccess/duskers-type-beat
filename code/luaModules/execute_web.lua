--connected to backend: LLM_chat_backend.py

local robot = require("robot")
local event = require("event")
local component = require("component")
local chat = component.chat
local internet = component.internet
local handle = internet.connect("127.0.0.1", 5000)
local name = robot.name()

while not handle.finishConnect() do
    os.sleep(0.1)
end

print("Connection established. " .. name .. " online.")
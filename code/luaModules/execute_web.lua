local robot = require("robot")
local event = require("event")
local component = require("component")
local internet = component.internet
local handle = internet.connect("127.0.0.1", 5000)
local name = robot.name()

while not handle.finishConnect() do
    os.sleep(0.1)
end

print("Connection established. " .. name .. " online.")

while true do
    local data = handle.read(1024)
    if #data > 0 then
        print("Received: " .. data)
    elseif err then
        print("Error reading from server: " .. err)
        break
    end
end

handle.close()

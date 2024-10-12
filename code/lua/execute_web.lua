robot = require("robot")
event = require("event")
component = require("component")
internet = component.internet
handle = internet.connect("127.0.0.1", 5000)
name = robot.name()

function executeInput(code)
    local func, err = load(code)
    
    if not func then
        print("Error loading code:", err)
        return
    end
    
    local success, execErr = pcall(func)
    
    if not success then
        print("Error executing code:", execErr)
    end
end

--inefficient but i dont really care, if its a problem change it later
local component_list = {}
for k, v in component.list() do
    table.insert(component_list, v)
end
local component_string = table.concat(component_list, ", ")

while not handle.finishConnect() do
    os.sleep(0.1)
end

print("Connection established. " .. name .. " online.")

handle.write(name .. "|" .. component_string)

while true do
    local data = handle.read(1024)
    if #data > 0 then
        print("Received: " .. data)
        executeInput(data)
    elseif err then
        print("Error reading from server: " .. err)
        break
    end
end

handle.close()

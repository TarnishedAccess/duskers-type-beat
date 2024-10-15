robot = require("robot")
event = require("event")
computer = require("computer")
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

--inefficient but i dont really care, will change later if it becomes an issue
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

        if string.sub(data, 1, 6) == "reply:" then
            local data = string.sub(data, 7):gsub("^%s*(.-)%s*$", "%1")
            executeInput(data)
            handle.write("reply:" .. queryReply)
            print("Data sent: " .. queryReply)
        else
            executeInput(data)
        end
            
    elseif err then
        print("Error reading from server: " .. err)
        break
    end
end

handle.close()

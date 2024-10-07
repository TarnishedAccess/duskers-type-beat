robot = require("robot")
event = require("event")
component = require("component")
chat = component.chat
local name = robot.name()

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

local running = true

while running do
    _, _, user, message = event.pull("chat_message")
    if string.find(message, name..":") then
        local new_string = string.gsub(message, name..":", "")
        executeInput(new_string)
    end
end

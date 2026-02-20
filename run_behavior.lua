-- run_behavior.lua

local json = require("dkjson")  -- or any JSON lib you choose
local behavior = require("behavior")

local input = io.read("*a")
local snapshot, _, err = json.decode(input, 1, nil)
if err then
    io.stderr:write("JSON decode error: " .. err .. "\n")
    os.exit(1)
end

local advice = behavior.adjust(snapshot)
local output = json.encode(advice, { indent = false })
print(output)
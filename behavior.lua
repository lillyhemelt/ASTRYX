-- behavior.lua

local M = {}

function M.adjust(snapshot)
    local advice = {
        notes = {},
        trait_adjustments = {}
    }

    if snapshot.perception and snapshot.perception.emotion == "sad" then
        table.insert(advice.notes, "User seems sad; consider more comfort.")
        advice.trait_adjustments["empathy"] = 0.05
    end

    if snapshot.goal == "comfort" then
        table.insert(advice.notes, "Comfort used; watch for overuse.")
    end

    return advice
end

return M
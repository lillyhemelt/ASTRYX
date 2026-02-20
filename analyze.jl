using JSON

function analyze(snapshot)
    mood = snapshot["state_snapshot"]["mood"]
    traits = snapshot["state_snapshot"]["traits"]

    drift_risk = mood < -0.5 && traits["directness"] > 0.7

    return Dict(
        "drift_risk" => drift_risk,
        "recommended_adjustments" => drift_risk ? Dict("caution" => 0.1) : Dict()
    )
end

input = read(stdin, String)
snapshot = JSON.parse(input)
result = analyze(snapshot)
print(JSON.json(result))
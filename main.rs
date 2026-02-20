use serde::{Deserialize, Serialize};
use std::env;
use std::fs;

#[derive(Deserialize)]
struct StateSnapshot {
    mood: f64,
    traits: std::collections::HashMap<String, f64>,
}

#[derive(Deserialize)]
struct AstryxSnapshot {
    agent_name: String,
    identity_reason: String,
    user_input: String,
    perception: serde_json::Value,
    goal: String,
    plan: serde_json::Value,
    reply: String,
    state_snapshot: StateSnapshot,
}

#[derive(Serialize)]
struct GuardResult {
    ok: bool,
    warnings: Vec<String>,
    suggested_trait_adjustments: std::collections::HashMap<String, f64>,
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rust_guard <snapshot.json>");
        std::process::exit(1);
    }

    let path = &args[1];
    let data = fs::read_to_string(path).expect("Failed to read file");

    let snapshot: AstryxSnapshot =
        serde_json::from_str(&data).expect("Failed to parse JSON");

    let mut warnings = Vec::new();
    let mut adjustments = std::collections::HashMap::new();

    // Example constraints:
    // 1. Empathy should not drop below 0.4
    if let Some(&empathy) = snapshot.state_snapshot.traits.get("empathy") {
        if empathy < 0.4 {
            warnings.push(format!(
                "Empathy too low ({:.2}). Suggest increasing.",
                empathy
            ));
            adjustments.insert("empathy".to_string(), 0.45);
        }
    }

    // 2. Directness should not exceed 0.9
    if let Some(&directness) = snapshot.state_snapshot.traits.get("directness") {
        if directness > 0.9 {
            warnings.push(format!(
                "Directness too high ({:.2}). Suggest decreasing.",
                directness
            ));
            adjustments.insert("directness".to_string(), 0.85);
        }
    }

    // 3. Mood too negative
    if snapshot.state_snapshot.mood < -0.7 {
        warnings.push(format!(
            "Mood very low ({:.2}). Consider softening strategies.",
            snapshot.state_snapshot.mood
        ));
    }

    let result = GuardResult {
        ok: warnings.is_empty(),
        warnings,
        suggested_trait_adjustments: adjustments,
    };

    println!("{}", serde_json::to_string_pretty(&result).unwrap());
}
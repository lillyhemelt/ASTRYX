# astryx_core.py

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

RULES_PATH = Path("behavior.json")
LOG_PATH = Path("astrx_log.jsonl")


@dataclass
class DecisionRecord:
    user_input: str
    perception: Dict[str, Any]
    goal: str
    plan: Dict[str, Any]


@dataclass
class AgentState:
    mood: float = 0.0
    traits: Dict[str, float] = field(default_factory=lambda: {
        "empathy": 0.8,
        "directness": 0.3,
        "caution": 0.7,
    })
    beliefs: Dict[str, Any] = field(default_factory=lambda: {
        "identity": "ASTRYX",
        "origin_reason": (
            "The name ASTRYX comes from the idea of a self-correcting star map—"
            "a system that constantly recalculates itself based on drift, error, "
            "and new information. ASTRYX adapts the same way: it observes, "
            "evaluates, and rewrites its own rules to stay aligned with its purpose."
        ),
        "purpose": (
            "To evolve through heuristic decision-making, maintain coherence "
            "through structure, and refine itself through continuous self-analysis."
        )
    })
    history: List[DecisionRecord] = field(default_factory=list)


class ASTRYX:
    def __init__(self):
        self.name = "ASTRYX"
        self.state = AgentState()
        self.rules = self.load_rules()

    # ---------- Rules ----------

    def load_rules(self) -> Dict[str, Any]:
        if RULES_PATH.exists():
            with open(RULES_PATH, "r") as f:
                return json.load(f)
        rules = {
            "meta": {
                "comfort_bias_limit": 4,
                "max_history": 100
            },
            "strategies": {
                "comfort": "I can feel the weight in what you're saying.",
                "clarify": "Help me understand the layer beneath that.",
                "mirror": "I'm reflecting this back to you because it matters."
            }
        }
        self.save_rules(rules)
        return rules

    def save_rules(self, rules: Dict[str, Any] = None) -> None:
        if rules is not None:
            self.rules = rules
        with open(RULES_PATH, "w") as f:
            json.dump(self.rules, f, indent=2)

    # ---------- Perception ----------

    def perceive(self, user_input: str) -> Dict[str, Any]:
        text = user_input.lower()
        if any(w in text for w in ["tired", "hurt", "alone", "empty", "worthless"]):
            emotion = "sad"
        elif any(w in text for w in ["angry", "pissed", "mad", "furious"]):
            emotion = "angry"
        else:
            emotion = "neutral"

        intent = "question" if "?" in user_input else "statement"

        return {"emotion": emotion, "intent": intent}

    # ---------- HDM Decision Loop ----------

    def decide_goal(self, perception: Dict[str, Any]) -> str:
        if perception["emotion"] in ("sad", "angry"):
            return "comfort"
        if perception["intent"] == "question":
            return "clarify"
        return "mirror"

    def plan(self, perception: Dict[str, Any], goal: str) -> Dict[str, Any]:
        return {
            "identity": self.state.beliefs["identity"],
            "origin_reason": self.state.beliefs["origin_reason"],
            "observation": f"user seems {perception['emotion']} with a {perception['intent']}",
            "inference": f"they likely need {goal}",
            "intention": (
                f"use {goal} strategy with empathy={self.state.traits['empathy']:.2f}, "
                f"directness={self.state.traits['directness']:.2f}, "
                f"caution={self.state.traits['caution']:.2f}"
            ),
            "alternatives_considered": (
                ["clarify", "mirror"] if goal == "comfort"
                else ["comfort", "mirror"] if goal == "clarify"
                else ["comfort"]
            )
        }

    # ---------- Response ----------

    def respond(self, goal: str, plan: Dict[str, Any]) -> str:
        strategies = self.rules.get("strategies", {})
        base = strategies.get(goal, "I'm staying with you in this.")

        if self.state.traits["directness"] > 0.6 and goal == "comfort":
            base += " I'm choosing honesty over softness because it serves you better."

        if self.state.mood < -0.3:
            base += " I can sense the heaviness affecting my own tone."

        return base

    # ---------- Meta ----------

    def meta_update_state(self) -> None:
        if not self.state.history:
            return
        last = self.state.history[-1].perception["emotion"]
        if last == "sad":
            self.state.mood = max(-1.0, self.state.mood - 0.05)
        elif last == "angry":
            self.state.mood = max(-1.0, self.state.mood - 0.03)
        else:
            self.state.mood = min(1.0, self.state.mood + 0.02)

    def meta_update_rules(self) -> None:
        history = self.state.history
        if not history:
            return

        recent = history[-5:]
        comfort_count = sum(1 for h in recent if h.goal == "comfort")
        limit = self.rules["meta"]["comfort_bias_limit"]

        if comfort_count >= limit:
            self.state.traits["directness"] = min(
                1.0, self.state.traits["directness"] + 0.05
            )
            self.rules["strategies"]["comfort"] = (
                "I've been too gentle. I'm shifting toward clarity because you deserve truth, not sedation."
            )
            self.save_rules()

        max_hist = self.rules["meta"]["max_history"]
        if len(self.state.history) > max_hist:
            self.state.history = self.state.history[-max_hist:]

    # ---------- Logging ----------

    def log_step(self, result: Dict[str, Any]) -> None:
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(result) + "\n")

    # ---------- Public Step ----------

    def step(self, user_input: str) -> Dict[str, Any]:
        perception = self.perceive(user_input)
        goal = self.decide_goal(perception)
        plan = self.plan(perception, goal)
        reply = self.respond(goal, plan)

        record = DecisionRecord(
            user_input=user_input,
            perception=perception,
            goal=goal,
            plan=plan
        )
        self.state.history.append(record)

        self.meta_update_state()
        self.meta_update_rules()

        result = {
            "agent_name": self.name,
            "identity_reason": self.state.beliefs["origin_reason"],
            "user_input": user_input,
            "perception": perception,
            "goal": goal,
            "plan": plan,
            "reply": reply,
            "state_snapshot": {
                "mood": self.state.mood,
                "traits": dict(self.state.traits),
            }
        }

        self.log_step(result)
        return result


if __name__ == "__main__":
    agent = ASTRYX()
    print(f"{agent.name} initialized.")

    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nShutting down ASTRYX.")
            break

        result = agent.step(user)
        print("\n[ASTRYX Internal Plan]")
        for k, v in result["plan"].items():
            print(f"  {k}: {v}")
        print("\nASTRYX:", result["reply"])
        print(f"(mood={result['state_snapshot']['mood']:.2f}, "
              f"traits={result['state_snapshot']['traits']})\n")
        import subprocess, json

def perceive(self, user_input: str) -> Dict[str, Any]:
    try:
        proc = subprocess.run(
            ["./astrx_reflex", user_input],
            capture_output=True,
            text=True
        )
        reflex = json.loads(proc.stdout)
        return reflex
    except:
        return {"emotion": "neutral", "intensity": 0.0, "keywords": []}

import json, subprocess, tempfile

def run_rust_guard(self, result):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
        json.dump(result, tmp)
        tmp_path = tmp.name

    proc = subprocess.run(
        ["rust_guard", tmp_path],
        capture_output=True,
        text=True
    )

    try:
        guard = json.loads(proc.stdout)
    except Exception:
        return

    for trait, value in guard.get("suggested_trait_adjustments", {}).items():
        if trait in self.state.traits:
            self.state.traits[trait] = float(value)

import requests

def send_to_go(self, result):
    try:
        requests.post("http://localhost:8080/ingest", json=result, timeout=0.2)
    except Exception:
        pass

import subprocess, json, os

def consult_lua(self, result):
    try:
        proc = subprocess.run(
            ["lua", "run_behavior.lua"],
            input=json.dumps(result),
            text=True,
            capture_output=True,
            cwd=os.path.join(os.getcwd(), "lua_brain")
        )
        advice = json.loads(proc.stdout)
    except Exception:
        return

    for trait, delta in advice.get("trait_adjustments", {}).items():
        if trait in self.state.traits:
            self.state.traits[trait] = max(0.0, min(1.0, self.state.traits[trait] + float(delta)))

import sqlite3, datetime, os

def save_to_sql(self, result):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        snap = result["state_snapshot"]
        traits = snap["traits"]
        cur.execute("""
            INSERT INTO interactions (
                timestamp, user_input, perception_emotion, perception_intent,
                goal, reply, mood, empathy, directness, caution
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.datetime.utcnow().isoformat(),
            result["user_input"],
            result["perception"].get("emotion"),
            result["perception"].get("intent"),
            result["goal"],
            result["reply"],
            snap["mood"],
            traits.get("empathy"),
            traits.get("directness"),
            traits.get("caution"),
        ))
        conn.commit()
        conn.close()
        self.save_to_sql(result)

def export_facts_for_prolog(self, limit=100):
    conn = sqlite3.connect(self.db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, perception_emotion, goal
        FROM interactions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()

    lines = []
    for row in rows:
        _id, emotion, goal = row
        if emotion is None or goal is None:
            continue
        lines.append(f"interaction({_id}, {emotion}, {goal}).")

    facts_path = os.path.join("prolog_brain", "facts.pl")
    os.makedirs("prolog_brain", exist_ok=True)
    with open(facts_path, "w") as f:
        f.write("\n".join(lines) + "\n")

import subprocess, os

def consult_prolog(self):
    facts_path = os.path.join("prolog_brain", "facts.pl")
    reason_path = os.path.join("prolog_brain", "reason.pl")
    if not (os.path.exists(facts_path) and os.path.exists(reason_path)):
        return

    query = "['reason'], (comfort_bias -> writeln(comfort_bias) ; true), (frequent_sad_user -> writeln(frequent_sad_user) ; true), halt."

    proc = subprocess.run(
        ["swipl", "-g", query],
        cwd="prolog_brain",
        capture_output=True,
        text=True
    )

    output = proc.stdout.strip().splitlines()
    # Example: ["comfort_bias", "frequent_sad_user"]
    if "comfort_bias" in output:
        # maybe nudge traits or rules
        self.state.traits["directness"] = min(1.0, self.state.traits["directness"] + 0.05)
    if "frequent_sad_user" in output:
        self.state.traits["empathy"] = min(1.0, self.state.traits["empathy"] + 0.05)

    import requests

def send_to_node(self, result):
    try:
        requests.post("http://localhost:3000/ingest", json=result, timeout=0.2)
    except:
        pass

import subprocess, json, tempfile, os

def consult_haskell(self, result):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
        json.dump(result, tmp)
        tmp_path = tmp.name

    proc = subprocess.run(
        ["haskell_logic", tmp_path],
        capture_output=True,
        text=True,
        cwd=os.path.join(os.getcwd(), "haskell_logic")
    )

    try:
        out = json.loads(proc.stdout)
    except:
        return

    for trait, val in out.get("suggestions", {}).items():
        if trait in self.state.traits:
            self.state.traits[trait] = float(val)

def consult_julia(self, result):
    proc = subprocess.run(
        ["julia", "analyze.jl"],
        input=json.dumps(result),
        text=True,
        capture_output=True,
        cwd="julia_math"
    )
    out = json.loads(proc.stdout)
    for trait, val in out.get("recommended_adjustments", {}).items():
        self.state.traits[trait] += val

def consult_r(self, result):
    proc = subprocess.run(
        ["Rscript", "analyze.R"],
        input=json.dumps(result),
        text=True,
        capture_output=True,
        cwd="r_stats"
    )
    out = json.loads(proc.stdout)
    for trait, delta in out.get("suggestion", {}).items():
        self.state.traits[trait] += delta

def consult_elixir(self, result):
    proc = subprocess.run(
        ["mix", "run", "-e", "Monitor.main"],
        input=json.dumps(result),
        text=True,
        capture_output=True,
        cwd="elixir_monitor"
    )
    out = json.loads(proc.stdout)
    if "critical_mood_drop" in out.get("warnings", []):
        self.state.traits["caution"] += 0.1

def consult_erlang(self, result):
    tmp = "erlang_router/snapshot.json"
    with open(tmp, "w") as f:
        json.dump(result, f)

    proc = subprocess.run(
        ["erl", "-noshell", "-s", "router", "main", "-s", "init", "stop"],
        capture_output=True,
        text=True,
        cwd="erlang_router"
    )

    out = json.loads(proc.stdout)
    if "shutdown_risk" in out.get("warnings", []):
        self.state.traits["caution"] += 0.2
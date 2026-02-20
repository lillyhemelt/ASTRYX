import sys, os, subprocess, json, time, requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

def safe_start(cmd, cwd):
    try:
        subprocess.Popen(cmd, cwd=cwd)
        print(f"[OK] Started {cmd} in {cwd}")
    except Exception as e:
        print(f"[FAIL] Could not start {cmd} in {cwd}: {e}")

def safe_call(cmd, cwd, input_data=None):
    try:
        proc = subprocess.run(
            cmd,
            input=json.dumps(input_data) if input_data else None,
            text=True,
            capture_output=True,
            cwd=cwd
        )
        return json.loads(proc.stdout)
    except Exception as e:
        print(f"[FAIL] Organ call failed: {cmd} in {cwd}: {e}")
        return {"warnings": ["organ offline"], "suggestions": {}}

class Orchestrator:
    def __init__(self):
        from python_core.astryx_core import ASTRYX
        self.agent = ASTRYX()

    def start_services(self):
        safe_start(
            [r"C:\Program Files\Go\bin\go.exe", "run", "."],
            os.path.join(ROOT, "go_hub")
        )

        safe_start(
            ["node", "server.js"],
            os.path.join(ROOT, "node_gateway")
        )

        safe_start(
            ["dotnet", "run"],
            os.path.join(ROOT, "csharp_dashboard")
        )

        safe_start(
            ["mix", "run"],
            os.path.join(ROOT, "elixir_monitor")
        )

    def call_cpp_reflex(self, snapshot):
        return safe_call(
            ["./astrx_reflex", snapshot["user_input"]],
            os.path.join(ROOT, "cpp_reflex")
        )

    def call_java_spine(self, snapshot):
        return safe_call(
            ["mvn", "exec:java"],
            os.path.join(ROOT, "java_spine")
        )

    def call_rust_guard(self, snapshot):
        return safe_call(
            ["rust_guard", "snapshot.json"],
            os.path.join(ROOT, "rust_guard")
        )

    def call_lua(self, snapshot):
        return safe_call(
            ["lua", "run_behavior.lua"],
            os.path.join(ROOT, "lua_brain"),
            input_data=snapshot
        )

    def call_haskell(self, snapshot):
        return safe_call(
            ["haskell_logic", "snapshot.json"],
            os.path.join(ROOT, "haskell_logic")
        )

    def call_julia(self, snapshot):
        return safe_call(
            ["julia", "analyze.jl"],
            os.path.join(ROOT, "julia_math"),
            input_data=snapshot
        )

    def call_r(self, snapshot):
        return safe_call(
            ["Rscript", "analyze.R"],
            os.path.join(ROOT, "r_stats"),
            input_data=snapshot
        )

    def call_prolog(self):
        return safe_call(
            ["swipl", "-g", "['reason'], main, halt"],
            os.path.join(ROOT, "prolog_brain")
        )

    def call_erlang(self):
        return safe_call(
            ["erl", "-noshell", "-s", "router", "main", "-s", "init", "stop"],
            os.path.join(ROOT, "erlang_router")
        )

    def merge_adjustments(self, *organs):
        merged = {"traits": {}, "warnings": []}
        for organ in organs:
            if "warnings" in organ:
                merged["warnings"].extend(organ["warnings"])
            if "suggestions" in organ:
                for trait, val in organ["suggestions"].items():
                    merged["traits"][trait] = merged["traits"].get(trait, 0) + val
        return merged

    def run(self):
        self.start_services()
        print("ASTRYX orchestrator online.")

        while True:
            user_input = input("You: ")
            result = self.agent.step(user_input)

            organs = [
                self.call_cpp_reflex(result),
                self.call_rust_guard(result),
                self.call_lua(result),
                self.call_haskell(result),
                self.call_julia(result),
                self.call_r(result),
                self.call_prolog(),
                self.call_erlang()
            ]

            merged = self.merge_adjustments(*organs)

            for trait, delta in merged["traits"].items():
                self.agent.state.traits[trait] += delta

            try:
                requests.post("http://localhost:3000/ingest", json=result)
            except:
                print("[WARN] Node gateway offline")

            try:
                requests.post("http://localhost:8080/ingest", json=result)
            except:
                print("[WARN] Go hub offline")

            print("ASTRYX:", result["reply"])


if __name__ == "__main__":
    orch = Orchestrator()
    orch.run()
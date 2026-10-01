"""The browser engine (app/engine.js) must decide like the Python core (design.py)."""
import json
import shutil
import subprocess
import unittest
from pathlib import Path

from palladio_code.design import run_design

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    {},
    {"module": 18, "wing": [{"form": "5:3", "size": "grande"}, {"form": "1:1", "size": "mediocre"},
                            {"form": "3:2", "size": "picciola"}]},
    {"module": 16, "wing": [{"form": "2:1", "size": "grande"}, {"form": "1:1", "size": "mediocre"}]},
    {"ceiling": "flat"},
    {"module": 20, "wing": [{"form": "3:2", "size": "grande"}, {"form": "1:1", "size": "mediocre"},
                            {"form": "2:1", "size": "picciola"}]},
]


def js_params(case):
    rooms = [{"size": r["size"], "form": r["form"], "ceiling": case.get("ceiling", "vault")}
             for r in case.get("wing", [{"size": "grande", "form": "5:3"}, {"size": "mediocre", "form": "1:1"},
                                        {"size": "picciola", "form": "4:3"}])]
    out = {"rooms": rooms}
    if "module" in case:
        out["module"] = case["module"]
    return out


@unittest.skipUnless(shutil.which("node"), "node not installed")
class EngineParityTests(unittest.TestCase):
    def test_same_rooms_and_heights(self):
        script = (
            "import('./app/engine.js').then(m => {"
            f"const cases = {json.dumps([js_params(c) for c in CASES])};"
            "console.log(JSON.stringify(cases.map(c => { const d = m.run(c);"
            " return {rooms: d.rooms.map(r => [r.length, r.breadth, Number(r.height.toFixed(6)), r.heightRule]),"
            " sala: [d.sala.length, d.sala.breadth]}; })));});"
        )
        out = subprocess.run(["node", "--input-type=module", "-e", script], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
        js = json.loads(out)
        for case, got in zip(CASES, js):
            py = run_design(case)
            want = [[r.length, r.breadth, round(r.height, 6), r.height_rule] for r in py.rooms]
            self.assertEqual(got["rooms"], want, case)
            self.assertEqual(got["sala"], [py.sala.length, py.sala.breadth], case)


if __name__ == "__main__":
    unittest.main()

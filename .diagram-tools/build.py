"""Regenerate this repo's diagrams.

Usage:  python3 build.py
Phase content is extracted from the reference design itself, so editing the
document and re-running keeps the diagram honest.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import diagrams
import render
from extract import workflow_spec
from spec import FRAMING
from theme import base_css

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "CSW-CJIS-Reference-Design.md"
OUT = REPO / "assets"

spec = workflow_spec(MD, **FRAMING)
rows = max(len(p["actions"]) for p in spec["phases"])
h = int(96 + 22 + (300 + rows * 26) + 16 + 58 + 92)
body = diagrams.evidence_workflow(spec)
p = render.render(render.page(body, base_css(), diagrams.W, h),
                  OUT / "csw-evidence-workflow.png", diagrams.W, h)
print(f"  csw-evidence-workflow.png  {diagrams.W}x{h}  {os.path.getsize(p) // 1024} KB")


# The scope-architecture graphic lives in its own script, so run it from here too.
import os as _os
import runpy as _runpy

_runpy.run_path(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "build_tree.py"),
                run_name="__main__")

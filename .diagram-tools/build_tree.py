"""Render the scope-architecture graphic from the design's own scope tree.

    python3 .diagram-tools/build_tree.py

The tree is parsed out of the design document, so editing the document and
re-running is the way to change the picture.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import render
import tree as treemod
from theme import base_css

REPO = HERE.parent
MD = REPO / 'CSW-CJIS-Reference-Design.md'
ASSETS = REPO / "assets"
W = 1600

TREE = {'kicker': 'FBI CJIS Security Policy',
 'rail': ['Label queries keep scope membership current automatically',
          'Every in-scope workload resolves into exactly one scope',
          'The tree is the boundary an assessor will ask you to defend'],
 'sub': 'The scope hierarchy this design recommends, with label-driven membership so the '
        'boundary stays current as the estate changes.',
 'takeaway': 'Scope membership is <b>label-driven, not a static list</b>, so the boundary '
             'stays accurate as the estate changes. Scope accuracy is itself evidence in '
             'most assessments.',
 'takeaway_tag': 'Key Takeaway',
 'title': 'Scope Architecture',
 'title_tail': '&mdash; CJIS'}


def main() -> int:
    block = treemod.find_scope_tree(MD.read_text())
    if not block:
        print("no scope tree found in the design")
        return 1
    nodes = treemod.parse_tree(block)
    spec = dict(TREE, nodes=nodes, cols=1)
    h = int(treemod.HEAD_H + treemod.layout_height(nodes, 1) + treemod.FOOT_H)
    ASSETS.mkdir(exist_ok=True)
    out = ASSETS / "csw-scope-architecture.png"
    render.render(render.page(treemod.scope_tree(spec), base_css(), W, h), out, W, h)
    print(f"  {out.name}  {W}x{h}  {out.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

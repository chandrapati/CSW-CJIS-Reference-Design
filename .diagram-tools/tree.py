"""Scope-architecture diagram: renders a reference design's own ASCII scope
tree as a styled hierarchy.

This is the content that genuinely differs per framework - all 33 trees in the
estate are distinct - so it is the diagram worth having everywhere.
"""
from __future__ import annotations

import html
import re

from theme import PALETTE as P

GLYPHS = "│├└─┬┐┘ "
NODE = re.compile(r"^(?P<lead>[\s│]*)(?:(?P<branch>├──|└──)\s*)?(?P<label>.+?)\s*$")


def parse_tree(block: str) -> list[dict]:
    """Return [{depth, label, note}] from an ASCII tree."""
    out = []
    for raw in block.rstrip().splitlines():
        if not raw.strip():
            continue
        m = NODE.match(raw)
        if not m:
            continue
        lead = m.group("lead") or ""
        depth = 0 if m.group("branch") is None and not lead.strip() else len(lead) // 4 + 1
        if m.group("branch") is None and lead.strip():
            # continuation of a wrapped annotation; attach to the previous node
            if out:
                out[-1]["note"] = (out[-1]["note"] + " " + m.group("label").strip()).strip()
            continue
        label = m.group("label").strip()
        # split an inline annotation: two or more spaces, or a parenthetical tail
        note = ""
        parts = re.split(r"\s{2,}", label, maxsplit=1)
        if len(parts) == 2:
            label, note = parts[0].strip(), parts[1].strip()
        elif label.endswith(")") and "(" in label:
            i = label.rindex("(")
            if i > 0:
                label, note = label[:i].strip(), label[i:].strip()
        out.append({"depth": depth, "label": label, "note": note})
    return out


FENCE = re.compile(r"```[a-z]*\n(.*?)```", re.S)
BRANCH = re.compile(r"(├──|└──)")


def find_scope_tree(text: str) -> str | None:
    """Pick the fenced block that is actually a scope hierarchy.

    Several designs contain fenced procedures that happen to include tree
    glyphs, so a block only qualifies when most of its lines are tree rows
    hanging off a single unindented root.
    """
    best, best_score = None, 0.0
    for block in FENCE.findall(text):
        lines = [l for l in block.rstrip().splitlines() if l.strip()]
        if len(lines) < 3 or not BRANCH.search(block):
            continue
        branch_rows = sum(1 for l in lines if BRANCH.search(l))
        roots = [l for l in lines if l[:1] not in (" ", "│", "├", "└")]
        score = branch_rows / len(lines)
        if len(roots) != 1 or roots[0] != lines[0]:
            score -= 0.35          # a real tree has exactly one root, first
        if score > best_score:
            best, best_score = block, score
    return best if best_score >= 0.6 else None


def _esc(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<b>\1</b>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return s


ROW_H, ROW_GAP, INDENT = 27.0, 4.0, 26.0
HEAD_H = 96.0
FOOT_H = 92.0


def layout_height(nodes: list[dict], cols: int = 1) -> float:
    rows = -(-len(nodes) // cols)
    return rows * (ROW_H + ROW_GAP) + 36


def scope_tree(spec: dict) -> str:
    from diagrams import W, _footer, _header

    nodes = spec["nodes"]
    cols = spec.get("cols", 1)
    pad = 28
    per = -(-len(nodes) // cols)
    colw = (W - 2 * pad - (cols - 1) * 20) / cols

    tone = {
        0: (P["navy"], "#FFFFFF", P["navy"], 700, 12.5),
        1: (P["blue_wash"], P["navy"], P["blue_tint"], 600, 12.0),
        2: ("#FFFFFF", P["ink_soft"], P["blue_tint"], 500, 11.5),
        3: (P["blue_wash_2"], P["muted"], P["rule"], 400, 11.0),
    }

    def open_levels(idx: int) -> set[int]:
        """Depths whose branch continues past this row, so a vertical rail is
        drawn there - the same information the ASCII tree carries in its pipes."""
        here = nodes[idx]["depth"]
        out = set()
        for lvl in range(1, here):
            for nxt in nodes[idx + 1:]:
                if nxt["depth"] < lvl:
                    break
                if nxt["depth"] == lvl:
                    out.add(lvl)
                    break
        return out

    def row(idx: int, nd: dict, local: int) -> str:
        fill, fg, border, weight, fs = tone.get(min(nd["depth"], 3), tone[3])
        ml = nd["depth"] * INDENT
        rails = "".join(
            f'<span style="position:absolute;left:{lvl * INDENT - 14:.0f}px;top:0;'
            f'width:1.5px;height:{ROW_H + ROW_GAP:.0f}px;background:{P["rule"]}"></span>'
            for lvl in open_levels(idx)
        )
        elbow = "" if nd["depth"] == 0 else (
            f'<span style="position:absolute;left:{ml - 14:.0f}px;top:0;width:1.5px;'
            f'height:{ROW_H / 2:.0f}px;background:{P["blue_tint"]}"></span>'
            f'<span style="position:absolute;left:{ml - 14:.0f}px;top:{ROW_H / 2:.0f}px;'
            f'width:12px;height:1.5px;background:{P["blue_tint"]}"></span>')
        note = (f'<span style="color:{P["muted_blue"]};font-weight:400;font-size:10.2px;'
                f'margin-left:9px">{_esc(nd["note"])}</span>') if nd["note"] else ""
        return f"""
<div style="position:relative;height:{ROW_H:.0f}px;margin-bottom:{ROW_GAP:.0f}px">
  {rails}{elbow}
  <div style="position:absolute;left:{ml:.0f}px;top:0;height:{ROW_H:.0f}px;
       background:{fill};border:1px solid {border};border-radius:5px;
       display:inline-flex;align-items:center;padding:0 12px;white-space:nowrap">
    <span style="font-size:{fs}px;font-weight:{weight};color:{fg}">
      {_esc(nd['label'])}</span>{note}
  </div>
</div>"""

    columns = []
    for c in range(cols):
        lo, hi = c * per, (c + 1) * per
        inner = "".join(row(lo + i, n, i) for i, n in enumerate(nodes[lo:hi]))
        columns.append(f'<div style="width:{colw:.0f}px">{inner}</div>')

    body = (
        _header(spec["kicker"], spec["title"], spec["title_tail"], spec["sub"], pad)
        + f"""
<div style="padding:22px {pad}px 14px;display:flex;gap:20px;align-items:flex-start">
  {''.join(columns)}
</div>"""
        + _footer(spec["takeaway_tag"], spec["takeaway"], spec["rail"], pad)
    )
    return body

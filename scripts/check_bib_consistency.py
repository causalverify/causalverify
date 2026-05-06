#!/usr/bin/env python3
"""Sanity check for references.bib after patching."""
import re, sys
from collections import Counter
from pathlib import Path

ENTRY_RE = re.compile(r"@(?P<type>\w+)\s*\{\s*(?P<key>[^,\s]+)\s*,(?P<body>.*?)\n\}\s*", re.DOTALL)
FIELD_NAME_RE = re.compile(r"(\w+)\s*=\s*\{", re.DOTALL)

def _read_braced_value(s, start):
    """Read a brace-balanced value starting at index `start` (which must be '{').
    Returns (value, end_index) where end_index is the position AFTER the closing brace."""
    assert s[start] == "{"
    depth = 1
    i = start + 1
    while i < len(s) and depth > 0:
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    return s[start + 1: i - 1], i

def parse(text):
    out = []
    for m in ENTRY_RE.finditer(text):
        body = m.group("body")
        fields = {}
        i = 0
        while i < len(body):
            fm = FIELD_NAME_RE.search(body, i)
            if not fm:
                break
            name = fm.group(1).lower()
            brace_start = fm.end() - 1  # position of opening '{'
            value, after = _read_braced_value(body, brace_start)
            fields[name] = " ".join(value.split())
            i = after
        out.append({"type": m.group("type").lower(), "key": m.group("key"), "fields": fields})
    return out

def main(path):
    entries = parse(Path(path).read_text(encoding="utf-8"))
    print(f"Parsed {len(entries)} entries")
    fail = 0

    keys = [e["key"] for e in entries]
    dup = [k for k, c in Counter(keys).items() if c > 1]
    if dup: fail += 1; print(f"FAIL duplicate keys: {dup}")
    else: print("OK   no duplicate keys")

    dois = [(e["key"], e["fields"].get("doi", "").lower()) for e in entries if e["fields"].get("doi")]
    dup_d = [d for d, c in Counter(d for _, d in dois).items() if c > 1]
    if dup_d: fail += 1; print(f"FAIL duplicate DOIs: {dup_d}")
    else: print("OK   no duplicate DOIs")

    eps = [(e["key"], e["fields"].get("eprint","")) for e in entries if e["fields"].get("eprint")]
    dup_e = [p for p, c in Counter(p for _, p in eps).items() if c > 1]
    if dup_e: fail += 1; print(f"FAIL duplicate eprints: {dup_e}")
    else: print("OK   no duplicate arXiv eprints")

    for e in entries:
        url = e["fields"].get("url", "").lower()
        title = e["fields"].get("title", "").lower()
        if "uqzpkwvtyo" in url and "comprehensive" not in title and "end-to-end" not in title:
            fail += 1
            print(f"FAIL CauSciBench {e['key']}: URL=uQzPkWvTyo but title lacks 'Comprehensive'/'End-to-End'")
        if "corr2cause" in title or "infer causation from correlation" in title:
            bt = e["fields"].get("booktitle", "").lower()
            if "neurips" in bt or "neural information" in bt:
                fail += 1
                print(f"FAIL Corr2Cause {e['key']} still says NeurIPS in booktitle")
        if "alphacode" in title:
            au = e["fields"].get("author", "").lower()
            if "kushnareva" in au:
                fail += 1
                print(f"FAIL AlphaCode {e['key']} still has 'Kushnareva' (should be 'Kushman')")

    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "paper/latex/references.bib"))

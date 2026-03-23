#!/usr/bin/env python3
"""
Generate SEO-friendly, brandable domain candidates from a short product idea.

This script is intentionally simple and dependency-free so it can travel with
the skill pack and run in constrained environments.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
from collections import OrderedDict


STOPWORDS = {
    "a",
    "an",
    "and",
    "app",
    "application",
    "for",
    "of",
    "the",
    "to",
    "with",
    "tool",
    "tools",
    "platform",
    "agent",
    "assistant",
    "using",
    "that",
}

SUFFIXES = [
    "ai",
    "hq",
    "lab",
    "labs",
    "base",
    "flow",
    "forge",
    "pilot",
    "deck",
    "kit",
    "stack",
    "works",
    "cloud",
    "hub",
    "studio",
    "gen",
    "wise",
    "ly",
    "ify",
]

PREFIXES = ["get", "try", "use", "my", "go", "auto", "smart", "hyper"]

ROOT_EXPANSIONS = {
    "calculator": ["calc", "calcu", "calculator", "calcurator", "compute"],
    "calc": ["calc", "calcu", "calculator", "calcurator", "compute"],
    "taxes": ["tax", "taxes", "fiscal", "file", "return"],
    "writer": ["write", "writer", "draft", "scribe", "copy"],
    "writing": ["write", "writer", "draft", "scribe", "copy"],
    "notes": ["note", "memo", "brief", "recap", "minutes"],
    "note": ["note", "memo", "brief", "recap"],
    "meeting": ["meeting", "meet", "sync", "brief"],
    "tax": ["tax", "fiscal", "file", "return"],
    "resume": ["resume", "cv", "career", "hire"],
    "research": ["research", "intel", "insight", "signal", "scan"],
    "sales": ["sales", "deal", "revenue", "pipeline"],
    "image": ["image", "vision", "pixel", "render"],
    "video": ["video", "clip", "stream", "motion"],
    "voice": ["voice", "speak", "audio", "speech"],
    "email": ["email", "mail", "inbox", "reply"],
    "support": ["support", "help", "assist", "resolve"],
}


def tokenize(text: str) -> list[str]:
    parts = re.findall(r"[a-z0-9]+", text.lower())
    return [part for part in parts if part not in STOPWORDS]


def uniq(items):
    return list(OrderedDict.fromkeys(items))


def expand_root(token: str) -> list[str]:
    if token in ROOT_EXPANSIONS:
        return ROOT_EXPANSIONS[token]

    stems = [token]
    if token.endswith("ing") and len(token) > 5:
        stems.append(token[:-3])
    if token.endswith("er") and len(token) > 4:
        stems.append(token[:-2])
    if token.endswith("or") and len(token) > 4:
        stems.append(token[:-2])
    if token.endswith("s") and len(token) > 4:
        stems.append(token[:-1])
    if token.endswith("es") and len(token) > 5:
        stems.append(token[:-2])
    if len(token) > 6:
        stems.append(token[:4])
        stems.append(token[:5])
    return uniq([stem for stem in stems if 3 <= len(stem) <= 14])


def build_roots(tokens: list[str]) -> list[str]:
    roots: list[str] = []
    for token in tokens:
        roots.extend(expand_root(token))
    return uniq([root for root in roots if re.fullmatch(r"[a-z0-9]+", root)])


def score_name(name: str, source_roots: set[str]) -> int:
    score = 0
    length = len(name)
    if 6 <= length <= 10:
        score += 6
    elif 11 <= length <= 14:
        score += 3
    elif 5 <= length <= 18:
        score += 2
    else:
        score -= 2

    root_hits = 0
    for root in source_roots:
        if root in name:
            root_hits += 1
    score += min(root_hits, 2) * 2

    if length > 12:
        score -= 3
    if length > 15:
        score -= 4

    if any(name.endswith(suffix) for suffix in SUFFIXES):
        score += 2
    if any(name.startswith(prefix) for prefix in PREFIXES):
        score += 1
    if re.search(r"(.)\1\1", name):
        score -= 2
    if len(re.findall(r"[aeiou]", name)) == 0:
        score -= 1
    return score


def build_names(roots: list[str]) -> list[str]:
    names: list[str] = []
    short_roots = [root for root in roots if len(root) <= 8][:12]

    for root in roots:
        names.append(root)
        for suffix in SUFFIXES:
            names.append(f"{root}{suffix}")
        for prefix in PREFIXES:
            names.append(f"{prefix}{root}")

    for left, right in itertools.permutations(short_roots, 2):
        if left == right:
            continue
        names.append(f"{left}{right}")
        names.append(f"{right}{left}")
        if len(right) >= 4:
            names.append(f"{left}{right[:4]}")
        if len(left) >= 4:
            names.append(f"{left[:4]}{right}")
        names.append(f"{left[:3]}{right[:4]}")
        for suffix in ("ai", "lab", "pilot", "flow", "forge"):
            names.append(f"{left}{right}{suffix}")

    cleaned = []
    for name in uniq(names):
        if not re.fullmatch(r"[a-z0-9]+", name):
            continue
        if len(name) < 4 or len(name) > 22:
            continue
        cleaned.append(name)
    return cleaned


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("idea", help="Product direction, keyword, or one-line concept")
    parser.add_argument("--tlds", nargs="+", default=["com", "ai", "io", "app"])
    parser.add_argument("--limit", type=int, default=60)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    tokens = tokenize(args.idea)
    roots = build_roots(tokens)
    names = build_names(roots)
    scored = sorted(
        names,
        key=lambda name: (-score_name(name, set(roots)), len(name), name),
    )

    domains = []
    for name in scored[: args.limit]:
        domains.extend(f"{name}.{tld}" for tld in args.tlds)

    result = {
        "idea": args.idea,
        "tokens": tokens,
        "roots": roots,
        "domains": uniq(domains)[: args.limit],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return

    print(f"# idea: {args.idea}")
    print("# roots:", ", ".join(result["roots"]))
    for domain in result["domains"]:
        print(domain)


if __name__ == "__main__":
    main()

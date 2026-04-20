#!/usr/bin/env python3
"""
bias_scan.py  --  et_tu_brute self-scan tool

A minimal scanner that searches a codebase for default-vocabulary tokens
that should not appear given a stated target vocabulary.  Part of the
et_tu_brute skill in Dstack.

USAGE
    python bias_scan.py <directory> --target <profile>

PROFILES
    sept       -- septenary codebase; flags float/matmul/embedding tokens
    lattice    -- lattice-walk codebase; flags matrix-multiplication tokens
    cag        -- cache-augmented-generation codebase; flags RAG/embedding tokens
    grounded   -- grounded-interface codebase; flags binary-framing tokens
    custom     -- pass --bias-file with one token per line

The scanner is a DISCIPLINE AID, not a static analyzer.  A clean scan does
not mean the code is correct.  A flagged scan does not mean the code is
wrong.  Both require human judgement.  The purpose is to surface drift
points for review, not to replace review.

EXAMPLE
    python bias_scan.py ./src --target sept
    python bias_scan.py ./src --target custom --bias-file my_biases.txt

LICENSE
    Part of DustyBasic/dstack.  See repository README for rights notice.
    All rights reserved; source-available for review and evaluation.
"""

import argparse
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Bias profiles -- extend by adding entries here or by loading via --bias-file
# ---------------------------------------------------------------------------

PROFILES = {
    "sept": {
        "description": "Hexadecimal / LUT-arithmetic codebase -- default vocabulary to flag is binary float/matrix.",
        "bias_tokens": [
            # float arithmetic defaults
            r"\bfloat32\b", r"\bfloat64\b", r"\bnp\.float", r"\btorch\.float",
            r"\bmath\.sqrt\b", r"\bmath\.sin\b", r"\bmath\.cos\b", r"\bmath\.exp\b",
            # matrix ops
            r"\bmatmul\b", r"\beinsum\b", r"\bdot\b(?!_sept)", r"@(?=\s*[A-Z][a-zA-Z_])",
            # tensor libraries
            r"import torch\b", r"import numpy\b", r"\btf\.keras\b", r"\btensor\b",
            # embedding-based retrieval
            r"\bcosine_similarity\b", r"\bembedding\b", r"\bvector_store\b",
            # binary collapse
            r"\bif .+ else\b(?!.*(sept|seven|SEPT|SEVEN))",  # only flag naked binary
        ],
        "suggestion": "Consider lookup-table (LUT) operations, sept-native arithmetic, role-aware slot bands.",
    },
    "lattice": {
        "description": "Lattice-walk codebase -- default to flag is matrix multiplication.",
        "bias_tokens": [
            r"\bmatmul\b", r"\beinsum\b", r"@(?=\s*[A-Z][a-zA-Z_])",
            r"\btorch\.matmul\b", r"\bnp\.dot\b",
            r"\bsoftmax\b(?!_sept)", r"\bcosine_similarity\b",
        ],
        "suggestion": "Consider graph/lattice traversal, page-walk retrieval, structured node-to-node hops.",
    },
    "cag": {
        "description": "Cache-augmented-generation codebase -- default to flag is RAG / embedding retrieval.",
        "bias_tokens": [
            r"\bembedding\b", r"\bcosine_similarity\b", r"\bchromadb\b", r"\bpinecone\b",
            r"\bweaviate\b", r"\bfaiss\b", r"\bchunk\b", r"\bvector_search\b",
            r"\bretrieve_top_k\b",
        ],
        "suggestion": "Consider preloaded context, prompt caching, structured-substrate caching, tier-promote/demote.",
    },
    "grounded": {
        "description": "Grounded-interface codebase -- default to flag is binary / peer-neutral framing.",
        "bias_tokens": [
            # binary collapse patterns
            r"\bis_valid\s*=\s*(True|False)\b",
            r"\baccept\s*or\s*reject\b",
            # performance-over-grounding markers
            r"\bupgrade\b(?!.*phase)", r"\bmigration\b(?!.*phase)",
            # power-asymmetry-blind markers
            r"\buser must\b", r"\brequired\b(?!.*reversible)",
        ],
        "suggestion": "Consider phased transitions, multi-channel affordances, explicit power-asymmetry calibration.",
    },
}


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def load_custom_biases(path):
    """One regex-or-token per line; blank lines and # comments ignored."""
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]


def scan_file(path, bias_patterns):
    """Scan a single file.  Returns list of (line_number, line_text, matched_pattern)."""
    hits = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                for pattern in bias_patterns:
                    if re.search(pattern, line):
                        hits.append((i, line.rstrip(), pattern))
                        break  # one hit per line is enough signal
    except (OSError, UnicodeDecodeError):
        pass
    return hits


def scan_directory(root, bias_patterns, extensions):
    """Recursively scan a directory.  Returns dict of {path: [hits]}."""
    results = {}
    for dirpath, dirnames, filenames in os.walk(root):
        # skip common noise
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}]
        for fn in filenames:
            if extensions and not any(fn.endswith(ext) for ext in extensions):
                continue
            path = os.path.join(dirpath, fn)
            hits = scan_file(path, bias_patterns)
            if hits:
                results[path] = hits
    return results


def format_results(results, root, suggestion):
    if not results:
        return "CLEAN SCAN\n\nNo default-vocabulary tokens found under the selected bias profile.\n\nNote: a clean scan is a necessary condition, not a sufficient one.  Drift\ncan live below the token layer.  Review the code against the target-\nvocabulary map regardless.\n"

    lines = []
    total = 0
    lines.append(f"DRIFT SCAN RESULTS  --  root: {root}")
    lines.append("=" * 72)
    for path in sorted(results.keys()):
        rel = os.path.relpath(path, root)
        hits = results[path]
        total += len(hits)
        lines.append(f"\n{rel}")
        for ln, text, pat in hits:
            lines.append(f"  {ln:5d}: {text}")
            lines.append(f"         ^ matched: {pat}")
    lines.append("\n" + "=" * 72)
    lines.append(f"Total drift candidates: {total} in {len(results)} file(s)")
    if suggestion:
        lines.append(f"\nSuggestion for target vocabulary:")
        lines.append(f"  {suggestion}")
    lines.append("\nReminder: this is a DISCIPLINE AID, not a verdict.")
    lines.append("Each hit is a candidate for review, not a confirmed bug.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="et_tu_brute self-scan tool -- surface default-vocabulary drift candidates.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("directory", help="Directory to scan.")
    parser.add_argument("--target", choices=list(PROFILES.keys()) + ["custom"], required=True,
                        help="Target-vocabulary profile.  'custom' requires --bias-file.")
    parser.add_argument("--bias-file", help="Path to a file of custom bias tokens (one regex per line).")
    parser.add_argument("--extensions", default=".py,.js,.ts,.jsx,.tsx,.ps1,.sh,.md",
                        help="Comma-separated file extensions to scan.  Default: common source types.")
    args = parser.parse_args()

    root = Path(args.directory).resolve()
    if not root.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        sys.exit(2)

    if args.target == "custom":
        if not args.bias_file:
            print("error: --target custom requires --bias-file", file=sys.stderr)
            sys.exit(2)
        bias_patterns = load_custom_biases(args.bias_file)
        suggestion = None
    else:
        profile = PROFILES[args.target]
        bias_patterns = profile["bias_tokens"]
        suggestion = profile["suggestion"]
        print(f"Profile: {args.target}  --  {profile['description']}\n")

    extensions = [e.strip() if e.strip().startswith(".") else "." + e.strip()
                  for e in args.extensions.split(",") if e.strip()]

    results = scan_directory(str(root), bias_patterns, extensions)
    print(format_results(results, str(root), suggestion))
    sys.exit(1 if results else 0)


if __name__ == "__main__":
    main()

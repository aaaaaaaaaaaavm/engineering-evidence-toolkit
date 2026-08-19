# Engineering Evidence Toolkit

[![CI](https://github.com/aaaaaaaaaaaavm/engineering-evidence-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/aaaaaaaaaaaavm/engineering-evidence-toolkit/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](pyproject.toml)
[![Scope: consistency only](https://img.shields.io/badge/scope-consistency%2C%20not%20validation-red.svg)](docs/VALIDATION.md)

A dependency-free command-line check for whether computational results, Markdown links and
declared artifacts still agree with their recorded sources.

**Boundary: a pass establishes consistency and file identity. It does not validate the
physics, certify an analysis or turn a numerical result into a measurement.**

## Why this exists

VOLLEY accumulated the ordinary failure modes of a long numerical project: a PDF older than
its source, copied JSON that no script regenerated, figures from a superseded operating point
and companion repositories that could drift from the engineering record. The project-specific
checks are retained under `reference/volley/`. This package extracts the smaller part that is
reusable elsewhere.

The chain it checks is deliberately narrow:

```text
source files -> numerical JSON -> report links -> declared artifact hashes
```

A green result means that declared chain still holds. It says nothing about whether the first
equation in the chain was right.

## Run the sample

```bash
python -m pip install -e .
engtrace examples/sample_project/engtrace.json
```

The configuration names JSON and Markdown patterns, then declares artifacts with SHA-256 values
and their source files. A declared pattern that matches nothing is a failure; otherwise a
misspelled pattern could make a check pass by checking no files.

## Verify it

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```

The tests include deliberately changed artifacts, broken links, non-finite JSON, missing source
files and empty patterns. The failure path is exercised rather than described.

## Configuration

```json
{
  "json": ["results/*.json"],
  "markdown": ["*.md"],
  "artifacts": [
    {
      "path": "report.md",
      "sha256": "<sha256>",
      "sources": ["source.txt", "results/output.json"]
    }
  ]
}
```

Paths are relative to the directory containing `engtrace.json`. External URLs and `mailto:`
links are outside this check.

## Repository layout

- `src/engtrace/` — the dependency-free checker and command-line entry point;
- `examples/sample_project/` — a self-contained non-VOLLEY example;
- `tests/` — clean and deliberately broken evidence chains;
- `reference/volley/` — original utilities and fixtures from VOLLEY commit `aa22a06`. **A dated snapshot, not a mirror.** VOLLEY has since changed its operating point and its architecture; the figures inside this directory are what that commit held and are not corrected here, because a fixture that tracks its source is not a fixture;
- `docs/` — validation boundary, provenance, decisions and roadmap.

See [summary](SUMMARY.md), [validation](docs/VALIDATION.md),
[provenance](docs/PROVENANCE.md), [decision log](docs/DECISION_LOG.md), and
[open problems](OPEN_PROBLEMS.md).

## Licence

**Apache-2.0** — full text in [`LICENSE`](LICENSE), scope note in [`NOTICE`](NOTICE).

Apache-2.0 is used here and **not** in the sibling VOLLEY design repositories, because this
repository contains no part of the deployer design: its original code is `src/engtrace/`, and the
copies under `reference/volley/` are repository tooling rather than the motor model or the
geometry. **Apache-2.0 §3 grants patent rights**, so it is applied only where no invention is
disclosed.

**Not retroactive:** snapshots taken before this change remain available under the MIT licence
they carried at the time, retained at [`LICENSE-MIT-superseded`](LICENSE-MIT-superseded).

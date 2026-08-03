# Contributing

A checker is only useful if it can fail. A change to `engtrace` should include a clean case
and the smallest broken case that proves the new guard is live. Do not add a check because its
name sounds rigorous; state the drift it detects and what a pass does not establish.

Commit subjects should describe the failure mode or consequence. “Make empty evidence patterns
fail closed” is useful later; “update core.py” is not.

The files under `reference/volley/` are retained from VOLLEY commit `aa22a06`. Change them only
by selecting a later reviewed VOLLEY commit, copying its exact blobs and regenerating
`SOURCE_MANIFEST.json`.

Before proposing a release, run:

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```

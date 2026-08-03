# Engineering Evidence Toolkit

A small command-line tool for checking whether computational engineering results,
Markdown links and declared artifacts still agree with their recorded sources.

I built the first versions of these checks after stale figures, duplicated JSON and copied
companion repositories drifted away from VOLLEY's calculations. This repository extracts the
reusable part and includes a self-contained sample that is not coupled to VOLLEY.

> **Boundary:** a passing traceability check establishes consistency and file identity. It
> does not validate the physics, certify an analysis, or turn a numerical result into a measurement.

## Run the example

```bash
python -m pip install -e .
engtrace examples/sample_project/engtrace.json
```

The configuration declares JSON files to inspect, Markdown links to resolve, and artifacts
whose SHA-256 values must match. The tests include deliberately changed artifacts and broken
links so a failure path is exercised, not merely described.

## Verify the repository

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```

The original VOLLEY utilities and corrected result fixtures remain under
`reference/volley/`. They are evidence of where the tool came from; they are not the public API.

See [summary](SUMMARY.md), [validation](docs/VALIDATION.md),
[provenance](docs/PROVENANCE.md), [decision log](docs/DECISION_LOG.md), and
[open problems](OPEN_PROBLEMS.md).

## License

MIT.

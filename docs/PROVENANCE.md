# Provenance

I extracted the reusable checks from VOLLEY's artifact, link, baseline and companion-export
utilities at commit
[`aa22a06`](https://github.com/aaaaaaaaaaaavm/VOLLEY/commit/aa22a069e5d2b4e4c58428904fedeafbcf594e46).
Every retained file is byte-identical to its blob in that commit. `SOURCE_MANIFEST.json`
records per-file SHA-256 values and an aggregate snapshot hash as a second identity check.

The installable `engtrace` package is independent of the VOLLEY directory layout. The sample
project and its failure tests establish that boundary.

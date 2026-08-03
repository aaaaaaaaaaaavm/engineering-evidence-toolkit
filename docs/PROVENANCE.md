# Provenance

I extracted the reusable checks from VOLLEY's artifact, link, baseline and companion-export
utilities. The reference files come from the reviewed 2026-08-03 working-tree snapshot derived
from `d82877a`. Because those corrections were not yet a source commit, the snapshot is defined
by `SOURCE_MANIFEST.json` and its aggregate SHA-256 value.

The installable `engtrace` package is independent of the VOLLEY directory layout. The sample
project and its failure tests establish that boundary.

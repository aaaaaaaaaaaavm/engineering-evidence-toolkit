# Change log / audit record

I record changes here by cause and consequence. A traceability tool that cannot account for
its own origin would be a contradiction.

## 0.1.1 — make an empty check fail closed

- Replaced the provisional working-tree provenance with VOLLEY commit `aa22a06`. Every retained
  source file was checked byte-for-byte against that commit before the manifest moved.
- Made declared JSON and Markdown patterns fail when they match no files. A misspelled pattern
  previously produced a clean result by checking nothing.
- Added explicit tests for non-finite JSON, missing source files and empty patterns.
- Expanded the implementation comments so each rejection path states which drift it prevents.
- Kept the central boundary unchanged: consistency is not validation.

## 0.1.0 — initial public baseline

- Extracted reusable artifact, numerical-result and link checks from VOLLEY.
- Added a standalone interface, a non-VOLLEY sample and deliberate failure-path tests.
- Retained the original project-specific utilities as provenance, not as the package API.

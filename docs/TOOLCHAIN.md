# Toolchain record

The installable package uses Python 3.11 or newer and the standard library. Python is
distributed under the PSF License. No external solver is invoked by `engtrace`.

The retained VOLLEY reference utilities use Git commit metadata, NumPy, Matplotlib and
Magpylib in their original project context. Their exact copied-file hashes are recorded in
`SOURCE_MANIFEST.json`; they are not executed by this package's CI workflow.

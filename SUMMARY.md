# Engineering Evidence Toolkit: one page

Computational engineering produces chains: source → result JSON → figure → report → PDF.
A fresh clone can preserve every file while hiding that the chain has drifted.

`engtrace` checks three narrower, defensible properties: JSON numbers remain finite, relative
Markdown links resolve, and declared artifacts retain their recorded SHA-256 values and source
files. The included tests prove that changed artifacts and broken links fail.

A pass means the declared files agree. It does not mean the underlying engineering is correct.

# Engineering Evidence Toolkit: one page

Computational engineering produces chains:

```text
source -> result JSON -> figure or report -> built artifact
```

A fresh clone can preserve every file while hiding that the chain drifted before the commit.
`engtrace` checks five narrower, defensible conditions:

1. declared JSON and Markdown patterns match at least one file;
2. JSON numbers are finite;
3. relative Markdown links resolve;
4. declared artifacts retain their recorded SHA-256 values;
5. every declared source file exists.

The tests deliberately change an artifact, break a link, insert NaN, remove a source and
misspell a pattern. Each condition must fail. A checker demonstrated only against clean files
has not demonstrated the part that matters.

A pass means the declared files agree. It does not mean the equations, models or measurements
behind them are correct. The package is dependency-free; the VOLLEY utilities that taught
these failure modes remain retained as provenance, not as public commands.

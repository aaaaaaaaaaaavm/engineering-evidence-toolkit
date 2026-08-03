# Decision log

## D1: hash artifacts rather than trust timestamps

Filesystem modification times change during cloning and archive extraction. The public
interface therefore verifies declared SHA-256 values. The original VOLLEY freshness checker
remains in the reference record because Git ordering solves a different project-specific problem.

## D2: make failure behavior part of the test suite

A checker demonstrated only against clean files is weak evidence. The tests deliberately alter
an artifact, break a link, insert a non-finite number and remove a source, then require each
condition to fail.

## D3: make an empty declared pattern fail closed

A misspelled glob previously selected no files and returned no failures. That is a false pass.
A declared JSON or Markdown pattern now has to match at least one file.

## D4: keep consistency separate from validation

Hashes, links and finite numbers say whether the declared chain still agrees. They do not say
whether the first model in the chain is physically right. That boundary appears in the CLI
documentation, README and validation record rather than in a footnote.

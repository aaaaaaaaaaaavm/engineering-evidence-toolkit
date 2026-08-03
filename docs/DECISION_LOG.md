# Decision log

## D1: hash artifacts rather than trust timestamps

Filesystem modification times change during cloning and archive extraction. The public
interface therefore verifies declared SHA-256 values. The original VOLLEY freshness checker
remains in the reference record because Git ordering solves a different project-specific problem.

## D2: make failure behavior part of the test suite

A checker demonstrated only against clean files is weak evidence. The tests deliberately alter
an artifact and break a link, then require both conditions to fail.

# Validation record

| Check | Declared behavior | Test |
|---|---|---|
| Finite JSON | reject NaN and infinity | deliberate NaN fixture |
| Artifact identity | reject a file whose SHA-256 changed | deliberately modified report |
| Relative links | reject a missing local target | deliberately broken link |
| Source presence | reject a declared source that is absent | deliberately missing source |
| Pattern coverage | reject a declared pattern that selects no files | deliberately empty glob |
| Valid sample | return no failures | independent temporary repository |

These are software behavior tests. They do not validate any engineering result stored in a
checked repository.

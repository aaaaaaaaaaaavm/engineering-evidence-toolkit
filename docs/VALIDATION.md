# Validation record

| Check | Declared behavior | Test |
|---|---|---|
| Finite JSON | reject NaN and infinity | unit test through the shared walker |
| Artifact identity | reject a file whose SHA-256 changed | deliberately modified report |
| Relative links | reject a missing local target | deliberately broken link |
| Valid sample | return no failures | independent temporary repository |

These are software behavior tests. They do not validate any engineering result stored in a
checked repository.

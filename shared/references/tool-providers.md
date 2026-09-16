# Capability-oriented provider selection

Use this guide only when deterministic tooling could materially improve the requested analysis. First inspect project configuration and available commands; a repository-configured provider takes precedence over this candidate list.

| Capability | Language-independent fallback | Ecosystem candidates to consider when already configured/available |
|---|---|---|
| History, churn, ownership, temporal coupling | Git helper in this suite | Code Maat for broader behavioral analyses and architectural mappings |
| Static dependencies | imports/configuration via targeted `rg` and source inspection | Python import-linter; JS/TS dependency-cruiser or Madge; Java `jdeps`/ArchUnit; Go `go list`; Rust `cargo metadata`; .NET build/project graph; C/C++ clang tooling |
| Complexity | size/control-flow inspection; do not fabricate scores | repository linters or Radon, PMD, golangci-lint, Clippy extensions, lizard/clang tooling as appropriate |
| Test coverage | test/config inspection; report coverage as unavailable | coverage.py/pytest-cov, Jest/Vitest coverage, JaCoCo, `go test -cover`, cargo-llvm-cov, Coverlet, llvm-cov |
| Architecture rules | source/config inspection | import-linter, dependency-cruiser, ArchUnit, NetArchTest or repository-native equivalents |

Candidate names are not automatic recommendations. Check maintenance, license, machine-readable output, offline/private-repository suitability, runtime cost, and exact metric semantics at time of use. Do not install silently.

Online/SaaS providers may transmit source, history, metadata, or results. Identify that explicitly and prefer a mature local open-source option when practical.

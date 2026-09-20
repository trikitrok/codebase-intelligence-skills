# Code Maat

[Code Maat](https://github.com/adamtornhill/code-maat) is Adam Tornhill’s command-line tool for mining and analyzing version-control history. It can provide historical signals that are not visible in a single snapshot of source code, including revisions, churn, authorship, and logical or change coupling.

The `codebase-hotspots` and `codebase-coupling` skills can use Code Maat as an optional local provider when it is explicitly available. The repository also has a Git fallback, so Code Maat is not required for either skill to work.

## Why install it?

Code Maat can be useful when you want provider-defined behavioral history metrics, especially for:

- identifying files with high historical churn;
- understanding how often files or modules change together;
- finding possible hidden dependencies or expensive change patterns;
- complementing source-level architecture and maintenance analysis.

These are investigation signals, not automatic diagnoses. A high-churn file can be healthy, and change coupling can be intentional—for example, production code changing alongside its tests.

The Code Maat project notes that these analyses have since evolved into CodeScene, but Code Maat remains a local command-line tool and is useful when you want a directly runnable, offline provider.

## Installation options

Use the official [Code Maat repository](https://github.com/adamtornhill/code-maat) and its [release page](https://github.com/adamtornhill/code-maat/releases) as the source of truth for current versions.

### Pre-built executable JAR

The simplest option is to download the latest standalone JAR from the releases page. You need a JVM; the project documentation specifies Java 8 or later for running the standalone JAR.

Verify the download with:

```bash
java -jar /path/to/code-maat-<version>-standalone.jar
```

This should print Code Maat’s command-line usage. You can create a local shell alias if you use it frequently:

```bash
alias maat='java -jar /path/to/code-maat-<version>-standalone.jar'
```

### Build from source

The official repository describes building Code Maat with Leiningen:

```bash
git clone https://github.com/adamtornhill/code-maat.git
cd code-maat
lein uberjar
```

This produces a standalone JAR under `target/`. Run that JAR with Java as shown above.

### Docker

The official repository also documents building a Docker image:

```bash
git clone https://github.com/adamtornhill/code-maat.git
cd code-maat
docker build -t code-maat-app .
```

On Apple Silicon, the upstream instructions note that the Dockerfile may need its base image changed from `clojure:alpine` to `clojure:latest` if the build fails.

## Preparing history input

Code Maat analyzes version-control log data rather than directly scanning the current source tree. The upstream README documents Git log formats, including a newer `git2` format, and recommends limiting the history window with a date such as `--after=YYYY-MM-DD`.

It is also useful to exclude vendor, generated, or other noisy paths when generating history input. On Windows, the upstream documentation recommends using Git Bash because the examples depend on Unix-style command-line behavior and line endings.

## Using Code Maat with this repository

The local history helper supports explicit provider selection and command prefixes. Its command-line options include:

```bash
python3 shared/scripts/history_candidates.py hotspots --provider auto
python3 shared/scripts/history_candidates.py hotspots --provider code-maat
```

The automatic mode prefers valid Code Maat input or an explicitly configured Code Maat command, then an exact `code-maat` executable on `PATH`, and finally falls back to Git.

If the JAR is not exposed as a `code-maat` executable, the helper accepts a JSON command prefix, for example:

```bash
python3 shared/scripts/history_candidates.py hotspots \
  --provider code-maat \
  --code-maat-command '["java", "-jar", "/path/to/code-maat-<version>-standalone.jar"]' \
  --code-maat-version '<version>'
```

The repository’s integration expects the configured command to support the helper’s provider interface. Verify the current adapter contract in [`SPEC-V3.md`](../SPEC-V3.md) and [`history_candidates.py`](../shared/scripts/history_candidates.py) before relying on a custom wrapper or direct JAR command.

## Data handling and safety

- Code Maat runs locally against version-control data you provide.
- Installing it is optional and should be an explicit user decision.
- Do not upload private repository history or source to an external service.
- Limit the history window and exclude noisy paths when that improves signal quality.
- Treat Code Maat metrics as provider-defined observations; inspect the source and tests before classifying a hotspot or coupling as a problem.

For the skill that investigates hotspot candidates, see the [Codebase Hotspots guide](codebase-hotspots.md).

# Installing `codebase-intelligence` in Codex

Install `codebase-intelligence` once from a personal Codex marketplace, then
use its skills in multiple existing or legacy repositories. The repositories
that use the plugin do not need to become plugins or marketplaces themselves.

## Prerequisites

- Codex with plugin support enabled.
- Network access to GitHub.
- Read access to the plugin repository:
  <https://github.com/trikitrok/codebase-intelligence-skills>

## 1. Create the personal marketplace

The personal marketplace is a user-level catalog at
`~/.agents/plugins/marketplace.json`. Create the directory and open the file in
your editor:

```bash
mkdir -p ~/.agents/plugins
$EDITOR ~/.agents/plugins/marketplace.json
```

Paste this content into the file and save it:

```json
{
  "name": "personal",
  "interface": {
    "displayName": "Personal"
  },
  "plugins": [
    {
      "name": "codebase-intelligence",
      "source": {
        "source": "url",
        "url": "https://github.com/trikitrok/codebase-intelligence-skills.git",
        "ref": "v0.2.0"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Developer Tools"
    }
  ]
}
```

The release tag pins the marketplace to a published semantic version. When a
new release is available, replace `v0.2.0` with the new release tag, such as
`v0.3.0`, and then refresh the marketplace.

## 2. Install the plugin

Run:

```bash
codex plugin add codebase-intelligence@personal
```

The personal marketplace is discovered automatically from
`~/.agents/plugins/marketplace.json`; it does not need to be added as a
repository marketplace.

## 3. Verify the installation

Run:

```bash
codex plugin list
```

The expected result includes an entry showing the installed plugin and version,
similar to:

```text
codebase-intelligence@personal  installed, enabled  0.2.0
```

Start a new Codex thread after installation so the plugin's skills are loaded.

## Using the plugin in legacy projects

No plugin or marketplace files are required in the legacy project. Open Codex
in any trusted repository and invoke the relevant `codebase-intelligence` skill
when needed.

In particular, do not add any of these to a legacy project just to use the
plugin:

- `.agents/plugins/marketplace.json`
- `.claude-plugin/marketplace.json`
- a `[marketplaces.*]` entry pointing at the project directory
- `codex plugin marketplace add` with the project directory as its source

Those files or registrations make Codex treat that project as a marketplace
source. The marketplace belongs under the user-level `~/.agents/plugins/`
directory instead.

## Updating to a newer release

Check the version currently installed by Codex:

```bash
codex plugin list
```

To move from `v0.2.0` to a newer release:

1. Edit `~/.agents/plugins/marketplace.json` and change the plugin source
   reference to the new release tag, for example `v0.3.0`.
2. Refresh the configured personal marketplace:

```bash
codex plugin marketplace upgrade personal
```

3. If the installed plugin does not refresh automatically, reinstall it from
   the same personal marketplace:

```bash
codex plugin add codebase-intelligence@personal
```

Do not point a legacy project at a new marketplace just to update the plugin.

After reinstalling:

1. Confirm the installed version with `codex plugin list`.
2. Start a new Codex thread so the updated skills are loaded.

If the plugin source is changed locally during development, publish or push a
release tag to GitHub first. Then update the personal marketplace reference as
described above.

## Troubleshooting

Check the configured marketplaces if Codex appears to discover the wrong
source:

```bash
codex plugin marketplace list
```

The personal marketplace should point to a path under the user directory, such
as `/home/<user>/.agents/plugins/marketplace.json`, not to a legacy project.

If a legacy project is being listed as a marketplace, remove its project-local
`.agents/plugins/marketplace.json` or `.claude-plugin/marketplace.json`, and
remove the corresponding `[marketplaces.<name>]` entry from
`~/.codex/config.toml`. A project-level plugin enablement entry can remain if
you need it, but it should refer to the personal marketplace:

```toml
[plugins."codebase-intelligence@personal"]
enabled = true
```

## Official documentation

- [OpenAI plugin management](https://developers.openai.com/docs/enterprise/plugin-management)
- [OpenAI plugin architecture](https://developers.openai.com/plugins/concepts/plugins)

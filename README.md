# arcsite-claude-plugins

Claude Code plugins for ArcSite staff. This public repository is the plugin
marketplace: installing needs no GitHub account.

| Plugin | What it does |
| --- | --- |
| [`arcsite-ks-update`](plugins/arcsite-ks-update) | Update Knowledge Studio knowledge from Claude Code: find the layer, preview and save a draft, run Replay, and hand publishing back to the Console. Connects to the **test** environment only. |

## Install (once)

You need Claude Code (CLI, the desktop app's Code tab, or VS Code).

1. Add the marketplace and install the plugin:

   ```
   /plugin marketplace add Arctuition/arcsite-claude-plugins
   /plugin install arcsite-ks-update@arcsite
   ```

2. Turn on updates: run `/plugin`, open **Marketplaces**, pick `arcsite`, and
   choose **Enable auto-update**. Claude Code does not update a marketplace
   like this one on its own until you do.

3. Connect: run `/mcp`, pick `plugin:arcsite-ks-update:ks-test`, choose
   **Authenticate**. A browser opens ArcSite's sign-in page: sign in with
   your ArcSite Google Workspace account and click **Allow**. Your account
   needs the Admin Console's Knowledge Studio authoring role
   (`SYSTEM_CONTENT`); without it the page tells you so.

That's it — no token to copy or renew. Claude Code keeps the credential and
refreshes it; if it ever lapses, `/mcp` → Authenticate again.

Organisation admins can pre-install for everyone with managed settings:

```json
{
  "extraKnownMarketplaces": {
    "arcsite": {
      "source": { "source": "github", "repo": "Arctuition/arcsite-claude-plugins" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": { "arcsite-ks-update@arcsite": true }
}
```

## Use

Ask in plain words, naming the company or layer and what to change:

> Update the Springfield branch configuration to prefer the tightener the
> customer just confirmed. Only this branch. Save the draft and check it
> against the earlier orders.

Say "save the draft" when you want the change written; otherwise the agent
only analyses and previews. The agent never publishes: it ends with a release
plan and Console links, and you publish in the Console, layer by layer in the
plan's order.

A Rule at `review_required` does not stop an order: the order completes as
"Ready with warnings". If someone must sign off before the order can go
ahead, ask for a required Workflow task instead.

## Fewer approval prompts (optional)

Claude Code asks before each tool call unless you allow it. To allow the
read-only tools, add this to your `~/.claude/settings.json` (a plugin cannot
ship permissions itself). `ks_apply` and `ks_replay` are deliberately left out
so saving a draft and queueing Replay still ask.

```json
{
  "permissions": {
    "allow": [
      "mcp__plugin_arcsite-ks-update_ks-test__ks_find_target",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_read_layer",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_read_object",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_preview",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_applies"
    ]
  }
}
```

## Troubleshooting

| You see | Do |
| --- | --- |
| The agent says the contract version does not match | Update the plugin: `/plugin` → **Installed** → `arcsite-ks-update` → **Update now**, or `claude plugin update arcsite-ks-update@arcsite` in a shell. Then restart Claude Code |
| Tools fail with 401 / "not authenticated" | `/mcp` → `ks-test` → Authenticate |
| "This account cannot connect" on the sign-in page | Ask an Admin Console administrator for the Knowledge Studio authoring role |
| `layer_not_editable` | Trade and Core layers are changed by the Knowledge Studio team, not through these tools |

## Pilot log

During the pilot, keep one row per task:

| Field | Example |
| --- | --- |
| Date, who | 2026-10-02, … |
| Request (one line) | Springfield prefers the new tightener |
| Target layer | `org-…-fence` (organization) |
| Time from request to reviewable draft | 12 min |
| Times you had to step in, and why | 1 — two companies matched the name |
| Preview rounds | 2 |
| Replay | 5 cases, 1 changed, as expected |
| Out-of-scope changes the agent proposed | none |
| Rework after publishing | none |

## Releasing a change (maintainers)

Users receive a new copy only when the plugin's version changes, so every
release bumps `version` in
[`plugins/arcsite-ks-update/.claude-plugin/plugin.json`](plugins/arcsite-ks-update/.claude-plugin/plugin.json)
(the only place it is set). Validate, then merge to `main`:

```
claude plugin validate --strict .
claude plugin validate --strict plugins/arcsite-ks-update
```

When the server's tool contract version changes, release the skill written
for it at the same time: the skill stops and asks people to update when the
two disagree.

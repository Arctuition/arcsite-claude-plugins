# arcsite-claude-plugins

Claude Code plugins for ArcSite staff. This public repository is the plugin
marketplace: installing needs no GitHub account.

| Plugin | What it does |
| --- | --- |
| [`arcsite-ks-update`](plugins/arcsite-ks-update) | Update Knowledge Studio knowledge from Claude Code: find the layer, preview and save a draft, run Replay, and hand publishing back to the Console. Connects to the **test** environment only. |

## Install (once)

You need Claude Code: the Claude desktop app's **Code** tab, a terminal
(`claude`), or VS Code. Your ArcSite Google Workspace account needs the Admin
Console's Knowledge Studio authoring role (`SYSTEM_CONTENT`) on admin-test;
without it the sign-in page tells you so.

### In the Claude desktop app

1. In the **Code** tab, open a local session. Click **+** next to the prompt
   box, then **Plugins** → **Add plugin**.
2. Add the marketplace `https://github.com/Arctuition/arcsite-claude-plugins`,
   then install **arcsite-ks-update** for your user account.
3. Connect the **ks-test** connector the plugin adds: start its sign-in, sign
   in with your ArcSite Google account in the browser that opens, and click
   **Allow**.

### In a terminal

1. Start `claude` and add the marketplace and the plugin:

   ```
   /plugin marketplace add Arctuition/arcsite-claude-plugins
   /plugin install arcsite-ks-update@arcsite
   ```

2. Connect: run `/mcp`, pick `plugin:arcsite-ks-update:ks-test`, choose
   **Authenticate**, then sign in and click **Allow** as above.

The desktop app, a terminal and VS Code on one computer share plugin
settings, so the plugin installed in one is there in the others. Signing in
is not shared: if you use both the desktop app and a terminal, connect
ks-test from each.

There is no token to copy or renew. Claude Code keeps the credential and
refreshes it; if it ever lapses, connect ks-test again.

### Updates

Claude Code does not update a marketplace like this one on its own until
auto-update is on for it. Turn it on once from a terminal: run `/plugin`,
open **Marketplaces**, pick `arcsite`, and choose **Enable auto-update**. The
setting is shared with the desktop app. To update right away, run
`claude plugin update arcsite-ks-update@arcsite` and start a new session.

### For organisation admins

Admins can pre-install the plugin for everyone with managed settings:

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
plan and Console links, and you publish in the Console from the changed
layer's Versions module, where the Release plan card publishes every layer in
the plan in one go.

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
| Tools fail with 401 / "not authenticated", or ks-test shows as needing sign-in | Connect ks-test again: the ks-test connector in the desktop app, or `/mcp` → `plugin:arcsite-ks-update:ks-test` → **Authenticate** in a terminal |
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

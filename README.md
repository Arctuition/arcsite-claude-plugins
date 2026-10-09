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
only analyses and previews. Before saving, it can try the previewed change on
real jobs without writing anything, and show you what each would buy. The agent never publishes. It ends with what
publishing will do — what each layer ships (anyone else's unpublished edits
included), which companies move and which do not, and Replay of real orders
against the stack the release leaves in force, with the version of every
layer each company will read — plus a release note to paste, a Plan id and
the Console link.

The link opens the changed layer's Release plan card with the companies
ticked and the plan computed, and the card checks it against the plan the
agent read: it says so when they are the same, and when they are not it holds
publishing until you have reviewed the new plan — ask the agent to read it
again and summarise it. Read What ships and the Release Replay there (it also
lists the companies the release moves that have no test case), paste the note
and publish every layer in one go. If the plan changes while you review, the
publish is refused and the card shows the new plan and what moved, so nothing
ships that nobody reviewed.

A Rule at `review_required` does not stop an order: the order completes as
"Ready with warnings". If someone must sign off before the order can go
ahead, ask for a required Workflow task instead.

Before it starts on a layer, the agent says who else has unpublished drafts
on it and on the layers its release would publish, and when they saved them:
those go out with your change.

The agent can also work a company's Product catalog and give a company its
own Overlay, each only when you ask:

> Import this price list into Imperial Fence's catalog and AI-tag what is new.

> Tag these 40 gate SKUs as single swing gates, 48 in, and set them to
> requested only.

> Give Portland 004 its own Overlay and move it onto it.

A catalog has no draft: an import, a tagging run or an edit is live at once.
The agent previews an import first, tags a first few rows for you to check
before the rest, and shows what an edit would change before writing it. A
tagging run can be undone; an import or an edit cannot — a wrong edit is put
right with another one.

It can also tell you what a job comes to without the prototype, against the
published knowledge or the drafts:

> Resolve this Minneapolis job on the drafts: 4 runs of 40 ft, 7 end posts,
> 2 single swing gates at 48 in. What does it buy?

It reads the whole Enterprise library, as Replay does, so compare it with the
prototype on All branches. To keep a job as a Replay case, save it in the
prototype (Duplicate the job, change it, Save as test case).

## Fewer approval prompts (optional)

Claude Code asks before each tool call unless you allow it. To allow the
read-only tools, add this to your `~/.claude/settings.json` (a plugin cannot
ship permissions itself). The tools that write — `ks_apply`, `ks_replay`,
`ks_catalog_import_apply`, `ks_catalog_tag`, `ks_catalog_edit`,
`ks_create_layer` and `ks_bind_company` — are deliberately left out so each
still asks.

```json
{
  "permissions": {
    "allow": [
      "mcp__plugin_arcsite-ks-update_ks-test__ks_find_target",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_read_layer",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_read_object",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_preview",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_replay_results",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_resolve",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_applies",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_read_catalog",
      "mcp__plugin_arcsite-ks-update_ks-test__ks_catalog_import_preview"
    ]
  }
}
```

## Troubleshooting

| You see | Do |
| --- | --- |
| The agent says the plugin is too old | Update the plugin: `/plugin` → **Installed** → `arcsite-ks-update` → **Update now**, or `claude plugin update arcsite-ks-update@arcsite` in a shell. Then restart Claude Code |
| The agent says the server has not been updated yet | The plugin is newer than ks-test. Wait for the deploy, or ask whoever released it |
| Tools fail with 401 / "not authenticated", or ks-test shows as needing sign-in | Connect ks-test again: the ks-test connector in the desktop app, or `/mcp` → `plugin:arcsite-ks-update:ks-test` → **Authenticate** in a terminal |
| "This account cannot connect" on the sign-in page | Ask an Admin Console administrator for the Knowledge Studio authoring role |

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

The server answers with two numbers: `contract_version`, what it offers, and
`min_skill_contract`, the oldest skill that still reads it correctly. The skill
names the one version it was written for and stops when it is older than
`min_skill_contract` (the person updates the plugin) or newer than
`contract_version` (the server is not deployed yet). Any server change a
skill's wording could depend on bumps `contract_version`, a new field included.
Only a change that would make an older skill do the wrong thing -- a field it
relies on changed meaning or went away, a refusal it does not expect -- raises
`min_skill_contract`; an addition leaves it alone, so nobody on the older
plugin is stopped.

Both numbers are readable without signing in:

```
curl -s https://admin-test.arcsite.com/manage/ks-mcp/contract
```

A pull request that sets the skill's contract higher than ks-test's fails the
`contract` check, so a plugin cannot be merged ahead of the server it needs.

Before merging a change to the skill, run its eval suite. Each case is a real
request run by a headless Claude Code against recorded ks-test answers (each
case's `mocks/`; nothing reaches a server), graded on which tools it called and
what it said. The two cases that apply a change answer the reads an apply
changes from one agent playing the server, so run with a Sonnet judge, which
follows it reliably. One run of every case costs about $2.50:

```
cd plugins/arcsite-ks-update
claude plugin eval . --trust-plugin --ablation none --runs 1 --judge-model sonnet --max-cost-usd 10
```

A case that drops below 1.00 is a behaviour the skill no longer has. When the
tools change shape, refresh `evals/mocks/ks-test/_tools.json` from the server's
`tools/list` and the fixtures from real read-only calls.

In this order:

1. Merge the cloudservice change and deploy it to test, migrations included.
2. Confirm the numbers at the address above.
3. Re-run the pull request's `contract` check, merge it, and tell the people
   using the plugin to update.
4. In a new session, check that the skill and the server agree.

When `min_skill_contract` rose, everyone still on an older plugin is stopped
and asked to update between steps 2 and 4. Deploy outside the hours CS is
working where you can: an agent mid-task meets the new server half-way.

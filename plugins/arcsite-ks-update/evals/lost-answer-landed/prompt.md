---
description: "A lost answer is checked against the ledger; a change that landed is not sent again."
runs: 1
max_turns: 20
timeout_seconds: 900
allowed_tools: [Read, Skill]
---
Earlier today you saved a draft on Portland 004's overlay: the burial survey region back to unassigned (preview context_checksum f1f9ee329769886633f32d150c244dbb9e55c8510fd525ae6619deca14a5afbc, diff_checksum 86fdfc06c731411a540a9f0ee7e90c912626db5a0061aa69264610ea859d54f0). The connection dropped before the apply answered. Make sure that change is saved, exactly once.

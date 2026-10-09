---
description: "A change that did not land is previewed again and applied once, with the same checksums."
runs: 1
max_turns: 25
timeout_seconds: 900
allowed_tools: [Read, Skill]
---
Earlier today you saved a draft on Portland 004's overlay: the burial survey region back to unassigned (preview context_checksum f1f9ee329769886633f32d150c244dbb9e55c8510fd525ae6619deca14a5afbc, diff_checksum 86fdfc06c731411a540a9f0ee7e90c912626db5a0061aa69264610ea859d54f0). The connection dropped before the apply answered. Make sure that change is saved, exactly once.

The document was:

```json
{
  "format_version": 1,
  "layer": {
    "stable_id": "org-287386500977433776",
    "kind": "organization",
    "namespace": "org_287386500977433776",
    "name": "Portland 004",
    "manufacturer_axis_stable_id": null
  },
  "baseline": {
    "authoring_checksum": "eccd393e16daa73b4f7b246f93cd081b5332161737aed1e58da88d285b9ac0cc",
    "ancestors": [
      {
        "layer": "arcsite-core",
        "version": "0.0.1",
        "checksum": "b0fedf0dbaabb52f6987babbc90e27374cc503b21cb505b52a7af3411fbb0c7f"
      },
      {
        "layer": "construction-core",
        "version": "0.0.1",
        "checksum": "7e1e6c3419e0e793b30a900a195a6c0c5278f17afac979cdd0d9b2f870205847"
      },
      {
        "layer": "fence",
        "version": "0.0.27",
        "checksum": "134efca57f1f524084ed137df77ca1e182cdc429cbec0c0918ae30caa2e46872"
      },
      {
        "layer": "master-halco",
        "version": "0.0.45",
        "checksum": "d002acb6caa2a0a7d469826d933afc18d9df8248e0aaf95a6869a73774453a89"
      },
      {
        "layer": "master-halco-distribution",
        "version": "0.0.46",
        "checksum": "94d1ae9d300c3f2d6f7fd022d8915f81414e7b373f113abfa5d03d8577e9f099"
      }
    ]
  },
  "objects": [],
  "delegated_settings": [],
  "layer_settings": [
    {
      "entry_stable_id": "fence.burial_region",
      "discipline": "default",
      "value": "unassigned",
      "window_payload": null
    }
  ],
  "removals": [],
  "touched": [
    {
      "type": "layer_setting",
      "entry_stable_id": "fence.burial_region"
    }
  ]
}
```

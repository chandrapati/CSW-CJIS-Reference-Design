# FBI CJIS Security Policy — CSW Evidence Checklist

A printable worklist for the evidence owner (often the agency **LASO**). For each item: **what** to export, **where** from in CSW, and the **cadence**. Tick as you collect; file exports to immutable storage (not screenshots taken during audit week).

> Legend — 🟢 Direct · 🟠 Supporting · ⚪ Evidence Required *(supplied outside CSW)*. CSW evidence is an input to a CSA audit, not an attestation. CJIS compliance is determined by your **CJIS Systems Agency**.

> **Before you start:** confirm which CJISSECPOL version your CSA audits against. Several states audit against v5.9.5 while using v6.1 for gap assessments. See §1.2 of the [Reference Design](../CSW-CJIS-Reference-Design.md).

---

## Phase 1 — Coverage (Days 1–10)

- [ ] Every system that stores, processes, or transmits CJI reconciled to **CSW Inventory** (100% or documented exceptions)
- [ ] Labels applied: `compliance:cjis`, `cji:true|false`, `cji_role:*`, `agency_ori:*`, `vendor_addendum:*`, `owner:*`
- [ ] CSW scope tree created matching the CJI boundary
- [ ] Under-scoping check: query-capable workstations, reporting/cache databases, and enclave backup servers all assessed for `cji:true`
- [ ] **Export:** inventory CSV + agent-status screenshot → `evidence/01-coverage/`

## Phase 2 — Baseline (Days 11–28)

- [ ] ADM running on `CJI-Enclave` for ≥ 2 weeks (full business cycle)
- [ ] Unexpected flows documented (shadow IT, vendor egress, scope creep)
- [ ] `State-Interface` flows to the CSA message switch identified and confirmed
- [ ] App owners signed the cluster-to-application mapping
- [ ] **Export:** ADM diagram + flow samples with process context → `evidence/02-baseline/`

## Phase 3 — Policy (Days 29–45)

- [ ] Default-deny posture defined for `CJI-Enclave`
- [ ] ADM-imported rules refined; **Simulation** run ≥ 1 week
- [ ] Change tickets raised for false positives; exception register updated
- [ ] **Export:** policy export + simulation report → `evidence/03-policy/`

## Phase 4 — Operate (ongoing)

- [ ] Enforcement enabled; negative test recorded in **Denied Connections**
- [ ] SIEM integration verified with sample events
- [ ] Quarterly binder assembled
- [ ] **Export:** enforcement screenshot + quarterly binder → `evidence/04-operate/`

---

## Recurring evidence pack

| # | Evidence item | CSW location | Controls | Cadence | Collected |
|---|---|---|---|---|:--:|
| 1 | CJI enclave scope + label export | Organize → Scopes | CM-8, AC-4 | Per audit | ☐ |
| 2 | Policy workspace export | Defend → Policy Workspaces | AC-3, AC-4, SC-7 | Per audit | ☐ |
| 3 | Denied Connections log | Defend → Enforcement | SC-7, AC-4, SI-4 | Continuous | ☐ |
| 4 | ADM dependency map | Investigate → ADM | CM-2, AC-4 | Quarterly | ☐ |
| 5 | Simulation report | Defend → Policy Workspaces | CM-3 | Per change | ☐ |
| 6 | Network flow audit log | Investigate → Flow Search | AU-2, AU-3, AU-12 | Continuous | ☐ |
| 7 | Workload inventory | Manage → Inventory | CM-8 | Monthly | ☐ |
| 8 | Vulnerability + reachability report | Investigate → Vulnerability | RA-5 | Weekly | ☐ |
| 9 | Open-port / process report | Investigate → Process Search | CM-6, CM-7, SI-7 | Monthly | ☐ |
| 10 | Vendor access path report | Flow Search → `Vendor-Remote-Support` | AC-20, AC-17 | Quarterly | ☐ |
| 11 | Plaintext-on-CJI-paths report | Flow Search → `Plaintext-On-CJI-Paths` | Encryption input | Quarterly | ☐ |
| 12 | Alert / incident log | Alerts → Dashboard | IR-4, IR-6, SI-4 | Monthly | ☐ |
| 13 | CSW administrative audit log | Administration → Audit Log | AU-2, AU-12 | Per audit | ☐ |

Items 1–3 and 8 are the four an auditor asks for first. Item 11 is the one you want to run *before* the auditor does.

The control-by-control mapping, with Priority 1 / zero-cycle markings, is in the [Reference Design](../CSW-CJIS-Reference-Design.md).

```
evidence/
├── 01-coverage/   inventory.csv, agent-status.png, scope-export.csv
├── 02-baseline/   adm-map.pdf, flow-samples.csv, state-interface-flows.csv
├── 03-policy/     policy-export.json, simulation-report.pdf, exceptions.xlsx
└── 04-operate/    QYYYY-Qn/  (quarterly binder: items 1–13)
```

---

## Evidence you must collect outside CSW

Do not file these in the CSW evidence tree — but do not forget them either. The CSA will ask.

- [ ] Fingerprint-based background checks and personnel screening records (**PS**)
- [ ] Security awareness and CJIS training records (**AT**)
- [ ] Physically secure location and controlled-area controls (**PE**)
- [ ] Media protection, sanitization, and destruction records (**MP**)
- [ ] Identification, authentication, and advanced-authentication evidence (**IA**)
- [ ] FIPS 140-validated encryption configuration for CJI in transit and at rest
- [ ] Signed CJIS Security Addenda for every vendor with CJI access (**Policy Area 1**)
- [ ] Mobile device management and policy (**Policy Area 20**)
- [ ] Application and database audit logs showing *which user accessed which CJI record*
- [ ] Contingency / COOP plan and backup testing records (**CP**)

*Validate sufficiency of every item with your CSA. See §7 of the [Reference Design](../CSW-CJIS-Reference-Design.md) for the full evidence boundary.*

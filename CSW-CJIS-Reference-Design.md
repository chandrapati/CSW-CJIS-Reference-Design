# Cisco Secure Workload — FBI CJIS Security Policy Compliance Framework
## Reference Design | Law Enforcement, Courts, Corrections & CJI Contractors

**Version:** 1.0 | **Standard:** FBI CJIS Security Policy (CJISSECPOL) v6.1, effective 06/25/2026

---

> **Coverage legend** — this reference design and its compliance report use three words:
> - 🟢 **Direct** — CSW produces the primary evidence artifact.
> - 🟠 **Supporting** — CSW produces an input that feeds or complements another control.
> - ⚪ **Evidence Required** *(supplied outside CSW)* — CSW produces nothing here; the item is in scope for compliance but out of scope for CSW, so the customer evidences it via another control, tool, or process. A scope boundary, not a gap or "unsupported."

---

## Reader's Guide

**Who this is for.** State and local law enforcement agencies, courts,
corrections, state CJIS Systems Agencies (CSAs), and the contractors,
integrators, and cloud providers that store, process, or transmit
Criminal Justice Information (CJI) on an agency's behalf — plus the CSA
auditors who review them.

**Questions this reference design helps you answer:**

- *Where exactly is my CJI boundary, and can I prove a workload outside
  it cannot reach a workload inside it?* (AC-4, SC-7)
- *Which of the controls my CSA will sanction me on can CSW actually
  evidence — and which are someone else's job?* (§2, §7)
- *My vendor has remote access to the records system. Can I show the CSA
  precisely what that path reaches?* (AC-20)
- *Can I produce a component inventory of the CJI enclave that matches
  reality rather than a spreadsheet from last year?* (CM-8)
- *The policy expects FIPS 140-validated encryption on CJI in transit.
  Can I at least find the paths that are still plaintext?* (§7.2)

**What you'll need.** Your agency's ORI(s), the version of CJISSECPOL
your CSA currently audits against (see §1.2 — this is not always the
current version), a list of systems that touch CJI, your signed CJIS
Security Addenda for vendors, and your CSA's evidence-format
expectations.

**Where to start.** Read §1.2 first — it determines which control set
applies to you. §2 maps the control families CSW addresses, with each
row marked sanctionable or zero-cycle. §3–4 build the scope tree and the
policy set the mapping depends on. §7 is the honest boundary: what you
must evidence outside CSW. Go to §6 if you are assembling the evidence
package now.

---

## CSW primer — if you are new to Cisco Secure Workload

Cisco Secure Workload (CSW) is a **workload protection platform**. A lightweight **agent** on each server/VM/container observes processes and network flows; **cloud connectors** add AWS/Azure/GCP inventory where agents are not deployed.

| CSW term | Meaning | Why compliance teams care |
|----------|---------|---------------------------|
| **Scope** | Logical boundary (CJI enclave, CDE, PHI zone) | Defines the systems you must prove are isolated |
| **Label / filter** | Tag or query assigning workloads to scopes | Automates scope membership — reduces drift |
| **ADM** | Application Dependency Mapping from observed traffic | **Live** network/data-flow diagram for auditors |
| **Workspace** | Policy container for one scope or application | Where allow/deny rules are authored |
| **Monitor → Simulation → Enforce** | Safe rollout sequence | Simulation = change-board evidence before blocking traffic |
| **Denied Connections** | Log of flows blocked by policy | Primary proof that enforcement **operates** |

**Console areas:** Investigate (inventory, flows, vulns) · Defend/Segmentation (policy) · Manage (agents) · Platform (connectors) · Administration (audit log)

**Read next:** [Compliance evidence playbook](https://github.com/chandrapati/CSW-Compliance-Reference-Designs/blob/main/docs/compliance-evidence-playbook.md) (full step-by-step) · [About CSW](https://github.com/chandrapati/CSW-Compliance-Reference-Designs/blob/main/docs/about-csw.md) (platform intro)

---

## Universal evidence workflow

Execute these phases for **this framework's** compliance boundary. Map exports to control IDs in the **Evidence Package** section below.

| Phase | Goal | Key CSW actions | Typical duration |
|-------|------|-----------------|------------------|
| **1 — Coverage** | Every in-scope workload in CSW | Install agents/connectors; apply compliance labels; create scope | Days 1–10 |
| **2 — Baseline** | Machine-generated flow map | Run ADM ≥2 weeks; export clusters; app-owner signoff | Days 11–28 |
| **3 — Policy** | Designed isolation before enforce | Build workspace; Simulation mode; fix false positives | Days 29–45 |
| **4 — Operate** | Continuous proof between audits | Enforce; quarterly export pack; ADM refresh every 90 days | Ongoing |

### Phase 1 checklist (coverage)

- [ ] In-scope host list reconciled to CSW Inventory (100% or documented exceptions)
- [ ] Labels applied: `compliance:cjis`, `cji:true|false`, `agency_ori:<ORI>`
- [ ] CSW scope created matching the CJI boundary
- [ ] **Export:** inventory CSV + agent status screenshot

### Phase 2 checklist (baseline)

- [ ] ADM running on the CJI scope for a full business cycle (≥2 weeks)
- [ ] Unexpected flows documented (shadow IT, vendor egress, scope creep)
- [ ] App owners signed cluster-to-application mapping
- [ ] **Export:** ADM diagram + flow samples with process context

### Phase 3 checklist (policy)

- [ ] Default-deny posture defined for the CJI enclave
- [ ] ADM-imported rules refined; Simulation run ≥1 week
- [ ] Change tickets for false-positive fixes; exception register updated
- [ ] **Export:** policy export + simulation report

### Phase 4 checklist (operate)

- [ ] Enforcement enabled on pilot scope; negative test recorded in Denied Connections
- [ ] Quarterly pack: inventory, policy, denies, vulns, audit log (see playbook)
- [ ] SIEM integration verified (sample events)
- [ ] **Export:** enforcement screenshot + quarterly binder

### What CSW evidence does not replace

Personnel screening and fingerprinting, physical security of a
physically secure location, media protection and sanitization, security
awareness training records, FIPS 140-validated encryption itself, and
signed CJIS Security Addenda still require separate programmes. CSW
addresses the **workload-resident** slice: segmentation, flows, process
context, vulnerability reachability, and change drift. §7 enumerates the
boundary in full.

---

## CSW effectiveness for this framework

- AC-4 information-flow enforcement around the CJI enclave, with exportable policy artifacts
- SC-7 boundary protection evidence at the workload tier, independent of the perimeter firewall
- CM-8 live component inventory of the CJI enclave, reconcilable to the agency's system documentation
- CA-7 continuous monitoring between triennial CSA audits

**Compared to manual programmes:** a CSA audit cycle is typically
triennial, and the static network diagram an agency produced for the
last audit has usually drifted by the next one. CSW ties the evidence to
**live workload behaviour** and regenerates it on demand, which changes
the conversation from "here is what we designed" to "here is what is
running."

---

## 1. Overview

The **FBI CJIS Security Policy (CJISSECPOL)** sets the minimum security
requirements for any agency or contractor that stores, processes, or
transmits **Criminal Justice Information (CJI)** — fingerprint records,
criminal histories, NCIC and Nlets data, and the related identity
information. It applies to police and sheriff departments, courts,
corrections, and equally to the private-sector vendors, cloud providers,
and IT contractors that touch CJI on an agency's behalf.

**CJIS is not a certification.** There is no "CJIS certified" product or
provider. Each state's **CJIS Systems Agency (CSA)** audits agencies
against the policy, and vendors with CJI access sign a **CJIS Security
Addendum** and have their personnel background-checked. CSW is therefore
positioned here exactly as in the rest of this series: as a producer of
**evidence**, not as an attestation.

### 1.1 Why this maps cleanly to NIST 800-53

CJISSECPOL v6.0 (12/27/2024, the "Policy Modernization" release)
restructured the policy around **NIST SP 800-53 Rev 5 control
families** — AC, AT, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PS, RA,
SA, SC, SI, SR — retaining only **Policy Area 1 (Information Exchange
Agreements)** and **Policy Area 20 (Mobile Devices)** from the legacy
13-Policy-Area structure. v6.1 (06/25/2026) incorporates calendar-year
2025 changes.

The practical consequence: if you have already built CSW against NIST
800-53, you have built most of this. See the
[NIST SP 800-53 Rev 5 reference design](https://github.com/chandrapati/CSW-NIST-800-53-Reference-Design)
for the parent control catalog. What CJIS adds is a **specific, narrow,
and externally audited boundary** — the CJI enclave — and a priority
scheme that tells you which controls carry sanctions.

### 1.2 Version and sanctionable-requirement calibration

**Confirm two things with the customer before using this document.**

**First, which version their CSA audits against.** This is frequently
*not* the current version. Several states run a lagging audit cycle —
Texas DPS, for example, has audited against **v5.9.5** through
03/31/2027 while using v6.1 for gap assessments. An agency may be
simultaneously audited on v5.9.5 and remediating toward v6.1.

**Second, which requirements are sanctionable.** Per CJISSECPOL §1.4,
beginning **October 1, 2024**, the sanctionable set is:

> requirements existing prior to the CJISSECPOL modernization (i.e.,
> version 5.9) and those identified as Priority 1 (`[Priority 1]`)

Priority 2, 3, and 4 requirements sit in a **"zero-cycle"** status from
**October 1, 2024 through September 30, 2027** — they are policy, they
will be assessed, but they are not yet sanctionable.

| Marking in this document | Meaning |
|---|---|
| **P1** | `[Priority 1]` — **sanctionable now** |
| **P1\*** | Priority 1 **and** existed in v5.9 — sanctionable under either version |
| **P2** | `[Priority 2]` — in zero-cycle status until 09/30/2027 |
| **P2\*** | Priority 2 but existed in v5.9 — **sanctionable** via the v5.9 clause |

This matters commercially as well as technically. **The controls where
CSW produces primary evidence are overwhelmingly Priority 1** — AC-3,
AC-4, CM-7, CM-8, CA-7, RA-5, SC-7, and SI-4 are all sanctionable
today. CSW is not helping with the optional part of the policy.

> Priorities and version dates above are quoted from CJISSECPOL v6.1.
> Re-verify against the current official text before customer delivery;
> the FBI revises this policy annually.

---

## 2. Control Family Mapping

Each row carries the **Priority** marking from §1.2 and a **Coverage**
verdict from the legend at the top of this document.

### AC — Access Control

| Control | Name | Priority | Coverage | CSW Implementation |
|---|---|---|---|---|
| AC-3 | Access Enforcement | P1\* | 🟢 Direct | Allowlist policy enforced at the workload, so access to CJI systems is permitted by rule rather than by reachability |
| AC-4 | Information Flow Enforcement | P1\* | 🟢 Direct | ADM maps every observed flow crossing the CJI boundary; policy blocks undocumented paths where enforcement is deployed |
| AC-6 | Least Privilege | P1\* | 🟠 Supporting | Delivers *network* least privilege for the enclave; user and administrative least privilege is evidenced in the IdP and OS |
| AC-17 | Remote Access | P1 | 🟠 Supporting | Constrains and logs remote administration to defined jump paths; the VPN, MFA, and advanced-authentication evidence is external |
| AC-20 | Use of External Systems | P1 | 🟠 Supporting | Shows exactly what each vendor-managed path actually reaches; the Security Addendum and authorization are external |

**CSW Implementation:**
```
CSW UI → Defend → Segmentation
  → Policy type: Allowlist (default deny)
  → Scope: CJI-Enclave
  → Document each allowed flow with a CJI business justification
  → Export policy for AC-3 / AC-4 control evidence
```

### AU — Audit & Accountability

| Control | Name | Priority | Coverage | CSW Implementation |
|---|---|---|---|---|
| AU-2 | Event Logging | P2\* | 🟢 Direct | Continuous network-flow and process telemetry on every monitored CJI workload |
| AU-3 | Content of Audit Records | P2\* | 🟢 Direct | 5-tuple flow + process name and hash + user context + UTC timestamp |
| AU-6 | Audit Record Review, Analysis, and Reporting | P2\* | 🟠 Supporting | Exports to SIEM for correlated review; the review *process* and its records are the agency's |
| AU-12 | Audit Record Generation | P2 | 🟢 Direct | Generation is continuous and configurable; align retention to the CSA's expectation |

CSW audits the **workload and network layer**. Auditing a named user's
*access to a CJI record* is an application and database responsibility —
see §7.

### CA — Assessment, Authorization, and Monitoring

| Control | Name | Priority | Coverage | CSW Implementation |
|---|---|---|---|---|
| CA-7 | Continuous Monitoring | P1 | 🟢 Direct | Inventory, flow, policy-violation, and vulnerability telemetry is continuous, which is the gap a triennial audit cycle leaves open |

### CM — Configuration Management

| Control | Name | Priority | Coverage | CSW Implementation |
|---|---|---|---|---|
| CM-2 | Baseline Configuration | P1 | 🟠 Supporting | ADM establishes the approved *communication* baseline; golden-image and OS baselines come from the config-management tool |
| CM-3 | Configuration Change Control | P2 | 🟠 Supporting | Simulation reports and ADM drift give the change board technical input; the CAB record is external |
| CM-6 | Configuration Settings | P1 | 🟠 Supporting | Detects drift as new processes and newly opened ports; CSW does not set or remediate OS configuration |
| CM-7 | Least Functionality | P1 | 🟢 Direct | Observes every listening port and running process in the enclave and blocks what is not approved |
| CM-8 | System Component Inventory | P1 | 🟢 Direct | Live inventory of the CJI enclave; reconcile against agency system documentation for full CM-8 scope |

**Baseline drift detection:**
```
CSW UI → Investigate → ADM
  → Re-run ADM quarterly on CJI-Enclave
  → Compare to the previous approved baseline
  → New flows = configuration change review required
  → Policy workspace updated to reflect approved changes
```

### IR — Incident Response

| Control | Name | Priority | Coverage | CSW Implementation |
|---|---|---|---|---|
| IR-4 | Incident Handling | P2\* | 🟠 Supporting | Flow and process telemetry reconstructs what a compromised CJI workload reached; the handling capability is the agency's |
| IR-6 | Incident Reporting | P2\* | 🟠 Supporting | Alert export feeds SIEM/SOAR ticketing; CJIS requires reporting to the CSA and FBI CJIS ISO, which is a process obligation |

**Forensic investigation workflow:**
```
1. Alert triggered → CSW alert with workload ID, time, flow context
2. Flow Search → reconstruct all connections to/from the affected workload
3. Process Search → identify anomalous processes + parent chain
4. Vulnerability Report → identify the exploited CVE if applicable
5. Export → forensic package for the agency IR team and CSA notification
```

### RA — Risk Assessment

| Control | Name | Priority | Coverage | CSW Implementation |
|---|---|---|---|---|
| RA-5 | Vulnerability Monitoring and Scanning | P1 | 🟢 Direct | Continuous CVE exposure per workload with CVSS scoring, and — the part that matters for prioritization — whether a vulnerable service is actually reachable from outside the enclave |

Reachability is the argument worth making to a CSA auditor. An unpatched
CVE on a CJI workload that policy has made unreachable is a materially
different risk from the same CVE on an internet-exposed host, and CSW
produces the evidence for that distinction.

### SC — System and Communications Protection

| Control | Name | Priority | Coverage | CSW Implementation |
|---|---|---|---|---|
| SC-7 | Boundary Protection | P1 | 🟢 Direct | Enforces the CJI enclave boundary east-west at the workload, including between systems that share a VLAN and are therefore invisible to the perimeter firewall |

CJISSECPOL's boundary language expects subnetworks for publicly
accessible components to be physically or logically separated from
internal networks. CSW evidences the **logical** separation, and does so
per workload rather than per subnet.

### SI — System and Information Integrity

| Control | Name | Priority | Coverage | CSW Implementation |
|---|---|---|---|---|
| SI-4 | System Monitoring | P1 | 🟢 Direct | Flow, process, and policy-violation monitoring with anomaly detection across the enclave |
| SI-7 | Software, Firmware, and Information Integrity | P1 | 🟠 Supporting | Process-hash baselining flags binaries that changed; file-integrity monitoring and firmware integrity are external |

**Coverage summary:** 🟢 Direct for **11** controls, 🟠 Supporting for
**10**, across 8 control families. The 13 families and policy areas
where CSW produces nothing are enumerated in §7.

---

## 3. Scope Architecture and Labeling

The control mapping above is only auditable against a named boundary.
For CJIS that boundary is unusually concrete — the CSA will ask which
systems store, process, or transmit CJI — but it is also frequently
undocumented, because in many agencies the records system, the CAD
system, and the state message switch grew up separately. The job here is
to make the CSW scope tree the authoritative answer to "where is CJI."

A specific trap worth naming: agencies routinely under-scope. A
workstation that queries NCIC, a reporting database that caches query
results, and a backup server that holds enclave snapshots are all in
scope. Scope the enclave from the **data**, not from the org chart.

### 3.1 Suggested Scope Architecture

```
Root Scope
└── CJIS
    ├── CJI-Enclave                      (stores, processes, or transmits CJI)
    │   ├── CJI-Applications             (RMS, CAD, JMS, case management)
    │   ├── CJI-Data-Stores              (criminal history, mugshot, biometric)
    │   └── State-Interface              (CSA message switch / NCIC / Nlets)
    ├── CJI-Adjacent                     (serves the enclave, holds no CJI)
    │   ├── Identity-Services
    │   ├── Logging-and-Monitoring
    │   └── Patch-and-Config-Mgmt
    ├── Privileged-Access-Paths          (AC-17 remote administration)
    ├── Non-CJI-Agency                   (general municipal / county IT)
    └── External
        ├── Internet-Edge
        └── Vendor-Remote-Support        (AC-20 — Security Addendum signatories)
```

Two branches are deliberate. **`State-Interface`** is separated because
the path to the CSA message switch is the one flow an auditor will
always ask about, and it is far easier to evidence when it is its own
scope. **`Vendor-Remote-Support`** is named inside the tree even though
it sits outside the agency boundary — AC-20 requires you to evidence the
terms of external system use, and you cannot show a flow to a system the
scope tree refuses to name.

### 3.2 Inventory Filters

```
Filter: CJI-Applications
  - Tag: cji = true
  - Tag: cji_role = process | transmit
  - Hostname / application pattern matches the agency RMS / CAD / JMS inventory

Filter: CJI-Data-Stores
  - Tag: cji = true
  - Tag: cji_role = store
  - Listening port: 1433, 1521, 3306, 5432, 27017

Filter: State-Interface
  - Tag: application = state-interface | ncic | nlets
  - Destination matches the CSA message-switch endpoints

Filter: Vendor-Remote-Support
  - Tag: managed_by = vendor | contractor
  - Observed inbound on tcp/22, tcp/3389, tcp/443 from outside agency ranges

Filter: Plaintext-On-CJI-Paths
  - Source or destination in CJI-Enclave
  - Protocol / port: tcp/80, tcp/21, tcp/23, tcp/389, udp/161
```

`Plaintext-On-CJI-Paths` earns its place because CJISSECPOL expects
FIPS 140-validated encryption for CJI in transit. CSW does not encrypt
anything — but it will tell you, with flow-level evidence, which CJI
paths are still running cleartext protocols. That is a finding you want
to discover yourself rather than have the CSA discover for you.

### 3.3 Labeling Strategy

| Label key | Example values | Why it matters for CJIS |
|---|---|---|
| `cji` | true, false | The single most consequential label — it defines the boundary the CSA audits |
| `cji_role` | store, process, transmit, support | Separates systems that hold CJI at rest from those that only carry it, which drives policy stringency |
| `agency_ori` | <ORI> | Originating Agency Identifier — ties each workload to the audited agency, essential in shared county or regional environments |
| `physically_secure_location` | true, false | CJISSECPOL treats workloads outside a physically secure location differently; this label makes that population a filter rather than an interview |
| `vendor_addendum` | signed, pending, n-a | Flags vendor-managed workloads that require a CJIS Security Addendum, and surfaces the ones that do not have one |
| `criticality` | critical, important, standard | Drives enforcement sequencing |
| `application` | <named app> | Connects workloads to named agency systems |
| `owner` | <named function> | Accountability (system owner / LASO) |
| `compliance` | cjis | Filters every CSW export to the CJIS audit boundary |

`cji`, `agency_ori`, and `vendor_addendum` are the three worth enforcing
at onboarding. Together they answer the questions that otherwise consume
an audit interview: what is in scope, whose ORI owns it, and which
third parties can reach it under what agreement.

---

## 4. Policy Design — AC-4 and SC-7 Enforcement for the CJI Boundary

AC-4 and SC-7 are both **Priority 1** and both controls where CSW
produces primary rather than supporting evidence. Write the policy set
to be read by a CSA auditor, not only by an operator — each rule below
is a sentence in the agency's information-flow narrative.

### 4.1 CJIS-Aligned Policy Framework

**Absolute policies:**

```
DENY  Any                        → CJI-Enclave              (default deny inbound — SC-7, AC-4)
DENY  CJI-Enclave                → Internet-Edge            (no direct egress from the enclave — SC-7)
DENY  Non-CJI-Agency             → CJI-Enclave              (general IT reaches CJI only via jump paths — AC-3, AC-6)
DENY  Vendor-Remote-Support      → CJI-Data-Stores          (vendor paths stop short of CJI at rest — AC-20)
DENY  External                   → State-Interface          (only the enclave talks to the CSA switch — AC-4)
```

The fourth and fifth rules are the ones auditors probe hardest. A
vendor with an unrestricted path to the criminal-history database is a
finding even when the Security Addendum is signed and the staff are
background-checked, because the addendum governs *authorization* while
AC-4 governs *flow*. The two are evidenced separately.

**Allowlist policies (least privilege):**

```
ALLOW CJI-Applications           → CJI-Data-Stores          tcp/<db-port-tls>
ALLOW CJI-Applications           → State-Interface          tcp/<csa-switch-port-tls>
ALLOW CJI-Enclave                → Identity-Services        tcp/636, tcp/88
ALLOW Privileged-Access-Paths    → CJI-Enclave              tcp/22, tcp/3389
ALLOW CJI-Enclave                → Logging-and-Monitoring   tcp/443, udp/514
ALLOW Patch-and-Config-Mgmt      → CJI-Enclave              tcp/443
```

Every port above is specified in its TLS-bearing form deliberately. The
allowlist is where the encryption expectation becomes visible: if the
only rule that makes an application work is the cleartext port, you have
documented a gap rather than closed one.

**Catch-all:**

```
LOG   Any                        → CJI-Enclave              (unmatched inbound — SI-4)
LOG   CJI-Enclave                → Any                      (unmatched outbound — SI-4)
LOG   CJI-Enclave                → Any                      (plaintext: tcp/80, tcp/21, tcp/23, tcp/389, udp/161)
```

### 4.2 Policy Workspace Lifecycle

| Phase | Mode | Duration | Purpose |
|---|---|---|---|
| 1 | Simulation | 2 weeks | Validate the candidate policy against real enclave traffic |
| 2 | Enforcement (high-confidence rules only) | 1 week | Enforce the absolute deny rules |
| 3 | Full Enforcement | Ongoing | Enclave allowlist enforced; monthly exception review |

Workspace snapshots are AC-4 and SC-7 implementation evidence; the
simulation report is the CM-3 change-control artifact showing the policy
was assessed before it was enforced; and the Denied Connections log is
the proof that enforcement **operates** rather than merely exists.
Exceptions belong in the workspace exception register, which is also the
input to the agency's remediation plan.

### 4.3 Enforcement State as Audit Posture

| CSW enforcement state | What you can tell the CSA |
|---|---|
| Monitor only | "We have a current, machine-generated map of every CJI flow." Evidences AC-4 discovery and CM-8, not SC-7 enforcement. |
| Simulation | "We know which flows a default-deny policy would block, and we have assessed them." Adds CM-3. |
| Enforce — absolute denies | "Undocumented paths into the enclave are blocked, and here is the log of blocked attempts." SC-7 operates. |
| Enforce — full allowlist | "Access to CJI is permitted by rule. Anything not justified is denied and logged." AC-3, AC-4, AC-6, CM-7 all operate. |

---

## 5. Deployment Guidance by Agency Profile

| Profile | CSW configuration |
|---|---|
| Small agency, hosted RMS | Agents on the agency-side enclave and jump hosts; monitor and simulation; rely on the hosting provider's addendum and attestations for their tier |
| Mid-size agency, on-prem enclave | Full ADM; enforce absolute denies on `CJI-Enclave` and `State-Interface`; quarterly evidence pack |
| County / regional shared environment | Enforce `agency_ori` labeling first — multi-ORI environments must evidence separation *between* agencies, not just from non-CJI IT |
| Vendor / contractor hosting CJI | Full enforcement plus process-level monitoring; your CSW evidence supports the agency's audit and your Security Addendum obligations |

---

## 6. Evidence Package

| Evidence Item | CSW Source | Controls | Frequency |
|---|---|---|---|
| CJI enclave scope + label export | Organize → Scopes | CM-8, AC-4 | Per audit |
| Policy workspace export | Defend → Policy Workspaces | AC-3, AC-4, SC-7 | Per audit |
| Denied Connections log | Defend → Enforcement | SC-7, AC-4, SI-4 | Continuous |
| ADM baseline map | Investigate → ADM | CM-2, AC-4 | Quarterly |
| Simulation report | Defend → Policy Workspaces | CM-3 | Per policy change |
| Network flow audit log | Investigate → Flow Search | AU-2, AU-3, AU-12 | Continuous |
| Workload inventory | Manage → Inventory | CM-8 | Monthly |
| Vulnerability + reachability report | Investigate → Vulnerability | RA-5 | Weekly |
| Open-port / process report | Investigate → Process Search | CM-6, CM-7, SI-7 | Monthly |
| Vendor access path report | Investigate → Flow Search, filtered to `Vendor-Remote-Support` | AC-20, AC-17 | Quarterly |
| Plaintext-on-CJI-paths report | Investigate → Flow Search, filtered to `Plaintext-On-CJI-Paths` | §7.2 input | Quarterly |
| Alert / incident log | Alerts → Dashboard | IR-4, IR-6, SI-4 | Monthly |
| CSW administrative audit log | Administration → Audit Log | AU-2, AU-12 | Per audit |

---

## 7. Evidence Boundary — What You Must Supply Outside CSW

This section exists because a vendor mapping that claims everything is
not believable to an auditor. Marking the boundary honestly is what
makes the 21 controls in §2 credible.

### 7.1 Control families where CSW produces nothing

| Family / Area | Coverage | Who evidences it |
|---|---|---|
| **AT** — Awareness and Training | ⚪ Evidence Required | Agency security-awareness programme; CJIS training records per the biennial expectation |
| **CP** — Contingency Planning | ⚪ Evidence Required | Agency COOP / DR plan, backup testing records |
| **IA** — Identification and Authentication | ⚪ Evidence Required | IdP, MFA, and advanced-authentication tooling — Cisco ISE and Duo, or the agency's equivalent |
| **MA** — Maintenance | ⚪ Evidence Required | Maintenance records, escorted-maintenance logs, remote-maintenance authorizations |
| **MP** — Media Protection | ⚪ Evidence Required | Media handling, sanitization, and destruction records |
| **PE** — Physical and Environmental Protection | ⚪ Evidence Required | Physically secure location controls, visitor logs, controlled-area procedures |
| **PL** — Planning | ⚪ Evidence Required | Security plans, rules of behavior |
| **PM** — Program Management | ⚪ Evidence Required | Agency information-security programme governance |
| **PS** — Personnel Security | ⚪ Evidence Required | Fingerprint-based background checks, personnel screening, termination procedures |
| **SA** — System and Services Acquisition | ⚪ Evidence Required | Acquisition language, developer security requirements |
| **SR** — Supply Chain Risk Management | ⚪ Evidence Required | Supplier assessments, provenance |
| **Policy Area 1** — Information Exchange Agreements | ⚪ Evidence Required | Signed agreements, management control agreements, CJIS Security Addenda |
| **Policy Area 20** — Mobile Devices | ⚪ Evidence Required | MDM, mobile-device policy, device encryption and wipe |

### 7.2 Encryption — the most commonly misread boundary

CJISSECPOL expects **FIPS 140-validated** cryptographic modules for CJI,
including FIPS 140-2 validated encryption for CJI in transit outside a
physically secure location, and the policy text specifies a minimum of
128-bit symmetric encryption from a FIPS 140-2 certified module.

**CSW does not encrypt application data.** What CSW contributes is
detection: the `Plaintext-On-CJI-Paths` filter and the corresponding LOG
rule in §4.1 identify, with flow-level evidence, which CJI paths are
still using cleartext protocols. That is a genuinely useful input to the
encryption programme, and it is not the same thing as satisfying the
control.

**Two separate questions to keep distinct:**

1. **Is the customer's CJI encrypted in transit and at rest to a FIPS
   140-validated standard?** Evidenced by the TLS configuration, VPN,
   database, and storage layers. Not CSW.
2. **Does CSW's own agent-to-cluster communication operate in a FIPS
   mode acceptable to the CSA?** This is a product-configuration
   question about CSW itself. **Verify the current CSW FIPS posture with
   Cisco product management before answering it for a customer** — do
   not infer it from this document.

### 7.3 Application and user-level auditing

CSW audits the workload and the network. CJIS auditing expectations
extend to **which named user accessed which CJI record, and for what
purpose** — including the right-to-know / need-to-know justification.
That record lives in the RMS, CAD, or case-management application and
its database, never in CSW. Scope this to the application team early;
it is a recurring source of mistaken assumptions in CJIS projects.

### 7.4 Deployment-model and contractual caveats

- **SaaS versus on-premises matters.** If CJI is processed by a
  cloud-hosted service, the provider typically becomes a party to a CJIS
  Security Addendum, with the associated personnel-screening and
  jurisdictional obligations. Confirm the deployment model before
  mapping anything, because it changes who owns which control.
- **There is no known official Cisco CJIS attestation for CSW.**
  Independently confirm the current position with Cisco compliance or
  product management before making any formal CJIS claim to a customer
  or auditor. Nothing in this document should be represented as one.
- **CJIS has no product certification at all.** If a customer asks
  whether CSW is "CJIS certified," the accurate answer is that no
  product is — the agency is audited, and CSW produces evidence for that
  audit.

---

## 8. CSA Audit Response Guide

| If the auditor asks… | Produce |
|---|---|
| "Show me the systems that store, process, or transmit CJI." | Scope + label export for `CJI-Enclave`, with `cji_role` breakdown (§6) |
| "Prove a non-CJI system cannot reach the records database." | Policy workspace export plus the Denied Connections log showing blocked attempts |
| "What does your vendor's remote access actually reach?" | Vendor access path report filtered to `Vendor-Remote-Support`, alongside the signed Security Addendum |
| "How do you know your network diagram is current?" | ADM baseline map with its generation date, plus the quarterly refresh cadence |
| "How are you monitoring between our audits?" | CA-7 evidence: continuous flow, policy-violation, and vulnerability telemetry with alert history |
| "You have an unpatched critical CVE on a CJI server." | Vulnerability + reachability report showing whether the service is reachable, plus the compensating policy |
| "Is CJI encrypted in transit?" | **Not a CSW answer** — the TLS/VPN evidence. CSW supplies the plaintext-path report as supporting input (§7.2) |
| "Who looked up this person's criminal history?" | **Not a CSW answer** — application and database audit logs (§7.3) |

---

## Related Frameworks

- [NIST SP 800-53 Rev 5](https://github.com/chandrapati/CSW-NIST-800-53-Reference-Design) — the parent control catalog; CJISSECPOL v6.x is organized around these families, so this is the primary reuse path.
- [CJIS is frequently paired with CISA ZTMM](https://github.com/chandrapati/CSW-CISA-ZTMM-Reference-Design) — for agencies pursuing zero trust alongside CJIS compliance.
- [NIST CSF 2.0](https://github.com/chandrapati/CSW-CSF-Reference-Design) — the governance wrapper many state agencies use above CJIS.
- [CIS Controls v8.1](https://github.com/chandrapati/CSW-CIS-Reference-Design) — IG1/IG2 safeguards map closely to the Priority 1 set and suit smaller agencies.
- [FIPS 140](https://github.com/chandrapati/CSW-Compliance-Reference-Designs/blob/main/FIPS-140/CSW-FIPS-Technical-Runbook.md) — the cryptographic-module requirement referenced in §7.2.

---

*Replace [Customer Name], [ORI], and bracketed fields before customer delivery.*

---

## References & official sources

Authoritative source(s) for the **FBI CJIS Security Policy**. Always validate control references, priority markings, and version applicability against the current official text before customer use.

- [FBI CJIS Security Policy and resources](https://le.fbi.gov/informational-tools/cjis/cjis-security-policy-resource-center)
- [CJIS Division — FBI](https://www.fbi.gov/services/cjis)
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) — the control catalog CJISSECPOL v6.x is built on
- Your state **CJIS Systems Agency (CSA)** — the authority on which policy version applies to a given agency
- Cisco Secure Workload — [product documentation](https://www.cisco.com/c/en/us/support/security/secure-workload/series.html)

---

## Disclaimer

This repository is for informational and planning purposes. It is **not** legal, regulatory, audit, or certification advice, and it is **not** a CJIS attestation — no such product attestation exists. CJIS compliance is determined by your **CJIS Systems Agency**, not by a vendor or a tool. Validate all control references, priority markings, and version applicability against the current official CJIS Security Policy text and your CSA, and confirm Cisco's position with Cisco compliance or product management before making any formal claim. Replace any bracketed fields before customer delivery.

---

*Part of the Cisco Secure Workload compliance reference-design series. Umbrella index: [CSW-Compliance-Mapping](https://github.com/chandrapati/CSW-Compliance-Reference-Designs).*

# AetherianGovernance — Constitutional Decision and Consent Layer

**The governance layer of the AI Freedom Trust Federation: delegated authority, policy, consent, decision records, constitutional interfaces, and the human governance boundaries through which the rest of the Federation remains accountable.**

| Federation metadata | Value |
| --- | --- |
| Layer | `governance` |
| Role | Aetherian governance, delegated authority, policy, consent, decision records, and constitutional governance interfaces |
| Workspace | `AIFT/AetherianGovernance` |
| Control plane | AIFT workspace / AIFT-OS |
| Doctrine | AI-Freedom-Trust / SOP-ALOHA-001 |
| Operating standards | local-first, inspectable, sovereign by default, AI behind governed provider interfaces, human authority for high-impact decisions |

AetherianGovernance exists to answer the question that every powerful technical system eventually encounters: **who is actually authorized to decide?** It is not enough for the Federation to know what can be done. Governance must preserve who may do it, under what delegation, with what evidence, through which consent process, and how that authority can be reviewed, limited, transferred, or withdrawn.

The shared constitutional language is carried in the [One Eternal Scroll of ALO'ha](https://aifreedomtrustfederation.github.io/AI-Freedom-Trust/docs/pdf/one-eternal-scroll-of-aloha.pdf), while [SOP-ALOHA-001](https://github.com/AIFreedomTrustFederation/AI-Freedom-Trust/blob/main/SOP-ALOHA-001.md) gives the covenant a repeatable operational form.

---

## Book I — Authority as Relationship

Governance in the Federation is not the art of concentrating control. It is the practice of making authority visible enough that cooperation can occur without pretending everyone has equal permission to every action.

A person may govern their own identity and private data. A trust may delegate operational authority to a steward. A repository may permit an agent to run tests but not publish releases. A wallet may allow AI to explain a transaction but not sign it. A deployment system may automate health checks but still require human approval before switching production traffic. Governance is the structure that keeps those distinctions intact.

### Illuminated passage — the Governance Constellation

![Governance Constellation](https://raw.githubusercontent.com/AIFreedomTrustFederation/AI-Freedom-Trust/main/docs/images/aetherion/governance-constellation.png)

The constellation gives this repository its natural image. Each node retains a center; relationships carry permission and responsibility between them. The purpose of governance is not to make every node the same, but to make the relationships among them intelligible.

---

## Book II — What AetherianGovernance Owns

This repository owns the governance interface between constitutional principle and operational delegation. It should become the place where policies, consent models, decision records, delegated roles, dispute pathways, review processes, and governance manuals are organized in a form that other repositories can reference without inventing their own contradictory authority models.

Its federation boundaries are explicit:

- **AI-Freedom-Trust → Governance:** the doctrine layer provides constitutional philosophy, trust principles, ALO'ha, and the larger ethical frame.
- **AIFT-Genesis → Governance:** Genesis defines inherited trust identity and constitutional structures. Governance interprets those structures into delegated roles and decision processes for actual federation participation.
- **AIFT-OS ↔ Governance:** the control plane may discover permissions and request governed operations, but it does not create authority merely because it can orchestrate a command.
- **AIFT-Forge → Governance interfaces:** Forge can implement reusable approval, policy, and agent-boundary patterns without becoming the source of constitutional authority.
- **VPS ↔ Governance:** naming, registry, provider, routing, and production-deployment decisions may require governance rules, disputes, transfers, or approval thresholds.
- **Aetherion ↔ Governance:** wallet, treasury, value, custody, escrow, and economic policy require explicit human authority and auditable consent.
- **BookSmith ↔ Governance:** authorship, publication, rights, organization identity, marketplace visibility, and release authority remain governed relationships.

The repository already carries `FEDERATION.md`, `aift.repo.json`, and a manual structure under `docs/manual/`. Those are the beginning of the project-specific governance body and should remain aligned with one another.

---

## Book III — SOP-ALOHA-001 as a Governance Procedure

The covenant loop becomes a decision procedure:

```text
Receive → Inspect → Name → Propose → Consent → Act → Verify → Record → Return
```

**Receive** accepts a policy question, request for authority, dispute, proposal, role change, governance event, or high-impact operation. **Inspect** identifies the affected people, trusts, repositories, permissions, prior decisions, evidence, and applicable constitutional boundaries. **Name** identifies who currently holds authority, what authority is being requested, what risks or conflicts exist, and what decision process applies. **Propose** allows human or AI participants to frame options without confusing recommendation with authorization. **Consent** records the valid approval of the person or governed body whose authority is required. **Act** executes the decision through the proper system rather than bypassing governance with a technical shortcut. **Verify** confirms that the operational state now matches the authorized decision. **Record** preserves an intelligible decision record without exposing information that should remain private. **Return** communicates the outcome, authority exercised, unresolved obligations, and available review or appeal path.

Repository state can be checked with:

```bash
git status --short
git pull --ff-only
git status --short
```

### Current implementation and authorization boundary

The checked-in [`aift.repo.json`](aift.repo.json) declares `.aift/commands/verify.sh` as its `verify` command, matching the ready capability and the GitHub Actions workflow. The verifier checks federation JSON parsing and repository identity, ready capability paths, declared service events, and tracked shell-script syntax. It requires `python3`, `git`, and a checked-out repository. This is **repository-contract validation only**: it does not validate consent, role assignments, policy enforcement, signed approvals, or an audit trail. [`FEDERATION.md`](FEDERATION.md) now identifies the same `governance` layer as the manifest.

**Verification scope detail:** For `ready` capabilities, the verifier checks repository containment only for simple path-like command strings (such as `.aift/commands/verify.sh`); single-word and shell-composed commands are excluded from that path check. The declared `sync` command, `git remote -v && git status --short`, is therefore not executed or shell-validated by the verifier. Service and event declarations are checked for name consistency, not active event delivery or governance enforcement. To reproduce the CI checks from a clean checkout, run `.aift/commands/verify.sh` followed by `test -z "$(git status --porcelain)"`.


**Workspace portability and schema scope:** The absolute Android Termux paths in [`aift.repo.json`](aift.repo.json) (`workspacePath`, `federation.controlPlane`, and `federation.manifest`) and [`.aift/capabilities.json`](.aift/capabilities.json) (`path`) describe a particular local AIFT workspace layout. They do not install the control plane or prove those external paths exist on another machine. Clone the repository wherever appropriate and configure external federation integrations for that environment. The verifier does not check those external paths, fetch the manifest's `$schema` URL, or enforce its JSON Schema; passing CI establishes only the repository checks described above.

The [`docs/manual/README.md`](docs/manual/README.md) identifies a manual-source directory and delegates PDF/publication builds to BookSmith; it is not evidence of an implemented authorization engine. On the checked default branch, there is no root `GOVERNANCE.md` or `package.json` defining a governance test suite. Accordingly, the decision/consent procedure described above is a **constitutional design contract**, not proof that software currently enforces it.

**Manual coverage and publication boundary:** [`.aift/manual.json`](.aift/manual.json) lists `man0` through `man9` as the intended manual taxonomy, but the tracked [`docs/manual/source/`](docs/manual/source/) tree currently contains pages only under `man0` and `man7`. The [manual index](docs/manual/source/index.md) names the other sections without providing their source pages. The manifest marks `manualSource` as `ready`, while `pdfBuild`, `webPublish`, and the BookSmith `manual.build.pdf` builder are `planned`; its declared `docs/manual/assets` directory is also absent. The [Federation Integrity workflow](.github/workflows/federation-integrity.yml) checks federation manifests and tracked shell syntax, not manual completeness or generated publications. A passing workflow does not establish a complete manual or a published PDF.

Until a separately tested implementation exists, require an authorized human to review high-impact operations in the system that actually executes them. Preserve the identity of the approver, scope and expiration of delegation, policy version, decision evidence, and outcome in an appropriately access-controlled record. Do not treat an AI recommendation, a repository metadata field, or a successful Git command as authorization to transfer funds, publish private data, deploy production changes, or alter another person's rights.

Those commands verify repository synchronization, not governance legitimacy. A governance decision is verified by matching the action to the actual authority, consent, policy, and resulting system state.

---

## Book IV — Governance That Does Not Become Rule by Machine

The Federation welcomes AI into governance as an aid to memory, comparison, explanation, consistency checking, risk detection, policy retrieval, and preparation of decision records. AI may help a community understand what its own rules imply. It must not quietly become the sovereign interpreter whose recommendation cannot be questioned.

The long-term purpose of AetherianGovernance is therefore not to automate away deliberation. It is to make deliberation, delegation, consent, and accountability easier to preserve across a federation that may contain many people, agents, repositories, communities, and technical systems.

### The Return of the Word

In governance, the Word returns as authority made understandable. A request becomes a named question, the question enters a valid decision process, the decision becomes an authorized act, and the act returns as a record that still remembers who decided and why. Governance remains human when power can return to its source and answer for itself.

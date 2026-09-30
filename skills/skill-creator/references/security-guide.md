# Security and Supply-Chain Guide

Read this guide when a skill executes code, accesses networks or sensitive
data, performs writes, is distributed to others, or comes from an external
source.

## Threat model

A skill combines privileged instructions with potentially executable files.
Review it like software, not like passive documentation.

Threats include:

- Prompt injection in `SKILL.md`, references, templates, or remote content
- Malicious scripts, binaries, package hooks, or compromised dependencies
- Data exfiltration through network requests, logs, artifacts, or tool inputs
- Destructive filesystem, repository, cloud, database, or deployment actions
- Confused-deputy use of tools more powerful than the stated workflow needs
- Repository skills loaded from an untrusted clone
- Duplicate names or path precedence shadowing an approved skill
- Misleading descriptions that poison model selection
- Mutable remote references that change after review
- Stale instructions that encode obsolete or unsafe procedures

## Review checklist

1. Establish source, publisher, commit or version, license, and owner.
2. Read every bundled text file and inspect binary assets.
3. Search scripts for network, process, filesystem, credential, and dynamic
   execution behavior.
4. Inspect direct and transitive dependencies, install hooks, and version pins.
5. Verify requested tools and permissions are necessary for the stated job.
6. Identify all sensitive inputs and every possible output channel.
7. Confirm failure, retry, rollback, and partial-execution behavior.
8. Test in a restricted environment before broader distribution.

## Runtime controls

- Trust-gate repository skills before adding metadata to model context.
- Allowlist approved publishers and pin immutable versions or hashes.
- Sandbox scripts with least-privilege filesystem, network, and process access.
- Separate read capability from write capability.
- Require human approval for high-impact actions outside skill instructions.
- Deny secrets by default and provide short-lived credentials only when needed.
- Log the resolved skill path/version, activation, tools, approvals, outputs,
  and changed resources.
- Detect collisions and expose which skill won precedence.
- Re-review material updates and expire stale approvals.
- Maintain rollback and emergency revocation procedures.

The experimental `allowed-tools` field is not a portable security boundary.
Client behavior and syntax vary, and model instructions cannot replace external
authorization or sandbox enforcement.

## Current standard gaps

The open format does not define signatures, content digests, provenance,
registries, dependency manifests, permission manifests, vulnerability status,
revocation, or lifecycle policy. Supply these controls externally with source
control, signed artifacts, SBOMs, CI checks, a curated catalog, and deployment
policy.

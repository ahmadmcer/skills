# Security Policy

## Supported Versions

Security updates and patches are applied to the latest release on the `main` branch.

| Version   | Supported          |
| :-------- | :----------------- |
| `0.1.x`   | :white_check_mark: |
| `< 0.1.0` | :x:                |

---

## Reporting a Vulnerability

We take the security of this repository, its automation tools, and agent instructions seriously. If you discover a security vulnerability (such as a remote code execution vector in a script, accidental credential exposure, or prompt injection vulnerability):

1. **Do not create a public GitHub issue.**
2. Send an email to the repository maintainer: `ahmadmcer@gmail.com` with the subject line: `[SECURITY] Agent Skills Vulnerability Report`.
3. Include:
   - Affected skill name or script path.
   - Detailed description of the vulnerability.
   - Proof of Concept (PoC) or reproduction steps.
   - Potential impact and recommended remediation.

You will receive an acknowledgment within 48 hours, followed by regular updates until a patch is released.

---

## Secret Protection & Invariants

All skills in this repository must maintain strict credential protection:

- **Zero Hardcoded Secrets**: No real API keys, bearer tokens, passwords, private keys, or cloud credentials may be included in code, reference documentation, or evaluation prompt test cases.
- **Mock Token Syntax**: Use RFC-compliant dummy examples (`sk-dummy-12345`, `urn:uuid:...`, `change-me-in-production`).
- **Automated Verification**: The `git-commit` skill automatically runs regular expression scans to block commits containing potential secrets.

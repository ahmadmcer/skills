# DevSecOps & Threat Modeling

Read this guide when conducting security risk assessments, STRIDE threat modeling,
integrating shift-left automated security scanners, or implementing secure coding practices.

---

## 1. STRIDE Threat Modeling Framework

Threat modeling must occur during the design phase—before code is merged into main.
Apply the STRIDE model across every trust boundary, API endpoint, and data store:

| Threat Category                | Security Property Violated | Example Attack Vector                               | Mitigation Pattern                                                                               |
| :----------------------------- | :------------------------- | :-------------------------------------------------- | :----------------------------------------------------------------------------------------------- |
| **S - Spoofing**               | Authenticity               | Forging JWT token or impersonating caller           | Mutual TLS (mTLS), strict cryptographic signature validation, OAuth2/OIDC                        |
| **T - Tampering**              | Integrity                  | Modifying request payload in transit or database    | HMAC signatures, TLS 1.3, DB row-level integrity hashes, input validation schemas                |
| **R - Repudiation**            | Non-repudiability          | Malicious actor denies performing fraudulent action | Append-only tamper-evident audit logs with authenticated user context & timestamps               |
| **I - Information Disclosure** | Confidentiality            | Leaking API keys, PII in log files, or stack traces | Secret vaults, zero PII logging, sanitized error handlers, data masking at rest                  |
| **D - Denial of Service**      | Availability               | Exhausting server memory or database connections    | Token-bucket rate limiting, request size limits, connection pooling, backpressure                |
| **E - Elevation of Privilege** | Authorization              | Regular user calling administrative API route       | Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC), least-privilege scoping |

---

## 2. Shift-Left Security Pipeline

Security checks must be automated at every stage of the development pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      SHIFT-LEFT SECURITY GATES                         │
├─────────────────┬──────────────────┬─────────────────┬─────────────────┤
│ Local / Pre-commit│ Pull Request / CI│ Build / Staging │ Production      │
├─────────────────┼──────────────────┼─────────────────┼─────────────────┤
│ Secret Scanning │ SAST (Static)    │ DAST (Dynamic)  │ Runtime (RASP)  │
│ Linter Security │ Dependency (SCA) │ Container Scan  │ Cloud Posture   │
│ Branch Hygiene  │ License Audit    │ Infrastructure  │ Real-time WAF   │
└─────────────────┴──────────────────┴─────────────────┴─────────────────┘
```

### Static Application Security Testing (SAST)

- Scan source code for insecure functions, SQL injection vectors, command injection, and deserialization flaws.
- Gate PR merges on zero high/critical SAST findings.

### Software Composition Analysis (SCA)

- Scan direct and transitive dependencies against known vulnerability databases (NVD, CVE).
- Automated dependency lockfile audits (e.g., `npm audit`, `pip-audit`, `cargo audit`).
- Automatically block dependencies containing known CVSS score >= 7.0 vulnerabilities.

### Secret Detection

- Enforce pre-commit hooks to screen for high-entropy strings, private keys (`BEGIN RSA PRIVATE KEY`), cloud provider API tokens, and database connection URIs.
- Invalidate and rotate any credential discovered in git history immediately.

---

## 3. Secure by Design Invariants

1. **Principle of Least Privilege**: Services and database connections should possess only the absolute minimum permissions required to perform their intended function.
2. **Fail-Safe Defaults**: Access decisions default to "DENY". If an authorization check fails or errors out, execution must immediately halt.
3. **Defense in Depth**: Do not rely solely on network perimeters or API gateways; enforce authentication and authorization at the application, component, and database levels.
4. **Parameterized Queries**: Never concatenate raw strings into SQL, NoSQL, shell commands, or HTML templates. Always use parameterized queries or trusted ORM sanitizers.
5. **Zero Trust Architecture**: Every internal service-to-service call must authenticate and authorize independently.

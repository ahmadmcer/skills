# Pre-Commit Safety & Secret Leak Prevention

Read this guide when auditing staged diffs for security risks, handling credential
exposure, or troubleshooting author identity issues.

---

## 1. The Pre-Commit Security Threat

Accidentally committing credentials to a git repository is one of the most common
causes of security breaches. Once committed, secrets persist in `.git` history even
if deleted in a subsequent commit.

### High-Risk Files Never to Commit

- `.env`, `.env.local`, `.env.production`
- `*.pem`, `*.key`, `id_rsa`, `id_ed25519`
- `credentials.json`, `service-account.json`
- `*.p12`, `*.pfx`, `*.keystore`
- `npmrc` or `pip.conf` with embedded auth tokens

Ensure all such file patterns are listed in [.gitignore](file:///C:/Users/Personal/.agents/.gitignore).

---

## 2. Common Secret Patterns to Audit

Inspect staged diffs for the following patterns before committing:

| Credential Type        | Regex Signature                                                  | Action         |
| :--------------------- | :--------------------------------------------------------------- | :------------- |
| **AWS Access Key**     | `AKIA[0-9A-Z]{16}`                                               | BLOCK          |
| **GitHub Token**       | `ghp_[A-Za-z0-9_]{36}` or `github_pat_[A-Za-z0-9_]{82}`          | BLOCK          |
| **Google API Key**     | `AIza[0-9A-Za-z\\-_]{35}`                                        | BLOCK          |
| **Slack Token**        | `xox[baprs]-[0-9a-zA-Z-]{10,}`                                   | BLOCK          |
| **Stripe Secret Key**  | `sk_live_[0-9a-zA-Z]{24}`                                        | BLOCK          |
| **Private Key Header** | `-----BEGIN (RSA \|EC \|OPENSSH )?PRIVATE KEY-----`              | BLOCK          |
| **Generic Secret**     | `(password\|secret\|api_key\|token)\s*=\s*['\"][^'\"]{16,}['\"]` | REVIEW / BLOCK |

---

## 3. What to Do If a Secret is Staged

If secret scanning flags a file:

1. **Immediately Unstage the File**:
   ```bash
   git restore --staged <filename>
   ```
2. **Move Secrets to Environment Variables**:
   Replace the hardcoded secret with an environment variable reference (`process.env.API_KEY` or `os.environ.get("API_KEY")`).
3. **Add the Sensitive File to `.gitignore`**:
   ```bash
   echo "<sensitive-file>" >> .gitignore
   git add .gitignore
   ```

---

## 4. Git Author Identity Troubleshooting

If `git commit` fails with `Author identity unknown`:

```text
fatal: unable to auto-detect email address
```

### Resolution

1. Check existing identity in other projects or system configuration:
   ```bash
   git config --list --show-origin
   ```
2. Configure your identity:
   - For global configuration (applies to all repos for this user):
     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "you@example.com"
     ```
   - For local configuration (applies only to this specific repository):
     ```bash
     git config user.name "Your Name"
     git config user.email "you@example.com"
     ```
3. Re-run `git commit`.

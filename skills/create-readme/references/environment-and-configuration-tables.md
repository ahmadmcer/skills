# Environment and Configuration Tables

A standardized specification for documenting application configuration, environment variables (`.env`), security boundaries, and multi-environment setups in repository documentation.

---

## 1. The Standard Configuration Table Schema

Whenever a project requires environment variables, document them using this standardized 5-column table schema:

| Variable | Description | Type | Default | Required |
| :--- | :--- | :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection string | `string (URI)` | `postgresql://user:pass@localhost:5432/db` | **Yes** |
| `PORT` | Local HTTP listener port | `number` | `3000` | No |
| `NODE_ENV` | Runtime environment mode | `enum ('development' \| 'test' \| 'production')` | `'development'` | No |
| `JWT_SECRET` | 256-bit symmetric encryption key | `string` | - | **Yes** |
| `ENABLE_METRICS` | Expose Prometheus metrics on `/metrics` | `boolean` | `false` | No |

---

## 2. Public vs. Private Variable Boundaries

Document the security boundary between client-exposed variables and server-side secrets:

### 1. Client-Exposed Variables (Bundled into Browser JS)
Frameworks bundle variables with specific prefixes directly into client-side JavaScript assets:
- **Next.js**: `NEXT_PUBLIC_*` (e.g., `NEXT_PUBLIC_APP_URL`, `NEXT_PUBLIC_STRIPE_KEY`)
- **Vite**: `VITE_*` (e.g., `VITE_API_BASE_URL`)
- **Create React App**: `REACT_APP_*`

> [!CAUTION]
> **Client Exposure Warning**: Never prefix sensitive keys (database passwords, private signing keys, backend webhook secrets) with client-exposed prefixes like `NEXT_PUBLIC_` or `VITE_`.

### 2. Server-Only Secrets
Variables accessed exclusively within backend runtimes (Node.js servers, Python workers, Go microservices) that must **never** leak into client builds.

---

## 3. The `.env.example` Workflow

Every repository utilizing environment variables must maintain a tracked `.env.example` file:
```bash
# Copy the example file to your local development environment
cp .env.example .env.local
```

### Best Practices for `.env.example`:
1. **Include Sensible Local Defaults**: Provide working local credentials (e.g. `localhost:5432`).
2. **Never Commit Production Secrets**: Use placeholder descriptors (e.g. `your-32-char-random-secret-here`).
3. **Group by Service**: Organize variables logically into commented sections:
   ```env
   # ==============================================================================
   # Core Application Settings
   # ==============================================================================
   PORT=8000
   ENVIRONMENT=development

   # ==============================================================================
   # Database Configuration
   # ==============================================================================
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app_dev

   # ==============================================================================
   # Third-Party API Keys
   # ==============================================================================
   STRIPE_SECRET_KEY=sk_test_...
   AWS_S3_BUCKET_NAME=app-uploads-dev
   ```

---

## 4. Multi-Environment Configuration Matrix

When documenting multi-stage deployments (development, staging, production):

```markdown
### Environment Support

| Environment | Config File | Database Target | Auth Provider |
| :--- | :--- | :--- | :--- |
| **Local Dev** | `.env.local` | Local Docker container | Mock / Local Auth |
| **Staging** | CI Secrets | Managed Cloud DB (Staging) | Staging OAuth2 |
| **Production** | Vault / K8s Secrets | Multi-AZ High Availability DB | Production Auth |
```

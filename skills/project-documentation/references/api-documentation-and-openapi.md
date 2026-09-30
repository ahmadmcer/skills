# API Documentation & OpenAPI 3.1 Standards

> *"Good API documentation does not just document what endpoints exist; it provides the context, constraints, and realistic payloads necessary for a developer to make a successful API call in under two minutes."*

Whether documenting a public REST API, a GraphQL schema, or an internal SDK, API documentation serves as an immutable contract between software systems.

---

## 1. OpenAPI 3.1 Core Best Practices

OpenAPI 3.1 is aligned with JSON Schema Draft 2020-12, enabling full schema compatibility and expressive type definitions.

### 1. `summary` vs. `description`
- **`summary`**: A concise, plain-text phrase (under 60 characters) used in navigation trees, sidebar menus, and API client lists.
  - *Example*: `"Create user API key"`
- **`description`**: Multi-paragraph Markdown explaining the endpoint's purpose, security implications, required scopes, and side-effects.

### 2. Grouping with `tags`
Every operation must be assigned at least one tag. Tags define the primary navigation categories in tools like Redoc, Scalar, and Swagger UI.
- *Examples*: `Authentication`, `Organizations`, `Webhooks`, `Billing`.

### 3. Unique and Stable `operationId`
Every endpoint must have an unambiguous `operationId` written in camelCase or snake_case:
- *Good*: `createApiKey`, `listOrganizationMembers`, `cancelSubscription`.
- *Bad*: `post_keys`, `get1`.
- **Why**: `operationId` is used by SDK code generators to name client functions and serves as the permalink anchor in documentation portals.

---

## 2. Standardized Error Handling: RFC 9457 Problem Details

Never leave status codes undocumented, and never invent ad-hoc error formats (`{ "error": "failed" }`). Adhere to **RFC 9457 Problem Details for HTTP APIs**:

### Standard Error Schema:
```json
{
  "type": "https://api.example.com/errors/insufficient-permissions",
  "title": "Forbidden",
  "status": 403,
  "detail": "Your API token lacks the 'members:write' scope required to modify organization roles.",
  "instance": "/v2/organizations/org_9921/members/usr_4412",
  "invalid_params": [
    {
      "name": "role",
      "reason": "Must be one of ['admin', 'member', 'billing']"
    }
  ]
}
```

---

## 3. Formatting Markdown API Reference Pages

When converting OpenAPI specifications or code interfaces into Markdown documentation pages, structure each endpoint using this battle-tested layout:

```markdown
## `POST /v1/organizations/{orgId}/keys`

Generate a scoped API key for automated service integrations.

### Authentication
- **Bearer Token**: Requires `keys:write` scope.
- **Rate Limit**: 100 requests per minute.

### Path Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `orgId` | `string` | **Yes** | Unique organization identifier (`org_...`). |

### Request Body (`application/json`)

| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | Human-readable label for the key. | `"CI Deployment Worker"` |
| `scopes` | `string[]`| **Yes** | Array of permission scopes. | `["deployments:write"]` |
| `expires_in`| `integer` | No | Expiration TTL in seconds (default: 30 days). | `2592000` |

#### Request Example
```bash
curl -X POST "https://api.example.com/v1/organizations/org_123/keys" \
  -H "Authorization: Bearer sec_tok_9912" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CI Deployment Worker",
    "scopes": ["deployments:write"],
    "expires_in": 2592000
  }'
```

### Responses

| Status Code | Description | Schema |
| :--- | :--- | :--- |
| `201 Created` | API key created successfully. | `ApiKeyResponse` |
| `400 Bad Request` | Invalid parameters or malformed JSON. | `ProblemDetails` |
| `401 Unauthorized`| Missing or invalid authentication token. | `ProblemDetails` |
| `403 Forbidden` | Token lacks `keys:write` permission. | `ProblemDetails` |

#### Response Example (`201 Created`)
```json
{
  "id": "key_8812a4b",
  "name": "CI Deployment Worker",
  "token": "sk_live_51Msz... (shown only once)",
  "scopes": ["deployments:write"],
  "created_at": "2026-09-30T12:00:00Z",
  "expires_at": "2026-10-30T12:00:00Z"
}
```
```

---

## 4. Code-Level API References (TypeDoc, Sphinx, Rustdoc)

For software libraries and SDKs, code comments are the single source of truth for reference generation:

- **TypeScript / JavaScript (TSDoc / JSDoc)**:
  Use `@param`, `@returns`, `@throws`, `@example`, and `@deprecated`.
- **Python (Sphinx / Google Style docstrings)**:
  Document `Args:`, `Returns:`, `Raises:`, and `Example:`.
- **Rust (rustdoc)**:
  Use triple-slash `///` with `# Examples`, `# Panics`, and `# Errors` sections.

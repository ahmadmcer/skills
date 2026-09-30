# Semantic Versioning 2.0.0: Specification & Edge Cases

> *"Given a version number MAJOR.MINOR.PATCH, increment the:*  
> *1. MAJOR version when you make incompatible API changes,*  
> *2. MINOR version when you add functionality in a backward compatible manner, and*  
> *3. PATCH version when you make backward compatible bug fixes."*  
> — [semver.org](https://semver.org/spec/v2.0.0.html)

Semantic Versioning solves the "dependency hell" problem by establishing a formal social contract between package maintainers and software consumers.

---

## 1. The Core SemVer Grammar

A standard SemVer 2.0.0 version string consists of three mandatory non-negative integers separated by dots, with optional pre-release and build metadata extensions:

```text
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILDMETADATA]
```

### 1. MAJOR (`X.0.0`)
- **When to increment**: Any incompatible change to the public API, removal of public methods, changing parameter signatures, or bumping minimum language/runtime versions.
- **Reset rule**: When `MAJOR` increments, `MINOR` and `PATCH` are reset to `0`.

### 2. MINOR (`X.Y.0`)
- **When to increment**: Any backward-compatible new functionality added to the public API, or any feature marked as deprecated.
- **Reset rule**: When `MINOR` increments, `PATCH` is reset to `0`.

### 3. PATCH (`X.Y.Z`)
- **When to increment**: Any backward-compatible bug fix or internal defect remediation that preserves API compatibility.

---

## 2. The Zero-Major (`0.y.z`) Initial Development Lifecycle

The single most common source of confusion in SemVer is versioning pre-release software:

> **SemVer 2.0.0 Rule 4**: *"Major version zero (0.y.z) is for initial development. Anything MAY change at any time. The public API SHOULD NOT be considered stable."*

### Zero-Major Bumping Rules:
1. **Breaking Changes in `0.y.z`**:
   - Because `0` represents unstable software, breaking changes **do NOT bump to 1.0.0**.
   - Instead, breaking changes bump the **MINOR** version (`0.1.0` $\to$ `0.2.0`).
2. **Backward-Compatible Changes in `0.y.z`**:
   - Backward-compatible features and bug fixes bump the **PATCH** version (`0.1.0` $\to$ `0.1.1`).
3. **Graduating to `1.0.0`**:
   - Release `1.0.0` when the public API is stable and ready for general production adoption.
   - Releasing `1.0.0` is an explicit public declaration: *"Breaking changes will no longer occur without a MAJOR version increment."*

---

## 3. Pre-Release Identifiers & Lexicographical Precedence

Pre-release versions signal an unstable release preceding an official version tag (e.g. `1.0.0-alpha.1`).

### Grammar
- Appended to `PATCH` with a hyphen (`-`).
- Composed of dot-separated alphanumeric identifiers: `[0-9A-Za-z-]`.
- Numeric identifiers must not contain leading zeros (`1.0.0-alpha.01` is invalid).

### Precedence Evaluation Rules
Pre-release versions have **lower precedence** than the associated normal version:
```text
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-rc.1 < 1.0.0
```

When comparing two pre-release versions with the same major, minor, and patch:
1. **Identifiers separated by dots are compared from left to right**.
2. **Pure numeric identifiers are compared numerically**:
   - `1.0.0-alpha.2` < `1.0.0-alpha.10` (numeric comparison: 2 < 10).
3. **Identifiers with letters or hyphens are compared lexically (ASCII sort)**:
   - `1.0.0-alpha` < `1.0.0-beta`.
4. **Numeric identifiers always have lower precedence than non-numeric identifiers**:
   - `1.0.0-1` < `1.0.0-beta`.
5. **A larger set of pre-release fields has a higher precedence than a smaller set, if all preceding identifiers are equal**:
   - `1.0.0-rc.1` < `1.0.0-rc.1.1`.

---

## 4. Build Metadata

Build metadata conveys continuous integration details, commit hashes, or build timestamps:
```text
1.0.0+20260930
1.0.0-beta.1+sha.5114f85
```
- Appended with a plus sign (`+`).
- Composed of dot-separated alphanumeric identifiers.
- **Critical Invariant**: Build metadata **MUST be ignored** when determining version precedence. Two versions that differ only in build metadata have identical precedence:
  - `1.0.0+build.1` == `1.0.0+build.2` in SemVer evaluation.

---

## 5. What Constitutes a Breaking Change?

| Action | API Impact | Required SemVer Bump |
| :--- | :--- | :--- |
| **Renaming an exported function/class** | Breaks consumer call sites | **MAJOR** |
| **Adding a new required parameter to a function** | Breaks existing function calls | **MAJOR** |
| **Adding a new optional parameter (with default)** | Backward compatible | **MINOR** |
| **Removing an exported method or CLI flag** | Incompatible removal | **MAJOR** |
| **Changing a method's return type** | Incompatible interface change | **MAJOR** |
| **Bumping minimum Node.js / Python / Java version** | Breaks environments running older runtimes | **MAJOR** |
| **Fixing a bug that changes accidental behavior** | If users relied on a bug, document as bugfix unless standard | **PATCH** (or **MAJOR** if changing documented contracts) |
| **Performance optimization with identical I/O** | Fully compatible internal refactor | **PATCH** |
| **Adding a new method to an exported interface** | In languages with strict interfaces (TypeScript, Go, Rust), this breaks external implementers | **MAJOR** (unless default methods supported) |

# The Diátaxis Documentation Framework

> _"Documentation is not one thing. It is four things. If you do not consciously separate them, they will collapse into each other, creating a tangled, unnavigable mess."_  
> — Daniele Procida, creator of [Diátaxis](https://diataxis.fr/)

The Diátaxis framework organizes technical documentation into four distinct quadrants based on two fundamental axes: **Action vs. Knowledge** and **Study vs. Work**.

```
                           ACTION
                             ▲
                             │
            TUTORIALS        │       HOW-TO GUIDES
        (Learning-oriented)  │    (Problem-oriented)
                             │
   STUDY ────────────────────┼──────────────────── WORK
                             │
           EXPLANATION       │         REFERENCE
     (Understanding-oriented)│   (Information-oriented)
                             │
                             ▼
                         KNOWLEDGE
```

---

## 1. The Four Quadrants

### 1. Tutorials (Learning-Oriented / Study + Action)

- **User's Goal**: _"I am a beginner; teach me how this system works."_
- **Primary Function**: To build skills and confidence through a guided, step-by-step hands-on experience.
- **Key Characteristics**:
  - Takes the learner from start to finish through a concrete project.
  - Must produce an immediate, visible result (e.g., a running web server, a created database).
  - Contains **zero choices or branching logic**: do not give options (_"You can use either SQLite or PostgreSQL"_ $\to$ force SQLite).
  - Explains only what is strictly necessary to complete the lesson; defer deep theoretical discussions to _Explanation_.
  - Every step must work 100% reliably. A broken tutorial creates immediate user distrust.
- **Example Titles**:
  - _"Building Your First REST API in 10 Minutes"_
  - _"Getting Started with Antigravity: From Zero to Deployed Agent"_

### 2. How-To Guides (Problem-Oriented / Work + Action)

- **User's Goal**: _"I have a real-world task to perform; show me how to solve it."_
- **Primary Function**: To provide a recipe that guides an experienced user through a specific problem.
- **Key Characteristics**:
  - Assumes basic competence: does not teach foundational concepts.
  - Goal-driven: focuses on a real-world problem encountered in daily work.
  - Step-by-step sequence of actionable instructions.
  - Focuses on the path to the solution; leaves technical parameter descriptions to _Reference_.
  - Flexible: may address varying environments (e.g., Docker, Kubernetes, AWS).
- **Example Titles**:
  - _"How to Configure OAuth2 Authentication with Okta"_
  - _"How to Migrate a PostgreSQL Database with Zero Downtime"_
  - _"How to Enable Distributed Tracing with OpenTelemetry"_

### 3. Reference (Information-Oriented / Work + Knowledge)

- **User's Goal**: _"I need exact technical facts, flags, schemas, or syntax."_
- **Primary Function**: To provide an austere, authoritative description of the machinery.
- **Key Characteristics**:
  - Consulted rather than read from top to bottom.
  - Structured to mirror the code, architecture, or CLI syntax.
  - Comprehensive, neutral, and factual.
  - Contains signature definitions, parameter types, default values, return schemas, and status codes.
  - Free from discursive storytelling or tutorial hand-holding.
- **Example Titles**:
  - _"CLI Reference: `agy deploy` Flags & Options"_
  - _"REST API Reference: `/v2/organizations/{id}/members`"_
  - _"Configuration Schema Reference (`config.yaml`)"_

### 4. Explanation (Understanding-Oriented / Study + Knowledge)

- **User's Goal**: _"I want to understand the architecture, concepts, and design decisions."_
- **Primary Function**: To illuminate the system from a high vantage point, providing context and rationale.
- **Key Characteristics**:
  - Discursive and explanatory: answers the question _"Why?"_ rather than _"How?"_.
  - Explores historical context, design trade-offs, and alternative approaches considered.
  - Connects multiple components into a coherent mental model.
  - Free from step-by-step command line instructions.
- **Example Titles**:
  - _"Understanding Our Distributed Consensus Architecture"_
  - _"Why We Chose Event Sourcing over Traditional CRUD"_
  - _"Memory Management & Garbage Collection in the Runtime"_

---

## 2. Diátaxis Comparison Matrix

| Attribute       | Tutorials             | How-To Guides          | Reference              | Explanation            |
| :-------------- | :-------------------- | :--------------------- | :--------------------- | :--------------------- |
| **Orientation** | Learning              | Problem-solving        | Information            | Understanding          |
| **Form**        | Lesson                | Recipe                 | Dictionary / Blueprint | Essay / Overview       |
| **User State**  | Beginner              | Competent practitioner | Busy professional      | Curious explorer       |
| **Voice**       | Encouraging, paternal | Direct, instructional  | Objective, austere     | Discursive, reflective |
| **Content**     | Practical steps       | Concrete solutions     | Factual specifications | Theoretical context    |
| **Branching**   | Strictly none         | Minimal                | Organized by API/CLI   | Conceptual narrative   |

---

## 3. The Content Sprawl Anti-Pattern

Content sprawl occurs when authors mix multiple quadrants into a single document:

```
[CONTENT SPRAWL DISASTER]
Title: "Getting Started with Redis Caching"
- Paragraph 1: What is in-memory caching? (Explanation)
- Paragraph 2: Installing Redis via apt-get (Tutorial)
- Paragraph 3: Complete table of all 140 Redis CLI flags (Reference)
- Paragraph 4: Troubleshooting cluster split-brain scenarios (How-To)
```

**Why it fails**:

- The beginner gets intimidated by 140 CLI flags and abandons the tutorial.
- The experienced engineer looking for the cluster troubleshooting step has to scroll through beginner installation guides.
- The reference user scanning for a flag is frustrated by narrative explanations.

### The Diátaxis Remedy:

Split the document into four distinct files:

1. `docs/tutorials/01-redis-quickstart.md` (Pure tutorial: install and set one key).
2. `docs/how-to/recover-split-brain-redis.md` (Focused recipe).
3. `docs/reference/redis-cli-flags.md` (Table of flags and options).
4. `docs/explanation/in-memory-caching-architecture.md` (Why caching matters and eviction policies).

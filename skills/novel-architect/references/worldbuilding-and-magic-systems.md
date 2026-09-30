# Worldbuilding and Magic Systems Guide

A comprehensive architectural reference for designing immersive speculative worlds, magic systems, and technological frameworks based on **Brandon Sanderson's Laws of Magic** and the **Iceberg Principle**.

---

## 1. Sanderson's Laws of Magic

Brandon Sanderson formulated four fundamental laws for speculative worldbuilding and magic system design:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      SANDERSON'S LAWS OF MAGIC                         │
├────────────────────────────────────────────────────────────────────────┤
│ FIRST LAW:   Understandability Proportionality                         │
│              An author's ability to solve problems with magic in a     │
│              satisfying way is directly proportional to how well the   │
│              reader understands said magic.                            │
│                                                                        │
│ SECOND LAW:  Limitations > Powers                                      │
│              Flaws, costs, vulnerabilities, and limits are far more    │
│              interesting and dramatic than what the power can do.      │
│                                                                        │
│ THIRD LAW:   Extrapolate Before Adding                                 │
│              Expand the deep consequences of existing elements before  │
│              introducing brand new magical or technological powers.    │
│                                                                        │
│ ZEROTH LAW:  Err on the Side of Awesome                                │
│              Never let worldbuilding rules stifle excitement and fun.  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Hard Magic vs. Soft Magic Spectrum

Every magic or speculative technological system exists along a continuum:

```
SOFT MAGIC ◄─────────────────────────────────────────────► HARD MAGIC
(Tolkien / Ghibli)                                     (Mistborn / Sci-Fi)
- Wonder, awe, mystery                                 - Predictable rules, clear costs
- Cannot solve climactic plots                         - Serves as a problem-solving tool
- Evokes danger and the unknown                        - Feels fair, rational, and earned
```

### 1. Hard Magic (Rule-Based Systems)

- The reader knows the rules, fuel source, costs, and exact limitations.
- Characters can use magic to solve problems like a scientific discipline or martial art.
- The dramatic tension comes from _how_ the character applies known constraints under stress.
- _Examples_: Brandon Sanderson's Allomancy (_Mistborn_), Fullmetal Alchemist's Alchemy, Avatar's Bending.

### 2. Soft Magic (Wonder-Based Systems)

- The rules remain mysterious, ethereal, or divine.
- Used to generate wonder, dread, and atmospheric scale.
- **Rule of Thumb**: Soft magic can create problems for the protagonist, but should rarely be used to solve the primary climax (which would feel like _deus ex machina_).
- _Examples_: Gandalf in _The Lord of the Rings_, Miyazaki's _Spirited Away_.

---

## 3. The Second Law: Engineering Limitations & Costs

When designing an ability, focus 80% of your effort on its boundaries:

| Limitation Category        | Description                                              | Example                                                                        |
| :------------------------- | :------------------------------------------------------- | :----------------------------------------------------------------------------- |
| **Material Cost (Fuel)**   | What resource must be consumed to activate it?           | Ingesting specific metals; rare gems; burning calories.                        |
| **Physical / Health Toll** | What damage or exhaustion does the user suffer?          | Blindness, cellular degradation, neurological strain.                          |
| **Tactical Weakness**      | Under what conditions does the power fail completely?    | Ineffective against iron; requires direct eye contact; negated by salt water.  |
| **Moral / Spiritual Toll** | What does using the power do to the user’s soul or mind? | Causes memory loss; induces uncontrollable paranoia; demands moral compromise. |
| **Societal Taboo**         | How does the law or religion view practitioners?         | Hunted by inquisitors; branded as outcasts; monopolized by royal dynasties.    |

---

## 4. The Third Law: Deep Societal Extrapolation

Never drop a magical or advanced technological element into a standard European medieval setting without asking how it transforms society:

- **Military**: If commoners can throw firebolts, castle walls become obsolete, and phalanx armor shifts from heavy plate to insulated leather.
- **Economy**: If healing magic is readily available, how does it disrupt life expectancy, pension systems, succession laws, and embalming guilds?
- **Law & Crime**: If telepaths exist, how does a court of law verify testimony without violating mental privacy? What prevents counterfeiters in an alchemy-rich city?

---

## 5. The World Bible Architecture Schema

Use this standard template when documenting your novel's setting in `00_BIBLE/world_bible.md`:

```markdown
# World Bible: [World / Realm Name]

### 1. Cosmology & Metaphysics

- **Origin Myth**: [How the world was created or discovered]
- **The Core Axiom**: [The fundamental rule of this reality]
- **The Supernatural / Tech Spectrum**: [Hard vs Soft / High vs Low Tech]

### 2. Geography & Ecology

- **Key Regions & Climate**: [Major biomes and geographical boundaries]
- **Unique Flora / Fauna**: [Speculative creatures and ecological niches]
- **Settlement Patterns**: [Where populations concentrate and why]

### 3. Factions & Geopolitics

- **Dominant Powers**: [Empires, megacorporations, kingdoms, alliances]
- **Political Systems**: [Oligarchy, theocracy, democracy, warlords]
- **Active Conflicts**: [Ongoing wars, border skirmishes, cold wars]

### 4. Economy & Resources

- **Currencies & Trade**: [What is traded and what holds true value?]
- **Resource Scarcity**: [The critical resource driving competition (e.g. spice, water, oil, mana)]

### 5. Culture & Daily Life

- **Social Stratification**: [Class hierarchies, caste systems, slavery]
- **Religious Practices & Taboos**: [What is revered? What is strictly forbidden?]
- **Sensory Textures**: [Architecture styles, street food, clothing fabrics, smells]
```

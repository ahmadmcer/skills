# Prose Rhythm, Sentence Mechanics & Linguistic Auditing

> *"This sentence has five words. Here are five more words. Five-word sentences are fine. But several together become monotonous. Listen to what is happening. The writing is getting boring. The sound of it drones. It's like a stuck record. The ear demands some variety.*  
>  
> *Now listen. I vary the sentence length, and I create music. Music. The writing sings. It has a pleasant rhythm, a lilt, a harmony. I use short sentences. And I use sentences of medium length. And sometimes, when I am certain the reader is rested, I will engage him with a sentence of considerable length, a sentence that burns with energy and builds with all the impetus of a crescendo, the roll of the drums, the crash of the cymbals—sounds that say listen to this, it is important."*  
> — Gary Provost, *100 Ways to Improve Your Writing* (1985)

Sentence mechanics are the musical notation of prose. A story with brilliant plotting and rich character psychology will still fall flat if its sentences drone along in uniform, unvarying cadence. Masterful novelists compose prose like symphonies: controlling tempo, syncopation, and weight at the syllable level.

---

## 1. Gary Provost's Law of Sentence Musicality

The human ear naturally fatigues when exposed to repetitive syntactic lengths. Sentences of identical length create an acoustic monotone that induces subconscious reader boredom.

### The Three Sentence Velocity Classes

```
┌────────────────────────────────────────────────────────┐
│               THREE SENTENCE VELOCITY CLASSES          │
├────────────────────────────────────────────────────────┤
│ 1. Short (1 - 7 words)   → Impact, shock, panic, stops │
│ 2. Medium (8 - 18 words) → Narrative momentum, spine  │
│ 3. Long (19 - 35+ words) → Crescendo, memory, texture  │
└────────────────────────────────────────────────────────┘
```

#### 1. Short Sentences (1–7 words)
- **Acoustic Feel**: Staccato, immediate, sharp.
- **Psychological Function**: Mimics rapid heart rate, sudden physical blows, or irrevocable decisions.
- *Examples*:
  > *"The rope snapped."*  
  > *"He didn't run."*  
  > *"Blood in the snow."*

#### 2. Medium Sentences (8–18 words)
- **Acoustic Feel**: Conversational, steady, muscular.
- **Psychological Function**: Forms the narrative backbone. Carries physical action from point A to point B without calling attention to the prose itself.
- *Example*:
  > *"Kael pulled the collar of his coat tight against the biting harbor wind and stepped onto the wharf."*

#### 3. Long Sentences (19–35+ words)
- **Acoustic Feel**: Lyrical, rolling, cumulative, sweeping.
- **Psychological Function**: Used for contemplative reverie, sensory accumulation, or building emotional crescendos that sweep the reader forward.
- *Example*:
  > *"He watched the lanterns flicker across the lower bay, their golden ribbons stretching over water so dark and still it seemed less like sea and more like obsidian, holding within its depths every wreck and drownling the port had claimed over two centuries of trade."*

---

## 2. Parataxis vs. Hypotaxis

How clauses are joined together fundamentally alters the velocity and psychological tone of a scene.

### Parataxis: The Accelerating Drive
- **Definition**: Placing clauses side by side with simple coordinating conjunctions (*and*, *but*, *or*) or no conjunctions at all (asyndeton). Clauses have equal grammatical weight.
- **Narrative Function**: Action scenes, breathless escapes, feverish panic, Hemingwayesque clarity.
- **Example**:
  > *"He kicked the stall door open, and the mare reared back, and his shoulder clipped the wooden lintel, but he kept his grip on the reins and dragged her into the rain."*

### Hypotaxis: The Analytical Web
- **Definition**: Arranging clauses in a hierarchical structure using subordinating conjunctions (*although*, *because*, *since*, *while*, *as if*, *whenever*).
- **Narrative Function**: Nuanced psychological deliberation, political intrigue, scholarly contemplation, high-stakes moral dilemmas.
- **Example**:
  > *"Although Lord Arlen had assured the council that the granaries were stocked for winter, Marcus knew, having audited the eastern manifests himself, that the supplies would expire before the second frost."*

---

## 3. The Filter Word Audit

Sensory filter words are the single most pervasive amateur habit in novel manuscripts. They turn active drama into passive reports.

### Common Filter Words to Purge

| Category | Filter Words | Detection Regex Pattern |
| :--- | :--- | :--- |
| **Vision** | *saw, watched, looked at, noticed, observed, gazed, peered* | `\b(saw\|watched\|looked at\|noticed\|observed\|gazed at\|peered at)\b` |
| **Auditory** | *heard, listened to, sounded like* | `\b(heard\|listened to\|sounded like)\b` |
| **Cognitive** | *realized, thought, wondered, decided, remembered, pondered* | `\b(realized\|wondered\|decided\|pondered\|occurred to)\b` |
| **Tactile** | *felt, could feel, touched* | `\b(felt\|could feel)\b` |
| **Hedge Words** | *seemed, appeared, looked as though* | `\b(seemed\|appeared to be\|looked as though)\b` |

### The Target Benchmark
- **Acceptable Density**: Less than **3 filter words per 1,000 words** of narrative prose.
- **Red Flag**: Greater than **8 filter words per 1,000 words** indicates detached, mediated narration requiring immediate conversion to Deep POV.

---

## 4. Smothered Verbs & Nominalizations

A **nominalization** occurs when a dynamic verb is smothered into a bloated abstract noun, requiring a weak auxiliary verb to operate:

```
[SMOTHERED / WEAK]  →  He came to the realization that the guard was asleep.
[KINETIC / STRONG]  →  The guard was asleep.
```

### The Smothered Verb Transformation Table

| Smothered Verb Phrase | Kinetic Active Verb |
| :--- | :--- |
| *made an entrance into* | *entered / stormed* |
| *held a suspicion that* | *suspected* |
| *engaged in a conversation* | *spoke / argued* |
| *came to a halt* | *halted / stopped* |
| *gave an indication of* | *signaled / indicated* |
| *provided an explanation for* | *explained* |
| *took into consideration* | *considered / weighed* |
| *effected an escape from* | *escaped / fled* |

---

## 5. Weak Verb Dependencies (The "Was/Were" Epidemic)

Continuous reliance on copular verbs (*was, were, is, are*) and passive progressives (*was running*, *were searching*) bleeds kinetic energy from action sequences:

```
[WEAK / PASSIVE PROGRESSIVE]
The fire was spreading across the rafters, and sparks were falling into the dry hay.

[STRONG / DIRECT KINETIC]
Fire raced across the rafters, showering sparks into the dry hay.
```

### Quick Diagnostic Heuristic
If more than **20%** of sentences on a page rely on *was* or *were* as the main predicate verb, the prose is suffering from sluggish narrative anemia. Convert static state descriptions into physical motion.

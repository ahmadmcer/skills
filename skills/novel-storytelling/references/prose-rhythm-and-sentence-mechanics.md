# Prose Rhythm, Sentence Mechanics & Linguistic Auditing

> _"This sentence has five words. Here are five more words. Five-word sentences are fine. But several together become monotonous. Listen to what is happening. The writing is getting boring. The sound of it drones. It's like a stuck record. The ear demands some variety._
>
> _Now listen. I vary the sentence length, and I create music. Music. The writing sings. It has a pleasant rhythm, a lilt, a harmony. I use short sentences. And I use sentences of medium length. And sometimes, when I am certain the reader is rested, I will engage him with a sentence of considerable length, a sentence that burns with energy and builds with all the impetus of a crescendo, the roll of the drums, the crash of the cymbals—sounds that say listen to this, it is important."_  
> — Gary Provost, _100 Ways to Improve Your Writing_ (1985)

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
- _Examples_:
  > _"The rope snapped."_  
  > _"He didn't run."_  
  > _"Blood in the snow."_

#### 2. Medium Sentences (8–18 words)

- **Acoustic Feel**: Conversational, steady, muscular.
- **Psychological Function**: Forms the narrative backbone. Carries physical action from point A to point B without calling attention to the prose itself.
- _Example_:
  > _"Kael pulled the collar of his coat tight against the biting harbor wind and stepped onto the wharf."_

#### 3. Long Sentences (19–35+ words)

- **Acoustic Feel**: Lyrical, rolling, cumulative, sweeping.
- **Psychological Function**: Used for contemplative reverie, sensory accumulation, or building emotional crescendos that sweep the reader forward.
- _Example_:
  > _"He watched the lanterns flicker across the lower bay, their golden ribbons stretching over water so dark and still it seemed less like sea and more like obsidian, holding within its depths every wreck and drownling the port had claimed over two centuries of trade."_

---

## 2. Parataxis vs. Hypotaxis

How clauses are joined together fundamentally alters the velocity and psychological tone of a scene.

### Parataxis: The Accelerating Drive

- **Definition**: Placing clauses side by side with simple coordinating conjunctions (_and_, _but_, _or_) or no conjunctions at all (asyndeton). Clauses have equal grammatical weight.
- **Narrative Function**: Action scenes, breathless escapes, feverish panic, Hemingwayesque clarity.
- **Example**:
  > _"He kicked the stall door open, and the mare reared back, and his shoulder clipped the wooden lintel, but he kept his grip on the reins and dragged her into the rain."_

### Hypotaxis: The Analytical Web

- **Definition**: Arranging clauses in a hierarchical structure using subordinating conjunctions (_although_, _because_, _since_, _while_, _as if_, _whenever_).
- **Narrative Function**: Nuanced psychological deliberation, political intrigue, scholarly contemplation, high-stakes moral dilemmas.
- **Example**:
  > _"Although Lord Arlen had assured the council that the granaries were stocked for winter, Marcus knew, having audited the eastern manifests himself, that the supplies would expire before the second frost."_

---

## 3. The Filter Word Audit

Sensory filter words are the single most pervasive amateur habit in novel manuscripts. They turn active drama into passive reports.

### Common Filter Words to Purge

| Category        | Filter Words                                                 | Detection Regex Pattern                                                 |
| :-------------- | :----------------------------------------------------------- | :---------------------------------------------------------------------- |
| **Vision**      | _saw, watched, looked at, noticed, observed, gazed, peered_  | `\b(saw\|watched\|looked at\|noticed\|observed\|gazed at\|peered at)\b` |
| **Auditory**    | _heard, listened to, sounded like_                           | `\b(heard\|listened to\|sounded like)\b`                                |
| **Cognitive**   | _realized, thought, wondered, decided, remembered, pondered_ | `\b(realized\|wondered\|decided\|pondered\|occurred to)\b`              |
| **Tactile**     | _felt, could feel, touched_                                  | `\b(felt\|could feel)\b`                                                |
| **Hedge Words** | _seemed, appeared, looked as though_                         | `\b(seemed\|appeared to be\|looked as though)\b`                        |

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

| Smothered Verb Phrase         | Kinetic Active Verb    |
| :---------------------------- | :--------------------- |
| _made an entrance into_       | _entered / stormed_    |
| _held a suspicion that_       | _suspected_            |
| _engaged in a conversation_   | _spoke / argued_       |
| _came to a halt_              | _halted / stopped_     |
| _gave an indication of_       | _signaled / indicated_ |
| _provided an explanation for_ | _explained_            |
| _took into consideration_     | _considered / weighed_ |
| _effected an escape from_     | _escaped / fled_       |

---

## 5. Weak Verb Dependencies (The "Was/Were" Epidemic)

Continuous reliance on copular verbs (_was, were, is, are_) and passive progressives (_was running_, _were searching_) bleeds kinetic energy from action sequences:

```
[WEAK / PASSIVE PROGRESSIVE]
The fire was spreading across the rafters, and sparks were falling into the dry hay.

[STRONG / DIRECT KINETIC]
Fire raced across the rafters, showering sparks into the dry hay.
```

### Quick Diagnostic Heuristic

If more than **20%** of sentences on a page rely on _was_ or _were_ as the main predicate verb, the prose is suffering from sluggish narrative anemia. Convert static state descriptions into physical motion.

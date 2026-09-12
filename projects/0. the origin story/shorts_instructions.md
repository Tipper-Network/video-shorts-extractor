# Agent Directive: Extraction & Assembly Strategy for Shorts

**Source Video:** [The Origin Story](https://studio.youtube.com/video/PJfvjQMPbGo) (1:07:30 total runtime)  
**Objective:** Parse long-form philosophical narrative into focused vertical Shorts (30–60s) connecting personal growth, startup strategy, and mindset.

---

## 1. Execution Engine Recommendation
* **Model:** **Gemini 1.5 Pro**
* **Capability Match:** Multimodal audio/video token processing ensures exact boundary cuts on spoken syllables, accurate whiteboard character alignment, and zero caption desynchronization across multi-point story splices.

---

## 2. Universal Agent Assembly Rules
* **Aspect Ratio:** 9:16 (1080x1920).
* **Crop Dynamics:** Center framing on speaker by default; dynamically punch into the whiteboard quadrant when diagrams/keywords are being annotated.
* **Audio Trimming:** Strip leading/trailing dead space (>250ms). Normalize voice track to -14 LUFS.
* **Captions:** Center-screen, high-contrast, dynamic kinetic subtitles.

---

## 3. Short Strategies & Timestamp Extraction Breakdown

### Strategy 1: "Reaction vs. Response" (The Ego Check)
* **Theme:** Psychological transition from automatic defensiveness to deliberate communication.
* **Timestamp Extraction Plan:**
  * **Clip A (Hook):** `05:40 - 06:12` (The question: *"What if there’s a 5% chance I'm the idiot?"*)
  * **Clip B (Concept):** `07:15 - 08:05` (Distinction between emotional Reaction vs. deliberate Response)
* **Agent Assembly Prompt:**
  1. Stitch Clip A directly into Clip B using a micro-jumpcut on the breath.
  2. Overlay text banner at 0:00: *"The question that broke my ego"*.
  3. Dynamic Subtitles: Highlight "Reaction" in red and "Response" in green.

---

### Strategy 2: "The Island Bum vs. Owning the Island" (The Wake-Up Call)
* **Theme:** How passive drift turns childhood jokes into harsh realities, and recognizing the moment to pivot.
* **Timestamp Extraction Plan:**
  * **Clip A (Setup):** `31:35 - 32:20` (Childhood declaration of owning an island vs. living as a bum)
  * **Clip B (Turning Point):** `33:45 - 34:50` (The storm on the shore, the fisherman, and the mirror realization)
* **Agent Assembly Prompt:**
  1. Cut straight from the cafe reflection into the storm takeaway.
  2. Visual Framing: Tighten frame to a close-up during Clip B to heighten narrative intimacy.
  3. Audio: Subtly drop background noise/music during the final sentence of Clip B for maximum impact.

---

### Strategy 3: "Focus vs. Tunnel Vision" (Startup & Execution Trap)
* **Theme:** Identifying the exact point where persistence becomes counterproductive blindness.
* **Timestamp Extraction Plan:**
  * **Clip A (The Dilemma):** `56:20 - 57:05` (Defining how clear focus mutates into stubborn tunnel vision)
  * **Clip B (The Resolution):** `57:45 - 58:35` (Knowing when to pivot without registering it as personal failure)
* **Agent Assembly Prompt:**
  1. Splice Clip A and B seamlessly.
  2. Punch-in zoom (1.15x) when the transition between Focus and Tunnel Vision is explained.
  3. End on the punchline sentence before topic shifts.

---

### Strategy 4: #WisdomBit — "Playing a Game WITH Life"
* **Theme:** Shifting from victim mindset (*Game OF Life*) to co-creator (*Game WITH Life*).
* **Timestamp Extraction Plan:**
  * **Target Range:** `03:30 - 04:15` (Direct philosophical breakdown)
* **Agent Assembly Prompt:**
  1. Extract continuous 40-second block.
  2. Subtitle Focus: Emphasize "OF" vs. "WITH" in bold, distinct typography.
  3. Cut immediately on the concluding philosophical statement.

---

### Strategy 5: #WisdomBit — "The 'Moving House' Phase"
* **Theme:** Normalizing the messy chaos that occurs during major life/business transitions.
* **Timestamp Extraction Plan:**
  * **Target Range:** `1:03:15 - 1:04:10` (The transitional moving house analogy)
* **Agent Assembly Prompt:**
  1. Extract single continuous narrative block.
  2. Fast-paced caption flow matching the conversational rhythm.
  3. Outro: End on the realization that temporary disorder is proof of forward movement.

---

## 4. Post-Assembly Metadata Directive
* Set **Related Video** for all generated Shorts to: `[The Origin Story](https://studio.youtube.com/video/PJfvjQMPbGo)` in YouTube Studio to drive viewers from standalone clips into the full long-form experience.
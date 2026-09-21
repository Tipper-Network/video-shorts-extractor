# Agent Directive: Extraction & Assembly Strategy for Shorts

**Source Video:** [The Origin Story](https://studio.youtube.com/video/PJfvjQMPbGo) (1:07:30 total runtime)  
**Objective:** Parse long-form philosophical narrative into focused vertical Shorts (50–75s, floor 50s) connecting personal growth, startup strategy, and mindset.

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
* **Theme block:** `05:50 - 10:08` — include the respond closer; do not stop at `09:40`.
* **Required hinge:** `07:34 - 07:46` + `07:50 - 08:02` — *"I'm an idiot, of course I'm not. But what if. I could do better."* v1 failed because this turn was cut.
* **Required close:** `10:04 - 10:08` — *"when I gave myself a chance to respond, I realized there's a whole lot that was happening."*
* **Three versions:**
  * **hook-first:** question → you say no → I'm not / I could → list as respond → closer
  * **story-first (winning so far):** 5% hook on the front → decisions / I asked the question → *what happens when you ask* / you say no → I'm not / I could → list → closer
  * **contiguous:** failed as a short — story only, no capture/resolve. Do not ship.
  * **story-first hinge:** drop `07:38–07:54` (output ~1:00–1:12) — “but what if” then “but I could” is the same turn twice.
* **Skip only:** handwriting `07:22–07:34`, "sorry" `07:46–07:50` and `09:04–09:12`. Do not skip the hinge.

---

### Strategy 2: "The Island Bum vs. Owning the Island" (The Wake-Up Call)
* **Theme:** How passive drift turns childhood jokes into harsh realities, and recognizing the moment to pivot.
* **Theme block:** `31:00 - 35:12`
* **Shared close:** `34:32 - 35:08` — include "move forward and reconnect with the better version of this life" (do not out at `34:56`).
* **Three versions** (same theme — compare, keep what connects):
  * **hook-first:** bet `31:52–32:04` → boats/storm `32:32–32:48` → close
  * **story-first:** broke/exposed `31:08–31:24` → telling her the bet `31:48–32:04` → close
  * **contiguous:** close window only `34:32–35:08`
* **Do not:** splice childhood bet into cafe poverty. That jump is why v1 felt disconnected. `33:45–34:32` is projection tangent.

---

### Strategy 3: "Focus vs. Tunnel Vision" (Startup & Execution Trap)
* **Theme:** Identifying the exact point where persistence becomes counterproductive blindness.
* **Theme block:** `56:00 - 58:40`
* **Timestamp Extraction Plan:**
  * **Hook:** `56:41 - 56:46` — when you start with focus … it becomes tunnel vision
  * **Pressure:** `56:46 - 56:57` — finish what you started; it no longer looks like you thought; it didn't work
  * **Stop:** `56:16 - 56:23` — people not responding, so we stopped
  * **Loop (pressure):** `58:44 - 58:52` — question, get depressed, three weeks later revive the loop
  * **Exit:** `58:40 - 58:43` — you have to keep track
  * **Keep-track payoff:** `47:48 - 47:52` + `47:56 - 48:16` — write a note, capture the thought, different perspective. Skip `47:52–47:56` (make a video).
* **Do not use:** platform/money recap (`56:08–56:24`) or businesses-first (`57:00–57:08`) — those are a second situation. Skip `57:45–58:35` (GAF rant).

---

### Strategy 4: #WisdomBit — "Playing a Game WITH Life"
* **Theme:** Shifting from victim mindset (*Game OF Life*) to co-creator (*Game WITH Life*).
* **Theme block:** opening tease `03:30 - 03:46` is too short and derails; real punch is later.
* **Timestamp Extraction Plan:** `extract_mode: contiguous` `54:44 - 55:40`
  * Consumed / prove something when we don't have to → adventurers playing a game WITH life, not OF life.
* **Do not use:** splice `55:32` + `54:48` + `1:05:24` (two situations; 28s). Do not use opening tease `03:30 - 04:15`. The `1:05:20` gamify close is a second situation (small business as a game).

---

### Strategy 5: #WisdomBit — "The 'Moving House' Phase"
* **Theme:** Normalizing the messy chaos that occurs during major life/business transitions.
* **Theme block:** `1:03:00 - 1:04:00`
* **Timestamp Extraction Plan:** `extract_mode: contiguous` `1:03:12 - 1:03:56`
  * Empty house → sort → new house / right now → **this is the first stream / the videos** (example of starting the move).
* **Do not use:** `1:03:56+` Hard Port / get-paid. Do not out at `1:03:46` (clips “this is the first”).
* Floor 50s. This take is ~44s — if it still feels tight, hold the same situation, don’t splice Hard Port.

---

## 4. Leftover themes (not in batch 1)

The five strategies above are not a cap. After they are scripted, scan the rest of the transcript. These blocks passed a situation→resolve read and were not cut:

| Theme | Neighborhood | Why it was skipped / when to cut |
|-------|--------------|----------------------------------|
| Fake productivity / pushing the wall | `23:20–24:24` (pad `22:52–24:24`) | Complete mini-rant. Stronger WisdomBit than sh04. |
| Desire vs running away | `18:40–19:28` (pad from `18:28`) | “What do I desire” → running away vs toward. |
| Capture thoughts / observer | `47:48–48:44` | Do **not** glue onto sh03. Own short. “Single most important thing.” |
| 50-person interview | `50:36–51:08` (pad `50:00–51:16`) | Founder rant: interviews as the test of what you know. |
| Presence digitized | `59:00–59:52` | Small-business economics. Better “business” short than Game WITH Life. |
| Recognition of failure | `06:46–07:02` | Too short alone. Alternate sh01 hook, not a sixth file. |
| We are being farmed | `35:44–36:16` | Mini-rant, no resolve. Do not ship. |

**sh04 note:** do not splice `55:32` + `54:48` + `1:05:24`. Those are two situations. Prefer contiguous `54:44–55:40` (prove / WITH life) if this theme is recut to clear 50s.

---

## 5. Post-Assembly Metadata Directive
* Set **Related Video** for all generated Shorts to: `[The Origin Story](https://studio.youtube.com/video/PJfvjQMPbGo)` in YouTube Studio to drive viewers from standalone clips into the full long-form experience.
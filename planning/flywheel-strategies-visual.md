# Flywheel Strategies — Visual

Companion to [`flywheel-strategies.md`](flywheel-strategies.md)

---

## Two strategies, one flywheel vocabulary

Both use stages: `attract` → `engage` → `trust` → `service` → `referral` → `loop`  
They differ in **what delivers service** and **what the viewer concludes with**.

---

## Strategy A: flywheel-shorts

```mermaid
flowchart LR
  subgraph SOURCE["Long source video"]
    V["10–30 min<br/>1 or many concepts"]
  end

  subgraph EXTRACT["Extract — all shorts"]
    S1["attract"]
    S2["engage"]
    S3["trust"]
    S4["service<br/>(short taste)"]
    S5["referral"]
    S6["loop"]
  end

  subgraph PUBLISH["Publish queue = product"]
    P1["1"] --> P2["2"] --> P3["3"] --> P4["4"] --> P5["5"] --> P6["6"]
  end

  V --> S1 --> P1
  S2 --> P2
  S3 --> P3
  S4 --> P4
  S5 --> P5
  S6 --> P6
```

**Conclusion:** Viewer finished the sequence — trust earned through the journey.  
Long video optional afterward.

---

## Strategy B: flywheel-episode

```mermaid
flowchart LR
  subgraph SOURCE["Long source video"]
    V["10–30 min"]
  end

  subgraph PRE["Pre-shorts"]
    A["attract"]
    B["engage"]
    C["trust?"]
  end

  subgraph HERO["Chapter — service"]
    CH["10–30 min<br/>full delivery"]
  end

  subgraph POST["Post-shorts"]
    R["referral"]
    L["loop"]
  end

  V --> A & B & C
  V --> CH
  V --> R & L

  A --> PREOUT["Post 1–3"]
  B --> PREOUT
  C --> PREOUT
  PREOUT --> CHOUT["Post 4<br/>CHAPTER DROP"]
  CH --> CHOUT
  CHOUT --> POSTOUT["Post 5–6"]
  R --> POSTOUT
  L --> POSTOUT
```

**Conclusion:** Viewer watched shorts → got full chapter payoff → post-shorts loop to next.  
Chapter is the center of gravity.

---

## Module layers (both strategies)

```mermaid
flowchart TB
  subgraph TECH["Technical modules — HOW"]
    T1[transcribe]
    T2[detect_topics]
    T3[render]
    T4[polish]
  end

  subgraph NAR_SHORTS["Narrative — flywheel-shorts"]
    NS[plan_flywheel_sequence]
  end

  subgraph NAR_EP["Narrative — flywheel-episode"]
    NC[plan_chapter]
    NP[plan_shorts_around_chapter]
  end

  subgraph SK["Skills — rules"]
    SK1[vertical_shorts]
    SK2[chunks]
    SK3[flywheel_series]
  end

  T1 --> T2
  T2 --> NS
  T2 --> NC
  NC --> NP
  NS --> SK
  NC --> SK
  NP --> SK
  NS --> T3
  NC --> T3
  NP --> T3
  T3 --> T4
```

---

## ASCII: pick a strategy

```
                    ┌─────────────────────┐
                    │   Long source video  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
   ┌──────────────────────┐        ┌──────────────────────┐
   │  FLYWHEEL-SHORTS     │        │  FLYWHEEL-EPISODE    │
   │  Product: short queue│        │  Product: chapter +  │
   │                      │        │  wrapper shorts      │
   │  s→s→s→s→s→s         │        │  s→s→CHAPTER→s→s     │
   └──────────────────────┘        └──────────────────────┘
```

---

## Project assignment

```
content_pipeline/projects/{name}/pipeline.json

  "playbook_id": "flywheel-shorts"   OR   "flywheel-episode"
```

Same source → two playbooks → two manifests → two conclusions.

# Autonomous Agent Pipeline Specification: Long-Form to Short-Form Video Repurposing

---

## 1. System Architecture Overview

An end-to-end autonomous agent pipeline for short-form video extraction operates across four sequential processing stages:

[Raw Video & Audio] │ ▼ [Stage 1: Ingestion & Temporal Alignment] │ ▼ [Stage 2: Semantic Segmentation & Candidate Generation] │ ▼ [Stage 3: Multi-Criteria Candidate Scoring & Selection] │ ▼ [Stage 4: Automated Assembly & Edit Structuring] │ ▼ [Standardized Output: Edit Decision List / Metadata Package]


---

## 2. Stage-by-Stage Functional Requirements

### Stage 1: Ingestion & Temporal Alignment
*   **Audio/Transcript Synchronization:** Ingest full-length audio tracks and align transcripts down to word-level timestamps (`start_ms`, `end_ms`, `confidence`).
*   **Speaker & Acoustic Profiling:** Detect speaker changes, pauses, pitch elevation, and emphasis markers.
*   **Visual Scene Detection:** Extract frame-level keyframes, detect shot boundaries, OCR on-screen text/diagrams (e.g., whiteboard drawings), and track speaker facial framing.

### Stage 2: Semantic Segmentation & Candidate Generation
*   **Thematic Boundary Detection:** Partition linear discourse into discrete thematic units based on semantic shifts rather than arbitrary time intervals.
*   **Self-Containment Verification:** Verify whether an excerpt contains an identifiable premise, core argument/narrative, and conclusion without requiring preceding context.
*   **Candidate Windowing:** Generate candidate clips within the target window (typically 30–75 seconds).

### Stage 3: Multi-Criteria Candidate Scoring & Selection
Each candidate segment is evaluated against a weighted scoring matrix ($S_{\text{total}} = \sum w_i S_i$):

| Criterion | Metric / Indicator | Target Value |
| :--- | :--- | :--- |
| **Hook Velocity (0–5s)** | Linguistic tension, controversial/novel statement, question format, or high vocal energy. | High semantic impact within first 3 seconds. |
| **Information Density** | Ratio of distinct concepts/insights relative to segment duration. | Elimination of filler words, tangents, or dead air. |
| **Narrative Completeness** | Semantic closure; the segment finishes the thought without dangling clauses. | Binary pass/fail threshold. |
| **Visual Correlation** | Presence of active gestures, whiteboard illustrations, product demos, or high-motion frames. | High visual engagement score. |
| **Standalone Understandability** | Absence of unresolved deictic references (e.g., *"like we said 10 minutes ago"*). | Minimum external context dependencies. |

### Stage 4: Automated Assembly & Edit Structuring
*   **Splice Point Optimization:** Select exact cut timestamps at natural breathing pauses or sentence boundaries.
*   **Multi-Segment Bridging:** When splicing non-contiguous segments (e.g., pairing a setup from Minute 42 with a resolution from Minute 44), ensure continuity of topic and tone.
*   **Caption & Asset Tagging:** Generate synchronized kinetic subtitle tracks, identify key moments for B-roll or dynamic zooms, and specify opening on-screen text overlays.

---

## 3. Agent Task Prompts & Algorithmic Heuristics

### Module A: Candidate Extraction Engine (NLP / Semantic Layer)

```text
SYSTEM INSTRUCTION:
You are an expert video narrative analyst. Your objective is to extract standalone short-form clips (30 to 75 seconds) from the provided timestamped transcript.

EVALUATION CRITERIA:
1. Hook Strength: The first 3–5 seconds must immediately establish conflict, novelty, or a central question.
2. Self-Containment: The excerpt must be completely understandable without watching any other part of the video. Filter out references like "as mentioned earlier" or "in the next chapter".
3. Value Delivery: The body of the clip must provide a clear insight, story beat, or actionable conclusion.
4. Clean Exit: The clip must conclude on a definitive statement, punchline, or clear conceptual ending.

OUTPUT REQUIREMENTS:
For each selected candidate, output:
- Segment Title & Theme
- Exact Source Timestamps (Start ms -> End ms)
- Verbatim Spoken Transcript
- Hook Text Overlay (under 7 words)
- Splice Logic (if joining two non-contiguous sections)
Module B: Edit Decision & Metadata Generator
SYSTEM INSTRUCTION:
Convert selected candidate segments into actionable editing blueprints for post-production assembly.

OUTPUT SCHEMA (Per Short):
- Target Duration: [Seconds]
- Source Range: [HH:MM:SS - HH:MM:SS]
- Spoken Hook: [0:00 - 0:05]
- Body Argument: [0:05 - X:XX]
- Outro/Conclusion: [X:XX - End]
- On-Screen Graphics: [List timestamped text overlays]
- Visual Framing Instructions: [e.g., 9:16 crop centered on speaker / split screen on whiteboard]
4. Standardized Output Schema (JSON Specification)
{
  "source_video_id": "string",
  "shorts_candidates": [
    {
      "candidate_id": 1,
      "theme": "string",
      "target_duration_seconds": 60,
      "segments": [
        {
          "start_timestamp": "00:31:33.000",
          "end_timestamp": "00:32:56.000",
          "text": "The internet is built around the individual..."
        }
      ],
      "hook": {
        "text_overlay": "Why the Internet Fails Local Businesses",
        "start_time": "00:00:00.000",
        "end_time": "00:00:05.000"
      },
      "pacing_notes": "Trim 1.2s pause between sentences at 00:32:10.000.",
      "visual_instructions": "Center crop 9:16 on speaker; cut to whiteboard close-up when diagram is referenced."
    }
  ]
}

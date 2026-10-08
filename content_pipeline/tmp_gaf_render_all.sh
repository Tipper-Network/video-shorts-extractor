#!/usr/bin/env bash
# Render all Future Ready lecture manifests (shorts + chunks).
set -uo pipefail
cd /home/psyfer/Desktop/workspace

LOG="step-1-projects/The-GAF-program future ready vids/output/logs/render-all-2026-10-07.log"
PROJ="program-future-ready"
RENDER=(python3 content_pipeline/render_manifest.py)

echo "=== START $(date -Iseconds) ===" | tee "$LOG"

for LEC in 13 14 15 16 17 18; do
  MAN="step-1-projects/The-GAF-program future ready vids/output/plan/manifest-l${LEC}.json"
  echo "" | tee -a "$LOG"
  echo "=== LECTURE ${LEC} chapters $(date -Iseconds) ===" | tee -a "$LOG"
  "${RENDER[@]}" --manifest "$MAN" --project "$PROJ" --type chapters --jobs 2 2>&1 | tee -a "$LOG"
  echo "chapters_exit=${PIPESTATUS[0]}" | tee -a "$LOG"

  echo "=== LECTURE ${LEC} shorts $(date -Iseconds) ===" | tee -a "$LOG"
  "${RENDER[@]}" --manifest "$MAN" --project "$PROJ" --type shorts --jobs 4 2>&1 | tee -a "$LOG"
  echo "shorts_exit=${PIPESTATUS[0]}" | tee -a "$LOG"

  echo "=== LECTURE ${LEC} DONE $(date -Iseconds) ===" | tee -a "$LOG"
done

BASE="step-1-projects/The-GAF-program future ready vids/output/deliverables"
echo "=== ALL DONE $(date -Iseconds) ===" | tee -a "$LOG"
echo "SHORTS MP4: $(find "$BASE/shorts" -name '*.mp4' | wc -l)" | tee -a "$LOG"
echo "CHUNKS MP4: $(find "$BASE/chunks" -name '*.mp4' | wc -l)" | tee -a "$LOG"
ls -la "$BASE/shorts"/*.mp4 2>/dev/null | tee -a "$LOG"
ls -la "$BASE/chunks"/*.mp4 2>/dev/null | tee -a "$LOG"

# Dynamic zoom

Cancelled. `content_pipeline/cli/viral_zoom.py` exits on purpose. A 1.15× zoom on a timer was step 2 between captions and sounds. It is not a stage.

`content_pipeline/cli/auto_edit.py` still contains that timer (`ZOOM_INTERVAL` 4 seconds). Do not run it.

If a zoom comes back, it has to be a turn in the signed script, and it has to run before captions. Until that exists, the edit is step 1 cut, then `viral_captions.py`, then `viral_sounds.py`.

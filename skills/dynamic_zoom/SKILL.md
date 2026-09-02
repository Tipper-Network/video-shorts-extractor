# Skill: Dynamic Zoom & Pattern Interrupts

## Objective
Apply timed zoom-in and zoom-out operations to video footage at set intervals or key moments to increase viewer retention.

## Parameters
- `zoom_factor`: Default 1.15x (15% zoom).
- `interval_seconds`: Default interval between zoom shifts (e.g., every 3 to 5 seconds).
- `duration_seconds`: Active duration of the zoomed state (e.g., hold zoom for 2 seconds).

## Execution Strategy
1. **Periodic Framing**: Shift camera frame state between normal scale (1.0x) and close-up scale (1.15x) based on configured timestamps.
2. **Center Cropping**: Keep crop anchors centered (`(width - crop_w) / 2`, `(height - crop_h) / 2`) so focal points remain stable.
3. **Audio Lock**: Maintain unbroken audio stream synchronization across zoom cuts.
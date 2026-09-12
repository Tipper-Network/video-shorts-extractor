# Input — drop raw footage here

Your job: move clips and stills into this folder before we run the pipeline.

**hikmat expects:**
- 11 MP4 screen recordings (chronological filenames `YYYYMMDD_HHMMSS`)
- 2 JPG result stills (`20260730_115835.jpg`, `20260731_121250.jpg`)

Exclude: `one.mp4`, incomplete `.crdownload` files.

If files live elsewhere for now, copy or symlink them here:

```bash
cp ~/Desktop/hikmat-project/*.mp4 ~/Desktop/hikmat-project/*.jpg projects/hikmat/input/
```

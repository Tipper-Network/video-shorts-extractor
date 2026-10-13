"""Turn a local mp4 into a stable HTTPS URL Instagram Graph can fetch.

With AWS credentials:
  1. Upload to ``s3://{bucket}/{prefix}/…`` (key mirrors step-4 relative path when possible)
  2. Return a **stable path-style URL** (bucket policy must allow public ``GetObject`` on that prefix)
  3. If public GET fails and ``S3_USE_PRESIGN=true``, fall back to a temporary presigned GET

Without AWS: ``MEDIA_PUBLIC_BASE_URL`` + filename (pre-hosted public files).
"""

from __future__ import annotations

import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from _root import WORKSPACE_ROOT
from publish.env import first

STEP4 = WORKSPACE_ROOT / "step-4-ready-to-post"


def _aws_keys() -> tuple[str, str]:
    return first("AWS_ACCESS_KEY_ID"), first("AWS_SECRET_ACCESS_KEY")


def _region() -> str:
    return first("AWS_REGION", "AWS_DEFAULT_REGION", default="eu-north-1") or "eu-north-1"


def _bucket() -> str:
    uri = first("S3_URI")
    if uri.startswith("s3://"):
        rest = uri[5:].split("/", 1)[0]
        if rest:
            return rest
    arn = first("S3_ARN")
    m = re.search(r"arn:aws:s3:::([^/\s]+)", arn)
    if m:
        return m.group(1)
    name = first("S3_BUCKET", "S3_BUCKET_NAME")
    if name:
        return name
    for key in ("S3_URL", "MEDIA_PUBLIC_BASE_URL"):
        base = first(key)
        if not base:
            continue
        parts = urlparse(base).path.strip("/").split("/")
        if parts and parts[0]:
            return parts[0]
    return ""


def _prefix() -> str:
    """Top-level prefix inside the bucket (default ``socials``)."""
    explicit = first("S3_PREFIX").strip("/")
    if explicit:
        return explicit
    uri = first("S3_URI")
    if uri.startswith("s3://"):
        parts = uri[5:].split("/", 1)
        if len(parts) == 2 and parts[1].strip("/"):
            return parts[1].strip("/").split("/")[0]
    return "socials"


def _presign_seconds() -> int:
    raw = first("S3_PRESIGN_EXPIRES", default="21600")
    try:
        return max(300, int(raw))
    except ValueError:
        return 21600


def _use_presign() -> bool:
    return first("S3_USE_PRESIGN", default="false").lower() in ("1", "true", "yes")


def _s3_client(*, signed: bool = True):
    try:
        import boto3
        from botocore.config import Config
    except ImportError as e:
        raise RuntimeError("boto3 not installed — pip install boto3") from e

    cfg = Config(signature_version="s3v4", s3={"addressing_style": "path"})
    if not signed:
        from botocore import UNSIGNED

        return boto3.client(
            "s3",
            region_name=_region(),
            config=Config(signature_version=UNSIGNED, s3={"addressing_style": "path"}),
        )

    key, secret = _aws_keys()
    if not key or not secret:
        raise RuntimeError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY required in integrations/.env"
        )
    return boto3.client(
        "s3",
        region_name=_region(),
        aws_access_key_id=key,
        aws_secret_access_key=secret,
        config=cfg,
    )


def object_key_for(local_mp4: Path) -> str:
    """Stable key: ``{prefix}/{path under step-4}/`` or ``{prefix}/{filename}``."""
    local_mp4 = local_mp4.resolve()
    prefix = _prefix()
    try:
        rel = local_mp4.relative_to(STEP4.resolve()).as_posix()
        return f"{prefix}/{rel}" if prefix else rel
    except ValueError:
        name = local_mp4.name
        return f"{prefix}/{name}" if prefix else name


def stable_public_url(object_key: str) -> str:
    """Path-style URL (required when the bucket name contains dots)."""
    return f"https://s3.{_region()}.amazonaws.com/{_bucket()}/{object_key}"


def upload_to_s3(local_mp4: Path, *, force: bool = False) -> str:
    """Upload ``local_mp4``. Returns object key. Skips when same size already exists."""
    local_mp4 = local_mp4.resolve()
    if not local_mp4.is_file():
        raise FileNotFoundError(local_mp4)

    bucket = _bucket()
    if not bucket:
        raise RuntimeError(
            "Set S3_URI (s3://bucket/prefix/) or S3_BUCKET / S3_ARN in integrations/.env"
        )

    key = object_key_for(local_mp4)
    client = _s3_client()
    size = local_mp4.stat().st_size

    if not force:
        try:
            head = client.head_object(Bucket=bucket, Key=key)
            if int(head.get("ContentLength") or 0) == size:
                print(f"  S3 skip (same size): s3://{bucket}/{key}")
                return key
        except Exception:
            pass

    print(f"  S3 upload → s3://{bucket}/{key} ({size} bytes)")
    client.upload_file(
        str(local_mp4),
        bucket,
        key,
        ExtraArgs={"ContentType": "video/mp4"},
    )
    return key


def presigned_get_url(object_key: str, *, expires: int | None = None) -> str:
    client = _s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": _bucket(), "Key": object_key},
        ExpiresIn=expires if expires is not None else _presign_seconds(),
    )


def public_get_ok(url: str, *, timeout: float = 20.0) -> bool:
    """True if anonymous GET (Range) succeeds — IG uses GET, not HEAD."""
    req = urllib.request.Request(url, headers={"Range": "bytes=0-15"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 300 or resp.status == 206
    except Exception:
        return False


def s3_configured() -> bool:
    key, secret = _aws_keys()
    return bool(key and secret and _bucket())


def public_url_for(
    local_mp4: Path,
    *,
    upload: bool = True,
    force_upload: bool = False,
) -> str:
    """Return a URL Graph can GET for ``local_mp4`` (stable public when possible)."""
    local_mp4 = local_mp4.resolve()
    if not local_mp4.is_file():
        raise FileNotFoundError(local_mp4)

    if s3_configured():
        key = upload_to_s3(local_mp4, force=force_upload) if upload else object_key_for(local_mp4)
        stable = stable_public_url(key)
        if public_get_ok(stable):
            return stable
        if _use_presign():
            print(f"  S3 public GET failed — using presign for {key}")
            return presigned_get_url(key)
        raise RuntimeError(
            f"Object not anonymously readable: {stable}\n"
            "Add a bucket policy Allow s3:GetObject on that prefix, or set "
            "S3_USE_PRESIGN=true for temporary URLs."
        )

    base = first("MEDIA_PUBLIC_BASE_URL").rstrip("/")
    if base:
        prefix = first("MEDIA_PUBLIC_PREFIX").strip("/")
        name = local_mp4.name
        if prefix:
            return f"{base}/{prefix}/{name}"
        return f"{base}/{name}"

    raise RuntimeError(
        "No media host. Set AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY + S3_URI "
        "in integrations/.env, or MEDIA_PUBLIC_BASE_URL for pre-hosted public files."
    )

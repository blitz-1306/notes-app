"""Snapshot test: the committed openapi.json must match what the app produces.

If this test fails, regenerate the snapshot:

    make openapi-dump
"""

import json
from pathlib import Path

from app.main import app

SNAPSHOT_PATH = Path(__file__).resolve().parent.parent / "openapi.json"


def test_openapi_snapshot_matches() -> None:
    assert SNAPSHOT_PATH.exists(), (
        f"{SNAPSHOT_PATH} is missing. Run 'make openapi-dump' to create it."
    )
    snapshot = json.loads(SNAPSHOT_PATH.read_text())
    live = app.openapi()
    assert live == snapshot, (
        "OpenAPI schema drift detected. Run 'make openapi-dump' to update the snapshot."
    )

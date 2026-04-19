"""Dump the current OpenAPI schema to stdout.

Usage: python -m scripts.dump_openapi > openapi.json
"""

import json
import sys

from app.main import app


def main() -> None:
    json.dump(app.openapi(), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

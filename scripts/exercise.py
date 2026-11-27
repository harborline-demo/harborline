"""Exercise Harborline's main code paths and report failures to Sentry.

Copy this file to ``scripts/exercise.py`` in the Harborline repository. The
orchestrator runs it after each merge via ``tools/exercise.py``. It expects
``harborline/exercises.py`` to define ``EXERCISES``: a list of zero-argument callables
that drive real service code (create a shipment, process a carrier webhook, ...).
The agent grows that list as it builds features.

Each exception becomes a Sentry event. Grouping is left to Sentry's default
(by stack trace), so a new defect opens a new issue and a repeat of a known one
groups into it. One ``SENTRY_EVENT_ID=<id>`` line is printed per captured event.
"""

from __future__ import annotations

import os
import sys

import sentry_sdk

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main() -> int:
    dsn = os.environ.get("SENTRY_DSN")
    if not dsn:
        print("SENTRY_DSN is not set", file=sys.stderr)
        return 2
    sentry_sdk.init(
        dsn=dsn,
        environment=os.environ.get("HARBORLINE_ENV", "production"),
        release=os.environ.get("GITHUB_SHA"),
    )

    from harborline.exercises import EXERCISES

    failures = 0
    for exercise in EXERCISES:
        try:
            exercise()
        except Exception as exc:  # noqa: BLE001 - the point is to report real failures
            failures += 1
            event_id = sentry_sdk.capture_exception(exc)
            print(f"SENTRY_EVENT_ID={event_id}")
            print(f"{exercise.__name__}: {type(exc).__name__}: {exc}", file=sys.stderr)
    sentry_sdk.flush(timeout=10)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

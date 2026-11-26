import sentry_sdk
import time

sentry_sdk.init(
    dsn="https://683593b7aeca7e648866c54faaa3ff4a@o4512363883659264.ingest.de.sentry.io/4512430467907664",
)

raise KeyError(f"harborline webhook smoke test — verify 001 {int(time.time())}")

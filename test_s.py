import sentry_sdk
import time

sentry_sdk.init(
    dsn="https://683593b7aeca7e648866c54faaa3ff4a@o4512363883659264.ingest.de.sentry.io/4512430467907664",
)

ts = int(time.time())
try:
    raise KeyError(f"harborline webhook smoke test {ts}")
except KeyError as e:
    sentry_sdk.capture_exception(e, fingerprint=[f"smoke-{ts}"])

sentry_sdk.flush(timeout=5)
print("sent", ts)

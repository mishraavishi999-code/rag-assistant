import time

_last_call_time = [0]
MIN_INTERVAL = 15  # seconds between ANY Gemini call — safely under 5/minute even with jitter

def wait_for_rate_limit():
    elapsed = time.time() - _last_call_time[0]
    if elapsed < MIN_INTERVAL:
        sleep_time = MIN_INTERVAL - elapsed
        print(f"    Waiting {sleep_time:.1f}s to respect rate limit...")
        time.sleep(sleep_time)
    _last_call_time[0] = time.time()
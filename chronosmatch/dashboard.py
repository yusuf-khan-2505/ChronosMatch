"""Small dependency-free live terminal dashboard."""
import sys
import time

def draw_dashboard(processed, total, metrics, book, started_at):
    snap = book.snapshot()
    elapsed = max(time.perf_counter() - started_at, 1e-9)
    throughput = processed / elapsed
    latencies = metrics.latencies_us
    avg = sum(latencies) / len(latencies) if latencies else 0.0
    p95 = metrics.percentile(latencies, 95) if latencies else 0.0
    bar_width = 28
    filled = int(bar_width * processed / total) if total else bar_width
    bar = "#" * filled + "-" * (bar_width - filled)
    print("\033[2J\033[H", end="")
    print("CHRONOSMATCH | LIVE SIMULATION DASHBOARD")
    print("=" * 46)
    print(f"Progress : [{bar}] {processed:,}/{total:,} ({processed / total * 100:.1f}%)")
    print(f"Elapsed  : {elapsed:.2f} s")
    print(f"Throughput: {throughput:,.0f} orders/s (approx.)")
    print(f"Avg latency: {avg:,.1f} µs | p95: {p95:,.1f} µs")
    print("-" * 46)
    print(f"Best bid : {snap['best_bid']} ticks")
    print(f"Best ask : {snap['best_ask']} ticks")
    print(f"Spread   : {snap['spread']} ticks")
    print(f"Trades   : {snap['trades']:,} | Matched quantity: {snap['trade_quantity']:,}")
    print(f"Book levels (bid/ask): {snap['bid_levels']} / {snap['ask_levels']}")
    print("\nSimulation only — no real exchange or broker connection.")
    sys.stdout.flush()

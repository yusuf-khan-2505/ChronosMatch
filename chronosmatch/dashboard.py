"""Professional dependency-free ChronosMatch terminal dashboard."""

import sys
import time


class TerminalStyle:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"
    GREY = "\033[90m"

    @staticmethod
    def enabled():
        return sys.stdout.isatty()

    @classmethod
    def paint(cls, value, color):
        if not cls.enabled():
            return str(value)
        return f"{color}{value}{cls.RESET}"


def draw_dashboard(processed, total, metrics, book, started_at):
    """Render the current simulation status in the terminal."""

    snap = book.snapshot()

    elapsed = max(time.perf_counter() - started_at, 1e-9)
    throughput = processed / elapsed
    latencies = metrics.latencies_us

    average_latency = (
        sum(latencies) / len(latencies) if latencies else 0.0
    )
    p95_latency = (
        metrics.percentile(latencies, 95) if latencies else 0.0
    )

    percentage = min(100.0, processed / total * 100) if total else 100.0

    bar_width = 36
    filled = int(bar_width * percentage / 100)
    progress_bar = (
        TerminalStyle.paint("#" * filled, TerminalStyle.GREEN)
        + "-" * (bar_width - filled)
    )

    def format_price(value):
        return f"{value:,}" if value is not None else "N/A"

    def format_spread(value):
        return f"{value:,} ticks" if value is not None else "N/A"

    line = "=" * 64

    print("\033[2J\033[H", end="")

    print(TerminalStyle.paint(line, TerminalStyle.CYAN))
    print(
        TerminalStyle.paint(
            "                 CHRONOSMATCH",
            TerminalStyle.BOLD + TerminalStyle.CYAN
        )
    )
    print(
        TerminalStyle.paint(
            "             TRADING ENGINE SIMULATOR",
            TerminalStyle.CYAN
        )
    )
    print(TerminalStyle.paint(line, TerminalStyle.CYAN))

    print()
    print(TerminalStyle.paint("SIMULATION STATUS", TerminalStyle.BOLD))
    print(f"  Progress       : [{progress_bar}] {percentage:5.1f}%")
    print(f"  Orders         : {processed:,} / {total:,}")
    print(f"  Elapsed time   : {elapsed:.2f} seconds")
    print(
        "  Throughput     : "
        + TerminalStyle.paint(
            f"{throughput:,.0f} orders/sec",
            TerminalStyle.GREEN
        )
    )

    print()
    print(TerminalStyle.paint("LATENCY PERFORMANCE", TerminalStyle.BOLD))
    print(f"  Average latency: {average_latency:,.2f} us")
    print(f"  P95 latency    : {p95_latency:,.2f} us")

    print()
    print(TerminalStyle.paint("MARKET OVERVIEW", TerminalStyle.BOLD))
    print(
        f"  Best bid       : "
        f"{TerminalStyle.paint(format_price(snap['best_bid']), TerminalStyle.GREEN)} ticks"
    )
    print(
        f"  Best ask       : "
        f"{TerminalStyle.paint(format_price(snap['best_ask']), TerminalStyle.RED)} ticks"
    )
    print(f"  Bid-ask spread : {format_spread(snap['spread'])}")
    print(f"  Last trade     : {format_price(snap['last_trade_price'])} ticks")

    print()
    print(TerminalStyle.paint("ORDER BOOK ACTIVITY", TerminalStyle.BOLD))
    print(f"  Trade matches  : {snap['trades']:,}")
    print(f"  Matched quantity: {snap['trade_quantity']:,}")
    print(f"  Bid price levels: {snap['bid_levels']:,}")
    print(f"  Ask price levels: {snap['ask_levels']:,}")

    print()
    print(TerminalStyle.paint(line, TerminalStyle.CYAN))
    print(
        TerminalStyle.paint(
            "  EDUCATIONAL SIMULATION | NO REAL MARKET CONNECTION",
            TerminalStyle.GREY
        )
    )
    print(TerminalStyle.paint(line, TerminalStyle.CYAN))

    sys.stdout.flush()

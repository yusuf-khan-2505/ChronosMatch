#!/usr/bin/env python3
"""ChronosMatch: educational low-latency trading-engine simulation."""

import argparse
import asyncio
import time

from chronosmatch.book import LimitOrderBook, Order
from chronosmatch.dashboard import draw_dashboard
from chronosmatch.ipc import MMapRingBuffer
from chronosmatch.metrics import Metrics
from chronosmatch.simulator import produce_orders


def print_final_report(report, snap, dropped, csv_path=""):
    """Display a structured summary after simulation completion."""

    line = "=" * 64

    print()
    print(line)
    print("                 CHRONOSMATCH")
    print("                 FINAL REPORT")
    print(line)

    successful = dropped == 0 and report["processed"] > 0

    status = "SUCCESS - SIMULATION COMPLETED" if successful else "COMPLETED WITH WARNINGS"
    print()
    print(f"  Execution status : {status}")
    print(f"  Orders processed : {report['processed']:,}")
    print(f"  Orders dropped   : {dropped:,}")

    print()
    print("-" * 64)
    print("  PERFORMANCE SUMMARY")
    print("-" * 64)
    print(f"  Elapsed time     : {report['elapsed_s']:.4f} seconds")
    print(f"  Throughput       : {report['throughput_ops_s']:,.0f} orders/sec")
    print(f"  Average latency  : {report['latency_avg_us']:,.2f} us")
    print(f"  Median latency   : {report['latency_p50_us']:,.2f} us")
    print(f"  P95 latency      : {report['latency_p95_us']:,.2f} us")
    print(f"  P99 latency      : {report['latency_p99_us']:,.2f} us")

    print()
    print("-" * 64)
    print("  ORDER MATCHING SUMMARY")
    print("-" * 64)
    print(f"  Units filled     : {report['filled_units']:,}")
    print(f"  Trade matches    : {snap['trades']:,}")
    print(f"  Matched quantity : {snap['trade_quantity']:,}")

    print()
    print("-" * 64)
    print("  MARKET SNAPSHOT")
    print("-" * 64)

    best_bid = snap["best_bid"]
    best_ask = snap["best_ask"]
    spread = snap["spread"]
    last_trade = snap["last_trade_price"]

    print(f"  Best bid         : {best_bid:,} ticks" if best_bid is not None else "  Best bid         : N/A")
    print(f"  Best ask         : {best_ask:,} ticks" if best_ask is not None else "  Best ask         : N/A")
    print(f"  Bid-ask spread   : {spread:,} ticks" if spread is not None else "  Bid-ask spread   : N/A")
    print(f"  Last trade price : {last_trade:,} ticks" if last_trade is not None else "  Last trade price : N/A")
    print(f"  Bid price levels : {snap['bid_levels']:,}")
    print(f"  Ask price levels : {snap['ask_levels']:,}")

    if csv_path:
        print()
        print("-" * 64)
        print("  EXPORT")
        print("-" * 64)
        print(f"  Latency CSV saved: {csv_path}")

    print()
    print(line)
    print("  EDUCATIONAL SIMULATION - NO REAL TRADES EXECUTED")
    print(line)


async def consume_orders(ring, book, metrics, expected_count, dashboard, started_at):
    processed = 0
    last_dashboard = time.perf_counter()

    while processed < expected_count:
        item = ring.get()

        if item is None:
            await asyncio.sleep(0)
            continue

        seq, side, price, quantity, timestamp_ns = item
        filled = book.process(Order(seq, side, price, quantity, timestamp_ns))
        metrics.record(timestamp_ns, filled)
        processed += 1

        now = time.perf_counter()

        if dashboard and (
            processed == expected_count
            or processed % 250 == 0
            or now - last_dashboard >= 0.25
        ):
            draw_dashboard(
                processed,
                expected_count,
                metrics,
                book,
                started_at
            )
            last_dashboard = now

    return processed


async def run(args):
    book = LimitOrderBook()
    metrics = Metrics()

    started_at = time.perf_counter()

    with MMapRingBuffer(capacity=args.capacity) as ring:
        producer = asyncio.create_task(
            produce_orders(
                ring,
                args.orders,
                args.rate,
                seed=args.seed
            )
        )

        consumer = asyncio.create_task(
            consume_orders(
                ring,
                book,
                metrics,
                args.orders,
                not args.no_dashboard,
                started_at
            )
        )

        await asyncio.gather(producer, consumer)
        dropped = ring.dropped

    report = metrics.report()
    snap = book.snapshot()

    if args.csv:
        metrics.save_csv(args.csv)

    print_final_report(report, snap, dropped, args.csv)


def parse_args():
    parser = argparse.ArgumentParser(
        description="ChronosMatch local trading-engine prototype"
    )

    parser.add_argument(
        "--orders",
        type=int,
        default=10000,
        help="number of mock orders"
    )

    parser.add_argument(
        "--rate",
        type=int,
        default=0,
        help="approximate producer rate (orders/s); 0 means unpaced"
    )

    parser.add_argument(
        "--capacity",
        type=int,
        default=65536,
        help="mmap ring capacity (power of two)"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=7,
        help="random seed for repeatable simulation"
    )

    parser.add_argument(
        "--no-dashboard",
        action="store_true",
        help="disable live terminal dashboard"
    )

    parser.add_argument(
        "--csv",
        default="",
        help="optional path for per-order latency CSV output"
    )

    args = parser.parse_args()

    if args.orders < 1:
        parser.error("--orders must be >= 1")

    if args.rate < 0:
        parser.error("--rate must be >= 0")

    return args


if __name__ == "__main__":
    asyncio.run(run(parse_args()))

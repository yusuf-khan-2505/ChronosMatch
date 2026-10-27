#!/usr/bin/env python3
"""ChronosMatch: local educational trading-engine simulation."""
import argparse
import asyncio
import time

from chronosmatch.book import LimitOrderBook, Order
from chronosmatch.ipc import MMapRingBuffer
from chronosmatch.metrics import Metrics
from chronosmatch.simulator import produce_orders


async def consume_orders(ring, book, metrics, expected_count):
    processed = 0
    while processed < expected_count:
        item = ring.get()
        if item is None:
            await asyncio.sleep(0)
            continue
        seq, side, price, quantity, timestamp_ns = item
        order = Order(seq, side, price, quantity, timestamp_ns)
        filled = book.process(order)
        metrics.record(timestamp_ns, filled)
        processed += 1
        if processed % 10000 == 0:
            print(f"\rProcessed {processed:,}/{expected_count:,} orders...", end="", flush=True)
    if expected_count >= 10000:
        print()


async def run(args):
    book = LimitOrderBook()
    metrics = Metrics()
    with MMapRingBuffer(capacity=args.capacity) as ring:
        producer = asyncio.create_task(
            produce_orders(ring, args.orders, args.rate, seed=args.seed)
        )
        consumer = asyncio.create_task(
            consume_orders(ring, book, metrics, args.orders)
        )
        await asyncio.gather(producer, consumer)
        dropped = ring.dropped

    report = metrics.report()
    snap = book.snapshot()
    print("\n=== ChronosMatch Results ===")
    print(f"Orders processed       : {report['processed']:,}")
    print(f"Orders dropped         : {dropped:,}")
    print(f"Elapsed time           : {report['elapsed_s']:.4f} s")
    print(f"Throughput             : {report['throughput_ops_s']:,.0f} orders/s")
    print(f"Average latency        : {report['latency_avg_us']:.2f} µs")
    print(f"Median latency (p50)   : {report['latency_p50_us']:.2f} µs")
    print(f"95th percentile (p95)  : {report['latency_p95_us']:.2f} µs")
    print(f"99th percentile (p99)  : {report['latency_p99_us']:.2f} µs")
    print(f"Units filled           : {report['filled_units']:,}")
    print(f"Trade matches          : {snap['trades']:,}")
    print(f"Matched quantity       : {snap['trade_quantity']:,}")
    print(f"Best bid (ticks)       : {snap['best_bid']}")
    print(f"Best ask (ticks)       : {snap['best_ask']}")
    print(f"Spread (ticks)         : {snap['spread']}")
    print(f"Last trade (ticks)     : {snap['last_trade_price']}")
    print(f"Bid / ask levels       : {snap['bid_levels']} / {snap['ask_levels']}")


def parse_args():
    parser = argparse.ArgumentParser(description="ChronosMatch local trading-engine prototype")
    parser.add_argument("--orders", type=int, default=10000, help="number of mock orders")
    parser.add_argument("--rate", type=int, default=0, help="approximate producer rate (orders/s); 0 means unpaced")
    parser.add_argument("--capacity", type=int, default=65536, help="mmap ring capacity (power of two)")
    parser.add_argument("--seed", type=int, default=7, help="random seed for repeatable simulation")
    args = parser.parse_args()
    if args.orders < 1:
        parser.error("--orders must be >= 1")
    if args.rate < 0:
        parser.error("--rate must be >= 0")
    return args


if __name__ == "__main__":
    asyncio.run(run(parse_args(1)))

"""Async mock order-flow generator."""
from __future__ import annotations
import asyncio
import random
import time
from .ipc import MMapRingBuffer


async def produce_orders(ring: MMapRingBuffer, count: int, rate: int,
                         base_price: int = 100_000, seed: int = 7):
    rng = random.Random(seed)
    interval = 1.0 / rate if rate > 0 else 0
    for seq in range(1, count + 1):
        side = rng.randrange(2)
        # Prices are integer ticks. Most orders sit near the mid-price; some cross.
        price = max(1, base_price + rng.randint(-20, 20))
        if rng.random() < 0.18:
            price += (25 if side == 0 else -25)
            price = max(1, price)
        quantity = rng.randint(1, 20)
        timestamp_ns = time.perf_counter_ns()
        while not ring.put(seq, side, price, quantity, timestamp_ns):
            await asyncio.sleep(0)
        if interval:
            await asyncio.sleep(interval)
        elif seq % 5000 == 0:
            await asyncio.sleep(0)

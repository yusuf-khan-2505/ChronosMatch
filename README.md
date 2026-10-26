# ChronosMatch — Python Trading Engine Prototype

An educational, local-only prototype inspired by the Project 2 brief. It simulates market orders, passes compact order records through a memory-mapped ring buffer, matches orders with a price-time-priority limit order book, and reports end-to-end latency.

> **Important:** This is a simulation, not a production high-frequency trading system. It does not connect to a broker/exchange, place real trades, or provide investment advice. Pure Python and an asyncio event loop are not suitable for guaranteed microsecond latency.

## Requirements
- Python 3.10+
- No third-party packages required

## Run
From this folder:

```bash
python main.py
```

Optional settings:

```bash
python main.py --orders 10000 --rate 20000 --capacity 65536
```

- `--orders`: number of simulated orders
- `--rate`: approximate producer rate in orders/second (0 = no intentional pacing)
- `--capacity`: ring-buffer capacity; must be a power of two

## Project layout
- `chronosmatch/ipc.py` — mmap-backed fixed-record ring buffer
- `chronosmatch/book.py` — price-time-priority limit order book
- `chronosmatch/simulator.py` — asynchronous mock market-data/order producer
- `chronosmatch/metrics.py` — latency and throughput statistics
- `main.py` — CLI and orchestration

## Record format
Each ring-buffer slot is a fixed-size binary record (`struct.Struct`) containing:
sequence number, side, price in integer ticks, quantity, and producer timestamp in nanoseconds. Fixed-size records avoid JSON serialization in the hot path.

## Scope and next steps
This version uses one producer and one consumer in a single process for portability. The mmap file can be shared by processes on the same host, but a truly safe multi-process ring buffer needs explicit inter-process synchronization and crash recovery. For a stronger version, add a Cython/Rust matching core, a sequence-number protocol for lock-free slots, real feed adapters, and extensive correctness/latency testing.

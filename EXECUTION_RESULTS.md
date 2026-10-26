# ChronosMatch — Execution Results

## Project Overview

ChronosMatch is an educational trading-engine simulation
that demonstrates order processing, order matching,
and performance measurement.

## Execution Command

python main.py

## Successful Execution Summary

The original project completed a simulation involving
10,000 orders.

| Metric | Result |
|---|---:|
| Orders Processed | 10,000 |
| Orders Dropped | 0 |
| Throughput | 36,658 orders/second |
| Average Latency | 62,146.85 microseconds |
| P50 Latency | 59,443.50 microseconds |
| P95 Latency | 73,415.50 microseconds |
| P99 Latency | 73,943.40 microseconds |
| Units Filled | 47,795 |
| Trades Executed | 8,666 |
| Matched Quantity | 47,795 |
| Best Bid | 99,996 |
| Best Ask | 100,002 |
| Bid-Ask Spread | 6 |

## Summary

- Processed 10,000 simulated orders.
- Reported zero dropped orders.
- Executed 8,666 simulated trades.
- Matched 47,795 units.
- Reported throughput of approximately 36,658 orders/second.

Note: These results are from an earlier local execution.
Performance may vary with hardware and runtime conditions.

This is an educational simulation and does not execute
real financial trades.

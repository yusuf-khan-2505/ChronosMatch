# 5. Technical Reference



## 5.1 Introduction



This document describes the technical implementation of ChronosMatch and explains the responsibilities of its main Python modules.



The project uses Python's standard library to simulate an electronic trading-engine workflow.



## 5.2 Project Modules



The main source code is organized into the following modules:



| File | Responsibility |

|---|---|

| `main.py` | Application entry point and simulation orchestration |

| `chronosmatch/simulator.py` | Generates simulated buy and sell orders |

| `chronosmatch/ipc.py` | Implements the memory-mapped ring buffer |

| `chronosmatch/book.py` | Implements the limit order book and matching logic |

| `chronosmatch/metrics.py` | Calculates latency and throughput statistics |

| `chronosmatch/dashboard.py` | Displays live simulation information |



## 5.3 Application Entry Point



The `main.py` module coordinates the complete simulation.



Its responsibilities include:



- Parsing command-line arguments.

- Creating the ring buffer.

- Initializing the limit order book and metrics collector.

- Starting the asynchronous producer.

- Consuming generated orders.

- Updating the terminal dashboard when enabled.

- Displaying final performance results.

- Exporting latency measurements when CSV output is requested.



## 5.4 Order Data Structure



Each simulated order contains the following information:



| Field | Description |

|---|---|

| Sequence | Unique sequence number assigned to the generated order |

| Side | BUY or SELL |

| Price | Order limit price represented in integer ticks |

| Quantity | Number of units requested |

| Timestamp | Producer timestamp in nanoseconds |



The internal order-book representation uses an `Order` data structure containing order ID, side, price, quantity, and timestamp.



## 5.5 Memory-Mapped Ring Buffer



The `chronosmatch/ipc.py` module implements the `MMapRingBuffer` class.



The buffer stores fixed-size binary order records in a memory-mapped file.



The record format is defined using:



```python

struct.Struct("<QBQIQ")

```



The fields are packed in the following order:



| Format | Data Type | Description |

|---|---|---|

| `Q` | Unsigned 64-bit integer | Sequence number |

| `B` | Unsigned 8-bit integer | Order side |

| `Q` | Unsigned 64-bit integer | Price ticks |

| `I` | Unsigned 32-bit integer | Quantity |

| `Q` | Unsigned 64-bit integer | Producer timestamp |



Each record occupies 29 bytes.



The ring buffer uses a fixed capacity, which must be a power of two and at least 2.



### Buffer Operations



The main operations are:



- `put()`: Writes an order record when space is available.

- `get()`: Reads and removes the next available record.

- `len()`: Reports the number of records currently stored.



When the buffer is full, a write attempt is rejected. The simulator retries the order instead of treating that rejection as a permanently lost order.



**Implementation limitation:** This is an educational, single-process producer-consumer demonstration. It is not a lock-free or synchronized multi-process queue.



## 5.6 Limit Order Book



The `chronosmatch/book.py` module implements the `LimitOrderBook` class.



The order book maintains two sides:



- Bids: Buy orders.

- Asks: Sell orders.



It uses heaps to identify the best available prices and deques to maintain FIFO order at each price level.



### Matching Conditions



A BUY order can match when its limit price is greater than or equal to the best available ask.



A SELL order can match when its limit price is less than or equal to the best available bid.



### Price-Time Priority



The matching engine follows price priority first and FIFO insertion order for orders at the same price.



For example:



- The highest-priced BUY order has priority over lower-priced BUY orders.

- The lowest-priced SELL order has priority over higher-priced SELL orders.

- Orders at the same price level are processed in insertion order.



Trades execute at the resting order's price.



### Partial Fills



If an incoming order cannot be completely matched, its remaining quantity is placed in the order book.



## 5.7 Simulation Engine



The `chronosmatch/simulator.py` module generates synthetic market activity.



The simulator:



- Uses Python's random number generator.

- Generates BUY and SELL orders.

- Produces randomized prices and quantities.

- Assigns sequence numbers and timestamps.

- Writes order records into the ring buffer.

- Supports an approximate producer rate.



The default random seed is 7, which helps make generated order sequences repeatable under the same configuration.



The producer uses asynchronous execution and yields control while waiting for buffer space or rate intervals.



## 5.8 Metrics Collection



The `chronosmatch/metrics.py` module records the processing latency of orders.



It calculates:



- Average latency.

- P50 latency.

- P95 latency.

- P99 latency.

- Total elapsed time.

- Processing throughput.



Latency is measured from the producer timestamp to the point after the consumer has processed the order and recorded its metrics.



Therefore, the measurement represents end-to-end processing latency, not just the time spent executing the matching operation.



## 5.9 Terminal Dashboard



The `chronosmatch/dashboard.py` module provides a dependency-free terminal dashboard.



It displays:



- Processing progress.

- Elapsed time.

- Approximate throughput.

- Average and P95 latency.

- Best bid and ask.

- Bid-ask spread.

- Trade count.

- Matched quantity.

- Order book information.



The dashboard can be disabled using the `--no-dashboard` command-line option.



## 5.10 Technical Limitations



ChronosMatch is an educational simulation and has the following limitations:



- It does not connect to real financial exchanges or brokers.

- It does not execute real financial transactions.

- It uses synthetic order data.

- The ring buffer is not a production-grade multi-process communication system.

- Python and asyncio do not guarantee microsecond-level execution.

- Performance measurements depend on hardware, operating-system scheduling, and runtime conditions.



## 5.11 Conclusion



ChronosMatch combines asynchronous order generation, memory-mapped record storage, price-time-priority matching, performance measurement, and terminal monitoring into a modular Python simulation.




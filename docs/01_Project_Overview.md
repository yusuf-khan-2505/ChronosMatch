# 1. Project Overview



## 1.1 Introduction



ChronosMatch is an educational Python-based trading engine simulation designed to demonstrate the fundamental concepts involved in electronic order processing.



The project simulates the generation of buy and sell orders, transfers fixed-size binary records through a memory-mapped ring buffer, processes orders using a limit order book, and calculates performance metrics.



It provides a practical demonstration of how different components of a simplified trading system work together.



## 1.2 Project Objectives



The main objectives are:



- Understand the basic workflow of an electronic trading engine.

- Simulate buy and sell order generation.

- Implement a memory-mapped ring buffer for passing order records.

- Develop a limit order book using price-time priority.

- Demonstrate order matching and partial order execution.

- Measure order-processing latency and throughput.

- Display simulation progress through a terminal dashboard.

- Validate core functionality using automated unit tests.



## 1.3 Key Features



### Simulated Order Generation



An asynchronous producer generates synthetic buy and sell orders using Python's random number generator.



Each order contains:



- Sequence number

- Order side (BUY or SELL)

- Price in integer ticks

- Quantity

- Producer timestamp in nanoseconds



### Memory-Mapped Ring Buffer



The project uses Python's `mmap` module to create a fixed-size memory-mapped buffer.



Order records are packed into a binary format using Python's `struct` module.



The ring buffer demonstrates how a producer can pass records to a consumer within the same process.



### Limit Order Book



The matching engine maintains separate buy and sell sides.



It uses:



- Price heaps to identify the best available bid and ask.

- FIFO queues to maintain insertion order at each price level.

- Price-based matching rules.

- Partial order execution.



### Performance Measurement



The metrics module calculates:



- Total processed orders

- Elapsed time

- Throughput in orders per second

- Average latency

- Median latency (P50)

- 95th percentile latency (P95)

- 99th percentile latency (P99)

- Total filled quantity



### Live Terminal Dashboard



The dashboard displays:



- Simulation progress

- Elapsed time

- Approximate throughput

- Average and P95 latency

- Best bid and ask

- Bid-ask spread

- Trade matches

- Matched quantity

- Active order-book levels



### CSV Export



The application optionally exports individual order latency measurements to a CSV file.



## 1.4 Technology Stack



| Technology | Purpose |

|---|---|

| Python | Main programming language |

| asyncio | Asynchronous producer and consumer tasks |

| mmap | Memory-mapped ring buffer |

| struct | Fixed-size binary record serialization |

| heapq | Price-level priority management |

| collections.deque | FIFO order queues |

| time | Timestamp and performance measurement |

| unittest | Automated testing |

| csv | Latency data export |



The project uses Python's standard library and does not require third-party packages for its core functionality.



## 1.5 High-Level Workflow



1\. The simulator generates a synthetic order.

2\. The order is converted into a fixed-size binary record.

3\. The record is written into the memory-mapped ring buffer.

4\. The consumer retrieves the record.

5\. The limit order book processes the incoming order.

6\. Matching and partial fills are calculated when prices cross.

7\. The metrics module records processing latency and filled quantity.

8\. The terminal dashboard displays progress and market statistics.

9\. Final performance results are printed after the simulation completes.



## 1.6 Project Scope



ChronosMatch focuses on demonstrating core trading-engine concepts in a local educational environment.



The current implementation includes:



- One simulated order producer.

- One order consumer.

- A memory-mapped ring buffer.

- A price-time-priority limit order book.

- A terminal-based dashboard.

- Performance measurement and optional CSV export.

- Automated unit tests for the order book and ring buffer.



## 1.7 Important Limitations



ChronosMatch is a simulation, not a production trading platform.



- It does not connect to a real stock exchange or broker.

- It does not execute real financial transactions.

- The producer and consumer operate as asynchronous tasks within one process.

- The ring buffer is not a lock-free or synchronized multi-process queue.

- Python and asyncio do not guarantee microsecond-level execution latency.

- Generated orders are synthetic and do not represent actual market data.



Performance results are experimental and depend on the execution environment.



## 1.8 Conclusion



ChronosMatch provides a practical introduction to electronic trading-engine architecture by combining asynchronous programming, binary data handling, memory-mapped communication, order matching, and performance analysis in one Python project.



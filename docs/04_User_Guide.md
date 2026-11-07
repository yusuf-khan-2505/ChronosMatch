# 4. User Guide



## 4.1 Introduction



This guide explains how to operate ChronosMatch, configure its simulation parameters, monitor order processing, and export latency measurements.



ChronosMatch runs locally through the command line and does not require a graphical interface.



## 4.2 Starting the Application



Open PowerShell in the ChronosMatch project directory and execute:



```bash

python main.py

```



This starts the simulation using the default configuration and displays the live terminal dashboard.



## 4.3 Command-Line Options



ChronosMatch supports the following command-line arguments:



| Argument | Description |

|---|---|

| `--orders` | Number of simulated orders |

| `--rate` | Approximate producer rate in orders per second |

| `--capacity` | Memory-mapped ring buffer capacity |

| `--seed` | Random seed for repeatable simulation |

| `--no-dashboard` | Disables the live terminal dashboard |

| `--csv` | Exports per-order latency measurements to a CSV file |



To view all available options:



```bash

python main.py --help

```



## 4.4 Running a Custom Simulation



Example: Process 5,000 orders.



```bash

python main.py --orders 5000

```



Example: Process 10,000 orders without the dashboard.



```bash

python main.py --orders 10000 --no-dashboard

```



Example: Run with a producer rate of approximately 20,000 orders per second.



```bash

python main.py --orders 10000 --rate 20000

```



Example: Use a ring buffer capacity of 32,768 records.



```bash

python main.py --orders 10000 --capacity 32768

```



The ring buffer capacity must be a power of two and at least 2.



## 4.5 Live Terminal Dashboard



When enabled, the dashboard displays simulation progress and performance information.



The dashboard includes:



- Processed order count and progress.

- Elapsed simulation time.

- Approximate processing throughput.

- Average and P95 latency.

- Best bid and best ask prices.

- Bid-ask spread.

- Number of trade matches.

- Total matched quantity.

- Order book levels.



The dashboard refreshes periodically while the simulation is running.



## 4.6 Understanding Simulation Results



After the simulation finishes, ChronosMatch reports several performance measurements.



| Metric | Meaning |

|---|---|

| Processed Orders | Number of orders successfully consumed and processed |

| Dropped | Number of rejected ring-buffer write attempts |

| Elapsed Time | Total measured simulation duration |

| Throughput | Number of processed orders per second |

| Average Latency | Average measured end-to-end order latency |

| P50 Latency | Median latency |

| P95 Latency | 95th percentile latency |

| P99 Latency | 99th percentile latency |

| Filled Units | Total quantity matched |

| Trade Matches | Number of individual matching events |



A rejected write attempt is not necessarily a permanently lost order. The producer retries when the buffer is full.



## 4.7 Exporting Latency Data



ChronosMatch can export per-order latency measurements to a CSV file.



Execute:



```bash

python main.py --orders 10000 --no-dashboard --csv latency_results.csv

```



The generated CSV file contains:



- `order_index`: Index of the processed order.

- `latency_us`: Measured latency in microseconds.



The CSV file can be opened using spreadsheet software for further analysis.



## 4.8 Repeatable Simulations



The `--seed` option controls the random number generator.



Example:



```bash

python main.py --orders 10000 --seed 7 --no-dashboard

```



Using the same seed and configuration helps reproduce the same generated order sequence.



Execution time and measured latency may still vary between runs.



## 4.9 Recommended Demonstration Command



For a simple project demonstration, execute:



```bash

python main.py --orders 10000

```



This demonstrates simulated order generation, memory-mapped communication, order matching, performance measurement, and live terminal monitoring.



## 4.10 Conclusion



ChronosMatch provides a command-line interface for configuring and executing an educational trading-engine simulation. Its dashboard, performance metrics, and CSV export functionality help users understand the order-processing workflow.



# 7. Performance Analysis



## 7.1 Introduction



Performance analysis evaluates how efficiently ChronosMatch processes simulated market orders.



The application collects processing time, latency, throughput, and order-matching statistics during execution.



This document explains these measurements and presents the results from one recorded benchmark run.



## 7.2 Benchmark Configuration



The following command was used for the recorded benchmark:



```powershell

python main.py --orders 10000 --no-dashboard

```



The benchmark configuration was:



| Parameter | Value |

|---|---|

| Number of orders | 10,000 |

| Producer rate | 0 (unpaced) |

| Ring buffer capacity | 65,536 |

| Random seed | 7 |

| Terminal dashboard | Disabled |

| Python version | 3.13.14 |



The dashboard was disabled to run the simulation without live terminal updates.



## 7.3 Recorded Performance Results



The following results were observed during one execution:



| Metric | Recorded Result |

|---|---:|

| Orders processed | 10,000 |

| Dropped orders | 0 |

| Total elapsed time | 0.2444 seconds |

| Throughput | 40,910 orders/second |

| Average latency | 56,171.27 microseconds |

| P50 latency | 56,252.60 microseconds |

| P95 latency | 60,991.90 microseconds |

| P99 latency | 61,430.70 microseconds |

| Matched quantity | 47,795 |

| Trade matches | 8,666 |

| Best bid | 99,996 ticks |

| Best ask | 100,002 ticks |

| Bid-ask spread | 6 ticks |



These values represent one recorded execution. They are not guaranteed performance figures.



## 7.4 Understanding the Performance Metrics



### 7.4.1 Processing Throughput



Throughput represents the number of orders processed per second.



It is calculated as:



```text

Throughput = Total Processed Orders / Elapsed Time

```



Higher throughput means that more orders are processed within a given period.



### 7.4.2 Average Latency



Latency represents the time taken for an order to travel through the processing pipeline.



ChronosMatch measures latency from the producer timestamp until after the consumer has processed the order and recorded its metrics.



The result is expressed in microseconds.



This is an end-to-end processing measurement, not just the time spent executing the matching operation.



### 7.4.3 Percentile Latency



Percentiles help explain how processing latency is distributed across orders.



- **P50:** The median latency. Approximately half of the recorded orders have latency at or below this value.

- **P95:** 95% of the recorded orders have latency at or below this value.

- **P99:** 99% of the recorded orders have latency at or below this value.



These measurements help identify slower order-processing cases that an average alone might hide.



### 7.4.4 Matched Quantity



Matched quantity represents the total quantity of units traded through successful order matches.



It is different from the number of trade matches because one matching event can involve multiple units.



### 7.4.5 Trade Matches



Trade matches represent the number of successful matching events between compatible BUY and SELL orders.



## 7.5 Factors Affecting Performance



The measured performance of ChronosMatch can vary depending on several factors:



- Processor speed and available system resources.

- Operating-system scheduling.

- Python runtime behavior.

- Number of simulated orders.

- Producer rate configuration.

- Ring buffer capacity.

- Terminal dashboard updates.

- Other applications running on the system.



Therefore, repeated executions may produce slightly different results.



## 7.6 Reproducing the Benchmark



To run the same basic benchmark configuration again, execute:



```powershell

python main.py --orders 10000 --no-dashboard

```



To run a larger simulation, use:



```powershell

python main.py --orders 50000 --no-dashboard

```



The larger simulation can help observe how the application behaves when processing more orders.



Record the results of each execution separately rather than assuming performance values will remain constant.



## 7.7 Performance Considerations



ChronosMatch demonstrates simulated order processing, memory-mapped record storage, order matching, and performance measurement in a Python environment.



However, it is an educational prototype rather than a production high-frequency trading system.



Its benchmark results should be understood as observations from a local simulation, not as guarantees of real-world exchange performance.



## 7.8 Conclusion



The recorded benchmark demonstrates that ChronosMatch successfully processed 10,000 simulated orders with zero dropped orders in the observed run.



The application also collected throughput, latency percentiles, matched quantity, and trade statistics.



These measurements provide a practical way to evaluate the behavior of the simulation and understand basic performance analysis in an order-processing system.




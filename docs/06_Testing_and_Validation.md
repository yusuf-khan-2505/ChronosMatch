# 6. Testing and Validation



## 6.1 Introduction



Testing is an important part of ChronosMatch because it helps verify that the core components behave as expected.



The project includes automated unit tests for the limit order book and memory-mapped ring buffer.



## 6.2 Testing Framework



ChronosMatch uses Python's built-in `unittest` framework.



No external testing packages are required.



The test files are located in the `tests/` directory:



```text

tests/

|-- test_book.py

`-- test_ipc.py

```



## 6.3 Running the Tests



Open PowerShell in the project root directory and execute:



```powershell

python -m unittest discover -s tests -v

```



The `-v` option enables verbose output, displaying the individual test names and their results.



## 6.4 Limit Order Book Tests



The `tests/test_book.py` file verifies important matching-engine behavior.



The tests cover:



- Matching compatible BUY and SELL orders.

- Executing trades at the resting order's price.

- Rejecting invalid order prices.

- Rejecting invalid order sides.

- Keeping non-crossing orders in the order book.

- Handling partial order fills.



These tests help verify the basic price-time-priority matching behavior.



## 6.5 Ring Buffer Tests



The `tests/test_ipc.py` file verifies the behavior of the memory-mapped ring buffer.



The tests cover:



- Writing and reading records.

- Returning no record when the buffer is empty.

- Rejecting writes when the buffer is full.

- Rejecting invalid buffer capacities.

- Tracking the number of stored records.

- Reusing buffer space after a record is read.



These tests help verify the basic storage and retrieval operations.



## 6.6 Test Results



During project validation, the following results were observed:



| Component | Tests Passed |

|---|---:|

| Limit Order Book | 6 |

| Memory-Mapped Ring Buffer | 6 |

| Total | 12 |



All 12 unit tests passed in the recorded validation run.



The test results confirm the tested behavior of the order book and ring buffer.



## 6.7 Manual Execution Validation



The application can also be tested by running a simulation from the terminal.



Example:



```powershell

python main.py --orders 10000 --no-dashboard

```



The application reports information such as:



- Number of processed orders.

- Number of dropped write attempts.

- Total elapsed time.

- Processing throughput.

- Average latency.

- P50, P95, and P99 latency.

- Matched quantity.

- Number of trade matches.

- Best bid and ask prices.



This provides a practical way to verify that the complete simulation can run and report its results.



## 6.8 Scope of Testing



The current automated tests focus on the limit order book and ring buffer.



The manual simulation run provides additional execution evidence, but it should not be treated as a complete integration, stress, or production-readiness test.



## 6.9 Conclusion



ChronosMatch uses automated unit tests and manual simulation runs to validate its core functionality.



The 12 passing unit tests provide evidence that the tested order-book and ring-buffer operations work as expected.




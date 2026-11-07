# 3. Installation and Setup



## 3.1 Prerequisites



Before running ChronosMatch, ensure that the following software is installed:



| Requirement | Version |

|---|---|

| Python | 3.10 or later |

| Operating System | Windows, Linux, or macOS |

| Git | Recommended for cloning the repository |



ChronosMatch uses Python's standard library and does not require third-party packages.



## 3.2 Verify Python Installation



Open a terminal or PowerShell window and execute:



```powershell

python --version

```



Expected output will show Python 3.10 or a later version.



Example:



```text

Python 3.13.14

```



If Python is not recognized, install Python and ensure that it is added to the system PATH.



## 3.3 Clone the Repository



Clone the ChronosMatch repository using Git:



```bash

git clone https://github.com/yusuf-khan-2505/ChronosMatch.git

```



Navigate to the project directory:



```bash

cd ChronosMatch

```



## 3.4 Verify Project Files



The main project structure is:



```text

ChronosMatch/
|-- chronosmatch/
|   |-- __init__.py
|   |-- book.py
|   |-- dashboard.py
|   |-- ipc.py
|   |-- metrics.py
|   `-- simulator.py
|-- tests/
|   |-- test_book.py
|   `-- test_ipc.py
|-- main.py
|-- README.md
|-- requirements.txt
|-- EXECUTION_RESULTS.md
`-- docs/


The `docs/` directory contains the project's detailed documentation.



## 3.5 Dependency Setup



ChronosMatch uses only Python standard-library modules.



The `requirements.txt` file contains:



```text

# Standard library only; Python 3.10+

```



No external packages need to be installed.



There is no requirement to create a virtual environment for the basic project execution.



## 3.6 Run the Application



From the project root directory, execute:



```bash

python main.py

```



This starts the simulation with the default settings and displays the live terminal dashboard.



## 3.7 Verify Installation



To verify that the application runs without the live dashboard, execute:



```bash

python main.py --orders 10000 --no-dashboard

```



The application should display its final simulation results, including:



- Number of processed orders

- Number of dropped write attempts

- Elapsed time

- Throughput

- Average latency

- P50, P95, and P99 latency

- Filled units

- Trade matches

- Best bid and ask

- Bid-ask spread



## 3.8 Run Automated Tests



To verify the core project components, execute:



```bash

python -m unittest discover -s tests -v

```



The test suite validates the limit order book and memory-mapped ring buffer.



## 3.9 Troubleshooting



### Python command not recognized



Ensure Python is installed and added to the Windows PATH. Restart the terminal after changing PATH settings.



### Invalid ring buffer capacity



The ring buffer capacity must be a power of two and at least 2.



For example, valid capacities include:



- 1024

- 4096

- 16384

- 65536



### Application runs but no dashboard appears



Check whether the `--no-dashboard` option was supplied. Remove it to enable the live terminal dashboard.



### Import errors



Ensure the terminal is opened in the ChronosMatch project root directory before running the application.



## 3.10 Conclusion



ChronosMatch is designed for simple installation and execution. Since it uses Python's standard library, users can run the simulation without installing additional dependencies.



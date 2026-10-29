# Automated-Log-File-Analyzer
Python utility that analyzes log files and creates a summary report
# Automated Log File Analyzer

A beginner-friendly Python utility that reads system log files, counts ERROR, WARNING and INFO messages, finds the most common problems, and saves a summary report.

Made for the Python Programming Lab (CSE-DS, Semester III), Experiential Learning.

## Features
- Read and analyze a log file
- Identify and count ERROR, WARNING and INFO messages
- Show frequency (count and percentage) and severity of each level
- Show the most common errors and warnings
- Generate and save a report as a text file
- Handle missing files and invalid log formats without crashing

## Project Structure
```
Automated-Log-File-Analyzer/
├── log_analyzer.py        # main program
├── test_log_analyzer.py   # test cases
├── sample_logs/           # sample.log, invalid.log
├── reports/               # saved reports appear here
├── .gitignore
└── README.md
```

## Requirements
- Python 3.8 or newer
- No extra libraries needed (uses only `os` and `datetime`)

## Installation
```
git clone https://github.com/YOUR-USERNAME/Automated-Log-File-Analyzer.git
cd Automated-Log-File-Analyzer
```

## How to Run
```
python log_analyzer.py
```
Choose an option from the menu:
1. Analyze a log file (press Enter to use the sample log)
2. Display the analysis summary
3. Show the most common errors and warnings
4. Generate and save a report
5. Exit

## Log Format
```
YYYY-MM-DD HH:MM:SS LEVEL message text
2026-10-24 08:10:45 ERROR Database connection failed
```
Valid levels: ERROR, WARNING, INFO. Other lines are skipped and counted as invalid.

## Logic Summary
1. Open the log file and read it line by line.
2. Split each line into date, time, level and message.
3. Skip lines with a wrong format.
4. Count each level, and count how often each error and warning message repeats (using dictionaries).
5. Calculate percentages and set severity: ERROR = High, WARNING = Medium, INFO = Low.
6. Sort the messages to find the most common ones.
7. Save everything to a `.txt` report using Python file handling.

## Sample Output
```
Level      Count   Percent   Severity
--------------------------------------------------
ERROR          7     35.0%   High
WARNING        5     25.0%   Medium
INFO           8     40.0%   Low
--------------------------------------------------
Overall status       : CRITICAL
```

## Run Tests
```
python test_log_analyzer.py
```

## Author
Your Name, CSE (Data Science), S. B. Jain Institute of Technology, Management & Research, Nagpur
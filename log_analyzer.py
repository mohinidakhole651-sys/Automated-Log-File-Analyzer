"""
Automated Log File Analyzer
Reads a log file, counts ERROR, WARNING and INFO messages,
and creates a summary report.

Log line format:  YYYY-MM-DD HH:MM:SS LEVEL message text
Example:          2026-10-24 08:10:45 ERROR Database connection failed
"""

import os
from datetime import datetime

# ---------- Settings ----------
SAMPLE_LOG_PATH = os.path.join("sample_logs", "sample.log")
REPORTS_FOLDER = "reports"
LEVELS = ["ERROR", "WARNING", "INFO"]
SEVERITY = {"ERROR": "High", "WARNING": "Medium", "INFO": "Low"}


def create_empty_results():
    """Make a fresh dictionary to store the analysis results."""
    return {
        "file_name": "",
        "total_lines": 0,
        "valid_lines": 0,
        "invalid_lines": 0,
        "counts": {"ERROR": 0, "WARNING": 0, "INFO": 0},
        "error_messages": {},
        "warning_messages": {},
    }


def add_to_dictionary(dictionary, key):
    """Add 1 to the count of 'key'. If the key is new, start from 1."""
    if key in dictionary:
        dictionary[key] = dictionary[key] + 1
    else:
        dictionary[key] = 1


def parse_log_line(line):
    """
    Break one log line into (level, message).
    Return None if the line is not in the correct format.
    """
    parts = line.strip().split(" ", 3)  # date, time, level, message
    if len(parts) < 4:
        return None

    date_text, time_text, level, message = parts
    level = level.upper()

    # Check that the date and time are real
    try:
        datetime.strptime(date_text + " " + time_text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    # Only ERROR, WARNING and INFO are accepted
    if level not in LEVELS:
        return None

    return level, message.strip()


def analyze_log_file(file_path):
    """
    Read the log file line by line and count the messages.
    Return the results dictionary, or None if something goes wrong.
    """
    results = create_empty_results()

    try:
        with open(file_path, "r", encoding="utf-8") as log_file:
            for line in log_file:
                if line.strip() == "":  # skip empty lines
                    continue

                results["total_lines"] += 1
                parsed = parse_log_line(line)

                if parsed is None:  # wrong format
                    results["invalid_lines"] += 1
                    continue

                level, message = parsed
                results["valid_lines"] += 1
                results["counts"][level] += 1

                if level == "ERROR":
                    add_to_dictionary(results["error_messages"], message)
                elif level == "WARNING":
                    add_to_dictionary(results["warning_messages"], message)

    except FileNotFoundError:
        print("Error: File not found -> " + file_path)
        return None
    except PermissionError:
        print("Error: You do not have permission to open this file.")
        return None
    except UnicodeDecodeError:
        print("Error: This file is not a normal text log file.")
        return None
    except OSError:
        print("Error: Could not read this path. Please enter a log file path.")
        return None

    if results["valid_lines"] == 0:
        print("No valid log entries found. Please check the log format.")
        return None

    results["file_name"] = os.path.basename(file_path)
    return results


def calculate_percent(count, total):
    """Return count as a percentage of total (avoid dividing by zero)."""
    if total == 0:
        return 0.0
    return count / total * 100


def get_health_status(results):
    """Give an overall status based on the percentage of errors."""
    error_percent = calculate_percent(results["counts"]["ERROR"], results["valid_lines"])
    if error_percent >= 30:
        return "CRITICAL"
    elif error_percent >= 10:
        return "NEEDS ATTENTION"
    else:
        return "HEALTHY"


def build_summary_text(results):
    """Create the summary as text (used for screen and for the report)."""
    valid = results["valid_lines"]
    lines = []
    lines.append("=" * 50)
    lines.append("LOG ANALYSIS SUMMARY")
    lines.append("=" * 50)
    lines.append("File analyzed        : " + results["file_name"])
    lines.append("Total lines read     : " + str(results["total_lines"]))
    lines.append("Valid log entries    : " + str(valid))
    lines.append("Invalid lines skipped: " + str(results["invalid_lines"]))
    lines.append("")
    lines.append(f"{'Level':<10}{'Count':>6}{'Percent':>10}   Severity")
    lines.append("-" * 50)
    for level in LEVELS:
        count = results["counts"][level]
        percent = calculate_percent(count, valid)
        lines.append(f"{level:<10}{count:>6}{percent:>9.1f}%   {SEVERITY[level]}")
    lines.append("-" * 50)
    lines.append("Overall status       : " + get_health_status(results))
    return "\n".join(lines)


def get_most_common(message_counts, top_n=3):
    """Sort messages from highest count to lowest and return the top ones."""
    sorted_items = sorted(message_counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_items[:top_n]


def format_common_section(title, message_counts):
    """Make the lines for one list (top errors or top warnings)."""
    lines = [title]
    top_items = get_most_common(message_counts)
    if len(top_items) == 0:
        lines.append("  None found.")
    else:
        rank = 1
        for message, count in top_items:
            lines.append(f"  {rank}. {message} -> {count} time(s)")
            rank = rank + 1
    return lines


def build_common_issues_text(results):
    """Create the 'most common errors and warnings' text."""
    lines = []
    lines.append("=" * 50)
    lines.append("MOST COMMON ERRORS AND WARNINGS")
    lines.append("=" * 50)
    lines.extend(format_common_section("Top Errors:", results["error_messages"]))
    lines.append("")
    lines.extend(format_common_section("Top Warnings:", results["warning_messages"]))
    return "\n".join(lines)


def save_report(results):
    """Save the analysis to a new .txt file inside the reports folder."""
    os.makedirs(REPORTS_FOLDER, exist_ok=True)  # create folder if missing

    now = datetime.now()
    file_stamp = now.strftime("%Y%m%d_%H%M%S")
    created_on = now.strftime("%Y-%m-%d %H:%M:%S")
    report_path = os.path.join(REPORTS_FOLDER, "report_" + file_stamp + ".txt")

    report_text = "AUTOMATED LOG FILE ANALYZER - REPORT\n"
    report_text += "Generated on: " + created_on + "\n\n"
    report_text += build_summary_text(results) + "\n\n"
    report_text += build_common_issues_text(results) + "\n"

    try:
        with open(report_path, "w", encoding="utf-8") as report_file:
            report_file.write(report_text)
    except OSError:
        print("Error: Could not save the report.")
        return None

    return report_path


def show_menu():
    """Print the menu options."""
    print("\n===== AUTOMATED LOG FILE ANALYZER =====")
    print("1. Analyze a log file")
    print("2. Display the analysis summary")
    print("3. Show the most common errors and warnings")
    print("4. Generate and save a report")
    print("5. Exit")


def main():
    """Run the menu in a loop until the user chooses Exit."""
    results = None  # nothing analyzed yet

    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            file_path = input("Enter the log file path (or press Enter for the sample log): ")
            file_path = file_path.strip().strip('"')
            if file_path == "":
                file_path = SAMPLE_LOG_PATH

            new_results = analyze_log_file(file_path)
            if new_results is not None:
                results = new_results
                print("Analysis complete for: " + results["file_name"])
                for level in LEVELS:
                    print(f"  {level:<8}: {results['counts'][level]}")

        elif choice == "2":
            if results is None:
                print("Please analyze a log file first (option 1).")
            else:
                print(build_summary_text(results))

        elif choice == "3":
            if results is None:
                print("Please analyze a log file first (option 1).")
            else:
                print(build_common_issues_text(results))

        elif choice == "4":
            if results is None:
                print("Please analyze a log file first (option 1).")
            else:
                saved_path = save_report(results)
                if saved_path is not None:
                    print("Report saved successfully: " + saved_path)

        elif choice == "5":
            print("Thank you for using the Log Analyzer. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


# This line runs main() only when you run this file directly
if __name__ == "__main__":
    main()
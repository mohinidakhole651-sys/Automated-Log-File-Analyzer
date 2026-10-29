from log_analyzer import parse_log_line, analyze_log_file, get_most_common


def test_valid_line():
    line = "2026-10-24 10:00:00 ERROR Disk failed"
    assert parse_log_line(line) == ("ERROR", "Disk failed")


def test_invalid_line():
    assert parse_log_line("this is not a log line") is None


def test_unknown_level():
    assert parse_log_line("2026-10-24 10:00:00 DEBUG Cache cleared") is None


def test_sample_counts():
    results = analyze_log_file("sample_logs/sample.log")
    assert results["counts"]["ERROR"] == 7
    assert results["counts"]["WARNING"] == 5
    assert results["counts"]["INFO"] == 8
    assert results["invalid_lines"] == 2


def test_most_common_error():
    results = analyze_log_file("sample_logs/sample.log")
    top_errors = get_most_common(results["error_messages"])
    assert top_errors[0] == ("Database connection failed", 3)


def test_missing_file():
    assert analyze_log_file("no_such_file.log") is None


def test_invalid_file():
    assert analyze_log_file("sample_logs/invalid.log") is None


if __name__ == "__main__":
    test_valid_line()
    test_invalid_line()
    test_unknown_level()
    test_sample_counts()
    test_most_common_error()
    test_missing_file()
    test_invalid_file()
    print("All tests passed!")
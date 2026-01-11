def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns: list of raw lines (strings)
    """
    encodings = ["utf-8", "latin-1", "cp1252"]
    lines = []

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                for line in file:
                    line = line.strip()
                    if line:
                        lines.append(line)
            break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filename}")

    return lines

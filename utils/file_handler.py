def read_sales_file(file_path):
    records = []
    with open(file_path, mode="r", encoding="latin-1") as file:
        header = file.readline().strip().split("|")

        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split("|")
            records.append(parts)

    return header, records

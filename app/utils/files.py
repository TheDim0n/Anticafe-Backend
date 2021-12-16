import os
import csv
import json
import tempfile


def data_to_csv(header, data, additional_rows=[]):
    with tempfile.NamedTemporaryFile(mode="w", delete=False,
                                     newline='', encoding="utf-8") as f:
        outcsv = csv.writer(f, delimiter=',')
        outcsv.writerow(header)
        for row in data:
            outcsv.writerow([getattr(row, c) for c in header])
        for row in additional_rows:
            outcsv.writerow([getattr(row, c) for c in header])
    return f


def delete_file(filepath: str):
    os.remove(filepath)


def json_loader(path: str):
    with open(path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data

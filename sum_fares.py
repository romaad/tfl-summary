import csv
import glob
import sys
from dataclasses import dataclass

import termplotlib as tpl

DATE_KEY = "Date"
FARE_KEY = "Daily Charge (GBP)"

MNTH_NAME = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


@dataclass
class Summary:
    total_fare: float
    num_trips: int
    days_covered: int
    days_per_month: dict[str, int]
    fare_per_month: dict[str, float]


@dataclass(frozen=True)
class Date:
    year: int
    month: int
    day: int


def fmt_month(year: int, month: int) -> str:
    return f"{year}/" + str(month).zfill(2)


def gen_key(row: dict[str, str]) -> str:
    return f"{row[DATE_KEY]}_{row[FARE_KEY]}"


def get_date(date_str: str) -> Date:
    day, month, year = date_str.split("/")
    return Date(int(year), int(month), int(day))


def sum_fares(file_patterns) -> Summary:
    total = 0.0
    hash_mp = {}
    dates_mp = set()
    months_summary = {}
    total_trips = 0
    for pattern in file_patterns:
        for filepath in glob.glob(pattern):
            with open(filepath, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if gen_key(row) in hash_mp:
                        print(f"Duplicate row skipped: {row[DATE_KEY]} {row[FARE_KEY]}")
                        continue
                    total_trips += 1
                    hash_mp[gen_key(row)] = 1
                    print(row[DATE_KEY], row[FARE_KEY])
                    total += float(row[FARE_KEY])
                    dt = get_date(row[DATE_KEY])
                    dates_mp.add(dt)
                    months_summary.setdefault(dt.year, {}).setdefault(dt.month, 0)
                    months_summary[dt.year][dt.month] += float(row[FARE_KEY])

    days_per_month = {
        fmt_month(y, m): sum(1 for d in dates_mp if d.month == m and d.year == y)
        for y in range(
            min({d.year for d in dates_mp}), max({d.year for d in dates_mp}) + 1
        )
        for m in range(1, 13)
    }
    fare_per_month = {
        fmt_month(y, m): months_summary[y][m]
        for y in months_summary.keys()
        for m in months_summary[y].keys()
    }

    return Summary(
        total_fare=total,
        num_trips=total_trips,
        days_covered=len(dates_mp),
        days_per_month=days_per_month,
        fare_per_month=fare_per_month,
    )


def printBarChart(arr: dict[str, int | float], title: str) -> None:
    print(title)
    fig = tpl.figure()
    # fig.set_title(title)
    sorted_items = sorted(arr.items(), key=lambda x: x[0], reverse=True)
    fig.barh(
        list(abs(val[1]) for val in sorted_items),
        list(val[0] for val in sorted_items),
        val_format="{:06.2f}",
    )
    fig.show()
    print("\n\n")


def print_summary(summary: Summary):
    print(f"Total: £{summary.total_fare:.2f}")
    print(f"Total Trips: {summary.num_trips}")
    print(f"Days Covered: {summary.days_covered}")
    # print(f"Days per Month: {summary.days_per_month}")
    print(f"Average Daily Fares: {summary.total_fare / summary.days_covered:.2f}")
    print(f"Average Monthly Fares: {summary.total_fare / 12:.2f}")
    printBarChart(summary.fare_per_month, "Monthly Fares (GBP)")
    printBarChart(summary.days_per_month, "Active days per Month")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sum_fares.py <file1.csv> [file2.csv ...]")
        sys.exit(1)
    result = sum_fares(sys.argv[1:])
    print_summary(result)
    # print(f"Total: £{result.total_fare:.2f}")


"""
 python3 -m venv venv
 source venv/bin/activate
 pip install termplotlib
 python3 sum_fares.py "folder/*.csv"
"""

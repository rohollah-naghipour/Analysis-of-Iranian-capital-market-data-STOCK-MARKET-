import json
import requests
import matplotlib.pyplot as plt

# ----------------------------------
# تنظیمات
# ----------------------------------

DB_FILE = "groups_database.json"

TARGET_DATE = 20260225  # 1404/12/06

# ----------------------------------
# پیدا کردن نمادهای یک گروه
# ----------------------------------

def get_group_symbols(group_name, db):

    for group in db["groups"]:

        if group["name"].strip() == group_name.strip():

            return group["companies"]

    return []


# ----------------------------------
# تبدیل نماد به InsCode
# ----------------------------------

def get_inscode_from_symbol(symbol):

    url = (
        "https://cdn.tsetmc.com/api/Instrument/"
        f"GetInstrumentSearch/{symbol}"
    )

    data = requests.get(
        url,
        timeout=20
    ).json()

    rows = data.get(
        "instrumentSearch",
        []
    )

    for row in rows:

        if (
            row.get(
                "lVal18AFC",
                ""
            ).strip()
            ==
            symbol.strip()
        ):

            return str(
                row["insCode"]
            )

    return None


# ----------------------------------
# قیمت امروز
# ----------------------------------

def get_today_price(ins_code):

    url = (
        f"https://cdn.tsetmc.com/api/ClosingPrice/"
        f"GetClosingPriceInfo/{ins_code}"
    )

    data = requests.get(
        url,
        timeout=20
    ).json()

    return data["closingPriceInfo"]["pDrCotVal"]


# ----------------------------------
# قیمت تاریخ هدف
# ----------------------------------

def get_old_price(ins_code):

    url = (
        f"https://cdn.tsetmc.com/api/ClosingPrice/"
        f"GetClosingPriceDailyList/{ins_code}/0"
    )

    data = requests.get(
        url,
        timeout=20
    ).json()

    rows = []

    if isinstance(data, list):

        rows = data

    elif isinstance(data, dict):

        rows = data.get(
            "closingPriceDaily",
            []
        )

    for row in rows:

        if (
            int(
                row.get(
                    "dEven",
                    0
                )
            )
            ==
            TARGET_DATE
        ):

            return (
                row.get("pDrCotVal")
                or row.get("pClosing")
                or row.get("priceYesterday")
            )

    return None


# ----------------------------------
# خواندن دیتابیس
# ----------------------------------

with open(
    DB_FILE,
    "r",
    encoding="utf-8"
) as f:

    db = json.load(f)

# ----------------------------------
# انتخاب گروه
# ----------------------------------

group_name = input(
    "نام گروه: "
).strip()

symbols = get_group_symbols(
    group_name,
    db
)

if not symbols:

    print("گروه پیدا نشد")
    exit()

print(
    f"{len(symbols)} نماد پیدا شد"
)

# ----------------------------------
# پردازش نمادها
# ----------------------------------

results = []

for symbol in symbols:

    try:

        print(
            f"در حال بررسی {symbol}"
        )

        ins_code = (
            get_inscode_from_symbol(
                symbol
            )
        )

        if not ins_code:

            print(
                f"{symbol} => InsCode پیدا نشد"
            )

            continue

        today_price = (
            get_today_price(
                ins_code
            )
        )

        old_price = (
            get_old_price(
                ins_code
            )
        )

        if old_price is None:

            print(
                f"{symbol} => تاریخ پیدا نشد"
            )

            continue

        percent_change = (
            (
                today_price
                -
                old_price
            )
            /
            old_price
        ) * 100

        results.append(
            (
                symbol,
                round(
                    percent_change,
                    2
                )
            )
        )

        print(
            f"{symbol} => "
            f"{percent_change:.2f}%"
        )

    except Exception as e:

        print(
            f"{symbol} => ERROR: {e}"
        )

# ----------------------------------
# مرتب سازی
# ----------------------------------

results.sort(
    key=lambda x: x[1],
    reverse=True
)

# ----------------------------------
# ذخیره خروجی
# ----------------------------------

with open(
    "output.txt",
    "w",
    encoding="utf-8"
) as f:

    for symbol, percent in results:

        f.write(
            f"{symbol} | "
            f"{percent:.2f}%\n"
        )

print(
    "\nSaved to output.txt"
)

# ----------------------------------
# رسم نمودار
# ----------------------------------

if not results:

    print("No data to plot.")
    exit()

names = [
    r[0]
    for r in results
]

values = [
    r[1]
    for r in results
]

plt.figure(
    figsize=(15, 8)
)

bars = plt.bar(
    names,
    values
)

for i, bar in enumerate(bars):

    if values[i] >= 0:

        bar.set_color(
            "green"
        )

    else:

        bar.set_color(
            "red"
        )

plt.axhline(
    y=0,
    color="black"
)

plt.title(
    f"درصد تغییر قیمت گروه {group_name}"
)

plt.ylabel(
    "Percent Change"
)

plt.xticks(
    rotation=90
)

plt.tight_layout()

plt.show()
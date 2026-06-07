import requests

def get_inscode_from_symbol(symbol):
    url = (
        "https://cdn.tsetmc.com/api/Instrument/"
        f"GetInstrumentSearch/{symbol}"
    )

    data = requests.get(url, timeout=20).json()

    rows = data.get("instrumentSearch", [])

    # پیدا کردن تطابق دقیق نماد
    for row in rows:

        if row.get("lVal18AFC", "").strip() == symbol.strip():

            return str(row["insCode"])

    return None


results = []



with open(
    "group_names.txt",
    "r",
    encoding="utf-8"
) as f:

    symbols = [
        line.strip()
        for line in f
        if line.strip()
    ]


today_price = 16542
old_price = 11325



for symbol in symbols:

        #ins_code = get_inscode_from_symbol(symbol)

        #if not ins_code:

           # results.append(
             #   f"{symbol} | INS_CODE_NOT_FOUND"
            #)
            #continue

       # today_price = get_today_price(ins_code)

      #  old_price = get_old_price(ins_code)

        #if old_price is None:

         #   results.append(
          #      f"{symbol} | DATE_NOT_FOUND"
           # )
            #continue

        percent_change = (
            (today_price - old_price)
            / old_price
        ) * 100

        results.append(
            (
                symbol,
                percent_change
            )
        )
        

numeric_results = [
    x for x in results
    if isinstance(x, tuple)
]

numeric_results.sort(
    key=lambda x: x[1],
    reverse=True
)


with open(
    "output.txt",
    "w",
    encoding="utf-8"
) as f:

    for symbol, percent in numeric_results:

        f.write(
            f"{symbol} | {percent:.2f}%\n"
        )


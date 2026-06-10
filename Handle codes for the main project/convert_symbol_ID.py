import json
import requests
import time

INPUT_FILE = "groups_database_fixed.json"
OUTPUT_FILE = "symbols_with_inscode.json"


def get_inscode_from_symbol(symbol):
    """
    پیدا کردن InsCode از روی نماد
    """

    url = (
        "https://cdn.tsetmc.com/api/Instrument/"
        f"GetInstrumentSearch/{symbol}"
    )

    try:

        response = requests.get(
            url,
            timeout=20
        )

        data = response.json()

        rows = data.get(
            "instrumentSearch",
            []
        )

        # تطابق دقیق نماد
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

        # اگر تطابق دقیق نبود
        if rows:

            return str(
                rows[0]["insCode"]
            )

    except Exception as e:

        print(
            f"Error for {symbol}: {e}"
        )

    return None


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    db = json.load(f)


result = {}


for group in db["groups"]:

    group_name = group["name"]

    print(
        f"\nProcessing: {group_name}"
    )

    result[group_name] = []

    for symbol in group["companies"]:

        print(
            f"  {symbol}"
        )

        ins_code = (
            get_inscode_from_symbol(
                symbol
            )
        )

        if ins_code:

            result[
                group_name
            ].append(
                {
                    "symbol": symbol,
                    "insCode": ins_code
                }
            )

        else:

            result[
                group_name
            ].append(
                {
                    "symbol": symbol,
                    "insCode": None
                }
            )

        time.sleep(0.3)


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        ensure_ascii=False,
        indent=2
    )


print(
    f"\nSaved => {OUTPUT_FILE}"
)
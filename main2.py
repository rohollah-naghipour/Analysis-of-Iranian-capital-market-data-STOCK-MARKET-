import requests

TARGET_DATE = 20260225  # 1404/12/06

ins_code = input("InsCode: ").strip()

# ------------------------
# قیمت امروز
# ------------------------
today_url = (
    f"https://cdn.tsetmc.com/api/ClosingPrice/"
    f"GetClosingPriceInfo/{ins_code}"
)

today_data = requests.get(today_url).json()

today_price = today_data["closingPriceInfo"]["pDrCotVal"]

# ------------------------
# نام نماد و نام لاتین
# ------------------------
info_url = (
    f"https://cdn.tsetmc.com/api/Instrument/"
    f"GetInstrumentInfo/{ins_code}"
)

symbol_name = ""
latin_name = ""

try:
    info = requests.get(info_url).json()

    # بسته به ساختار پاسخ API
    symbol_name = str(info)
    latin_name = str(info)

except:
    pass

# ------------------------
# تاریخچه
# ------------------------
history_url = (
    f"https://cdn.tsetmc.com/api/ClosingPrice/"
    f"GetClosingPriceDailyList/{ins_code}/0"
)

history = requests.get(history_url).json()

old_price = None

# بعضی endpointها لیست مستقیم برمی‌گردانند
if isinstance(history, list):

    for row in history:

        if int(row.get("dEven", 0)) == TARGET_DATE:

            # معمولاً یکی از این فیلدها وجود دارد
            old_price = (
                row.get("pDrCotVal")
                or row.get("pClosing")
                or row.get("priceYesterday")
            )

            break

# بعضی endpointها آبجکت برمی‌گردانند
elif isinstance(history, dict):

    for row in history.get("closingPriceDaily", []):

        if int(row.get("dEven", 0)) == TARGET_DATE:

            old_price = (
                row.get("pDrCotVal")
                or row.get("pClosing")
                or row.get("priceYesterday")
            )

            break

if old_price is None:
    print("Price for 2026-02-25 not found")
    exit()

ratio = today_price / old_price
percent_change = (ratio - 1) * 100

print("-" * 50)
print(f"InsCode: {ins_code}")
print(f"Today Price: {today_price}")
print(f"2026-02-25 Price: {old_price}")
print(f"Ratio: {ratio:.4f}")
print(f"Percent Change: {percent_change:.2f}%")

if latin_name:
    print(f"English Name: {latin_name}")
import requests
import time
import matplotlib.pyplot as plt

TARGET_DATE = 20260225

INPUT_FILE = "symbols.txt"
OUTPUT_FILE = "output.txt"


def get_today_price(ins_code):
    url = f"https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/{ins_code}"

    data = requests.get(url, timeout=20).json()

    return data["closingPriceInfo"]["pDrCotVal"]


def get_old_price(ins_code):
    url = (
        f"https://cdn.tsetmc.com/api/ClosingPrice/"
        f"GetClosingPriceDailyList/{ins_code}/0"
    )

    data = requests.get(url, timeout=20).json()

    rows = []

    if isinstance(data, list):
        rows = data

    elif isinstance(data, dict):
        rows = data.get("closingPriceDaily", [])

    for row in rows:

        if int(row.get("dEven", 0)) == TARGET_DATE:

            return (
                row.get("pDrCotVal")
                or row.get("pClosing")
                or row.get("priceYesterday")
            )

    return None

def get_symbol_name(ins_code):

    url = (
        f"https://cdn.tsetmc.com/api/Instrument/"
        f"GetInstrumentInfo/{ins_code}"
    )

    data = requests.get(url, timeout=20).json()

    instrument = data.get("instrumentInfo", {})

    symbol_name = (
        instrument.get("lVal18AFC")
        or instrument.get("lVal30")
        or ins_code
    )

    return symbol_name



with open(INPUT_FILE, "r", encoding="utf-8") as f:
    symbols = [line.strip() for line in f if line.strip()]

results = []

x = []
y = []

for ins_code in symbols:
    try:
        today_price = get_today_price(ins_code)
        old_price = get_old_price(ins_code)

        if old_price is None:
            results.append(
                f"{ins_code} => DATE_NOT_FOUND"
            )
            continue

        percent_change = (
            (today_price - old_price)
            / old_price
        ) * 100
        
        symbol_name = get_symbol_name(ins_code)
        
        x.append(symbol_name)
        y.append(percent_change)

        results.append(f"{symbol_name} | {ins_code} | {percent_change:.2f}%")

        results.append(f"{ins_code} => {percent_change:.2f}%")

        print(f"{ins_code} => {percent_change:.2f}%")

        time.sleep(0.3)

    except Exception as e:
        results.append(f"{ins_code} => ERROR: {e}")
        
    #Drawing a chart            
#plt.bar(x,y)
#plt.show()        
    if x and y:  
        plt.figure(figsize=(10, 6))
        plt.bar(x, y)
        plt.title('درصد تغییر قیمت سهام نسبت به تاریخ هدف', fontsize=14)
        plt.xlabel('نام سهم', fontsize=12)
        plt.ylabel('درصد تغییر', fontsize=12)
        plt.xticks(rotation=45, ha='right')  # چرخاندن نام سهام‌ها برای خوانایی بهتر
        plt.tight_layout()  # تنظیم خودکار فاصله‌ها
        plt.show()
    else:
        print("داده‌ای برای رسم نمودار وجود ندارد.")

#with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    #for row in results:
        #f.write(row + "\n")

#print(f"Saved to {OUTPUT_FILE}")
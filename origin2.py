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
    url = f"https://cdn.tsetmc.com/api/Instrument/GetInstrumentInfo/{ins_code}"
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
        symbol_name = get_symbol_name(ins_code)
        
        today_price = get_today_price(ins_code)
        old_price = get_old_price(ins_code)

        if old_price is None:
            results.append(f"{symbol_name} ({ins_code}) => DATE_NOT_FOUND")
            continue

        percent_change = ((today_price - old_price) / old_price) * 100

        # استفاده از کد به جای نام فارسی
        x.append(symbol_name)  # تغییر: به جای نام فارسی، کد سهم
        y.append(percent_change)

        results.append(f"{symbol_name} | {ins_code} | {percent_change:.2f}%")
        print(f"{symbol_name} ({ins_code}) => {percent_change:.2f}%")

        time.sleep(0.3)

    except Exception as e:
        results.append(f"{ins_code} => ERROR: {e}")

# رسم نمودار با سایز مناسب
if x and y:
    plt.figure(figsize=(10, 6))  # سایز کوچکتر
    
    # تنظیم عرض میله‌ها
    bars = plt.bar(x, y, width=0.6)  # width=0.6 باعث می‌شود میله‌ها باریک‌تر شوند
    
    # رنگ‌بندی بر اساس مثبت یا منفی بودن
    for i, bar in enumerate(bars):
        if y[i] >= 0:
            bar.set_color('green')
        else:
            bar.set_color('red')
    
    plt.title('Stock Price Change Percentage', fontsize=12)
    plt.xlabel('Symbol Code', fontsize=10)
    plt.ylabel('Change (%)', fontsize=10)
    
    # چرخاندن برچسب‌ها و تنظیم فاصله
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=8)
    
    # اضافه کردن خط صفر
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # اضافه کردن مقدار روی میله‌ها (اختیاری)
    for i, (code, value) in enumerate(zip(x, y)):
        plt.text(i, value + (0.5 if value >= 0 else -2), 
                f'{value:.1f}%', 
                ha='center', 
                fontsize=8)
    
    plt.tight_layout()
    plt.grid(True, alpha=0.3, axis='y')
    plt.show()
else:
    print("No data to plot.")

# ذخیره نتایج در فایل
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for row in results:
        f.write(row + "\n")

print(f"Saved to {OUTPUT_FILE}")
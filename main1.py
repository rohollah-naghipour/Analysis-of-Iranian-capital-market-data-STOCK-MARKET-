import requests

ins_code = input("InsCode: ")

# آخرین معامله امروز
url_today = f"https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/{ins_code}"
today_data = requests.get(url_today).json()


print(today_data)

temp = str(today_data)

with open("test.txt", "w", encoding="utf-8") as f:
  f.write(temp)

#open and read the file after the appending:
#with open("demofile.txt") as f:
  #print(f.read())


last_price_today = today_data["closingPriceInfo"]["priceYesterday"]


# این فیلد را بعد از تست API با فیلد آخرین معامله جایگزین کن


#print("last_price_today: ", last_price_today)

print("_______________________________________________________________")


# تاریخ مورد نظر
date = "14041206"

# سابقه قیمت
url_history = (
    f"https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/{ins_code}/0"
)

history = requests.get(url_history).json()

old_price = None

for row in history["closingPriceDaily"]:
    if str(row["dEven"]) == date:
        old_price = row["priceYesterday"]  # فیلد آخرین معامله آن روز
        break

if old_price is None:

    print("Date not found")
else:
    ratio = last_price_today / old_price
    percent_change = (ratio - 1) * 100

    print(f"Today's price: {last_price_today}")
    print(f"Price 1404/12/06: {old_price}")
    print(f"Ratio: {ratio:.4f}")
    print(f"Percentage change: {percent_change:.2f}%")
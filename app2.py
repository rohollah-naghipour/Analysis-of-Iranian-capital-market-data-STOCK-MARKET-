import time
import requests

symbol_id = "46348559193224090"  


url = f"http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/{symbol_id}"


data = requests.get(url).json()

close_price = data["closingPriceInfo"]["pClosing"]

print(close_price)



#current_price = data["closingPriceInfo"]["pDrCotVal"]

        
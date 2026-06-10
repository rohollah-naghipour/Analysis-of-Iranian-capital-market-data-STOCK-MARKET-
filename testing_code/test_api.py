import requests

ins_code = input("InsCode: ")

# آخرین معامله امروز
url_today = f"https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/{ins_code}"
response = requests.get(url_today)

# Check if request was successful
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {response.headers}")
print(f"Response Text (first 500 chars): {response.text[:500]}")

# Only parse JSON if response is OK
if response.status_code == 200:
    try:
        today_data = response.json()
        print(today_data)
        
        with open("test.txt", "w", encoding="utf-8") as f:
            f.write(str(today_data))
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print("Response content is not valid JSON")
        # Save raw response for debugging
        #with open("debug_response.txt", "w", encoding="utf-8") as f:
            #f.write(response.text)
else:
    print(f"API returned error status code: {response.status_code}")
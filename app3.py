import requests



symbols = requests.get(
    "http://cdn.tsetmc.com/api/Instrument/GetInstrumentSearch/خودرو"
).json()

print(symbols)
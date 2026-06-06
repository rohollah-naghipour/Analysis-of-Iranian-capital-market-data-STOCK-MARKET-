import requests


url = "https://tle.ivanstanojevic.me/api/tle/"

headers = {
    'User-Agent': 'python-requests/2.31.0',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Connection': 'keep-alive',
}

r = requests.get(url, headers=headers)

print(r.text, r.status_code)





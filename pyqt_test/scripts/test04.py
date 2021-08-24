import requests, json

def test04():
    barcode_data = 1
    data = {'barcode_data': barcode_data} 
    URL = 'http://1.232.197.66:3000/studentbarcode'
    res = requests.post(URL, data=json.dumps(data))
    print(res.json())

test04()
import json

import requests

scanner_type = "turkey"
exchange_name = "BIST"

x = requests.get('https://scanner.tradingview.com/' + scanner_type + '/scan')
y = json.loads(x.content)
print(y)
print()

symbol_names = list()
exchange_names = set()
if exchange_name not in {"GOLD", "SILVER"}:
    for i in range(y['totalCount']):
        if y['data'][i]['s'].split(":")[0] == exchange_name:
            symbol_names.append(y['data'][i]['s'].split(":")[1])
else:
    symbol_names.append(exchange_name)
print()
symbol_names.sort()
print(symbol_names)
# Veri çekme ve kaydetme işlemi

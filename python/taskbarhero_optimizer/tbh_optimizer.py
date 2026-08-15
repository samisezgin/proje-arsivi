#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TBH Task Bar Hero — Farming Optimizer & Save Editor"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import hashlib, json, gzip, os, sys, time, shutil
from Crypto.Cipher import AES

# ─── Config ──────────────────────────────────────────────────────────────────
ES3_PASSWORD = 'emuMqG3bLYJ938ZDCfieWJ'
SAVE_DIR  = os.path.expandvars(r'%USERPROFILE%\AppData\LocalLow\TesseractStudio\TaskBarHero')
SAVE_FILE = os.path.join(SAVE_DIR, 'SaveFile_Live.es3')

HERO_NAMES = {101: 'Knight', 201: 'Ranger', 301: 'Sorcerer', 401: 'Priest', 501: 'Hunter', 601: 'Slayer'}
CURRENCY_NAMES = {100001: 'Gold', 100002: 'Diamonds', 100003: 'SoulStones'}

DIFF_ORDER = {'NORMAL': 0, 'NIGHTMARE': 1, 'HELL': 2, 'TORMENT': 3}

# ─── Stage data (source: tbh-copilot farm_data.js) ───────────────────────────
STAGES = [
    {"key":1101,"label":"1-1","level":1, "difficulty":"NORMAL",    "name":"Pasture",                   "waves":10,"totalHP":560,       "expectedGold":14,    "expectedEXP":16},
    {"key":1102,"label":"1-2","level":2, "difficulty":"NORMAL",    "name":"Shadow Meadow",              "waves":11,"totalHP":2040,      "expectedGold":50,    "expectedEXP":46},
    {"key":1103,"label":"1-3","level":3, "difficulty":"NORMAL",    "name":"Wasteland",                  "waves":11,"totalHP":3137,      "expectedGold":99,    "expectedEXP":79},
    {"key":1104,"label":"1-4","level":5, "difficulty":"NORMAL",    "name":"Eerie Canyon",               "waves":12,"totalHP":6795,      "expectedGold":197,   "expectedEXP":298},
    {"key":1105,"label":"1-5","level":6, "difficulty":"NORMAL",    "name":"Burning Village Entrance",   "waves":12,"totalHP":15475,     "expectedGold":339,   "expectedEXP":739},
    {"key":1106,"label":"1-6","level":7, "difficulty":"NORMAL",    "name":"Rumstreet Square",           "waves":12,"totalHP":33335,     "expectedGold":463,   "expectedEXP":1170},
    {"key":1107,"label":"1-7","level":8, "difficulty":"NORMAL",    "name":"City Outskirts",             "waves":12,"totalHP":21072,     "expectedGold":356,   "expectedEXP":1511},
    {"key":1108,"label":"1-8","level":10,"difficulty":"NORMAL",    "name":"Cemetery",                   "waves":13,"totalHP":33838,     "expectedGold":580,   "expectedEXP":2697},
    {"key":1109,"label":"1-9","level":11,"difficulty":"NORMAL",    "name":"Cursed Land",                "waves":13,"totalHP":80949,     "expectedGold":1007,  "expectedEXP":5981},
    {"key":1201,"label":"2-1","level":13,"difficulty":"NORMAL",    "name":"Oasis Road",                 "waves":14,"totalHP":92524,     "expectedGold":911,   "expectedEXP":7443},
    {"key":1202,"label":"2-2","level":14,"difficulty":"NORMAL",    "name":"Sandstorm Valley",           "waves":14,"totalHP":134475,    "expectedGold":1213,  "expectedEXP":10024},
    {"key":1203,"label":"2-3","level":15,"difficulty":"NORMAL",    "name":"Desert Underground Cave",    "waves":14,"totalHP":221918,    "expectedGold":1266,  "expectedEXP":11742},
    {"key":1204,"label":"2-4","level":16,"difficulty":"NORMAL",    "name":"Bug Nest",                   "waves":15,"totalHP":284696,    "expectedGold":1444,  "expectedEXP":15130},
    {"key":1205,"label":"2-5","level":17,"difficulty":"NORMAL",    "name":"Scorching Dunes",            "waves":15,"totalHP":263907,    "expectedGold":1342,  "expectedEXP":15344},
    {"key":1206,"label":"2-6","level":18,"difficulty":"NORMAL",    "name":"Sunset Ruins",               "waves":15,"totalHP":680580,    "expectedGold":2593,  "expectedEXP":35242},
    {"key":1207,"label":"2-7","level":19,"difficulty":"NORMAL",    "name":"Midnight Sands",             "waves":15,"totalHP":891585,    "expectedGold":2645,  "expectedEXP":35572},
    {"key":1208,"label":"2-8","level":20,"difficulty":"NORMAL",    "name":"Sacred Tomb",                "waves":16,"totalHP":800772,    "expectedGold":2160,  "expectedEXP":30556},
    {"key":1209,"label":"2-9","level":21,"difficulty":"NORMAL",    "name":"Pharaoh's Crypt",            "waves":16,"totalHP":1580495,   "expectedGold":3893,  "expectedEXP":58580},
    {"key":1301,"label":"3-1","level":23,"difficulty":"NORMAL",    "name":"Snowbound Outpost",          "waves":16,"totalHP":963024,    "expectedGold":2942,  "expectedEXP":50059},
    {"key":1302,"label":"3-2","level":24,"difficulty":"NORMAL",    "name":"Frozen Battlefield",         "waves":16,"totalHP":1507394,   "expectedGold":3122,  "expectedEXP":44816},
    {"key":1303,"label":"3-3","level":25,"difficulty":"NORMAL",    "name":"Glacial Cave Entrance",      "waves":17,"totalHP":2073809,   "expectedGold":4297,  "expectedEXP":56309},
    {"key":1304,"label":"3-4","level":26,"difficulty":"NORMAL",    "name":"Frozen Glacier Cavern",      "waves":17,"totalHP":3240508,   "expectedGold":4586,  "expectedEXP":59357},
    {"key":1305,"label":"3-5","level":27,"difficulty":"NORMAL",    "name":"Hell Gate",                  "waves":17,"totalHP":2912177,   "expectedGold":4626,  "expectedEXP":69831},
    {"key":1306,"label":"3-6","level":28,"difficulty":"NORMAL",    "name":"Burning Ravine",             "waves":17,"totalHP":3952520,   "expectedGold":9121,  "expectedEXP":176363},
    {"key":1307,"label":"3-7","level":29,"difficulty":"NORMAL",    "name":"Plains of Torment",          "waves":17,"totalHP":3856274,   "expectedGold":9609,  "expectedEXP":171368},
    {"key":1308,"label":"3-8","level":30,"difficulty":"NORMAL",    "name":"Citadel of Ruin",            "waves":18,"totalHP":3800014,   "expectedGold":16044, "expectedEXP":279857},
    {"key":1309,"label":"3-9","level":31,"difficulty":"NORMAL",    "name":"Core of the Abyss",          "waves":18,"totalHP":4645986,   "expectedGold":16072, "expectedEXP":296958},
    # Nightmare
    {"key":2101,"label":"NM 1-1","level":33,"difficulty":"NIGHTMARE","name":"Pasture",                  "waves":20,"totalHP":3005765,   "expectedGold":10192, "expectedEXP":182120},
    {"key":2102,"label":"NM 1-2","level":34,"difficulty":"NIGHTMARE","name":"Shadow Meadow",            "waves":20,"totalHP":2920297,   "expectedGold":12352, "expectedEXP":219150},
    {"key":2103,"label":"NM 1-3","level":35,"difficulty":"NIGHTMARE","name":"Wasteland",                "waves":20,"totalHP":2757354,   "expectedGold":14501, "expectedEXP":237770},
    {"key":2104,"label":"NM 1-4","level":35,"difficulty":"NIGHTMARE","name":"Eerie Canyon",             "waves":21,"totalHP":4081496,   "expectedGold":15216, "expectedEXP":272569},
    {"key":2105,"label":"NM 1-5","level":36,"difficulty":"NIGHTMARE","name":"Burning Village Entrance", "waves":21,"totalHP":5872189,   "expectedGold":20233, "expectedEXP":363813},
    {"key":2106,"label":"NM 1-6","level":37,"difficulty":"NIGHTMARE","name":"Rumstreet Square",         "waves":21,"totalHP":10473654,  "expectedGold":24488, "expectedEXP":451836},
    {"key":2107,"label":"NM 1-7","level":38,"difficulty":"NIGHTMARE","name":"City Outskirts",           "waves":21,"totalHP":4560526,   "expectedGold":15233, "expectedEXP":262068},
    {"key":2108,"label":"NM 1-8","level":39,"difficulty":"NIGHTMARE","name":"Cemetery",                 "waves":21,"totalHP":6015676,   "expectedGold":21005, "expectedEXP":369918},
    {"key":2109,"label":"NM 1-9","level":40,"difficulty":"NIGHTMARE","name":"Cursed Land",              "waves":22,"totalHP":11638496,  "expectedGold":30766, "expectedEXP":559362},
    {"key":2201,"label":"NM 2-1","level":41,"difficulty":"NIGHTMARE","name":"Oasis Road",               "waves":22,"totalHP":7265474,   "expectedGold":23235, "expectedEXP":435396},
    {"key":2202,"label":"NM 2-2","level":41,"difficulty":"NIGHTMARE","name":"Sandstorm Valley",         "waves":22,"totalHP":8410545,   "expectedGold":28825, "expectedEXP":533392},
    {"key":2203,"label":"NM 2-3","level":42,"difficulty":"NIGHTMARE","name":"Desert Underground Cave",  "waves":22,"totalHP":11298681,  "expectedGold":28668, "expectedEXP":519365},
    {"key":2204,"label":"NM 2-4","level":42,"difficulty":"NIGHTMARE","name":"Bug Nest",                 "waves":22,"totalHP":10998498,  "expectedGold":27710, "expectedEXP":516648},
    {"key":2205,"label":"NM 2-5","level":43,"difficulty":"NIGHTMARE","name":"Scorching Dunes",          "waves":22,"totalHP":8425008,   "expectedGold":24443, "expectedEXP":457841},
    {"key":2206,"label":"NM 2-6","level":43,"difficulty":"NIGHTMARE","name":"Sunset Ruins",             "waves":22,"totalHP":16059497,  "expectedGold":36802, "expectedEXP":699465},
    {"key":2207,"label":"NM 2-7","level":44,"difficulty":"NIGHTMARE","name":"Midnight Sands",           "waves":22,"totalHP":19572726,  "expectedGold":37037, "expectedEXP":717045},
    {"key":2208,"label":"NM 2-8","level":44,"difficulty":"NIGHTMARE","name":"Sacred Tomb",              "waves":22,"totalHP":15209799,  "expectedGold":30534, "expectedEXP":574840},
    {"key":2209,"label":"NM 2-9","level":45,"difficulty":"NIGHTMARE","name":"Pharaoh's Crypt",          "waves":23,"totalHP":27009170,  "expectedGold":49682, "expectedEXP":940346},
    {"key":2301,"label":"NM 3-1","level":46,"difficulty":"NIGHTMARE","name":"Snowbound Outpost",        "waves":23,"totalHP":13782027,  "expectedGold":32159, "expectedEXP":613768},
    {"key":2302,"label":"NM 3-2","level":47,"difficulty":"NIGHTMARE","name":"Frozen Battlefield",       "waves":23,"totalHP":31047091,  "expectedGold":37354, "expectedEXP":648988},
    {"key":2303,"label":"NM 3-3","level":48,"difficulty":"NIGHTMARE","name":"Glacial Cave Entrance",    "waves":23,"totalHP":21806872,  "expectedGold":36161, "expectedEXP":516194},
    {"key":2304,"label":"NM 3-4","level":49,"difficulty":"NIGHTMARE","name":"Frozen Glacier Cavern",    "waves":23,"totalHP":32132226,  "expectedGold":37392, "expectedEXP":516764},
    {"key":2305,"label":"NM 3-5","level":50,"difficulty":"NIGHTMARE","name":"Hell Gate",                "waves":23,"totalHP":29201288,  "expectedGold":36213, "expectedEXP":563858},
    {"key":2306,"label":"NM 3-6","level":50,"difficulty":"NIGHTMARE","name":"Burning Ravine",           "waves":23,"totalHP":30876371,  "expectedGold":63799, "expectedEXP":1273497},
    {"key":2307,"label":"NM 3-7","level":51,"difficulty":"NIGHTMARE","name":"Plains of Torment",        "waves":23,"totalHP":32020934,  "expectedGold":59057, "expectedEXP":1125011},
    {"key":2308,"label":"NM 3-8","level":51,"difficulty":"NIGHTMARE","name":"Citadel of Ruin",          "waves":23,"totalHP":27117133,  "expectedGold":100695,"expectedEXP":1921344},
    {"key":2309,"label":"NM 3-9","level":52,"difficulty":"NIGHTMARE","name":"Core of the Abyss",        "waves":23,"totalHP":30901926,  "expectedGold":102931,"expectedEXP":1976633},
    # Hell
    {"key":3101,"label":"H 1-1","level":53,"difficulty":"HELL","name":"Pasture",                        "waves":24,"totalHP":16687185,  "expectedGold":51065, "expectedEXP":989604},
    {"key":3102,"label":"H 1-2","level":54,"difficulty":"HELL","name":"Shadow Meadow",                  "waves":24,"totalHP":15862077,  "expectedGold":60855, "expectedEXP":1170450},
    {"key":3103,"label":"H 1-3","level":55,"difficulty":"HELL","name":"Wasteland",                      "waves":25,"totalHP":13647619,  "expectedGold":66066, "expectedEXP":1164789},
    {"key":3104,"label":"H 1-4","level":56,"difficulty":"HELL","name":"Eerie Canyon",                   "waves":25,"totalHP":20243102,  "expectedGold":68707, "expectedEXP":1328008},
    {"key":3105,"label":"H 1-5","level":57,"difficulty":"HELL","name":"Burning Village Entrance",       "waves":25,"totalHP":25749918,  "expectedGold":82004, "expectedEXP":1584403},
    {"key":3106,"label":"H 1-6","level":58,"difficulty":"HELL","name":"Rumstreet Square",               "waves":25,"totalHP":44517564,  "expectedGold":96458, "expectedEXP":1890567},
    {"key":3107,"label":"H 1-7","level":59,"difficulty":"HELL","name":"City Outskirts",                 "waves":25,"totalHP":18522358,  "expectedGold":57977, "expectedEXP":1055593},
    {"key":3108,"label":"H 1-8","level":59,"difficulty":"HELL","name":"Cemetery",                       "waves":25,"totalHP":23090972,  "expectedGold":75698, "expectedEXP":1406488},
    {"key":3109,"label":"H 1-9","level":60,"difficulty":"HELL","name":"Cursed Land",                    "waves":25,"totalHP":41391124,  "expectedGold":103769,"expectedEXP":1981588},
    {"key":3201,"label":"H 2-1","level":61,"difficulty":"HELL","name":"Oasis Road",                     "waves":26,"totalHP":26526950,  "expectedGold":79907, "expectedEXP":1565190},
    {"key":3202,"label":"H 2-2","level":62,"difficulty":"HELL","name":"Sandstorm Valley",               "waves":26,"totalHP":32073241,  "expectedGold":103096,"expectedEXP":2004248},
    {"key":3203,"label":"H 2-3","level":63,"difficulty":"HELL","name":"Desert Underground Cave",        "waves":26,"totalHP":40832600,  "expectedGold":100883,"expectedEXP":1917335},
    {"key":3204,"label":"H 2-4","level":64,"difficulty":"HELL","name":"Bug Nest",                       "waves":26,"totalHP":42333079,  "expectedGold":115054,"expectedEXP":2244311},
    {"key":3205,"label":"H 2-5","level":65,"difficulty":"HELL","name":"Scorching Dunes",                "waves":26,"totalHP":31512877,  "expectedGold":88032, "expectedEXP":1720981},
    {"key":3206,"label":"H 2-6","level":66,"difficulty":"HELL","name":"Sunset Ruins",                   "waves":26,"totalHP":60161619,  "expectedGold":133632,"expectedEXP":2642528},
    {"key":3207,"label":"H 2-7","level":67,"difficulty":"HELL","name":"Midnight Sands",                 "waves":26,"totalHP":72107814,  "expectedGold":151932,"expectedEXP":3040696},
    {"key":3208,"label":"H 2-8","level":68,"difficulty":"HELL","name":"Sacred Tomb",                    "waves":26,"totalHP":59638889,  "expectedGold":135806,"expectedEXP":2661217},
    {"key":3209,"label":"H 2-9","level":69,"difficulty":"HELL","name":"Pharaoh's Crypt",                "waves":26,"totalHP":97030543,  "expectedGold":173234,"expectedEXP":3408104},
    {"key":3301,"label":"H 3-1","level":70,"difficulty":"HELL","name":"Snowbound Outpost",              "waves":27,"totalHP":51936891,  "expectedGold":113190,"expectedEXP":2235912},
    {"key":3302,"label":"H 3-2","level":71,"difficulty":"HELL","name":"Frozen Battlefield",             "waves":27,"totalHP":118570346, "expectedGold":130890,"expectedEXP":2340631},
    {"key":3303,"label":"H 3-3","level":72,"difficulty":"HELL","name":"Glacial Cave Entrance",          "waves":27,"totalHP":76815983,  "expectedGold":122481,"expectedEXP":1773576},
    {"key":3304,"label":"H 3-4","level":73,"difficulty":"HELL","name":"Frozen Glacier Cavern",          "waves":27,"totalHP":110942045, "expectedGold":125102,"expectedEXP":1758240},
    {"key":3305,"label":"H 3-5","level":74,"difficulty":"HELL","name":"Hell Gate",                      "waves":27,"totalHP":99182193,  "expectedGold":119757,"expectedEXP":1889522},
    {"key":3306,"label":"H 3-6","level":75,"difficulty":"HELL","name":"Burning Ravine",                 "waves":27,"totalHP":112198292, "expectedGold":226330,"expectedEXP":4624921},
    {"key":3307,"label":"H 3-7","level":76,"difficulty":"HELL","name":"Plains of Torment",              "waves":27,"totalHP":118334238, "expectedGold":246401,"expectedEXP":4830175},
    {"key":3308,"label":"H 3-8","level":76,"difficulty":"HELL","name":"Citadel of Ruin",                "waves":27,"totalHP":98908163,  "expectedGold":339759,"expectedEXP":6673679},
    {"key":3309,"label":"H 3-9","level":77,"difficulty":"HELL","name":"Core of the Abyss",              "waves":27,"totalHP":98809856,  "expectedGold":341801,"expectedEXP":6737764},
    # Torment
    {"key":4101,"label":"T 1-1","level":78,"difficulty":"TORMENT","name":"Pasture",                     "waves":29,"totalHP":57437379,  "expectedGold":169729,"expectedEXP":3363833},
    {"key":4102,"label":"T 1-2","level":79,"difficulty":"TORMENT","name":"Shadow Meadow",               "waves":29,"totalHP":54005163,  "expectedGold":200167,"expectedEXP":3943012},
    {"key":4103,"label":"T 1-3","level":80,"difficulty":"TORMENT","name":"Wasteland",                   "waves":29,"totalHP":43814710,  "expectedGold":205871,"expectedEXP":3710290},
    {"key":4104,"label":"T 1-4","level":81,"difficulty":"TORMENT","name":"Eerie Canyon",                "waves":29,"totalHP":64287432,  "expectedGold":211409,"expectedEXP":4173800},
    {"key":4105,"label":"T 1-5","level":82,"difficulty":"TORMENT","name":"Burning Village Entrance",    "waves":29,"totalHP":80272177,  "expectedGold":249394,"expectedEXP":4918933},
    {"key":4106,"label":"T 1-6","level":83,"difficulty":"TORMENT","name":"Rumstreet Square",            "waves":29,"totalHP":136725856, "expectedGold":288821,"expectedEXP":5752464},
    {"key":4107,"label":"T 1-7","level":84,"difficulty":"TORMENT","name":"City Outskirts",              "waves":29,"totalHP":55462412,  "expectedGold":170052,"expectedEXP":3145356},
    {"key":4108,"label":"T 1-8","level":84,"difficulty":"TORMENT","name":"Cemetery",                    "waves":29,"totalHP":69455300,  "expectedGold":222346,"expectedEXP":4204031},
    {"key":4109,"label":"T 1-9","level":85,"difficulty":"TORMENT","name":"Cursed Land",                 "waves":29,"totalHP":122252666, "expectedGold":301130,"expectedEXP":5841800},
    {"key":4201,"label":"T 2-1","level":86,"difficulty":"TORMENT","name":"Oasis Road",                  "waves":30,"totalHP":77605355,  "expectedGold":228070,"expectedEXP":4533452},
    {"key":4202,"label":"T 2-2","level":86,"difficulty":"TORMENT","name":"Sandstorm Valley",            "waves":30,"totalHP":90789008,  "expectedGold":284759,"expectedEXP":5623880},
    {"key":4203,"label":"T 2-3","level":87,"difficulty":"TORMENT","name":"Desert Underground Cave",     "waves":30,"totalHP":112003885, "expectedGold":276234,"expectedEXP":5336082},
    {"key":4204,"label":"T 2-4","level":87,"difficulty":"TORMENT","name":"Bug Nest",                    "waves":30,"totalHP":113186934, "expectedGold":303233,"expectedEXP":5996101},
    {"key":4205,"label":"T 2-5","level":88,"difficulty":"TORMENT","name":"Scorching Dunes",             "waves":30,"totalHP":83615919,  "expectedGold":228048,"expectedEXP":4515134},
    {"key":4206,"label":"T 2-6","level":88,"difficulty":"TORMENT","name":"Sunset Ruins",                "waves":30,"totalHP":159274211, "expectedGold":340808,"expectedEXP":6798582},
    {"key":4207,"label":"T 2-7","level":89,"difficulty":"TORMENT","name":"Midnight Sands",              "waves":30,"totalHP":182644981, "expectedGold":378065,"expectedEXP":7652267},
    {"key":4208,"label":"T 2-8","level":89,"difficulty":"TORMENT","name":"Sacred Tomb",                 "waves":30,"totalHP":145466118, "expectedGold":279382,"expectedEXP":5536560},
    {"key":4209,"label":"T 2-9","level":90,"difficulty":"TORMENT","name":"Pharaoh's Crypt",             "waves":30,"totalHP":234871076, "expectedGold":414001,"expectedEXP":8218613},
    {"key":4301,"label":"T 3-1","level":91,"difficulty":"TORMENT","name":"Snowbound Outpost",           "waves":31,"totalHP":124538656, "expectedGold":266942,"expectedEXP":5314181},
    {"key":4302,"label":"T 3-2","level":91,"difficulty":"TORMENT","name":"Frozen Battlefield",          "waves":31,"totalHP":276415235, "expectedGold":300022,"expectedEXP":5411717},
    {"key":4303,"label":"T 3-3","level":92,"difficulty":"TORMENT","name":"Glacial Cave Entrance",       "waves":31,"totalHP":185284825, "expectedGold":372336,"expectedEXP":6240936},
    {"key":4304,"label":"T 3-4","level":92,"difficulty":"TORMENT","name":"Frozen Glacier Cavern",       "waves":31,"totalHP":248855072, "expectedGold":276321,"expectedEXP":3905099},
    {"key":4305,"label":"T 3-5","level":93,"difficulty":"TORMENT","name":"Hell Gate",                   "waves":31,"totalHP":250371338, "expectedGold":342741,"expectedEXP":5673939},
    {"key":4306,"label":"T 3-6","level":93,"difficulty":"TORMENT","name":"Burning Ravine",              "waves":31,"totalHP":236632136, "expectedGold":532657,"expectedEXP":10831727},
    {"key":4307,"label":"T 3-7","level":94,"difficulty":"TORMENT","name":"Plains of Torment",           "waves":31,"totalHP":212026519, "expectedGold":607174,"expectedEXP":12345044},
    {"key":4308,"label":"T 3-8","level":94,"difficulty":"TORMENT","name":"Citadel of Ruin",             "waves":31,"totalHP":205070592, "expectedGold":722939,"expectedEXP":14300189},
    {"key":4309,"label":"T 3-9","level":95,"difficulty":"TORMENT","name":"Core of the Abyss",           "waves":31,"totalHP":208944800, "expectedGold":725995,"expectedEXP":14396303},
]
STAGES_BY_KEY = {s['key']: s for s in STAGES}

# ─── Crypto ──────────────────────────────────────────────────────────────────
def decrypt_save(path):
    data = open(path, 'rb').read()
    iv = data[:16]; ct = data[16:]
    key = hashlib.pbkdf2_hmac('sha1', ES3_PASSWORD.encode(), iv, 100, dklen=16)
    pt  = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pt  = pt[:-pt[-1]]
    if pt[:2] == b'\x1f\x8b':
        pt = gzip.decompress(pt)
    outer  = json.loads(pt)
    player = json.loads(outer['PlayerSaveData']['value'])
    return outer, player

def encrypt_save(outer, player, path):
    backup = path + '.tbhopt.bak'
    if not os.path.exists(backup):
        shutil.copy2(path, backup)
        print(f'  Yedek oluşturuldu: {backup}')

    outer['PlayerSaveData']['value'] = json.dumps(
        player, separators=(',', ':'), ensure_ascii=False
    )
    pt = json.dumps(outer, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    pad = 16 - (len(pt) % 16)
    pt += bytes([pad] * pad)

    iv  = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha1', ES3_PASSWORD.encode(), iv, 100, dklen=16)
    ct  = AES.new(key, AES.MODE_CBC, iv).encrypt(pt)

    with open(path, 'wb') as f:
        f.write(iv + ct)

# ─── Helpers ─────────────────────────────────────────────────────────────────
def fmt(n):
    """Format large number with K/M suffix."""
    if n >= 1_000_000: return f'{n/1_000_000:.1f}M'
    if n >= 1_000:     return f'{n/1_000:.1f}K'
    return str(int(n))

def stage_label(key):
    s = STAGES_BY_KEY.get(key)
    return f"{s['label']} {s['name']}" if s else f'Stage {key}'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask_float(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print('  Geçersiz değer, tekrar dene.')

def ask_int(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print('  Geçersiz değer, tekrar dene.')

# ─── Farming calculator ───────────────────────────────────────────────────────
def calc_farming(max_stage, time_floor, dps=None, exp_bonus=0, gold_bonus=0):
    """
    Returns list of stages sorted by EXP/h and Gold/h.
    time_floor: 1-1 clear time (wave overhead seconds)
    dps: damage per second (None = raw density ranking, no time estimate)
    """
    results = []
    for s in STAGES:
        if s['key'] > max_stage:
            continue
        if dps is not None:
            clear_time = time_floor + s['totalHP'] / dps
        else:
            clear_time = time_floor  # fallback, not meaningful

        exp_ph  = s['expectedEXP']  * (1 + exp_bonus  / 100) * 3600 / clear_time if dps else None
        gold_ph = s['expectedGold'] * (1 + gold_bonus / 100) * 3600 / clear_time if dps else None
        results.append({**s, 'clear_time': clear_time if dps else None,
                        'exp_ph': exp_ph, 'gold_ph': gold_ph})
    return results

# ─── Display ─────────────────────────────────────────────────────────────────
def print_header():
    print('=' * 70)
    print('  TBH Task Bar Hero — Farming Optimizer & Save Editor')
    print('=' * 70)

def print_player(player):
    c = player['commonSaveData']
    current = c.get('currentStageKey', 0)
    max_s   = c.get('maxCompletedStage', 0)
    heroes  = player.get('heroSaveDatas', [])
    curr_data = player.get('currenySaveDatas', [])

    print(f"\n  Mevcut stage : {stage_label(current)}  (key: {current})")
    print(f"  En yüksek   : {stage_label(max_s)}  (key: {max_s})")
    print(f"  Oyun süresi  : {c.get('playTime', 0)/3600:.1f} saat")

    print("\n  Herolar:")
    for h in heroes:
        name = HERO_NAMES.get(h['heroKey'], f"Hero {h['heroKey']}")
        lv   = h.get('HeroLevel', '?')
        exp  = h.get('HeroExp', 0)
        print(f"    {name:<12} Lv {lv:>3}  EXP: {fmt(exp)}")

    print("\n  Para birimi:")
    for c_entry in curr_data:
        cname = CURRENCY_NAMES.get(c_entry['Key'], f"Currency {c_entry['Key']}")
        print(f"    {cname:<12} {fmt(c_entry['Quantity'])}")

def print_ranking(results, top=8, sort_by='exp'):
    key = 'exp_ph' if sort_by == 'exp' else 'gold_ph'
    ranked = sorted([r for r in results if r[key] is not None], key=lambda x: -x[key])
    label  = 'EXP/saat' if sort_by == 'exp' else 'Gold/saat'
    print(f"\n  {'Stage':<22} {'Diff':<10} {'Lv':>3}  {label:>12}  {'Clear':>6}  {'EXP/saat':>10}  {'Gold/saat':>10}")
    print('  ' + '-' * 78)
    for i, r in enumerate(ranked[:top]):
        cur  = r['clear_time']
        marker = ' <-- BURASI' if i == 0 else ''
        print(f"  {r['label']+' '+r['name']:<22} {r['difficulty']:<10} {r['level']:>3}  "
              f"{fmt(r['exp_ph']):>12}  {cur:>5.1f}s  {fmt(r['exp_ph']):>10}  {fmt(r['gold_ph']):>10}{marker}")

# ─── Main menu ───────────────────────────────────────────────────────────────
def menu_farming(player):
    c     = player['commonSaveData']
    max_s = c.get('maxCompletedStage', 0)
    cur_s = c.get('currentStageKey', 0)

    print("\n  --- Farming Optimizer ---")
    print(f"  Mevcut stage : {stage_label(cur_s)}")
    print(f"  Max stage    : {stage_label(max_s)}")
    print()
    print("  Mod seç:")
    print("  1) Otomatik  — süre girmene gerek yok (EXP/HP & Gold/HP yoğunluğuna göre)")
    print("  2) Manuel    — kendi clear sürelerini gir (daha hassas)")
    mod = input("  Seçim [1/2]: ").strip() or '1'

    exp_bonus  = ask_float("  EXP bonus % (rune+gear, 0 ise boş bırak): ", 0)
    gold_bonus = ask_float("  Gold bonus % (rune+gear, 0 ise boş bırak): ", 0)

    if mod == '2':
        t_floor = ask_float("  1-1 (Pasture) temizleme süresi (saniye): ")
        dps = None
        while True:
            raw = input(f"  Referans stage key (örn {max_s}) [boş=atla]: ").strip()
            if not raw:
                break
            try:
                ceil_key   = int(raw)
                ceil_stage = STAGES_BY_KEY.get(ceil_key)
                if not ceil_stage:
                    print("  Bilinmeyen stage key."); continue
                t_ceil = ask_float(f"  {ceil_stage['label']} ({ceil_stage['name']}) süresi (saniye): ")
                if t_ceil <= t_floor:
                    print("  Referans stage süresi 1-1'den büyük olmalı."); continue
                dps = ceil_stage['totalHP'] / (t_ceil - t_floor)
                print(f"  Hesaplanan DPS: {fmt(dps)}")
                break
            except ValueError:
                print("  Geçersiz.")
        results = calc_farming(max_stage=max_s, time_floor=t_floor, dps=dps,
                               exp_bonus=exp_bonus, gold_bonus=gold_bonus)
        print("\n  === EXP/saat En İyi 8 Stage ===")
        print_ranking(results, top=8, sort_by='exp')
        print("\n  === Gold/saat En İyi 8 Stage ===")
        print_ranking(results, top=8, sort_by='gold')
    else:
        # Otomatik mod: EXP/HP ve Gold/HP yoğunluğuna göre sırala
        # (DPS sabit varsayımında clear_time ∝ HP, dolayısıyla EXP/hr ∝ EXP/HP)
        accessible = [s for s in STAGES if s['key'] <= max_s]
        by_exp  = sorted(accessible, key=lambda s: -s['expectedEXP']  * (1 + exp_bonus/100)  / s['totalHP'])
        by_gold = sorted(accessible, key=lambda s: -s['expectedGold'] * (1 + gold_bonus/100) / s['totalHP'])

        print("\n  === EXP için En İyi 8 Stage (EXP/HP yoğunluğu) ===")
        print(f"  {'Stage':<28} {'Diff':<10} {'Lv':>3}  {'EXP/HP':>10}  {'EXP/clear':>10}")
        print("  " + "-" * 68)
        for i, s in enumerate(by_exp[:8]):
            density = s['expectedEXP'] * (1 + exp_bonus/100) / s['totalHP']
            marker  = " <-- BURASI" if i == 0 else ""
            cur_mark = " (şu an)" if s['key'] == cur_s else ""
            print(f"  {s['label']+' '+s['name']:<28} {s['difficulty']:<10} {s['level']:>3}  "
                  f"{density:>10.4f}  {fmt(s['expectedEXP']):>10}{marker}{cur_mark}")

        print(f"\n  === Gold için En İyi 8 Stage (Gold/HP yoğunluğu) ===")
        print(f"  {'Stage':<28} {'Diff':<10} {'Lv':>3}  {'Gold/HP':>10}  {'Gold/clear':>10}")
        print("  " + "-" * 68)
        for i, s in enumerate(by_gold[:8]):
            density = s['expectedGold'] * (1 + gold_bonus/100) / s['totalHP']
            marker  = " <-- BURASI" if i == 0 else ""
            cur_mark = " (şu an)" if s['key'] == cur_s else ""
            print(f"  {s['label']+' '+s['name']:<28} {s['difficulty']:<10} {s['level']:>3}  "
                  f"{density:>10.6f}  {fmt(s['expectedGold']):>10}{marker}{cur_mark}")

        print("\n  Not: Otomatik mod wave overhead'i saymaz.")
        print("       Manuel mod ile daha kesin sonuç alırsın.")

def _skill_keys_for(hero_key, level):
    """Level'a göre açık skill key listesi döndür."""
    base = (hero_key // 100) * 10000 + 1
    if level >= 10:
        return [base, base + 100, base + 200]
    elif level >= 5:
        return [base, base + 100, -1]
    else:
        return [base, -1, -1]

def menu_editor(outer, player):
    c     = player['commonSaveData']
    max_s = c.get('maxCompletedStage', 0)

    print("\n  --- Save Editor ---")
    print("  Oyun KAPALI olmalı! Değişiklik sonrası aç.")
    print()
    print("  1) Hero level & skill editörü")
    print("  2) Farming stage değiştir")
    print("  3) Gold ekle")
    print("  0) Geri dön")
    choice = input("  Seçim: ").strip()

    if choice == '1':
        heroes = player.get('heroSaveDatas', [])
        print()
        print(f"  {'Hero':<12} {'Lv':>4}  {'Allocated':>10}  {'Unspent':>8}")
        print("  " + "-" * 42)
        for h in heroes:
            name = HERO_NAMES.get(h['heroKey'], f"Hero {h['heroKey']}")
            lv   = h['HeroLevel']
            alloc = h['AllocatedHeroAbilityPoint']
            unspent = h['AbilityPoint']
            locked = '' if h['IsUnLock'] else ' (kilitli)'
            print(f"  {name:<12} {lv:>4}  {alloc:>10}  {unspent:>8}{locked}")

        print()
        print("  Hedef level gir (tüm açık herolar için).")
        print("  Her hero için ayrı girmek istersen 0 gir.")
        target_all = ask_int("  Hedef level (0=ayrı ayrı): ", default=0)

        changed = []
        for h in heroes:
            if not h['IsUnLock']:
                continue
            name = HERO_NAMES.get(h['heroKey'], f"Hero {h['heroKey']}")
            if target_all > 0:
                target = target_all
            else:
                target = ask_int(f"  {name} (şu an Lv{h['HeroLevel']}) → hedef level: ",
                                 default=h['HeroLevel'])

            if target <= h['HeroLevel']:
                print(f"  {name}: değişiklik yok.")
                continue

            old_lv  = h['HeroLevel']
            alloc   = h['AllocatedHeroAbilityPoint']
            # Yeni unspent = toplam yeni nokta - zaten harcanmış
            new_unspent = max(0, target - alloc)

            h['HeroLevel']  = target
            h['AbilityPoint'] = new_unspent
            h['HeroExp']    = max(h.get('HeroExp', 0), float(target * 50000))
            h['equippedSKillKey'] = _skill_keys_for(h['heroKey'], target)
            if target >= 10 and 10002 not in h.get('unlockedAttributeGroupKeys', []):
                h.setdefault('unlockedAttributeGroupKeys', []).append(10002)

            changed.append(f"    {name}: Lv{old_lv} → Lv{target}  (+{new_unspent} harcanmamış nokta)")

        if changed:
            encrypt_save(outer, player, SAVE_FILE)
            print("\n  Kaydedildi:")
            for line in changed:
                print(line)
        else:
            print("  Hiçbir değişiklik yapılmadı.")

    elif choice == '2':
        print(f"\n  Erişilebilir stageler (max: {stage_label(max_s)}):")
        for s in STAGES:
            if s['key'] <= max_s:
                print(f"    {s['key']}  {s['label']}  {s['name']}")
        new_key = ask_int("  Yeni stage key: ")
        if new_key not in STAGES_BY_KEY:
            print("  Bilinmeyen stage key, iptal.")
            return
        if new_key > max_s:
            print("  Bu stage henüz açık değil, iptal.")
            return
        c['currentStageKey'] = new_key
        c['currentStageWave'] = 1
        encrypt_save(outer, player, SAVE_FILE)
        print(f"  Stage {stage_label(new_key)} olarak ayarlandı ve kaydedildi.")

    elif choice == '3':
        curr = player.get('currenySaveDatas', [])
        gold_entry = next((x for x in curr if x['Key'] == 100001), None)
        if not gold_entry:
            print("  Gold kaydı bulunamadı.")
            return
        print(f"  Mevcut gold: {fmt(gold_entry['Quantity'])}")
        add = ask_int("  Eklenecek gold miktarı: ")
        gold_entry['Quantity'] = gold_entry['Quantity'] + add
        encrypt_save(outer, player, SAVE_FILE)
        print(f"  Gold {fmt(gold_entry['Quantity'])} yapıldı ve kaydedildi.")

# ─── Watch mode ──────────────────────────────────────────────────────────────
def watch_mode():
    print("\n  Otomatik izleme modu - save değiştiğinde ekran yenilenir.")
    print("  Çıkmak için Ctrl+C\n")
    last_mtime = 0
    last_max   = 0

    # Kalibre et
    t_floor = ask_float("  1-1 temizleme süresi (saniye): ")
    t_ceil_raw = input("  Üst referans stage key (boş=skip): ").strip()
    dps = None
    if t_ceil_raw:
        try:
            ceil_key  = int(t_ceil_raw)
            ceil_st   = STAGES_BY_KEY.get(ceil_key)
            if ceil_st:
                t_ceil = ask_float(f"  {ceil_st['label']} temizleme süresi (saniye): ")
                dps = ceil_st['totalHP'] / (t_ceil - t_floor) if t_ceil > t_floor else None
        except Exception:
            pass
    exp_bonus  = ask_float("  EXP bonus %: ", 0)
    gold_bonus = ask_float("  Gold bonus %: ", 0)

    try:
        while True:
            mtime = os.path.getmtime(SAVE_FILE)
            if mtime != last_mtime:
                last_mtime = mtime
                try:
                    outer, player = decrypt_save(SAVE_FILE)
                    max_s = player['commonSaveData'].get('maxCompletedStage', 0)
                    clear()
                    print_header()
                    print(f"\n  Son güncelleme: {time.strftime('%H:%M:%S')}")
                    print_player(player)
                    results = calc_farming(max_s, t_floor, dps, exp_bonus, gold_bonus)
                    print("\n  === EXP/saat Top 5 ===")
                    print_ranking(results, top=5, sort_by='exp')
                    print("\n  === Gold/saat Top 5 ===")
                    print_ranking(results, top=5, sort_by='gold')
                    last_max = max_s
                except Exception as e:
                    print(f'  Okuma hatası: {e}')
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n  İzleme modu sonlandırıldı.")

# ─── Entry point ─────────────────────────────────────────────────────────────
def main():
    if not os.path.exists(SAVE_FILE):
        print(f"Save dosyası bulunamadı: {SAVE_FILE}")
        sys.exit(1)

    clear()
    print_header()

    outer, player = decrypt_save(SAVE_FILE)
    print_player(player)

    while True:
        print("\n  Ana Menü:")
        print("  1) Farming optimizer (manuel kalibrasyon)")
        print("  2) Otomatik izleme modu (save değişince güncelle)")
        print("  3) Save editor (yakında)")
        print("  0) Çıkış")
        choice = input("\n  Seçim: ").strip()

        if choice == '1':
            menu_farming(player)
        elif choice == '2':
            watch_mode()
        elif choice == '3':
            print("  Save editor henüz aktif değil.")
        elif choice == '0':
            print("  Çıkılıyor...")
            break
        else:
            print("  Geçersiz seçim.")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buton koordinat kayıt aracı — fareyi götür, Enter'a bas."""
import sys, os, json
import pyautogui
from PIL import ImageGrab, Image

pyautogui.FAILSAFE = True

GAME_LEFT = 1410
GAME_TOP  =  134
GAME_RECT = (GAME_LEFT, GAME_TOP, 2380, 1026)
OUT_FILE  = os.path.join(os.path.dirname(__file__), 'tbh_coords.json')
SS_DIR    = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SS_DIR, exist_ok=True)

def ask(label, hint=''):
    print(f'\n  >>> {label}')
    if hint:
        print(f'      ({hint})')
    print('      Fareyi o butona götür → ENTER. Atlamak: s + ENTER')
    val = input('      > ').strip().lower()
    if val == 's':
        print('      Atlandı.')
        return None
    x, y = pyautogui.position()
    rx, ry = x - GAME_LEFT, y - GAME_TOP
    print(f'      Kaydedildi: abs({x},{y})  raw({rx},{ry})')
    # 40x40px crop kaydet (template olarak)
    sc = ImageGrab.grab(bbox=GAME_RECT, all_screens=False)
    cx1, cy1 = max(0, rx-20), max(0, ry-20)
    cx2, cy2 = min(sc.width, rx+20), min(sc.height, ry+20)
    crop = sc.crop((cx1, cy1, cx2, cy2))
    crop_path = os.path.join(SS_DIR, f'tmpl_{label.replace(" ","_")}.png')
    crop.save(crop_path)
    return {'x': x, 'y': y, 'rx': rx, 'ry': ry, 'template': crop_path}

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print('=' * 55)
    print('  TBH Buton Haritası')
    print('=' * 55)
    print("""
  Oyunu aç, her adımda fareyi istenen butona götür ve ENTER bas.
  "s" + ENTER ile adımı atla.
  Sol üst köşeye gidersen script durur (failsafe).
""")
    input('  Hazır olunca ENTER...')

    coords = {}

    # --- HERO paneli alt sekmeleri ------------------------------------
    print('\n--- HERO PANELİ ALT SEKMELERİ ---')
    r = ask('Envanter sekmesi', 'HERO paneli altında "Envanter" butonu')
    if r: coords['tab_envanter'] = r

    r = ask('Dizilis sekmesi', 'HERO paneli altında "Dizilis" butonu')
    if r: coords['tab_dizilis'] = r

    # --- Nav ikonlar --------------------------------------------------
    print('\n--- NAV İKONLARI (HERO paneli en alt satır) ---')
    for name in ['Depo', 'Durum', 'Run', 'Kup', 'Portal']:
        r = ask(f'nav_{name}', f'Nav ikonları satırında {name} butonu')
        if r: coords[f'nav_{name.lower()}'] = r

    # --- Küp paneli ---------------------------------------------------
    print('\n--- KÜP PANELİ ---')
    print('  Önce Küp nav butonuna bas, Küp paneli açılsın.')
    input('  Küp paneli açıkken ENTER...')

    r = ask('Kup dropdown Sentez', 'Küp paneli üst dropdown — "Sentez" seçili')
    if r: coords['kup_dropdown'] = r

    r = ask('Kup Otomatik Doldir', '"Otomatik Doldir" butonu')
    if r: coords['kup_otomatik'] = r

    r = ask('Kup Sentezle', '"Sentezle" veya birleştirme başlat butonu')
    if r: coords['kup_sentezle'] = r

    # Simya için dropdown'ı aç
    print('\n  Şimdi dropdown\'a tıkla ve "Simya" seçeneğini göster.')
    input('  Simya görününce ENTER...')
    r = ask('Kup Simya secenegi', 'Dropdown\'da "Simya" seçeneği')
    if r: coords['kup_simya'] = r

    # --- Savaş alanı --------------------------------------------------
    print('\n--- SAVAŞ ALANI ---')
    r = ask('Mavi loot kutu', 'Savaş alanında mavi renkli loot kutusu (5dk\'da bir)')
    if r: coords['loot_box'] = r

    # --- Kaydet -------------------------------------------------------
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(coords, f, indent=2, ensure_ascii=False)

    print(f'\n  ✓ {len(coords)} koordinat kaydedildi → {OUT_FILE}')
    for k, v in coords.items():
        print(f'    {k}: raw({v["rx"]},{v["ry"]})')

if __name__ == '__main__':
    main()

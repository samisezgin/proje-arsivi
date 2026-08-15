#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TBH Koordinat Kurulum Aracı
Oyunun arayüz elemanlarını görsel olarak kaydeder.
"""
import sys, os, json, time
import pyautogui
from PIL import Image

pyautogui.FAILSAFE = True   # sol üst köşeye gidince dur

COORDS_FILE = os.path.join(os.path.dirname(__file__), 'tbh_coords.json')
TEMPL_DIR   = os.path.join(os.path.dirname(__file__), 'tbh_templates')
os.makedirs(TEMPL_DIR, exist_ok=True)

CROP_SIZE = 40   # buton etrafında ±40px kırp

def capture(label: str, key: str, hint: str = '') -> dict:
    """
    Kullanıcı fareyi istenen elemana götürür, ENTER'a basar.
    O anki mouse pozisyonunu ve etrafındaki küçük görüntüyü kaydeder.
    """
    print(f'\n  → {label}')
    if hint:
        print(f'     ({hint})')
    print('     Fareyi o elemana götür, sonra ENTER\'a bas. (Atlamak için "s" + ENTER)')
    inp = input('     > ').strip().lower()
    if inp == 's':
        print('     Atlandı.')
        return None

    x, y = pyautogui.position()
    print(f'     Kaydedildi: ({x}, {y})')

    # Küçük template kırpma
    sc  = pyautogui.screenshot()
    x1  = max(0, x - CROP_SIZE)
    y1  = max(0, y - CROP_SIZE)
    x2  = min(sc.width,  x + CROP_SIZE)
    y2  = min(sc.height, y + CROP_SIZE)
    crop = sc.crop((x1, y1, x2, y2))
    path = os.path.join(TEMPL_DIR, f'{key}.png')
    crop.save(path)

    return {'x': x, 'y': y, 'template': path}


def main():
    print('=' * 60)
    print('  TBH Kurulum — Arayüz Haritalama')
    print('=' * 60)
    print("""
  Oyunu aç, stage seçim ekranına gel.
  Her adımda fareyi istenen butona götürüp ENTER'a bas.
  "s" + ENTER ile o adımı atlayabilirsin.
""")
    input('  Hazır olunca ENTER\'a bas...')

    coords = {}

    # ── 1. Oyun penceresi / taskbar ikonu ─────────────────────────────────
    r = capture(
        'Oyun Taskbar İkonu',
        'taskbar_icon',
        'Oyun kapalıysa açmak için tıklanacak yer'
    )
    if r: coords['taskbar_icon'] = r

    print('\n  Şimdi oyun penceresini aç ve stage seçim ekranına gel.')
    input('  Hazır olunca ENTER\'a bas...')

    # ── 2. Dünya sekmeleri ────────────────────────────────────────────────
    for w in [1, 2, 3]:
        r = capture(f'Dünya {w} sekmesi / butonu', f'world_{w}')
        if r: coords[f'world_{w}'] = r

    # ── 3. Her dünya için stage butonları ─────────────────────────────────
    for w in [1, 2, 3]:
        print(f'\n  --- Dünya {w} stage butonları ---')
        r = capture(
            f'Dünya {w} sekmesine bas (geç)',
            f'world_{w}_tab',
            'Önce o sekmeye tıkla'
        )
        if r:
            pyautogui.click(r['x'], r['y'])
            time.sleep(0.5)

        for s in range(1, 10):
            stage_key = f'stage_{w}_{s}'
            stage_name = f'{w}-{s}'
            r = capture(
                f'Stage {stage_name} butonu',
                stage_key
            )
            if r: coords[stage_key] = r

    # ── 4. Başlat butonu ─────────────────────────────────────────────────
    r = capture(
        'BAŞLAT / GİR butonu',
        'btn_start',
        'Stage seçtikten sonra çıkan "Başlat" / "Enter" / "Go" butonu'
    )
    if r: coords['btn_start'] = r

    # ── 5. Hero ekranı ───────────────────────────────────────────────────
    print('\n  Şimdi Hero ekranını aç (karakter / hero listesi).')
    input('  Hazır olunca ENTER\'a bas...')

    HERO_NAMES = ['Knight','Ranger','Sorcerer','Priest','Hunter','Slayer']
    for name in HERO_NAMES:
        key = f'hero_{name.lower()}'
        r = capture(f'{name} hero kartı / portresi', key)
        if r: coords[key] = r

    r = capture(
        'Ability Puan Ekle butonu (+)',
        'btn_ability_add',
        'Hero seçince çıkan "+" veya puan harcama butonu'
    )
    if r: coords['btn_ability_add'] = r

    r = capture(
        'Skill / Yetenek sekmesi',
        'btn_skills_tab',
        'Hero\'nun skill listesini açan sekme/buton'
    )
    if r: coords['btn_skills_tab'] = r

    r = capture(
        'Skill kilidi açma butonu',
        'btn_skill_unlock',
        'Yeni skill\'i etkinleştiren buton'
    )
    if r: coords['btn_skill_unlock'] = r

    # ── 6. Envanter ekranı ───────────────────────────────────────────────
    print('\n  Şimdi Envanter ekranını aç.')
    input('  Hazır olunca ENTER\'a bas...')

    r = capture('Envanter / Çanta butonu', 'btn_inventory',
                'Envanter ekranını açan ana buton')
    if r: coords['btn_inventory'] = r

    r = capture('Equip / Giy butonu', 'btn_equip',
                'Item seçince çıkan "Giy / Equip" butonu')
    if r: coords['btn_equip'] = r

    r = capture('Yükselt / Upgrade butonu', 'btn_upgrade',
                'Item veya ekipman yükseltme butonu')
    if r: coords['btn_upgrade'] = r

    # ── 7. Level Up bildirimi ─────────────────────────────────────────────
    print('\n  Son olarak: Eğer level up bildirimi görünüyorsa aç.')
    input('  (Yoksa direkt ENTER\'a bas...) ')

    r = capture(
        'Level Up bildirim butonu / OK',
        'btn_levelup_ok',
        'Level atlandığında çıkan bildirimdeki Tamam/OK butonu'
    )
    if r: coords['btn_levelup_ok'] = r

    r = capture(
        'Level Up ikonu / rozeti',
        'icon_levelup',
        'Ekranda hero level atladığında çıkan ikon/efekt'
    )
    if r: coords['icon_levelup'] = r

    # ── 8. Kaydet ─────────────────────────────────────────────────────────
    with open(COORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(coords, f, indent=2, ensure_ascii=False)

    print(f'\n  ✓ {len(coords)} eleman kaydedildi → {COORDS_FILE}')
    print('  Artık tbh_auto.py ile otomasyon çalıştırabilirsin.')


if __name__ == '__main__':
    main()

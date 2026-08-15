#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TBH Vision — menü keşif ve koordinat tespiti"""
import os, sys, time
import pyautogui
from PIL import ImageGrab, Image, ImageDraw

pyautogui.PAUSE    = 0.4
pyautogui.FAILSAFE = True

GAME_LEFT = 1410
GAME_TOP  =  134
GAME_RECT = (GAME_LEFT, GAME_TOP, 2380, 1026)
SS_DIR    = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SS_DIR, exist_ok=True)

def grab():
    return ImageGrab.grab(bbox=GAME_RECT, all_screens=True)

def save(img, name, zoom=1):
    if zoom > 1:
        img = img.resize((img.width * zoom, img.height * zoom), Image.NEAREST)
    path = os.path.join(SS_DIR, name)
    img.save(path)
    sys.stdout.write(f'  Kaydedildi: {name}\n')
    sys.stdout.flush()

def grid(img, cell=10, color=(60, 60, 60), label_color=(255, 220, 0), major=50):
    out = img.copy().convert('RGB')
    draw = ImageDraw.Draw(out)
    w, h = out.size
    for x in range(0, w, cell):
        thick = 2 if x % major == 0 else 1
        col   = (200, 200, 0) if x % major == 0 else color
        draw.line([(x, 0), (x, h)], fill=col, width=thick)
        if x % major == 0:
            draw.text((x + 1, 1), str(x), fill=label_color)
    for y in range(0, h, cell):
        thick = 2 if y % major == 0 else 1
        col   = (200, 200, 0) if y % major == 0 else color
        draw.line([(0, y), (w, y)], fill=col, width=thick)
        if y % major == 0:
            draw.text((1, y + 1), str(y), fill=label_color)
    return out

def click(rx, ry, label=''):
    ax, ay = GAME_LEFT + rx, GAME_TOP + ry
    pyautogui.click(ax, ay)
    sys.stdout.write(f'  click raw({rx},{ry}) abs({ax},{ay}) {label}\n')
    sys.stdout.flush()

def focus_game():
    # STATUS paneli ortasina tıkla — güvenli, bir şeyi değiştirmiyor
    click(150, 400, 'focus')
    time.sleep(0.5)

# ─── ADIM 1: Hero panel alt bölgesi grid ile analiz ──────────────────────────
def step1_find_nav_buttons():
    sys.stdout.write('\n=== ADIM 1: Hero panel nav buton grid analizi ===\n')
    focus_game()
    img = grab()
    w, h = img.size
    sys.stdout.write(f'  Pencere: {w}x{h}\n')

    save(img, 'step1_full_raw.png')

    # Hero paneli tamami: x=265-595, tüm y
    hero_full = img.crop((265, 0, 595, h))
    save(grid(hero_full, cell=5, major=25), 'step1_hero_full_grid5.png', zoom=3)

    # Alt bölge odak: y=380-570 (nav butonları burada)
    bottom = img.crop((265, 380, 595, 570))
    save(grid(bottom, cell=5, major=25), 'step1_hero_bottom_grid5.png', zoom=4)

    sys.stdout.write('  >> step1_hero_bottom_grid5.png incelenerek nav y koordinatlari bulunacak\n')

# ─── ADIM 2: Nav menüleri gez ────────────────────────────────────────────────
# Koordinatlar fresh2x.png'den tahmin edildi — step1 sonrası güncelle
NAV = {
    'envanter': (385, 585),
    'dizilis':  (540, 585),
    'depo':     (327, 618),
    'durum':    (392, 618),
    'run':      (457, 618),
    'kup':      (522, 618),
    'portal':   (587, 618),
}

def step2_explore_menus():
    sys.stdout.write('\n=== ADIM 2: Tüm menüleri gez ===\n')
    focus_game()
    time.sleep(0.5)
    save(grab(), 'nav_00_baslangic.png')

    for name, (rx, ry) in NAV.items():
        sys.stdout.write(f'\n  -- {name.upper()} --\n')
        click(rx, ry, name)
        time.sleep(1.5)
        img = grab()
        save(img, f'nav_{name}.png')
        save(grid(img, cell=25, major=100), f'nav_{name}_grid.png')

    sys.stdout.write('\n  Tüm menüler gezildi.\n')

# ─── ADIM 3: Küp alt menüleri ────────────────────────────────────────────────
def step3_kup_submenu():
    sys.stdout.write('\n=== ADIM 3: Küp alt menüleri ===\n')
    focus_game()

    click(*NAV['kup'], 'Kup')
    time.sleep(1.5)
    save(grab(), 'kup_00_sentez.png')

    # CUBE panelinde üst sekme/dropdown çubuğu: raw x=650-970, y=65-95 arası
    kup_tabs = [
        (700, 75), (750, 75), (800, 75), (850, 75), (900, 75),
        (700, 90), (750, 90), (800, 90), (850, 90),
    ]
    for i, (rx, ry) in enumerate(kup_tabs):
        click(rx, ry, f'kup_tab_{i}')
        time.sleep(0.8)
        save(grab(), f'kup_tab_{i}_{rx}x{ry}.png')

    sys.stdout.write('  Küp alt menüleri tamamlandı.\n')

# ─── ADIM 4: Savaş alanı — mavi kutu ─────────────────────────────────────────
def step4_battle_area():
    sys.stdout.write('\n=== ADIM 4: Savaş alanı analizi ===\n')
    focus_game()

    img = grab()
    battle = img.crop((0, 680, 970, 892))
    save(battle, 'battle_raw.png', zoom=2)
    save(grid(battle, cell=10, major=50), 'battle_grid10.png', zoom=2)

    sys.stdout.write('  >> battle_grid10.png incelenerek mavi kutu koordinati bulunacak\n')

# ─── ADIM 5: Durum sekmesi scroll — beceriler ─────────────────────────────────
def step5_durum_scroll():
    sys.stdout.write('\n=== ADIM 5: Durum sekmesi scroll ===\n')
    focus_game()

    click(*NAV['durum'], 'Durum')
    time.sleep(1.5)
    save(grab(), 'durum_00_top.png')

    for i in range(1, 6):
        pyautogui.scroll(-3, x=GAME_LEFT + 130, y=GAME_TOP + 400)
        time.sleep(0.6)
        save(grab(), f'durum_{i:02d}_scroll.png')
        sys.stdout.write(f'  Scroll {i}/5\n')

    sys.stdout.write('  Durum scroll tamamlandı.\n')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')

    step1_find_nav_buttons()
    time.sleep(2)
    step2_explore_menus()
    step3_kup_submenu()
    step4_battle_area()
    step5_durum_scroll()

    sys.stdout.write('\nTamamlandi. screenshots/ klasorune bak.\n')

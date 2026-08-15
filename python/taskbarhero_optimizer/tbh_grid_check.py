#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HERO paneli tamamini goster — nav buton tespiti."""
import sys, os
from PIL import ImageGrab, Image, ImageDraw

GAME_LEFT = 1410
GAME_TOP  =  134
GAME_RECT = (GAME_LEFT, GAME_TOP, 2380, 1026)
SS_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')

def grab():
    return ImageGrab.grab(bbox=GAME_RECT, all_screens=False)

def save(img, name, zoom=1):
    if zoom > 1:
        img = img.resize((img.width * zoom, img.height * zoom), Image.NEAREST)
    img.save(os.path.join(SS_DIR, name))
    print(f'  {name}  ({img.width}x{img.height})')

def grid(img, cell=10, major=50, label_color=(255,220,0)):
    out = img.copy().convert('RGB')
    d = ImageDraw.Draw(out)
    w, h = out.size
    for x in range(0, w, cell):
        col = (220,220,0) if x % major == 0 else (60,60,60)
        d.line([(x,0),(x,h)], fill=col, width=2 if x % major == 0 else 1)
        if x % major == 0: d.text((x+1,1), str(x), fill=label_color)
    for y in range(0, h, cell):
        col = (220,220,0) if y % major == 0 else (60,60,60)
        d.line([(0,y),(w,y)], fill=col, width=2 if y % major == 0 else 1)
        if y % major == 0: d.text((1,y+1), str(y), fill=label_color)
    return out

sys.stdout.reconfigure(encoding='utf-8')
img = grab()
print(f'Oyun penceresi: {img.size}')

# HERO paneli tamami — x=295-665, tum y
hero = img.crop((295, 0, 665, 892))
save(grid(hero, cell=10, major=50), 'hero_full_grid10.png', zoom=2)
save(hero, 'hero_full_raw.png', zoom=2)

# Alt yari — y=400-892
hero_bot = img.crop((295, 400, 665, 892))
save(grid(hero_bot, cell=5, major=25), 'hero_bot_grid5.png', zoom=3)

print('Tamamlandi.')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Oyun penceresini bul — yeni monitör düzeni için koordinat tespiti."""
import sys, os
import pyautogui
from PIL import ImageGrab, Image, ImageDraw

SS_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SS_DIR, exist_ok=True)

def save(img, name, zoom=1):
    if zoom > 1:
        img = img.resize((img.width * zoom, img.height * zoom), Image.NEAREST)
    path = os.path.join(SS_DIR, name)
    img.save(path)
    sys.stdout.write(f'  Kaydedildi: {name}\n')
    sys.stdout.flush()

def grid(img, cell=50, major=200, color=(60,60,60), label_color=(255,220,0)):
    out = img.copy().convert('RGB')
    draw = ImageDraw.Draw(out)
    w, h = out.size
    for x in range(0, w, cell):
        col = (200,200,0) if x % major == 0 else color
        draw.line([(x,0),(x,h)], fill=col, width=2 if x % major == 0 else 1)
        if x % major == 0:
            draw.text((x+2, 2), str(x), fill=label_color)
    for y in range(0, h, cell):
        col = (200,200,0) if y % major == 0 else color
        draw.line([(0,y),(w,y)], fill=col, width=2 if y % major == 0 else 1)
        if y % major == 0:
            draw.text((2, y+2), str(y), fill=label_color)
    return out

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdout.write('Tum ekran yakalanıyor...\n')

    # Tüm ekranı yakala (tek monitör)
    full = ImageGrab.grab(all_screens=False)
    w, h = full.size
    sys.stdout.write(f'  Ekran boyutu: {w}x{h}\n')

    # Tam ekran kaydet
    save(full, 'monitor_full.png')

    # Grid ile kaydet (her 200px'de büyük etiket)
    save(grid(full, cell=50, major=200), 'monitor_grid200.png')

    # Sağ yarı (muhtemelen oyun burada)
    right_half = full.crop((w//2, 0, w, h))
    save(grid(right_half, cell=25, major=100), 'monitor_right_grid100.png')

    sys.stdout.write(f'\n  monitor_grid200.png dosyasina bak.\n')
    sys.stdout.write(f'  Oyun penceresinin sol-ust ve sag-alt koordinatlarini not et.\n')

    # Pencere başlığına göre otomatik bul
    try:
        wins = pyautogui.getWindowsWithTitle('TaskBar')
        if not wins:
            wins = pyautogui.getWindowsWithTitle('taskbar')
        if not wins:
            wins = pyautogui.getWindowsWithTitle('Task')
        if wins:
            for w_obj in wins:
                sys.stdout.write(f'\n  Pencere bulundu: "{w_obj.title}"\n')
                sys.stdout.write(f'    Sol-ust: ({w_obj.left}, {w_obj.top})\n')
                sys.stdout.write(f'    Boyut:   {w_obj.width}x{w_obj.height}\n')
                sys.stdout.write(f'    Sag-alt: ({w_obj.left+w_obj.width}, {w_obj.top+w_obj.height})\n')
        else:
            sys.stdout.write('\n  TaskBar penceresi bulunamadi, screenshot\'a bakarak koordinat ver.\n')
    except Exception as e:
        sys.stdout.write(f'  Pencere arama desteklenmiyor: {e}\n')
        sys.stdout.write('  Screenshot\'a bakarak koordinat ver.\n')

if __name__ == '__main__':
    main()

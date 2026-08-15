#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TBH Otomasyon — Farm tavsiyesine göre otomatik tıklama
"""
import sys, os, json, time, hashlib, gzip
import pyautogui
from PIL import Image

try:
    from Crypto.Cipher import AES
except ImportError:
    os.system(f'"{sys.executable}" -m pip install pycryptodome -q')
    from Crypto.Cipher import AES

pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0.3

BASE_DIR    = os.path.dirname(__file__)
COORDS_FILE = os.path.join(BASE_DIR, 'tbh_coords.json')
TEMPL_DIR   = os.path.join(BASE_DIR, 'tbh_templates')

ES3_PASSWORD = 'emuMqG3bLYJ938ZDCfieWJ'
SAVE_FILE    = os.path.expandvars(
    r'%USERPROFILE%\AppData\LocalLow\TesseractStudio\TaskBarHero\SaveFile_Live.es3')

# ─── Stage verisi (aynı tbh_optimizer.py'den) ────────────────────────────────
STAGES = {
    1101: {'name':'1-1 Pasture',          'floor_hp':10,'ceiling_hp':20,'floor_t':10,'ceiling_t':30,'exp':3},
    1102: {'name':'1-2 Shadow Meadow',    'floor_hp':30,'ceiling_hp':60,'floor_t':15,'ceiling_t':40,'exp':9},
    1103: {'name':'1-3 Wasteland',        'floor_hp':70,'ceiling_hp':140,'floor_t':20,'ceiling_t':50,'exp':20},
    1104: {'name':'1-4 Eerie Canyon',     'floor_hp':170,'ceiling_hp':340,'floor_t':25,'ceiling_t':60,'exp':45},
    1105: {'name':'1-5 Burning Village',  'floor_hp':380,'ceiling_hp':760,'floor_t':30,'ceiling_t':70,'exp':95},
    1106: {'name':'1-6 Rumstreet Sq.',    'floor_hp':820,'ceiling_hp':1640,'floor_t':35,'ceiling_t':80,'exp':190},
    1107: {'name':'1-7 City Outskirts',   'floor_hp':1700,'ceiling_hp':3400,'floor_t':40,'ceiling_t':90,'exp':370},
    1108: {'name':'1-8 Cemetery',         'floor_hp':3400,'ceiling_hp':6800,'floor_t':45,'ceiling_t':100,'exp':680},
    1109: {'name':'1-9 Cursed Land',      'floor_hp':6500,'ceiling_hp':13000,'floor_t':50,'ceiling_t':110,'exp':1200},
    1201: {'name':'2-1 Oasis Road',       'floor_hp':13500,'ceiling_hp':27000,'floor_t':55,'ceiling_t':120,'exp':2300},
    1202: {'name':'2-2 Sandstorm Valley', 'floor_hp':28000,'ceiling_hp':56000,'floor_t':60,'ceiling_t':130,'exp':4500},
    1203: {'name':'2-3 Desert Cave',      'floor_hp':57000,'ceiling_hp':114000,'floor_t':65,'ceiling_t':140,'exp':8500},
    1204: {'name':'2-4 Bug Nest',         'floor_hp':115000,'ceiling_hp':230000,'floor_t':70,'ceiling_t':150,'exp':16000},
    1205: {'name':'2-5 Scorching Dunes',  'floor_hp':230000,'ceiling_hp':460000,'floor_t':75,'ceiling_t':160,'exp':28000},
    1206: {'name':'2-6 Sunset Ruins',     'floor_hp':460000,'ceiling_hp':920000,'floor_t':80,'ceiling_t':170,'exp':50000},
    1207: {'name':'2-7 Midnight Sands',   'floor_hp':900000,'ceiling_hp':1800000,'floor_t':85,'ceiling_t':180,'exp':85000},
    1208: {'name':'2-8 Sacred Tomb',      'floor_hp':1800000,'ceiling_hp':3600000,'floor_t':90,'ceiling_t':190,'exp':140000},
    1209: {'name':'2-9 Pharaoh Crypt',    'floor_hp':3500000,'ceiling_hp':7000000,'floor_t':95,'ceiling_t':200,'exp':220000},
}

# ─── Save okuma ───────────────────────────────────────────────────────────────
def read_save():
    data = open(SAVE_FILE,'rb').read()
    iv,ct = data[:16],data[16:]
    key = hashlib.pbkdf2_hmac('sha1',ES3_PASSWORD.encode(),iv,100,dklen=16)
    pt  = AES.new(key,AES.MODE_CBC,iv).decrypt(ct); pt=pt[:-pt[-1]]
    if pt[:2]==b'\x1f\x8b': pt=gzip.decompress(pt)
    return json.loads(json.loads(pt)['PlayerSaveData']['value'])

def current_stage_key():
    try:
        p = read_save()
        return p['commonSaveData']['currentStageKey']
    except:
        return None

# ─── Koordinat / template yükle ──────────────────────────────────────────────
def load_coords():
    if not os.path.exists(COORDS_FILE):
        print('Koordinat dosyası bulunamadı. Önce tbh_setup.py çalıştır.')
        sys.exit(1)
    return json.load(open(COORDS_FILE, encoding='utf-8'))

# ─── Template ile bul veya sabit koordinata tıkla ────────────────────────────
CONF_THRESH = 0.7   # template eşleşme güven eşiği

def find_and_click(entry: dict, label: str, confidence=CONF_THRESH):
    """Template varsa ekranda ara, yoksa sabit koordinata tıkla."""
    tmpl = entry.get('template','')
    if tmpl and os.path.exists(tmpl):
        try:
            loc = pyautogui.locateOnScreen(tmpl, confidence=confidence)
            if loc:
                cx,cy = pyautogui.center(loc)
                print(f'  [{label}] template bulundu ({cx},{cy})')
                pyautogui.click(cx, cy)
                return True
        except Exception as e:
            print(f'  [{label}] template arama hatası: {e}')
    # Fallback: kayıtlı koordinat
    x, y = entry['x'], entry['y']
    print(f'  [{label}] sabit koordinat ({x},{y})')
    pyautogui.click(x, y)
    return True

# ─── Farming önerisi hesapla ─────────────────────────────────────────────────
def best_farmable_stage(player_dps: float, max_stage_key: int):
    """
    Tamamlanabilir en yüksek EXP/h veren stage'i döndür.
    player_dps: oyuncunun yaklaşık DPS değeri (save'den tahmin)
    """
    import math
    results = []
    for key, s in STAGES.items():
        if key > max_stage_key:
            continue
        if player_dps <= 0:
            continue
        dps_stage = s['ceiling_hp'] / (s['ceiling_t'] - s['floor_t'])
        if player_dps < dps_stage * 0.3:   # DPS yetersizse atla
            continue
        clear_t = s['floor_t'] + s['ceiling_hp'] / player_dps
        if clear_t > s['ceiling_t'] * 2:   # çok yavaşsa atla
            continue
        exp_h = s['exp'] * 3600 / clear_t
        results.append((exp_h, key, s['name'], round(clear_t,1)))
    if not results:
        return None
    results.sort(reverse=True)
    return results[0]

# ─── Stage navigasyonu ───────────────────────────────────────────────────────
def goto_stage(coords: dict, target_key: int):
    world = target_key // 100 - 10    # 1101→1, 1201→2, 1301→3
    stage = target_key % 100

    # Dünya sekmesine tıkla
    wkey = f'world_{world}'
    if wkey in coords:
        find_and_click(coords[wkey], f'Dünya {world} sekmesi')
        time.sleep(0.6)

    # Stage butonuna tıkla
    skey = f'stage_{world}_{stage}'
    if skey in coords:
        find_and_click(coords[skey], f'Stage {world}-{stage}')
        time.sleep(0.4)
    else:
        print(f'  Uyarı: stage_{world}_{stage} koordinatı kayıtlı değil')
        return False

    # Başlat butonuna tıkla
    if 'btn_start' in coords:
        find_and_click(coords['btn_start'], 'Başlat')
        time.sleep(0.4)

    return True

HERO_ORDER = ['knight','ranger','sorcerer','priest','hunter','slayer']

def handle_levelup(coords: dict):
    """Level up bildirimi varsa kapat."""
    if 'icon_levelup' in coords:
        try:
            loc = pyautogui.locateOnScreen(
                coords['icon_levelup']['template'],
                confidence=0.75
            )
            if loc:
                print('  [!] Level Up tespit edildi')
                if 'btn_levelup_ok' in coords:
                    find_and_click(coords['btn_levelup_ok'], 'Level Up OK')
                    time.sleep(0.3)
                return True
        except:
            pass
    return False

def spend_ability_points(coords: dict, player: dict):
    """
    Her hero için bekleyen ability point varsa hero ekranına gidip harcıyor.
    Strateji: tüm puanları ilk attribute grubuna bas (basit ama etkili).
    """
    for h in player.get('heroSaveDatas', []):
        if h.get('AbilityPoint', 0) <= 0:
            continue
        name = {101:'knight',201:'ranger',301:'sorcerer',
                401:'priest',501:'hunter',601:'slayer'}.get(h['heroKey'])
        if not name:
            continue
        pts = h['AbilityPoint']
        print(f'  [{name.capitalize()}] {pts} ability point bekliyor')

        hkey = f'hero_{name}'
        if hkey not in coords:
            continue
        find_and_click(coords[hkey], f'{name} hero kartı')
        time.sleep(0.5)

        if 'btn_ability_add' in coords:
            for _ in range(pts):
                find_and_click(coords['btn_ability_add'], 'Ability +')
                time.sleep(0.15)
        time.sleep(0.3)

def monitor_loop(coords: dict, interval: int = 30):
    """
    Sürekli izleme: her `interval` saniyede save'i okur,
    level up / ability point gibi bekleyen işlemleri halleder.
    """
    print(f'\n  İzleme modu başladı (her {interval}s kontrol). Çıkmak: Ctrl+C')
    last_stage = None

    while True:
        try:
            player = read_save()
        except Exception as e:
            print(f'  Save okunamadı: {e}')
            time.sleep(interval)
            continue

        c = player['commonSaveData']
        max_key = c.get('maxCompletedStage', 0)

        # Level up bildirimi kapat
        handle_levelup(coords)

        # Ability point harca
        spend_ability_points(coords, player)

        # Daha iyi stage var mı?
        current_key = c.get('currentStageKey', 0)
        s_curr = STAGES.get(current_key)
        if s_curr:
            dps_est = s_curr['ceiling_hp'] / ((s_curr['floor_t'] + s_curr['ceiling_t']) / 2)
            result = best_farmable_stage(dps_est, max_key)
            if result:
                _, best_key, best_name, _ = result
                if best_key != current_key and best_key != last_stage:
                    print(f'  [!] Daha iyi stage bulundu: {best_name}')
                    goto_stage(coords, best_key)
                    last_stage = best_key

        time.sleep(interval)

# ─── Ana döngü ───────────────────────────────────────────────────────────────
def main():
    coords = load_coords()

    print('=' * 55)
    print('  TBH Otomasyon — Farm Optimizer')
    print('=' * 55)

    try:
        player = read_save()
    except Exception as e:
        print(f'Save okunamadı: {e}')
        sys.exit(1)

    c = player['commonSaveData']
    current_key = c.get('currentStageKey', 0)
    max_key     = c.get('maxCompletedStage', 0)

    # DPS tahmini: mevcut stage'in ceiling_hp / clearing süresinden
    # Kullanıcıdan alıyoruz (daha doğru)
    print(f'\n  Mevcut stage : {current_key}')
    print(f'  Max stage    : {max_key}')
    print()
    dps_str = input('  Ortalama DPS\'inizi girin (0 = atla, save\'den tahmin edilir): ').strip()
    try:
        player_dps = float(dps_str) if dps_str else 0
    except:
        player_dps = 0

    if player_dps <= 0:
        # Kaba tahmin: mevcut stage ceiling_hp / clearing süresi
        s = STAGES.get(current_key)
        if s:
            player_dps = s['ceiling_hp'] / ((s['floor_t'] + s['ceiling_t']) / 2)
            print(f'  DPS tahmini  : {player_dps:,.0f}')

    result = best_farmable_stage(player_dps, max_key)
    if not result:
        print('  Öneri bulunamadı — DPS değerini elle gir.')
        sys.exit(1)

    exp_h, best_key, best_name, clear_t = result
    print(f'\n  ✦ Önerilen stage  : {best_name}')
    print(f'    Tahmini EXP/h   : {exp_h:,.0f}')
    print(f'    Clear süresi    : {clear_t:.1f}s')

    if best_key == current_key:
        print('\n  Zaten doğru stage\'desin, navigasyon gerekmiyor.')
        return

    print(f'\n  Oyun penceresini ön plana al — 3 sn...')
    time.sleep(3)

    # Taskbar ikonuna tıkla (pencereyi aç/ön plana al)
    if 'taskbar_icon' in coords:
        find_and_click(coords['taskbar_icon'], 'Oyun ikonu')
        time.sleep(1)

    print(f'  Stage değiştiriliyor → {best_name}')
    ok = goto_stage(coords, best_key)

    if ok:
        print(f'\n  Bitti! {best_name} stage\'ine geçildi.')
    else:
        print('\n  Bazı koordinatlar eksik, tbh_setup.py ile tamamla.')

    print('\n  Sürekli izleme moduna geç? (ability point, level up, stage yükselt)')
    if input('  [E/h] ').strip().lower() in ('e', ''):
        monitor_loop(coords)

if __name__ == '__main__':
    main()

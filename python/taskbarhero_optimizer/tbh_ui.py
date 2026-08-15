#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TBH Optimizer — Web UI (built-in http.server, no extra deps)"""

import sys, os, hashlib, json, gzip, shutil, threading, time, copy, webbrowser
import socketserver, traceback, logging
from http.server import BaseHTTPRequestHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('tbh_ui.log', encoding='utf-8'),
    ]
)
log = logging.getLogger('tbh')
try:
    from Crypto.Cipher import AES
except ImportError:
    os.system(f'"{sys.executable}" -m pip install pycryptodome -q')
    from Crypto.Cipher import AES

# ─── Config ──────────────────────────────────────────────────────────────────
ES3_PASSWORD = 'emuMqG3bLYJ938ZDCfieWJ'
SAVE_FILE    = os.path.expandvars(
    r'%USERPROFILE%\AppData\LocalLow\TesseractStudio\TaskBarHero\SaveFile_Live.es3')
PORT         = 8734

HERO_NAMES = {101:'Knight',201:'Ranger',301:'Sorcerer',401:'Priest',501:'Hunter',601:'Slayer'}
STAGE_NAMES = {
    1101:'1-1 Pasture',1102:'1-2 Shadow Meadow',1103:'1-3 Wasteland',
    1104:'1-4 Eerie Canyon',1105:'1-5 Burning Village',1106:'1-6 Rumstreet Sq.',
    1107:'1-7 City Outskirts',1108:'1-8 Cemetery',1109:'1-9 Cursed Land',
    1201:'2-1 Oasis Road',1202:'2-2 Sandstorm Valley',1203:'2-3 Desert Cave',
    1204:'2-4 Bug Nest',1205:'2-5 Scorching Dunes',1206:'2-6 Sunset Ruins',
    1207:'2-7 Midnight Sands',1208:'2-8 Sacred Tomb',1209:'2-9 Pharaoh Crypt',
    1301:'3-1 Snowbound',1302:'3-2 Frozen Battlefield',1303:'3-3 Glacial Cave',
    1304:'3-4 Frozen Glacier',1305:'3-5 Hell Gate',1306:'3-6 Burning Ravine',
    1307:'3-7 Plains Torment',1308:'3-8 Citadel Ruin',1309:'3-9 Core Abyss',
}

# ─── Crypto ──────────────────────────────────────────────────────────────────
def decrypt_save(path):
    data  = open(path,'rb').read()
    iv,ct = data[:16],data[16:]
    key   = hashlib.pbkdf2_hmac('sha1',ES3_PASSWORD.encode(),iv,100,dklen=16)
    pt    = AES.new(key,AES.MODE_CBC,iv).decrypt(ct); pt=pt[:-pt[-1]]
    if pt[:2]==b'\x1f\x8b': pt=gzip.decompress(pt)
    outer=json.loads(pt); return outer,json.loads(outer['PlayerSaveData']['value'])

def encrypt_save(outer,player,path):
    bak=path+'.tbhui.bak'
    if not os.path.exists(bak): shutil.copy2(path,bak)
    outer['PlayerSaveData']['value']=json.dumps(player,separators=(',',':'),ensure_ascii=False)
    pt=json.dumps(outer,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    pad=16-(len(pt)%16); pt+=bytes([pad]*pad)
    iv=os.urandom(16)
    key=hashlib.pbkdf2_hmac('sha1',ES3_PASSWORD.encode(),iv,100,dklen=16)
    ct=AES.new(key,AES.MODE_CBC,iv).encrypt(pt)
    open(path,'wb').write(iv+ct)

def skill_keys(hero_key,level):
    b=(hero_key//100)*10000+1
    if level>=10: return [b,b+100,b+200]
    if level>=5:  return [b,b+100,-1]
    return [b,-1,-1]

def fmt(n):
    if n>=1_000_000: return f'{n/1_000_000:.1f}M'
    if n>=1_000:     return f'{n/1_000:.1f}K'
    return str(int(n))

# ─── Shared state ─────────────────────────────────────────────────────────────
HERO_MAX_LEVEL = 100

class State:
    lock       = threading.RLock()  # reentrant: handler lock içinde save() çağırabilir
    outer      = None
    player     = None
    mtime      = 0
    item_names = {}   # ItemKey → name string
    _rune_max  = {}   # RuneKey → max level (gamedata'dan)

    @classmethod
    def rune_max_levels(cls):
        if cls._rune_max: return cls._rune_max
        try:
            import urllib.request
            url  = 'https://raw.githubusercontent.com/shigake/tbh-copilot/main/engine/gamedata.js'
            text = urllib.request.urlopen(url, timeout=6).read().decode('utf-8')
            s    = text.find('"runes":{')
            depth=0; i=s+7; buf=[]
            while i < len(text):
                ch=text[i]
                if ch=='{': depth+=1
                elif ch=='}':
                    depth-=1
                    if depth==0: buf.append(ch); i+=1; break
                buf.append(ch); i+=1
            db = json.loads(''.join(buf))
            cls._rune_max = {int(k): v['max'] for k,v in db.items()}
            log.info(f'Rune DB: {len(cls._rune_max)} rün yüklendi')
        except Exception as e:
            log.warning(f'Rune DB yüklenemedi: {e} — fallback max=5')
        return cls._rune_max

    @classmethod
    def load(cls):
        with cls.lock:
            try:
                mt = os.path.getmtime(SAVE_FILE)
                if mt != cls.mtime:
                    cls.outer,cls.player = decrypt_save(SAVE_FILE)
                    cls.mtime = mt
            except Exception as e:
                print(f'[load error] {e}')

    @classmethod
    def save(cls):
        with cls.lock:
            encrypt_save(cls.outer,cls.player,SAVE_FILE)
            cls.mtime = os.path.getmtime(SAVE_FILE)

    @classmethod
    def snapshot(cls):
        with cls.lock:
            if cls.player is None: return None
            return json.loads(json.dumps(cls.player))

    @classmethod
    def fetch_item_names(cls):
        try:
            import urllib.request
            url = 'https://raw.githubusercontent.com/shigake/tbh-copilot/main/engine/gamedata.js'
            with urllib.request.urlopen(url, timeout=5) as r:
                text = r.read().decode('utf-8')
            # Find gear object: "gear":{...}
            start = text.find('"gear":{')
            if start == -1: return
            # Extract by counting braces
            depth,i,buf = 0,start+7,[]
            while i < len(text):
                ch = text[i]
                if ch=='{': depth+=1
                elif ch=='}':
                    depth-=1
                    if depth==0: buf.append(ch); i+=1; break
                buf.append(ch); i+=1
            gear = json.loads(''.join(buf))
            with cls.lock:
                for k,v in gear.items():
                    name = v.get('name') or v.get('n') or ''
                    if name: cls.item_names[int(k)] = name
            print(f'[gamedata] {len(cls.item_names)} item adı yüklendi.')
        except Exception as e:
            print(f'[gamedata] Item adları yüklenemedi: {e}')

def build_api_data():
    p = State.snapshot()
    if not p: return {'error':'save yok'}

    c       = p['commonSaveData']
    heroes  = p.get('heroSaveDatas',[])
    curr    = p.get('currenySaveDatas',[])
    gold    = next((x['Quantity'] for x in curr if x['Key']==100001),0)
    items   = {i['UniqueId']:i for i in p.get('itemSaveDatas',[])}
    inv     = [s for s in p.get('inventorySaveDatas',[]) if s['ItemUniqueId']!=0]
    stash   = [s for s in p.get('stashSaveDatas',[])     if s['ItemUniqueId']!=0]

    def slot_to_dict(slot,src):
        uid  = slot['ItemUniqueId']
        item = items.get(uid,{})
        key  = item.get('ItemKey',0)
        return {
            'slot'    : slot['Index'],
            'uid'     : uid,
            'itemKey' : key,
            'name'    : State.item_names.get(key, f'Item #{key}'),
            'chaotic' : item.get('IsChaotic',False),
            'blocked' : item.get('IsBlocked',False),
            'enchants': sum(item.get('EnchantCount',[0,0,0])),
            'src'     : src,
        }

    return {
        'stage'   : STAGE_NAMES.get(c.get('currentStageKey',0), str(c.get('currentStageKey',0))),
        'maxStage': STAGE_NAMES.get(c.get('maxCompletedStage',0), str(c.get('maxCompletedStage',0))),
        'gold'    : gold,
        'goldFmt' : fmt(gold),
        'playtime': round(c.get('playTime',0)/3600,1),
        'heroes'  : [{
            'key'    : h['heroKey'],
            'name'   : HERO_NAMES.get(h['heroKey'],f"Hero {h['heroKey']}"),
            'level'  : h['HeroLevel'],
            'alloc'  : h['AllocatedHeroAbilityPoint'],
            'unspent': h['AbilityPoint'],
            'locked' : not h.get('IsUnLock',False),
            'skills' : sum(1 for s in h.get('equippedSKillKey',[]) if s!=-1),
        } for h in heroes],
        'inventory': [slot_to_dict(s,'inv')   for s in inv],
        'stash'    : [slot_to_dict(s,'stash') for s in stash],
        'runes'    : {
            'total'  : len(p.get('RuneSaveData',[])),
            'maxed'  : sum(1 for r in p.get('RuneSaveData',[]) if r['Level']>=5),
            'locked' : sum(1 for r in p.get('RuneSaveData',[]) if r['Level']==0),
        },
    }

# ─── Embedded HTML ───────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>TBH Optimizer</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1e1e2e;color:#cdd6f4;font-family:'Segoe UI',sans-serif;font-size:14px;min-height:100vh}
header{background:#181825;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #313244}
header h1{color:#89b4fa;font-size:18px}
#status{color:#a6adc8;font-size:12px}
.layout{display:grid;grid-template-columns:260px 1fr 340px;gap:12px;padding:14px;height:calc(100vh - 50px)}
.panel{background:#181825;border-radius:8px;padding:12px;overflow-y:auto;border:1px solid #313244}
.section-title{color:#89b4fa;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px}
/* Hero cards */
.hero-card{background:#313244;border-radius:6px;padding:10px;margin-bottom:8px}
.hero-name{font-weight:700;color:#cba6f7;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center}
.hero-name .lock{color:#f38ba8;font-size:11px}
.hero-row{display:flex;align-items:center;gap:8px;margin-bottom:4px;font-size:13px}
.hero-row label{color:#a6adc8;width:80px;flex-shrink:0}
.hero-row input[type=number]{background:#45475a;border:1px solid #585b70;color:#cdd6f4;border-radius:4px;padding:3px 6px;width:70px;font-size:13px}
.hero-row input[type=number]:focus{outline:none;border-color:#89b4fa}
.skills-badge{display:flex;gap:4px}
.skill-on{background:#a6e3a1;color:#1e1e2e;border-radius:3px;padding:1px 5px;font-size:11px;font-weight:700}
.skill-off{background:#45475a;color:#6c7086;border-radius:3px;padding:1px 5px;font-size:11px}
/* Save info */
.info-grid{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin-bottom:14px}
.info-grid .lbl{color:#a6adc8}
.info-grid .val{color:#cdd6f4;font-weight:600}
.gold-val{color:#f9e2af;font-size:20px;font-weight:700;margin-bottom:8px}
/* Buttons */
btn,button,.btn{border:none;border-radius:5px;cursor:pointer;font-family:inherit;font-weight:600;transition:opacity .15s}
.btn-primary{background:#89b4fa;color:#1e1e2e;padding:8px 16px;font-size:13px;width:100%}
.btn-primary:hover{opacity:.85}
.btn-sm{background:#45475a;color:#cdd6f4;padding:3px 8px;font-size:11px;border-radius:3px;border:none;cursor:pointer}
.btn-sm:hover{background:#585b70}
.btn-red{background:#f38ba8;color:#1e1e2e}
.btn-green{background:#a6e3a1;color:#1e1e2e}
.btn-yellow{background:#f9e2af;color:#1e1e2e}
/* Divider */
.divider{border:none;border-top:1px solid #313244;margin:12px 0}
/* Gold input */
.input-row{display:flex;gap:6px;margin-bottom:8px}
.input-row input{flex:1;background:#45475a;border:1px solid #585b70;color:#cdd6f4;border-radius:4px;padding:5px 8px;font-size:13px}
/* Tabs */
.tabs{display:flex;gap:0;margin-bottom:10px;border-bottom:2px solid #313244}
.tab{padding:6px 14px;cursor:pointer;color:#a6adc8;font-size:13px;font-weight:600;border-bottom:2px solid transparent;margin-bottom:-2px}
.tab.active{color:#89b4fa;border-bottom-color:#89b4fa}
/* Item table */
.item-table{width:100%;border-collapse:collapse;font-size:12px}
.item-table th{color:#a6adc8;text-align:left;padding:4px 6px;border-bottom:1px solid #313244;font-weight:600;font-size:11px;text-transform:uppercase}
.item-table td{padding:5px 6px;border-bottom:1px solid #1e1e2e;vertical-align:middle}
.item-table tr:hover td{background:#2a2a3e}
.badge{display:inline-block;border-radius:3px;padding:1px 5px;font-size:10px;font-weight:700;margin-left:4px}
.badge-chaotic{background:#f38ba8;color:#1e1e2e}
.badge-blocked{background:#f9e2af;color:#1e1e2e}
.item-name{max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
/* Toast */
#toast{position:fixed;bottom:20px;right:20px;background:#a6e3a1;color:#1e1e2e;padding:10px 18px;border-radius:6px;font-weight:700;display:none;z-index:999;box-shadow:0 4px 12px rgba(0,0,0,.4)}
#toast.error{background:#f38ba8}
</style>
</head>
<body>
<header>
  <h1>TBH Optimizer</h1>
  <span id="status">Yükleniyor…</span>
</header>
<div class="layout">

<!-- LEFT: Heroes -->
<div class="panel">
  <div class="section-title">Herolar</div>
  <div id="heroes"></div>
  <button class="btn btn-primary" onclick="saveHeroes()" style="margin-top:8px">Kaydet &amp; Uygula</button>
</div>

<!-- MIDDLE: Save info + Gold -->
<div class="panel">
  <div class="section-title">Save Bilgisi</div>
  <div class="info-grid" id="save-info"></div>
  <hr class="divider">
  <div class="section-title">Gold</div>
  <div class="gold-val" id="gold-display">—</div>
  <div class="input-row">
    <input type="number" id="gold-add" placeholder="Eklenecek miktar" min="1">
    <button class="btn btn-sm btn-yellow" onclick="addGold()">Ekle</button>
  </div>
  <hr class="divider">
  <div class="section-title">Rünler</div>
  <div id="rune-info" style="color:#a6adc8;font-size:13px;margin-bottom:8px">Yükleniyor…</div>
  <button class="btn btn-primary" onclick="maxRunes()" style="background:#cba6f7">Tüm Rünleri Max Yap</button>
</div>

<!-- RIGHT: Items -->
<div class="panel">
  <div class="section-title">Item Yöneticisi</div>
  <div class="tabs">
    <div class="tab active" onclick="switchTab('inv',this)">Envanter (<span id="inv-count">0</span>)</div>
    <div class="tab" onclick="switchTab('stash',this)">Stash (<span id="stash-count">0</span>)</div>
  </div>
  <div id="item-panel"></div>
</div>

</div>
<div id="toast"></div>

<script>
let saveData = null;
let activeTab = 'inv';
let heroesBuilt = false;

async function fetchSave() {
  try {
    const r = await fetch('/api/save');
    saveData = await r.json();
    renderAll();
    document.getElementById('status').textContent =
      'Son güncelleme: ' + new Date().toLocaleTimeString();
  } catch(e) {
    document.getElementById('status').textContent = 'Bağlantı hatası';
  }
}

function renderAll() {
  if (!saveData) return;
  renderInfo();
  renderHeroes();
  renderItems();
}

function renderInfo() {
  const d = saveData;
  document.getElementById('save-info').innerHTML = `
    <span class="lbl">Stage</span><span class="val">${d.stage}</span>
    <span class="lbl">Max</span><span class="val">${d.maxStage}</span>
    <span class="lbl">Süre</span><span class="val">${d.playtime} saat</span>
  `;
  document.getElementById('gold-display').textContent = d.goldFmt;
  if (d.runes) {
    const r = d.runes;
    document.getElementById('rune-info').textContent =
      `Toplam: ${r.total}  |  Max (Lv5): ${r.maxed}  |  Kilitli: ${r.locked}`;
  }
}

async function maxRunes() {
  if (!confirm('Oyun KAPALI mı? Tüm rünler Level 5 yapılacak.')) return;
  const r = await fetch('/api/runes/max', {method:'POST', headers:{'Content-Type':'application/json'}, body:'{}'});
  const res = await r.json();
  if (res.ok) { toast(res.msg,'ok'); await fetchSave(); }
  else toast(res.msg,'error');
}

function buildHeroCards() {
  const container = document.getElementById('heroes');
  container.innerHTML = '';
  for (const h of saveData.heroes) {
    const skills = [1,2,3].map(i =>
      i <= h.skills
        ? `<span class="skill-on">S${i}</span>`
        : `<span class="skill-off">S${i}</span>`
    ).join('');
    container.innerHTML += `
      <div class="hero-card">
        <div class="hero-name">
          ${h.name}${h.locked ? '<span class="lock">KILITLI</span>' : ''}
        </div>
        <div class="hero-row">
          <label>Mevcut Lv</label><span id="hlv-curr-${h.key}">${h.level}</span>
        </div>
        <div class="hero-row">
          <label>Hedef Lv</label>
          <input type="number" id="hlv-${h.key}" value="${h.level}" min="1" max="100"
            ${h.locked ? 'disabled' : ''}>
        </div>
        <div class="hero-row">
          <label>Ability Pts</label>
          <span id="hlv-pts-${h.key}">Harcanmış: ${h.alloc} / Bekleyen: ${h.unspent}</span>
        </div>
        <div class="hero-row">
          <label>Skill</label><div class="skills-badge" id="hlv-sk-${h.key}">${skills}</div>
        </div>
      </div>`;
  }
  heroesBuilt = true;
}

function renderHeroes() {
  if (!heroesBuilt) { buildHeroCards(); return; }
  // Auto-refresh: update display only, leave inputs untouched
  for (const h of saveData.heroes) {
    const el = document.getElementById('hlv-curr-' + h.key);
    const pts = document.getElementById('hlv-pts-'  + h.key);
    const sk  = document.getElementById('hlv-sk-'   + h.key);
    if (el)  el.textContent  = h.level;
    if (pts) pts.textContent = `Harcanmış: ${h.alloc} / Bekleyen: ${h.unspent}`;
    if (sk)  sk.innerHTML    = [1,2,3].map(i =>
      i <= h.skills
        ? `<span class="skill-on">S${i}</span>`
        : `<span class="skill-off">S${i}</span>`
    ).join('');
  }
}

function renderItems() {
  const items = activeTab === 'inv' ? saveData.inventory : saveData.stash;
  document.getElementById('inv-count').textContent   = saveData.inventory.length;
  document.getElementById('stash-count').textContent = saveData.stash.length;

  if (!items.length) {
    document.getElementById('item-panel').innerHTML =
      '<p style="color:#6c7086;padding:12px">Gösterilecek item yok.</p>';
    return;
  }

  const rows = items.map(it => {
    const chaotic = it.chaotic ? '<span class="badge badge-chaotic">CHAOTIC</span>' : '';
    const blocked = it.blocked ? '<span class="badge badge-blocked">LOCKED</span>' : '';
    return `<tr>
      <td>${it.slot}</td>
      <td><span class="item-name" title="${it.name}">${it.name}</span>${chaotic}${blocked}</td>
      <td style="color:#a6adc8">${it.enchants > 0 ? '⚡'+it.enchants : '—'}</td>
      <td>
        <button class="btn-sm btn-green" onclick="dupItem(${it.uid})">Dup</button>
        <button class="btn-sm btn-red" onclick="removeItem(${it.slot},'${it.src}',${it.uid})" style="margin-left:3px">Sil</button>
      </td>
    </tr>`;
  }).join('');

  document.getElementById('item-panel').innerHTML = `
    <table class="item-table">
      <thead><tr>
        <th>Slot</th><th>Item</th><th>Ench.</th><th>İşlem</th>
      </tr></thead>
      <tbody>${rows}</tbody>
    </table>`;
}

function switchTab(tab, el) {
  activeTab = tab;
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  renderItems();
}

async function saveHeroes() {
  if (!confirm('Oyun KAPALI mı? Hero leveller kaydedilecek.')) return;
  const updates = {};
  for (const h of saveData.heroes) {
    if (h.locked) continue;
    const el = document.getElementById('hlv-' + h.key);
    if (el) updates[h.key] = parseInt(el.value);
  }
  const r = await fetch('/api/heroes', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({updates})
  });
  const res = await r.json();
  if (res.ok) { heroesBuilt = false; toast(res.msg,'ok'); await fetchSave(); }
  else toast(res.msg, 'error');
}

async function addGold() {
  if (!confirm('Oyun KAPALI mı?')) return;
  const amount = parseInt(document.getElementById('gold-add').value);
  if (!amount || amount <= 0) { toast('Geçerli bir miktar gir','error'); return; }
  const r = await fetch('/api/gold', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({amount})
  });
  const res = await r.json();
  if (res.ok) { toast(res.msg,'ok'); await fetchSave(); }
  else toast(res.msg,'error');
}

async function dupItem(uid) {
  const r = await fetch('/api/items/dup', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({uid})
  });
  const res = await r.json();
  if (res.ok) { toast(res.msg,'ok'); await fetchSave(); }
  else toast(res.msg,'error');
}

async function removeItem(slot, src, uid) {
  if (!confirm(`Slot ${slot} silinecek. Emin misin?`)) return;
  const r = await fetch('/api/items/remove', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({slot, src, uid})
  });
  const res = await r.json();
  if (res.ok) { toast(res.msg,'ok'); await fetchSave(); }
  else toast(res.msg,'error');
}

function toast(msg, type='ok') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = type === 'error' ? 'error' : '';
  el.style.display = 'block';
  setTimeout(() => el.style.display = 'none', 2800);
}

// Initial load + auto refresh
fetchSave();
setInterval(fetchSave, 4000);
</script>
</body>
</html>"""

# ─── HTTP Handler ─────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        log.info(f'{self.address_string()} {fmt % args}')

    def _send(self, code, ctype, body):
        if isinstance(body, str): body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code,'application/json',json.dumps(obj,ensure_ascii=False))

    def _read_body(self):
        n = int(self.headers.get('Content-Length',0))
        return json.loads(self.rfile.read(n)) if n else {}

    def do_GET(self):
        State.load()
        if self.path == '/':
            self._send(200,'text/html; charset=utf-8', HTML)
        elif self.path == '/api/save':
            self._json(build_api_data())
        else:
            log.warning(f'GET 404: {self.path}')
            self._send(404,'text/plain',b'Not found')

    def do_POST(self):
        try:
            self._handle_post()
        except Exception:
            tb = traceback.format_exc()
            log.error(f'POST {self.path} hata:\n{tb}')
            self._json({'ok':False,'msg':'Sunucu hatası, log dosyasına bakın'}, code=500)

    def _handle_post(self):
        State.load()
        body = self._read_body()
        log.info(f'POST {self.path} body={body}')
        path = self.path

        if path == '/api/heroes':
            updates = body.get('updates',{})
            if State.player is None:
                return self._json({'ok':False,'msg':'Save yüklenmedi'})
            with State.lock:
                changed = []
                for h in State.player.get('heroSaveDatas',[]):
                    k = h['heroKey']
                    new_lv = updates.get(str(k)) or updates.get(k)
                    if new_lv is None: continue
                    new_lv = max(1, min(new_lv, HERO_MAX_LEVEL))
                    if new_lv == h['HeroLevel']: continue
                    old_lv = h['HeroLevel']
                    alloc  = h['AllocatedHeroAbilityPoint']
                    h['HeroLevel']    = new_lv
                    h['AbilityPoint'] = max(0, new_lv - alloc)
                    h['HeroExp']      = max(h.get('HeroExp',0), float(new_lv*50000))
                    h['equippedSKillKey'] = skill_keys(k, new_lv)
                    if new_lv >= 10 and 10002 not in h.get('unlockedAttributeGroupKeys',[]):
                        h.setdefault('unlockedAttributeGroupKeys',[]).append(10002)
                    changed.append(f"{HERO_NAMES.get(k,'?')}: Lv{old_lv}→{new_lv}")
                if not changed:
                    return self._json({'ok':False,'msg':'Değişiklik yok (mevcut leveldan küçük/eşit değer girildi)'})
                State.save()
                log.info(f'Hero save: {changed}')
            self._json({'ok':True,'msg':'Kaydedildi: '+', '.join(changed)})

        elif path == '/api/gold':
            amount = int(body.get('amount',0))
            if amount <= 0:
                return self._json({'ok':False,'msg':'Geçersiz miktar'})
            with State.lock:
                curr = State.player.get('currenySaveDatas',[])
                entry = next((x for x in curr if x['Key']==100001),None)
                if not entry:
                    return self._json({'ok':False,'msg':'Gold kaydı bulunamadı'})
                entry['Quantity'] += amount
                new_gold = entry['Quantity']
                State.save()
            self._json({'ok':True,'msg':f'Gold: {fmt(new_gold)}'})

        elif path == '/api/items/dup':
            uid = body.get('uid')
            if uid is None:
                return self._json({'ok':False,'msg':'uid eksik'})
            with State.lock:
                items = State.player.get('itemSaveDatas',[])
                src   = next((i for i in items if i['UniqueId']==uid),None)
                if not src:
                    return self._json({'ok':False,'msg':'Item bulunamadı'})
                new_uid  = max(i['UniqueId'] for i in items) + 1
                new_item = copy.deepcopy(src)
                new_item['UniqueId'] = new_uid
                new_item['IsServerPendingItem'] = False
                items.append(new_item)
                # Boş envanter slotu bul
                inv = State.player.get('inventorySaveDatas',[])
                slot = next((s for s in inv if s['ItemUniqueId']==0 and s.get('IsUnlock',False)),None)
                if not slot:
                    # son item'i geri al
                    items.pop()
                    return self._json({'ok':False,'msg':'Boş envanter slotu yok'})
                slot['ItemUniqueId'] = new_uid
                State.save()
            self._json({'ok':True,'msg':f'Item kopyalandı → Slot {slot["Index"]} (UID {new_uid})'})

        elif path == '/api/items/remove':
            slot_idx = body.get('slot')
            src_name = body.get('src','inv')
            uid      = body.get('uid')
            with State.lock:
                col_key = 'inventorySaveDatas' if src_name=='inv' else 'stashSaveDatas'
                col     = State.player.get(col_key,[])
                slot    = next((s for s in col if s['Index']==slot_idx),None)
                if not slot:
                    return self._json({'ok':False,'msg':'Slot bulunamadı'})
                slot['ItemUniqueId'] = 0
                # itemSaveDatas'tan da kaldır
                State.player['itemSaveDatas'] = [
                    i for i in State.player.get('itemSaveDatas',[])
                    if i['UniqueId'] != uid
                ]
                State.save()
            self._json({'ok':True,'msg':f'Slot {slot_idx} temizlendi'})

        elif path == '/api/runes/max':
            with State.lock:
                runes = State.player.get('RuneSaveData',[])
                rune_max = State.rune_max_levels()
                for r in runes:
                    r['Level'] = rune_max.get(r['RuneKey'], 5)
                State.save()
                log.info(f'Runes maxed: {len(runes)} adet')
            self._json({'ok':True,'msg':f'{len(runes)} rün kendi max seviyesine alındı'})

        else:
            self._send(404,'text/plain',b'Not found')

# ─── Entry ────────────────────────────────────────────────────────────────────
def file_watcher():
    while True:
        time.sleep(3)
        State.load()

if __name__ == '__main__':
    log.info(f'Save: {SAVE_FILE}')
    State.load()
    threading.Thread(target=State.fetch_item_names, daemon=True).start()
    threading.Thread(target=file_watcher, daemon=True).start()

    server = socketserver.TCPServer(('127.0.0.1', PORT), Handler)
    server.allow_reuse_address = True
    url = f'http://127.0.0.1:{PORT}'
    log.info(f'UI → {url}')
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nKapatılıyor...')

import asyncio
import aiohttp
import json
import re
from datetime import datetime
from telegram import Bot
from telegram.constants import ParseMode

# ============================================================

# КОНФИГ — вставь свои данные

# ============================================================

TELEGRAM_TOKEN = "8774353889:AAH_UdJEir8d9D88yqywJlqjJfqsISm3n7U"
CHAT_ID = "967491277"

# Пороги срабатывания

MIN_MINUTE = 58          # Минимальная минута для сигнала
MAX_MINUTE = 80          # Максимальная минута
MIN_SHOTS_ON_TARGET = 5  # Минимум ударов в створ суммарно
MIN_CORNERS = 6          # Минимум угловых суммарно
CHECK_INTERVAL = 90      # Проверка каждые 90 секунд

# ============================================================

# СПИСОК ЛИГ — все забивные лиги мира

# ============================================================

LEAGUES = {
# 🇦🇺 АВСТРАЛИЯ
“AUS: A-League”: “australia/a-league”,
“AUS: NPL Victoria”: “australia/npl-victoria”,
“AUS: NPL Queensland”: “australia/npl-queensland”,
“AUS: NPL NSW”: “australia/npl-nsw”,

```
# 🇩🇪 ГЕРМАНИЯ
"GER: Bundesliga": "germany/bundesliga",
"GER: 2. Bundesliga": "germany/2-bundesliga",
"GER: 3. Liga": "germany/3-liga",

# 🇬🇧 АНГЛИЯ
"ENG: Premier League": "england/premier-league",
"ENG: Championship": "england/championship",
"ENG: League One": "england/league-one",
"ENG: League Two": "england/league-two",
"ENG: National League": "england/national-league",

# 🇫🇷 ФРАНЦИЯ
"FRA: Ligue 1": "france/ligue-1",
"FRA: Ligue 2": "france/ligue-2",

# 🇪🇸 ИСПАНИЯ
"ESP: LaLiga": "spain/laliga",
"ESP: Segunda": "spain/segunda-division",

# 🇮🇹 ИТАЛИЯ
"ITA: Serie A": "italy/serie-a",
"ITA: Serie B": "italy/serie-b",

# 🇳🇱 НИДЕРЛАНДЫ
"NED: Eredivisie": "netherlands/eredivisie",
"NED: Eerste Divisie": "netherlands/eerste-divisie",

# 🇧🇪 БЕЛЬГИЯ
"BEL: Pro League": "belgium/pro-league",

# 🇵🇹 ПОРТУГАЛИЯ
"POR: Primeira Liga": "portugal/primeira-liga",
"POR: Liga Portugal 2": "portugal/liga-portugal-2",

# 🇹🇷 ТУРЦИЯ
"TUR: Süper Lig": "turkey/super-lig",
"TUR: 1. Lig": "turkey/1-lig",

# 🇷🇴 РУМЫНИЯ
"ROU: Liga 1": "romania/liga-1",

# 🇵🇱 ПОЛЬША
"POL: Ekstraklasa": "poland/ekstraklasa",

# 🇺🇦 УКРАИНА
"UKR: Premier League": "ukraine/premier-league",

# 🇸🇪 ШВЕЦИЯ
"SWE: Allsvenskan": "sweden/allsvenskan",
"SWE: Superettan": "sweden/superettan",

# 🇳🇴 НОРВЕГИЯ
"NOR: Eliteserien": "norway/eliteserien",
"NOR: 1. divisjon": "norway/1-divisjon",

# 🇩🇰 ДАНИЯ
"DEN: Superliga": "denmark/superliga",

# 🇫🇮 ФИНЛЯНДИЯ — очень забивная!
"FIN: Veikkausliiga": "finland/veikkausliiga",
"FIN: Ykkösliiga": "finland/ykkosliiga",
"FIN: Kakkonen": "finland/kakkonen",

# 🇪🇪 ЭСТОНИЯ — очень забивная!
"EST: Meistriliiga": "estonia/meistriliiga",
"EST: Esiliiga": "estonia/esiliiga",

# 🇱🇻 ЛАТВИЯ
"LAT: Virsliga": "latvia/virsliga",

# 🇱🇹 ЛИТВА
"LTU: A Lyga": "lithuania/a-lyga",

# 🇸🇬 СИНГАПУР — топ по голам!
"SGP: S.League": "singapore/s-league",

# 🇯🇵 ЯПОНИЯ
"JPN: J1 League": "japan/j1-league",
"JPN: J2 League": "japan/j2-league",
"JPN: J3 League": "japan/j3-league",

# 🇰🇷 КОРЕЯ
"KOR: K League 1": "south-korea/k-league-1",
"KOR: K League 2": "south-korea/k-league-2",

# 🇨🇳 КИТАЙ
"CHN: Super League": "china/super-league",

# 🇹🇭 ТАИЛАНД
"THA: Thai League 1": "thailand/thai-league-1",

# 🇲🇾 МАЛАЙЗИЯ
"MYS: Super League": "malaysia/super-league",

# 🇮🇩 ИНДОНЕЗИЯ
"IDN: Liga 1": "indonesia/liga-1",

# 🇧🇷 БРАЗИЛИЯ
"BRA: Série A": "brazil/serie-a",
"BRA: Série B": "brazil/serie-b",

# 🇦🇷 АРГЕНТИНА
"ARG: Primera División": "argentina/primera-division",

# 🇲🇽 МЕКСИКА
"MEX: Liga MX": "mexico/liga-mx",

# 🇺🇸 США
"USA: MLS": "usa/mls",
"USA: USL Championship": "usa/usl-championship",

# 🇸🇦 САУДОВСКАЯ АРАВИЯ
"KSA: Pro League": "saudi-arabia/pro-league",

# 🇦🇪 ОАЭ
"UAE: Pro League": "uae/pro-league",

# 🇮🇱 ИЗРАИЛЬ
"ISR: Premier League": "israel/premier-league",

# 🇬🇷 ГРЕЦИЯ
"GRE: Super League": "greece/super-league",

# 🇨🇿 ЧЕХИЯ
"CZE: Fortuna Liga": "czech-republic/fortuna-liga",

# 🇭🇺 ВЕНГРИЯ
"HUN: OTP Bank Liga": "hungary/otp-bank-liga",

# 🇸🇰 СЛОВАКИЯ
"SVK: Niké Liga": "slovakia/nike-liga",

# 🇷🇸 СЕРБИЯ
"SRB: Super Liga": "serbia/super-liga",

# 🇭🇷 ХОРВАТИЯ
"HRV: HNL": "croatia/hnl",

# 🇸🇮 СЛОВЕНИЯ
"SVN: PrvaLiga": "slovenia/prvaliga",

# 🇧🇦 БОСНИЯ
"BIH: Premier League": "bosnia/premier-league",

# 🇲🇰 МАКЕДОНИЯ
"MKD: First League": "north-macedonia/first-league",

# 🇦🇱 АЛБАНИЯ
"ALB: Superliga": "albania/superliga",
```

}

# ============================================================

# УТИЛИТЫ

# ============================================================

def get_intensity_emoji(shots: int, corners: int) -> str:
score = shots + corners
if score >= 20:
return “🔥🔥🔥”
elif score >= 15:
return “🔥🔥”
else:
return “🔥”

def get_scenario_label(score_home: int, score_away: int, minute: int) -> tuple:
total = score_home + score_away
if total == 0:
return “⚡ НУЛИ — ВЗРЫВ ПОД ЗАНАВЕС”, “СЦЕНАРИЙ 2”
elif total == 1:
return “🎯 ЖИВАЯ ИГРА — ДОБАВКА БЛИЗКО”, “СЦЕНАРИЙ 1”
else:
return “💥 УЖЕ ГОРИТ — ЕЩЁ НЕ КОНЕЦ”, “СЦЕНАРИЙ 3”

def format_alert(match: dict) -> str:
home = match[‘home_team’]
away = match[‘away_team’]
score_h = match[‘score_home’]
score_a = match[‘score_away’]
minute = match[‘minute’]
shots = match[‘shots_on_target’]
corners = match[‘corners’]
league = match[‘league’]
odds = match.get(‘odds_over’, ‘~1.90’)

```
label, scenario = get_scenario_label(score_h, score_a, minute)
intensity = get_intensity_emoji(shots, corners)

remaining = 90 - minute

msg = f"""
```

{intensity} <b>СИГНАЛ ТОТАЛ БОЛЬШЕ</b> {intensity}
━━━━━━━━━━━━━━━━━━━━━━
🏆 <b>{league}</b>

⚽ <b>{home}</b> vs <b>{away}</b>
📊 Счёт: <b>{score_h} : {score_a}</b>  |  ⏱ <b>{minute}’</b>

{label}

━━━━━━━━━━━━━━━━━━━━━━
📈 <b>СТАТИСТИКА МАТЧА:</b>
🎯 Удары в створ:  <b>{shots}</b>
🚩 Угловые:        <b>{corners}</b>
⏳ До конца:       <b>~{remaining} мин</b>

━━━━━━━━━━━━━━━━━━━━━━
💰 <b>СТАВКА:</b>  ТБ {score_h + score_a + 0.5:.1f}  |  Кэф <b>{odds}</b>
━━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime(’%H:%M:%S’)}
“””
return msg.strip()

# ============================================================

# ПАРСЕР FLASHSCORE (через API)

# ============================================================

class FlashScoreParser:
def **init**(self):
self.session = None
self.headers = {
‘User-Agent’: ‘Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36’,
‘Accept’: ‘application/json, text/plain, */*’,
‘Accept-Language’: ‘en-US,en;q=0.9’,
‘Origin’: ‘https://www.flashscore.com’,
‘Referer’: ‘https://www.flashscore.com/’,
‘x-fsign’: ‘SW9D1eZo’,
}

```
async def get_session(self):
    if not self.session:
        self.session = aiohttp.ClientSession(headers=self.headers)
    return self.session

async def fetch_live_matches(self) -> list:
    """Получает все живые матчи с flashscore"""
    session = await self.get_session()
    matches = []
    
    try:
        url = "https://d.flashscore.com/x/feed/f_1_0_1_en_1"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status == 200:
                text = await resp.text()
                matches = self.parse_matches(text)
    except Exception as e:
        print(f"[ERROR] Ошибка получения матчей: {e}")
        
    return matches

def parse_matches(self, raw: str) -> list:
    """Парсит сырые данные flashscore"""
    matches = []
    
    # Flashscore использует специальный формат с разделителями
    chunks = raw.split('¬~AA÷')
    
    for chunk in chunks[1:]:
        try:
            match = self.parse_single_match(chunk)
            if match:
                matches.append(match)
        except Exception:
            continue
            
    return matches

def parse_single_match(self, chunk: str) -> dict:
    """Парсит один матч"""
    def extract(pattern, text, default=''):
        m = re.search(pattern, text)
        return m.group(1) if m else default

    # ID матча
    match_id = extract(r'^([^¬]+)', chunk)
    
    # Команды
    home = extract(r'¬AB÷([^¬]+)', chunk)
    away = extract(r'¬AC÷([^¬]+)', chunk)
    
    # Счёт
    score_h = extract(r'¬AG÷([^¬]+)', chunk)
    score_a = extract(r'¬AH÷([^¬]+)', chunk)
    
    # Минута
    minute_raw = extract(r'¬AD÷([^¬]+)', chunk)
    
    # Статус (живой матч = 2)
    status = extract(r'¬AA÷[^¬]+¬AB÷[^¬]+¬AC÷[^¬]+¬[^A]*AE÷([^¬]+)', chunk)
    
    # Лига
    league_id = extract(r'¬ZEE÷([^¬]+)', chunk)
    
    try:
        minute = int(minute_raw) if minute_raw.isdigit() else 0
        s_home = int(score_h) if score_h.isdigit() else 0
        s_away = int(score_a) if score_a.isdigit() else 0
    except:
        return None
        
    if not home or not away or minute == 0:
        return None
        
    return {
        'id': match_id,
        'home_team': home,
        'away_team': away,
        'score_home': s_home,
        'score_away': s_away,
        'minute': minute,
        'league': league_id,
        'shots_on_target': 0,
        'corners': 0,
    }

async def fetch_match_stats(self, match_id: str) -> dict:
    """Получает статистику конкретного матча"""
    session = await self.get_session()
    stats = {'shots_on_target': 0, 'corners': 0}
    
    try:
        url = f"https://d.flashscore.com/x/feed/d_st_{match_id}_1_en_1"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 200:
                text = await resp.text()
                stats = self.parse_stats(text)
    except Exception as e:
        print(f"[ERROR] Статистика {match_id}: {e}")
        
    return stats

def parse_stats(self, raw: str) -> dict:
    """Парсит статистику матча"""
    shots_home = 0
    shots_away = 0
    corners_home = 0
    corners_away = 0
    
    # Ищем удары в створ
    shots_match = re.findall(r'Shots on Goal[^~]*?¬([0-9]+)¬([0-9]+)', raw)
    if shots_match:
        shots_home = int(shots_match[0][0])
        shots_away = int(shots_match[0][1])
        
    # Альтернативный паттерн
    if not shots_home and not shots_away:
        shots_alt = re.findall(r'On Target[^~]*?¬([0-9]+)¬([0-9]+)', raw)
        if shots_alt:
            shots_home = int(shots_alt[0][0])
            shots_away = int(shots_alt[0][1])

    # Ищем угловые
    corners_match = re.findall(r'Corner Kicks[^~]*?¬([0-9]+)¬([0-9]+)', raw)
    if corners_match:
        corners_home = int(corners_match[0][0])
        corners_away = int(corners_match[0][1])

    return {
        'shots_on_target': shots_home + shots_away,
        'corners': corners_home + corners_away,
    }

async def close(self):
    if self.session:
        await self.session.close()
```

# ============================================================

# ОСНОВНАЯ ЛОГИКА БОТА

# ============================================================

class FootballBot:
def **init**(self):
self.parser = FlashScoreParser()
self.bot = Bot(token=TELEGRAM_TOKEN)
self.sent_alerts = set()  # Чтобы не дублировать сигналы

```
def should_alert(self, match: dict) -> bool:
    """Проверяет все условия для сигнала"""
    minute = match['minute']
    shots = match['shots_on_target']
    corners = match['corners']
    
    # Временное окно
    if not (MIN_MINUTE <= minute <= MAX_MINUTE):
        return False
        
    # Статистика живой игры
    if shots < MIN_SHOTS_ON_TARGET:
        return False
        
    if corners < MIN_CORNERS:
        return False
        
    return True

async def process_matches(self):
    """Основной цикл обработки матчей"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Проверка матчей...")
    
    matches = await self.parser.fetch_live_matches()
    print(f"[INFO] Найдено живых матчей: {len(matches)}")
    
    candidates = []
    
    for match in matches:
        if not (MIN_MINUTE <= match['minute'] <= MAX_MINUTE):
            continue
            
        # Подгружаем статистику
        stats = await self.parser.fetch_match_stats(match['id'])
        match.update(stats)
        
        if self.should_alert(match):
            candidates.append(match)
            
    print(f"[INFO] Кандидатов для сигнала: {len(candidates)}")
    
    for match in candidates:
        alert_key = f"{match['id']}_{match['score_home']}_{match['score_away']}"
        
        if alert_key not in self.sent_alerts:
            await self.send_alert(match)
            self.sent_alerts.add(alert_key)
            # Очищаем старые ключи чтобы не раздувалось
            if len(self.sent_alerts) > 500:
                self.sent_alerts = set(list(self.sent_alerts)[-200:])

async def send_alert(self, match: dict):
    """Отправляет красивый алерт в Telegram"""
    try:
        text = format_alert(match)
        await self.bot.send_message(
            chat_id=CHAT_ID,
            text=text,
            parse_mode=ParseMode.HTML
        )
        print(f"[SENT] {match['home_team']} vs {match['away_team']} {match['minute']}'")
    except Exception as e:
        print(f"[ERROR] Отправка: {e}")

async def send_startup_message(self):
    """Приветственное сообщение при запуске"""
    text = f"""
```

🚀 <b>БОТ ЗАПУЩЕН</b>
━━━━━━━━━━━━━━━━━━━━━━
⚽ Мониторинг: <b>{len(LEAGUES)} лиг</b>
⏱ Окно: <b>{MIN_MINUTE}’ — {MAX_MINUTE}’</b>
🎯 Мин. удары в створ: <b>{MIN_SHOTS_ON_TARGET}</b>
🚩 Мин. угловые: <b>{MIN_CORNERS}</b>
🔄 Проверка каждые: <b>{CHECK_INTERVAL}с</b>
━━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime(’%d.%m.%Y %H:%M:%S’)}
“””
await self.bot.send_message(
chat_id=CHAT_ID,
text=text.strip(),
parse_mode=ParseMode.HTML
)

```
async def run(self):
    """Главный цикл"""
    print("=" * 50)
    print("  FOOTBALL BETTING BOT — TOTAL OVER ALERTS")
    print("=" * 50)
    
    await self.send_startup_message()
    
    while True:
        try:
            await self.process_matches()
        except Exception as e:
            print(f"[ERROR] Главный цикл: {e}")
        
        await asyncio.sleep(CHECK_INTERVAL)
```

# ============================================================

# ЗАПУСК

# ============================================================

if **name** == “**main**”:
bot = FootballBot()
asyncio.run(bot.run())

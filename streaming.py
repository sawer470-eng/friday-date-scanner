"""
Проверка доступности — ТОЛЬКО Netflix и HBO Max (наши подписки).
"""
import requests
import re

# Только то, что есть на Netflix или HBO Max
NETFLIX_SHOWS = {
    "stranger things", "wednesday", "bridgerton", "the crown", "squid game",
    "dark", "money heist", "la casa de papel", "ozark", "narcos", "you",
    "lupin", "the witcher", "black mirror", "love is blind", "emily in paris",
    "sex education", "queen's gambit", "the queen's gambit", "outer banks",
    "cobra kai", "peaky blinders", "elite", "mindhunter", "the umbrella academy",
    "arcane", "beef", "the night agent", "fool me once", "baby reindeer",
    "ripley", "glass onion", "the gentlemen", "3 body problem",
    "avatar the last airbender", "one piece", "heartstopper", "shadow and bone",
    "the diplomat", "griselda", "fubar", "wednesday",
}

HBO_SHOWS = {
    "house of the dragon", "game of thrones", "the last of us", "succession",
    "euphoria", "true detective", "white lotus", "the white lotus", "chernobyl",
    "westworld", "the sopranos", "barry", "industry", "the gilded age",
    "his dark materials", "watchmen", "mare of easttown", "the penguin",
    "hacks", "barbie", "dune", "dune part two", "dune: part two",
    "the menu", "the batman", "harry potter", "friends", "sex and the city",
    "and just like that", "big little lies", "band of brothers",
}


def normalize(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    for article in ['the ', 'a ', 'an ']:
        if text.startswith(article):
            text = text[len(article):]
    return text.strip()


def check_local(title):
    """Проверка по локальному словарю Netflix/HBO"""
    norm = normalize(title)
    if not norm:
        return []
    
    platforms = []
    
    # Точное + частичное совпадение Netflix
    for show in NETFLIX_SHOWS:
        ns = normalize(show)
        if ns == norm or ns in norm or norm in ns:
            platforms.append("Netflix")
            break
    
    # Точное + частичное совпадение HBO
    for show in HBO_SHOWS:
        ns = normalize(show)
        if ns == norm or ns in norm or norm in ns:
            platforms.append("HBO Max")
            break
    
    return platforms


def check_watchmode(title, api_key):
    """Watchmode API — фильтруем только Netflix и HBO Max"""
    try:
        r = requests.get(
            "https://api.watchmode.com/v1/search/",
            params={"apiKey": api_key, "search_field": "name", "search_value": title},
            timeout=10
        )
        r.raise_for_status()
        results = r.json().get("title_results", [])
        if not results:
            return []
        
        title_id = results[0]["id"]
        
        r = requests.get(
            f"https://api.watchmode.com/v1/title/{title_id}/sources/",
            params={"apiKey": api_key},
            timeout=10
        )
        r.raise_for_status()
        sources = r.json()
        
        platforms = set()
        for s in sources:
            name = s.get("name", "").lower()
            stype = s.get("type", "")
            if stype not in ("sub", "free"):
                continue
            
            if "netflix" in name:
                platforms.add("Netflix")
            elif "hbo" in name or "max" == name:
                platforms.add("HBO Max")
        
        return sorted(platforms)
    except Exception:
        return []


def check_availability(title, config):
    """
    Возвращает список из подмножества ['Netflix', 'HBO Max'].
    Пустой список = недоступно на наших подписках.
    """
    api_key = config.get("WATCHMODE_API_KEY", "").strip()
    
    # 1. Watchmode
    if api_key:
        platforms = check_watchmode(title, api_key)
        if platforms:
            return platforms
    
    # 2. Локальный словарь
    return check_local(title)

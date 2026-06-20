import json
from openai import OpenAI
from streaming import check_availability

SYSTEM_PROMPT = """You are a TV show and movie recommendation expert for date nights.

⚠️ STRICT RULES:
1. Recommend ONLY shows/movies available on Netflix OR HBO Max (Max).
2. DO NOT recommend Apple TV+, Disney+, Amazon Prime, Hulu, Paramount+ exclusives.
3. "title_en" MUST be the ORIGINAL ENGLISH title (Latin alphabet, IMDb format).
4. "title_ru" is the Russian translation for display.

GOOD EXAMPLES (Netflix/HBO only):
✅ Stranger Things (Netflix), Wednesday (Netflix), Money Heist (Netflix)
✅ House of the Dragon (HBO), The Last of Us (HBO), Succession (HBO)
✅ Euphoria (HBO), The White Lotus (HBO), Bridgerton (Netflix)

BAD EXAMPLES (DO NOT RECOMMEND):
❌ Ted Lasso (Apple TV+) — NOT on Netflix/HBO
❌ The Mandalorian (Disney+) — NOT on Netflix/HBO
❌ The Boys (Amazon) — NOT on Netflix/HBO
❌ The Bear (Hulu) — NOT on Netflix/HBO

Return STRICTLY this JSON:
{
  "recommendations": [
    {
      "title_en": "English IMDb title",
      "title_ru": "Русское название",
      "year": 2022,
      "genre": "Genre",
      "platform_hint": "Netflix" or "HBO Max",
      "reason": "Почему подходит (на русском, 2-3 предложения)",
      "mood": "Атмосфера (на русском)"
    }
  ]
}

Return exactly 5 recommendations, ALL available on Netflix or HBO Max.
"""

def analyze_profile(profile, config):
    client = OpenAI(
        api_key=config["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )

    user_prompt = f"""Analyze this Instagram profile and recommend 5 shows/movies for a date.

PROFILE:
{json.dumps(profile, ensure_ascii=False, indent=2)}

CRITICAL: Only recommend titles available on Netflix or HBO Max.
title_en must be in English (Latin alphabet) for API search.
reason and mood — на русском языке."""

    response = client.chat.completions.create(
        model=config["GROQ_MODEL"],
        max_tokens=2000,
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    data = json.loads(response.choices[0].message.content)
    recommendations = data.get("recommendations", [])

    filtered = []
    for rec in recommendations:
        search_title = rec.get("title_en") or rec.get("title", "")
        rec["title"] = rec.get("title_ru") or search_title
        rec["title_original"] = search_title

        platforms = check_availability(search_title, config)
        
        # Если не нашли — доверяем подсказке от Groq
        if not platforms:
            hint = rec.get("platform_hint", "")
            if "netflix" in hint.lower():
                platforms = ["Netflix"]
            elif "hbo" in hint.lower() or "max" in hint.lower():
                platforms = ["HBO Max"]
        
        # Оставляем только если есть на Netflix или HBO
        if platforms:
            rec["platforms"] = platforms
            filtered.append(rec)

    return filtered

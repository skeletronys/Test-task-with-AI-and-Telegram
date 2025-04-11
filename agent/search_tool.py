import os
import re
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()


def clean_text(text: str) -> str:
    return re.sub(r'[*_`\[\]]', '', text)


def search_google(query: str) -> str:

    params = {
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google",
        "num": 5,
        "hl": "uk"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    output = []

    for result in results.get("organic_results", []):
        title = clean_text(result.get("title", "Без назви"))
        link = result.get("link", "")
        snippet = clean_text(result.get("snippet", ""))
        output.append(f"🔹 {title}\n{snippet}\n{link}\n")

    return "\n".join(output) if output else "Нічого не знайдено"


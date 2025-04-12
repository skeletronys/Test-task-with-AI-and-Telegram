import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()
RIA_KEY = os.getenv("RIA_API_KEY")
BASE = "https://developers.ria.com/auto"

def get_marka_id(name: str) -> int:
    response = requests.get(f"{BASE}/categories/1/marks", params={"api_key": RIA_KEY}).json()
    if not isinstance(response, list):
        print("[ERROR] get_marka_id: API returned not a list:", response)
        return None
    for mark in response:
        if name.lower() in mark["name"].lower():
            return mark["value"]
    return None


def get_model_id(marka_id: int, model_name: str) -> int:
    response = requests.get(f"{BASE}/categories/1/marks/{marka_id}/models", params={"api_key": RIA_KEY}).json()
    if not isinstance(response, list):
        print("[ERROR] get_model_id: API returned not a list:", response)
        return None
    model_name = model_name.lower().strip()
    for model in response:
        name = model["name"].lower()
        if name.startswith(model_name) or model_name in name:
            return model["value"]
    return None


def extract_filters(text: str):
    # Основна назва
    main_part = text.replace("/find", "").split(",")[0].strip()
    brand, model = (main_part.split(" ", 1) + [""])[:2]

    # Рік
    year_match = re.search(r"від\s*(\d{4})", text)
    year_from = int(year_match.group(1)) if year_match else 2015

    # Ціна
    price_from = None
    price_to = None
    p_from = re.search(r"від\s*(\d{4,5})\s*\$", text)
    p_to = re.search(r"до\s*(\d{4,5})\s*\$", text)
    if p_from: price_from = int(p_from.group(1))
    if p_to: price_to = int(p_to.group(1))

    # Тип коробки
    gearbox = None
    if "автомат" in text.lower(): gearbox = 2
    elif "механіка" in text.lower(): gearbox = 1

    # Тип палива
    fuel = None
    if "бензин" in text.lower(): fuel = 1
    elif "дизель" in text.lower(): fuel = 2
    elif "газ" in text.lower(): fuel = 3
    elif "гібрид" in text.lower(): fuel = 4
    elif "електро" in text.lower() or "електричний" in text.lower(): fuel = 5

    return brand.strip(), model.strip(), year_from, price_from, price_to, gearbox, fuel

def find_auto(raw_query: str, limit=5) -> str:
    brand, model, year_from, price_from, price_to, gearbox, fuel = extract_filters(raw_query)

    marka_id = get_marka_id(brand)
    if not marka_id:
        return f"Марку '{brand}' не знайдено"

    model_id = get_model_id(marka_id, model) if model else None

    params = {
        "api_key": RIA_KEY,
        "category_id": 1,
        "marka_id": marka_id,
        "s_yers": year_from,
        "countpage": limit,
        "with_photo": 1
    }

    if model_id:
        params["model_id"] = model_id
    if price_from:
        params["price_ot"] = price_from
    if price_to:
        params["price_do"] = price_to
    if gearbox:
        params["gearbox"] = gearbox
    if fuel:
        params["fuel_type"] = fuel

    search = requests.get(f"{BASE}/search", params=params).json()
    raw_ids = search.get("result", "")
    ids = raw_ids.split(",")[:limit] if isinstance(raw_ids, str) else []

    if not ids:
        return "Нічого не знайдено"

    results = []
    for car_id in ids:
        car = requests.get(f"{BASE}/info", params={"api_key": RIA_KEY, "auto_id": car_id}).json()
        results.append(f"{car.get('title', 'Без назви')} ({car.get('year', '')})\n"
                       f"Ціна: ${car.get('USD', '???')}, Пробіг: {car.get('race', '---')} км\n"
                       f"{car.get('link_to_view', '')}\n")

    return "\n".join(results)

from flask import Flask, render_template
import os
import requests

app = Flask(__name__)

# Базовый URL до UI backend-а (uiserver), который агрегирует данные.
# В контейнере берём из переменной окружения UI_SERVER_URL, локально по умолчанию localhost.
UI_SERVER_URL = os.getenv("UI_SERVER_URL", "http://localhost:8500")


def map_quality_to_color(quality_state: str) -> str:
    """
    Преобразовать логическое состояние качества в цвет рамки.
    quality_state приходит из uiserver: "good" / "bad" / "unknown".
    """
    if quality_state == "good":
        return "limegreen"
    if quality_state == "bad":
        return "red"
    return "gray"


def build_empty_view_model() -> dict:
    """Запасная модель, если данных от сервисов пока нет или произошла ошибка."""
    return {
        "has_data": False,
        "fruit_name": "Нет данных",
        "weight": "—",
        "price_per_kg": "—",
        "total_price": "—",
        "freshness": "Положите фрукт на лоток, и мы проверим его свежесть",
        "freshness_color": "gray",
        "image_url": None,
        "fps": 0,
    }


def fetch_view_model() -> dict:
    """
    Получить текущие агрегированные данные из uiserver (`/api/current`).
    uiserver уже ходит в mainserver/weight/camera/детекторы и строит view-модель.
    """
    try:
        resp = requests.get(f"{UI_SERVER_URL}/api/current", timeout=1.0)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        # Любая ошибка сети/формата — просто показываем "нет данных"
        return build_empty_view_model()

    if not data.get("has_data"):
        return build_empty_view_model()

    view = data.get("result", {})

    quality_state = view.get("quality_state", "unknown")
    image_id = view.get("image_id")

    return {
        "has_data": True,
        # Имена и числа уже подготовлены в uiserver/app/services/ui_mapping.py
        "fruit_name": view.get("fruit_name", "Нет данных"),
        "weight": view.get("weight_display", "—"),
        "price_per_kg": view.get("price_display", "—"),
        "total_price": view.get("total_display", "—"),
        "freshness": view.get("quality_text", "Нет данных о качестве"),
        "freshness_color": map_quality_to_color(quality_state),
        # Картинка проксируется через uiserver, который в свою очередь берёт её из camera-сервиса
        "image_url": f"{UI_SERVER_URL}/image/{image_id}" if image_id else None,
        # При необходимости сюда можно подставить реальные FPS, если они где-то считаются
        "fps": 0,
    }


# =========================
# Главная страница
# =========================
@app.route('/')
def index():
    vm = fetch_view_model()

    return render_template(
        "index.html",
        fruit_name=vm["fruit_name"],
        weight=vm["weight"],
        price_per_kg=vm["price_per_kg"],
        total_price=vm["total_price"],
        freshness=vm["freshness"],
        freshness_color=vm["freshness_color"],
        fps=vm["fps"],
        image_url=vm["image_url"],
    )


# =========================
# Запуск сервера
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
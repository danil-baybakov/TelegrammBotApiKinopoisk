from api_kinopoisk.core import api_kp
from api_telegramm_bot.resource.path import DEFAULT_IMAGE_PATH
from api_telegramm_bot.core import bot
from typing import BinaryIO


def is_number(text: str) -> int | None:
    try:
        return int(text)
    except (ValueError, TypeError):
        return None


def is_float(text: str) -> float | None:
    try:
        return float(text)
    except (ValueError, TypeError):
        return None


def search_films(genre: str,
                 limit: int = 10,
                 sort_param: int = 1,
                 rating_min: float = 0.0,
                 rating_max: float = 10.0) -> list[tuple[BinaryIO | str, str]]:
    films = api_kp.get_films_by_filter(
        genre=genre,
        limit=limit,
        sort_param=sort_param,
        rating_min=rating_min,
        rating_max=rating_max)

    list_films = films.get("docs", None)
    output = []

    if list_films:
        for film in list_films:

            # постер
            poster = film.get("poster", None)
            url_preview = None
            if poster is not None:
                url_preview = poster.get("previewUrl", None)
                if url_preview is None:
                    url_preview = poster.get("url", None)
            if url_preview is None:
                url_preview = open(DEFAULT_IMAGE_PATH, "rb")

            # наименование
            name = film.get("name", None)
            if name is None:
                name = film.get("alternativeName", None)
                if name is None:
                    name = "***"

            # жанр
            genres = film.get("genres", None)
            if genres:
                genres = ', '.join([genre["name"] for genre in genres])
            else:
                genres = "***"

            # рейтинг
            rating = film.get("rating", None)
            if rating is not None:
                kp_rating = rating.get("kp", None)
                if kp_rating is None:
                    kp_rating = "***"
                imdb_rating = rating.get("imdb", None)
                if imdb_rating is None:
                    imdb_rating = "***"
            else:
                kp_rating, imdb_rating = "***", "***"

            # год выпуска
            year = film.get("year", None)
            if year is None:
                year = "***"

            # возрастное ограничение
            edge_rating = film.get("ageRating", None)
            if edge_rating is None:
                edge_rating = "***"
            else:
                edge_rating = f"{edge_rating}+"

            # описание
            description = film.get("description", None)
            if description is None:
                description = "__________"

            caption = (f"🌈Название: {name} \n🍿Жанр: {genres} \n☃️Кинопоиск: {kp_rating} \t 🦏IMDB: {imdb_rating} "
                       f"\n📅Год выпуска: {year} \n😯Возрастной рейтинг: {edge_rating} "
                       f"\n\n🎬Описание:\n{description}")

            output.append((url_preview, caption))
    return output

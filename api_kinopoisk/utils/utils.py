import requests
from requests import Response
from settings import ApiSettings
from typing import TypeVar


class ApiKpRequestsException(Exception):
    """
    Класс объекта ошибки запроса к серверу
    """

    def __init__(self, message, extra_info):
        super().__init__(message)
        self.extra_info = extra_info


settings = ApiSettings()


class ApiClientKpInterface:
    """
    Базовый класс - интерфейс взаимодействия с API https://kinopoisk.dev/#tariffs

    Args:

    Attributes:
        BASE_URL (str): базовый URL сервера
        HEADERS (dict[str, str]): заголовок запросов на сервер
        TIMEOUT (int): ограничение по времени на загрузку всего ответа сервера
    """

    BASE_URL = settings.site_api_host
    HEADERS = {
        "accept": "application/json",
        "X-API-KEY": settings.site_api_key.get_secret_value()
    }
    TIMEOUT = 100

    def __init__(self) -> None:
        self.session = requests.Session()

    def get_list_genre_film(self) -> dict:
        """
        Метод для получения списка жанров фильмов

        :return: response.json() - словарь со списком жанров фильмов
        :rtype list[dict]
        :raise ApiKpRequestsException: если ответ от сервера вернулся с ошибкой
        """
        query_params = 'field=genres.name'
        url = f'{self.BASE_URL}/v1/movie/possible-values-by-field?{query_params}'
        response = self.session.get(url=url, headers=self.HEADERS, timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise ApiKpRequestsException(str(response.json()))

    def get_films_by_filter(self,
                            genre: str,
                            limit: int = 10,
                            sort_param: int = 1,
                            rating_min: float = 0.0,
                            rating_max: float = 10.0
                            ) -> dict:
        """
        Метод поиска фильмов с фильтрами

        :param genre: жанр фильма
        :param limit: кол-во фильмов для вывода
        :param sort_param: тип сортировки: 1 - по возрастанию, -1 - по убыванию
        :param rating_min: минимальный рейтинг фильма
        :param rating_max: максимальный рейтинг фильма

        :return: response.json() - словарь со списком фильмов
        :rtype list[dict]
        :raise ApiKpRequestsException: если ответ от сервера вернулся с ошибкой
        """
        if sort_param not in [1, - 1]:
            sort_param = 1
        query_params = (f'page=1&'
                        f'limit={limit}&'
                        f'sortField=rating.kp&'
                        f'sortType={sort_param}&'
                        f'rating.kp={str(rating_min)}-{str(rating_max)}&'
                        f'genres.name={genre}')
        url = f"{self.BASE_URL}/v1.4/movie?{query_params}"
        response = self.session.get(url=url, headers=self.HEADERS, timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise ApiKpRequestsException(str(response.json()))


if __name__ == "__main__":
    ...

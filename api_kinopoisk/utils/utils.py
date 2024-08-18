import requests
from requests import Response
from settings import ApiSettings


class ApiKpRequestsException(Exception):
    def __init__(self, message, extra_info):
        super().__init__(message)
        self.extra_info = extra_info


settings = ApiSettings()


class ApiClientKpInterface:
    BASE_URL = settings.site_api_host
    HEADERS = {
        "accept": "application/json",
        "X-API-KEY": settings.site_api_key.get_secret_value()
    }
    TIMEOUT = 5

    def __init__(self):
        self.session = requests.Session()

    def get_list_genre_film(self) -> list[dict]:
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
        query_params = (f'page=1&'
                        f'limit={limit}&'
                        f'sortField=rating.kp&'
                        f'sortType={sort_param}&'
                        f'rating.kp={str(rating_min)}-{str(rating_max)}&'
                        f'genres.name={genre}')
        print(sort_param)
        url = f"{self.BASE_URL}v1.4/movie?{query_params}"
        response = self.session.get(url=url, headers=self.HEADERS, timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise ApiKpRequestsException(str(response.json()))


if __name__ == "__main__":
    ...

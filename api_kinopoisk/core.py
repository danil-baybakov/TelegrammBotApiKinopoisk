from utils.utils import ApiClientKpInterface, ApiKpRequestsException

api_kp = ApiClientKpInterface()

if __name__ == "__main__":
    try:
        cmd = int(input('Какие данные получать (1 - low, 2 - high, 3 - custom): '))
        genres = api_kp.get_list_genre_film()
        if genres:
            for i, g in enumerate(genres):
                print(f"{i + 1} - {g['name']}")

            genre = int(input(f'Выберете жанр фильма для поиска (от 1 до {len(genres)}): '))
            limit = int(input(f'Введите кол-во фильмов для поиска (от 1 до 20): '))
            sort_param = 1 if cmd == 1 or cmd == 3 else -1
            rating_min = 0.0
            rating_nax = 10.0
            if cmd == 3:
                rating_min = max(0.0, float(input(f"Введите нижнюю границу рейтинга для поиска (от 0 до 10): ")))
                rating_nax = min(10.0, max(rating_min,
                                           float(input(f"Введите верхнюю границу рейтинга для поиска (от 0 до 10): "))))
            films = api_kp.get_films_by_filter(
                genre=genres[genre-1]["name"],
                limit=limit,
                sort_param=sort_param,
                rating_min=rating_min,
                rating_max=rating_nax
            )
            print("Список фильмов: ")
            if films.get("docs", None):
                for film in films["docs"]:
                    print("-"*30)
                    print(f"name: {film["name"]}, "
                          f"alternativeName: {film["alternativeName"]}, "
                          f"rating: {film["rating"]["kp"]}")
        else:
            print('Список жанров пуст.')

    except ApiKpRequestsException as exc:
        print('Ошибка запроса к Api')


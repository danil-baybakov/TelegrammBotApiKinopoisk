from api_database.common.model import db, ParamsStorage, History
from peewee import IntegrityError
from typing import TypeVar, Optional, Any
from datetime import datetime

A = TypeVar("A", ParamsStorage, History)


class InterfaceApiDatabase:
    """
    Базовый класс - интерфейс взаимодействия с БД sqlite

    Args:
    Attributes:
    """
    @classmethod
    def get_param_storage_by_cid(cls, cid: int) -> Optional[ParamsStorage]:
        """
        Метод получения по идентификатору пользователя данных текущего запроса в чат

        :param cid: идентификатор пользователя чата
        :return: объект с текущими параметрами запроса в чат
        """
        try:
            with db.atomic():
                return ParamsStorage.get(ParamsStorage.cid == cid)
        except Exception:
            pass

    @classmethod
    def get_history(cls, cid: int | None = None, limit: int = 10) -> list[History]:
        """
        Метод получения по идентификатору пользователя его истории запросов в чат

        :param cid: идентификатор пользователя чата
        :param limit: ограничение на кол-во получаемых данных, по умолчанию 10
        :return: список объектов истории запросов в чат
        """
        with db.atomic():
            where = History.cid == cid if cid is not None else True
            result = History.select().where(where).limit(limit).order_by(History.timestamp.desc())
        return [item for item in result]

    @classmethod
    def set_param_storage_by_cid(cls,
                                 model: A,
                                 cid: int,
                                 command: str | None = None,
                                 genre: str | None = None,
                                 limit: int | None = None,
                                 order: int | None = None,
                                 min_rating: float | None = None,
                                 max_rating: float | None = None,
                                 timestamp: datetime | None = None
                                 ) -> Optional[bool]:
        """
        Метод сохранения в БД данных запроса пользователя в чат

        :param model: модель БД
        :param cid: идентификатор пользователя
        :param command: команда
        :param genre: жанр фильма
        :param limit: кол-во
        :param order: метод сортировки: 1 - по возрастанию, -1 - по убыванию
        :param min_rating: минимальный рейтинг
        :param max_rating: максимальный рейтинг
        :param timestamp: отметка времени записи в БД
        :return:
        """
        with (db.atomic()):
            try:
                if model == ParamsStorage:
                    params = cls.get_param_storage_by_cid(cid=cid)
                    if params is None:
                        with db.atomic():
                            model.insert(cid=cid).execute()
                            params = cls.get_param_storage_by_cid(cid=cid)
                    if command is not None:
                        params.command = command
                    if genre is not None:
                        params.genre = genre
                    if limit is not None:
                        params.limit = limit
                    if order is not None:
                        params.order = order
                    if min_rating is not None:
                        params.min_rating = min_rating
                    if max_rating is not None:
                        params.max_rating = max_rating
                    if timestamp is None:
                        params.timestamp = datetime.now()
                    else:
                        params.timestamp = timestamp
                    params.save()
                else:
                    with db.atomic():
                        if timestamp is None:
                            timestamp = datetime.now()
                        model.insert(
                            cid=cid,
                            command=command,
                            genre=genre,
                            limit=limit,
                            order=order,
                            min_rating=min_rating,
                            max_rating=max_rating,
                            timestamp=timestamp
                        ).execute()
                return True
            except IntegrityError as ex:
                return

    @classmethod
    def delete_param_storage_by_cid(cls, cid: int) -> Optional[bool]:
        """
        Метод удаления записи с данными текущего запроса в чат по id пользователя

        :param cid: идентификатор пользователя
        :return: при успешной операции возвращает True, иначе False
        """
        with db.atomic():
            params = cls.get_param_storage_by_cid(cid=cid)
            if params is None:
                return
            params.delete_instance()
            params.save()
            return True


if __name__ == "__main__":
    ...

from api_database.common.model import db, ParamsStorage
from peewee import IntegrityError
import datetime


class InterfaceApiDatabase:

    @classmethod
    def get_param_storage_by_cid(cls, cid: int):
        try:
            with db.atomic():
                return ParamsStorage.get(ParamsStorage.cid == cid)
        except Exception:
            pass

    @classmethod
    def insert_param_storage_by_cid(cls, cid: int) -> bool | None:
        try:
            with db.atomic():
                ParamsStorage.insert(cid=cid).execute()
            return True
        except IntegrityError:
            pass

    @classmethod
    def set_param_storage_by_cid(cls,
                                 cid: int,
                                 command: str | None = None,
                                 genre: str | None = None,
                                 limit: int | None = None,
                                 order: int | None = None,
                                 min_rating: float | None = None,
                                 max_rating: float | None = None
                                 ) -> bool | None:
        with db.atomic():
            params = cls.get_param_storage_by_cid(cid=cid)
            if params is None:
                return
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
            params.timestamp = datetime.datetime.now()
            params.save()
        return True

    @classmethod
    def delete_param_storage_by_cid(cls, cid: int):
        with db.atomic():
            params = cls.get_param_storage_by_cid(cid=cid)
            if params is None:
                return
            params.delete_instance()
            params.save()
            return True


if __name__ == "__main__":
    ...
